import requests
from datetime import timedelta


def get_tasks_from_api(api_key, workspace_id, project_id):
    url = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks'

    headers = {
        'X-Api-Key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        tasks = response.json()
        return tasks
    else:
        print(f"Can't connect. Status: {response.status_code}")
        return []


# function to get records about the start date of the task
def get_task_with_date(api_key, workspace_id, user_id):
    url = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries'

    headers = {
        'X-Api-Key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tasks = response.json()
        return tasks
    else:
        print(f"Can't connect. Status: {response.status_code}")
        return []


# function to convert the duration format
def convert_iso_duration(duration):
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


def convert_to_stdout(general_tasks, tasks_with_date, print_option="yes"):

    tasks = combine_tasks(general_tasks, tasks_with_date)

    per_task = {}
    for task in tasks:
        task_name = task['name']
        duration = convert_iso_duration(task['duration'])
        per_task[task_name] = duration

    grouped_by_date = {}
    for task in tasks:
        date = task['timeInterval']['start']
        day = date.split("T")[0]
        duration = convert_iso_duration(task['duration'])
        
        if day in grouped_by_date.keys():
            grouped_by_date[day] += duration
        else:
            grouped_by_date[day] = duration

    
    if print_option == "yes":
        print("\nTime spent on each task:\n")
        for key, value in per_task.items():
            print(f"Task: {key} \nDuration: {value}")

        print('\n\n')

        print("Spent time per day\n")
        for key, value in grouped_by_date.items():
            print(f"Date: {key} \nDuration: {value}")

    return per_task, grouped_by_date


# function to combine tasks by id and get data about the start date
def combine_tasks(task1, task2):
    new_tasks = []
    for task in task1:
        name = task['name']
        duration = task['duration']
        id = task['id']

        for second_task in task2:
            if id == second_task['taskId']:
                time_interval = second_task['timeInterval']
                task_dict = {
                    'name': name,
                    'duration': duration,
                    'timeInterval': time_interval
                }

                new_tasks.append(task_dict)

    return new_tasks


def write_to_file(path, per_task, grouped_by_date):
    with open(path, 'w', encoding='utf-8') as file:
        file.write("Time spent on each task:\n")
        for key, value in per_task.items():
            line = f"Task: {key} \nDuration: {value}\n"
            file.write(line)

        file.write('\n\n')

        file.write("Spent time per day\n")
        for key, value in grouped_by_date.items():
            line = f"Date: {key} \nDuration: {value}\n"
            file.write(line) 
    

if __name__ == "__main__":
    # my data for example
    api_key = "YmM4NjAxNGMtZTg4OC00MWIzLWFjNDEtYjhlNDk3NTRiYTJl"

    workspace_id = "66c497f4e355191cb4517df5"
    project_id = "66c498c6e355191cb451a286"
    user_id = "66c497f4e355191cb4517df9"

    tasks = get_tasks_from_api(api_key, workspace_id, project_id)
    tasks_with_date = get_task_with_date(api_key, workspace_id, user_id)

    per_task, grouped_by_date = convert_to_stdout(tasks, tasks_with_date)
    write_to_file("Report.txt", per_task, grouped_by_date)
