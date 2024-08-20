# Report generator from Clockify

## This is a program that allows you to get data from Clockify and generate a report. You get the following data: task description, duration, start date.

The report is generated for each task and the duration of its execution, as well as for each date and the total time spent on that day.

The report is saved in a txt file and can also be viewed in the console.

To generate the report successfully, you need to enter the following data: ``Clockify api key, workspace id, user id, and project id``. 

To get the report, you need to generate two lists with tasks (the first using function ``get_tasks_from_api`` and the second using function ``get_task_with_date``)

For example:

```
api_key = "YOUR API KEY"
workspace_id = "YOUR WORKSPACE ID"
project_id = "YOUR PROJECT ID"
user_id = "YOUR USER ID"

first_task_list = get_tasks_from_api(api_key, workspace_id, project_id)
second_task_list = get_task_with_date(api_key, workspace_id, user_id)
```
After that, to display the report on the console, you need to pass this data to the ``convert_to_stdout`` function and save its output to a variable (this is necessary for its further writing to a file if necessary)
```
per_task, grouped_by_date = convert_to_stdout(first_task_list, second_task_list)
```
if you want to just pull data from the function without displaying a report on the console, specify the no option in the parameters ``print_option="no"``
```
per_task, grouped_by_date = convert_to_stdout(first_task_list, second_task_list, print_option="no")
```

If you want to write your report to a file, call ``write_to_file`` function and specify the path. 
```
path = "Report.txt"
write_to_file(path, per_task, grouped_by_date)
```

### I emphasize that you should not share your api key anywhere, as it is dangerous for your account and may contribute to the leakage of your data.

