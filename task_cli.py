import json,  sys

filename = "tasks.json"
statustodo = "todo"
statusinprogress = "in-progress"
statusdone = "done"

def load_tasks(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            file_content = file.read()
    except FileNotFoundError:
        return []
    except OSError as e:
        print(f"Error. File may have no read permission or there's a problem with the file.: {e}", file=sys.stderr)
        sys.exit(1)

    if len(file_content.strip()) == 0 :
        return []
    try:
        return json.loads(file_content)
    except json.JSONDecodeError as e:
        print(f"Error. File might contain invalid json.: {e}", file=sys.stderr)
        sys.exit(1)

def save_tasks(filename, tasks):
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(tasks, file, indent=2)
    except OSError as e:
        print(f"Error. This file may not have a write permission.: {e}", file=sys.stderr)
        sys.exit(1)
        


print(load_tasks("tasks.json"))

