import requests

def get_tasks_from_api(api_key, workspace_id, project_id):
    url = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks'

    headers = {
        'X-Api-Key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            print(task)
        return task
    else:
        print(f"Can't connect. Status: {response.status_code}")
        return []

    
if __name__ == "__main__":
    # my data for example
    api_key = "YmM4NjAxNGMtZTg4OC00MWIzLWFjNDEtYjhlNDk3NTRiYTJl"

    workspace_id = "66c497f4e355191cb4517df5"
    project_id = "66c498c6e355191cb451a286"

    tasks = get_tasks_from_api(api_key, workspace_id, project_id)
