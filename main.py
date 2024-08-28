import requests
from datetime import datetime, timedelta


def _selectDataFromAPi(api_key, url):
    
    """
    The function that returns data at the specified api and address

    Returns:
        list: data or empty list
    """

    headers = {
        'X-Api-Key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Can't connect. Status: {response.status_code}")
        return []


def getTasksGeneralInfo(api_key, workspace_id, project_id):
    
    """
    The function that returns data about tasks.

    Returns:
        list: tasks
    """

    url = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks'
    tasks = _selectDataFromAPi(api_key, url)
    return tasks


def getTimeEntries(api_key, workspace_id, user_id):
   
    """
    The function that returns data about time entries.

    Returns:
        list: time entries
    """

    url = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries'

    tasks = _selectDataFromAPi(api_key, url)
    return tasks


def convertDurationToISO(duration):
    if duration is None:
        return timedelta(hours=0, minutes=0, seconds=0)

    hours = 0
    minutes = 0
    seconds = 0

    if duration.startswith("PT"):
        duration = duration[2:]

    if 'H' in duration:
        hours_part = duration.split('H')[0]
        hours = int(hours_part) if hours_part else 0
        duration = duration.split('H')[1]  

    if 'M' in duration:
        minutes_part = duration.split('M')[0]
        minutes = int(minutes_part) if minutes_part else 0
        duration = duration.split('M')[1]  

    if 'S' in duration:
        seconds_part = duration.split('S')[0]
        seconds = int(seconds_part) if seconds_part else 0

    time_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    
    return time_delta


def combineTaskWithTimeEntries(tasks, time_entries):

    """
    This function combines records of tasks and their completion dates. 
    First, create a dictionary with a key: task id and value - 
    a list of records of the start and end dates. 
    After that, create a dictionary of the format:
    
    task_dict = {
                    'name': name,
                    'duration': duration,
                    'timeIntervals': time_intervals
                }
    
    and add to the list "combined_tasks".

    Returns:
        list: combined tasks
    """

    sorted_entries = {}
    for entire in time_entries:
        task_id = entire['taskId']
        if task_id not in sorted_entries.keys():
            sorted_entries[task_id] = []

        time_interval = entire['timeInterval']
        sorted_entries[task_id].append(time_interval)

    combined_tasks = []
    for task in tasks:
        name = task['name']
        duration = task['duration']
        id = task['id']

        if sorted_entries.get(id) is None:
            time_intervals = None
        else:
            time_intervals = sorted_entries[id]

        task_dict = {
                    'name': name,
                    'duration': duration,
                    'timeIntervals': time_intervals
                }
        
        combined_tasks.append(task_dict)

    return combined_tasks


def convertToStdout(general_tasks, time_entries, print_option="yes"):

    """
    This function returns two dictionaries: 
    the first one contains a description of the task and the duration of its execution, 
    and the other one contains the total time spent on that day for each date. 
    There is also an output option that outputs two dictionaries by default, 
    but you can change it by setting this parameter in the function call.

    """

    tasks = combineTaskWithTimeEntries(general_tasks, time_entries)

    per_task = {}
    for task in tasks:
        task_name = task['name']
        duration = convertDurationToISO(task['duration'])
        per_task[task_name] = duration


    grouped_by_date = {}
    for task in tasks:
        time_intervals = task['timeIntervals']
        if time_intervals is None:
            continue

        for interval in time_intervals:
            start_date_str = interval['start']
            end_date_str = interval['end']

            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%SZ')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%SZ')

            duration = end_date - start_date
            day = start_date_str.split("T")[0]

            if day in grouped_by_date.keys():
                grouped_by_date[day] += duration
            else:
                grouped_by_date[day] = duration

    if print_option == "yes":
        printOutput(per_task, grouped_by_date)

    return per_task, grouped_by_date


def _formatOutput(per_task, grouped_by_date):

    """
    this function returns the generated report (string),
    which can then be displayed on the console or written to a file

    """

    lines = []

    lines.append("Time spent on each task:")
    for key, value in per_task.items():
        lines.append(f"Task: {key} \nDuration: {value}\n")

    lines.append('\n\n')

    lines.append("Spent time per day:")
    for key, value in grouped_by_date.items():
        lines.append(f"Date: {key} \nDuration: {value}\n")

    return "\n".join(lines)

def printOutput(per_task, grouped_by_date):
    output = _formatOutput(per_task, grouped_by_date)
    print(output)

def writeToFile(path, per_task, grouped_by_date):
    output = _formatOutput(per_task, grouped_by_date)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(output)


if __name__ == "__main__":

    api_key = "NTUxOTBjYjEtZjk4Yy00NDMyLWIwODAtZmU5YTM4YWE5ZGM3"

    workspace_id = "66c497f4e355191cb4517df5"
    project_id = "66c498c6e355191cb451a286"
    user_id = "66c497f4e355191cb4517df9"

    tasks = getTasksGeneralInfo(api_key, workspace_id, project_id)
    time_entries = getTimeEntries(api_key, workspace_id, user_id)
 
    per_task, grouped_by_date = convertToStdout(tasks, time_entries)
    writeToFile("Report.txt", per_task, grouped_by_date)
