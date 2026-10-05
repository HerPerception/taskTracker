from datetime import datetime
import json, sys

FILENAME = "tasks.json"
STATUS_TODO = "todo"
STATUS_IN_PROGRESS = "in-progress"
STATUS_DONE = "done"

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
            json.dump(tasks, file, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"Error. This file may not have a write permission.: {e}", file=sys.stderr)
        sys.exit(1)

def get_timestamp():
    return datetime.now().isoformat()

def generate_id(tasks):
    #I used generator expression because I need to get just the id integer and want to save memory
    highest_id = max((task['id'] for task in tasks), default=None)
    if highest_id is None:
        return 1
    return highest_id + 1

def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def parse_id(input_id):
    try:
        return int(input_id)
    except ValueError:
        print(f"Input '{input_id}' is not a valid integer", file=sys.stderr)
        sys.exit(1)

def add_task(args):
    if len(args) == 0:
        print("Input should include the task to be added.", file=sys.stderr)
        sys.exit(1)
    if len(args) > 1:
        print('Task description should be sorrounded by quotes so whitespace does not truncate description. Example: "Do the laundry"', file=sys.stderr)
        sys.exit()
    task_description = args[0]
    task_description = task_description.strip()
    if len(task_description) == 0:
        print("Input missing the task to be added.", file=sys.stderr)
        sys.exit(1)
    tasks = load_tasks(FILENAME)
    new_id = generate_id(tasks)
    createdAt = get_timestamp()
    updatedAt = createdAt
    task_dict = {"id": new_id, "description": task_description, "status": STATUS_TODO, "createdAt": createdAt, "updatedAt": updatedAt}
    tasks.append(task_dict)
    save_tasks(FILENAME, tasks)

    print(f"Task added successfully (ID: {new_id})")


def update_task(args):
    return "update_task called"

def delete_task(args):
    return "delete_task called"

def list_tasks(args):
    return "list_tasks called"

def mark_in_progress(args):
    return "mark_in_progress called"

def mark_done(args):
    return "mark_done called"

def main():
    command_info = """Usage: python3 task_cli.py <command> [arguments]
        add [task to add]
        update <taskId> [task description]
        mark-in-progress <id>
        mark-done <id>
        delete <id>
        list
        list done
        list todo
        list in-progress
        """
    if len(sys.argv) < 2:
        print("Incomplete number of arguments.\n")
        print(command_info, file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "add":
        add_task(args)
    elif command == "update":
        update_task(args)
    elif command == "delete":
        delete_task(args)
    elif command == "list":
        list_tasks(args)
    elif command == "mark-done":
        mark_done(args)
    elif command == "mark-in-progress":
        mark_in_progress(args)
    else:
        print("Unknown command.\n")
        print(command_info, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()