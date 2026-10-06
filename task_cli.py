from datetime import datetime
import json, sys

FILENAME = "tasks.json"
STATUS_TODO = "todo"
STATUS_IN_PROGRESS = "in-progress"
STATUS_DONE = "done"
VALID_STATUSES = (STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE)

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
        tasks = json.loads(file_content)
    except json.JSONDecodeError as e:
        print(f"Error. File might contain invalid json.: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(tasks, list):
        print(f"Expected type=list for file: {filename}, got {type(tasks).__name__}", file=sys.stderr)
        sys.exit(1)
    all_dicts = all(isinstance(task, dict) for task in tasks)
    if not all_dicts:
        print(f"{filename} should be a list of dictionaries. One or more tasks are not valid dictionaries.", file=sys.stderr)
        sys.exit(1)
    return tasks


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

#Safely prints an error message and exits if task with provided ID is not found to avoid repeating checks in the other functions.
def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
        
    print(f"Task with id {task_id} not found.", file=sys.stderr)
    sys.exit(1)


def parse_id(input_id):
    try:
        int_id = int(input_id)
    except ValueError:
        print(f"Input '{input_id}' is not a valid integer", file=sys.stderr)
        sys.exit(1)
    if int_id <= 0:
        print("Task id can not be negative or zero.", file=sys.stderr)
        sys.exit(1)
    return int_id

def add_task(args):
    if len(args) == 0:
        print("Input should include the task to be added.", file=sys.stderr)
        sys.exit(1)
    if len(args) > 1:
        print('Task description should be surrounded by quotes so whitespace does not truncate description. Example: "Do the laundry"', file=sys.stderr)
        sys.exit(1)
    task_description = args[0]
    task_description = task_description.strip()
    if len(task_description) == 0:
        print("Input missing the task to be added.", file=sys.stderr)
        sys.exit(1)
    tasks = load_tasks(FILENAME)
    new_id = generate_id(tasks)
    created_at = get_timestamp()
    task_dict = {"id": new_id, "description": task_description, "status": STATUS_TODO, "createdAt": created_at, "updatedAt": created_at}
    tasks.append(task_dict)
    save_tasks(FILENAME, tasks)
    print(f"Task added successfully (ID: {new_id})")


def print_task(task):
    print(f'|ID: {task["id"]:<5}||Current Status: {task["status"]:<12}|| Task Description: {task["description"]}')


def list_tasks(args):
    if len(args) > 1:
        print("Wrong number of arguments for list. Usage: list [filter]", file=sys.stderr)
        sys.exit(1)
    status_filter = None
    if len(args) == 1:
        status_filter = args[0]
    if status_filter is not None and status_filter not in VALID_STATUSES:
        print(f"Status filter '{status_filter}' is not a valid filter for list command. Only {VALID_STATUSES} available.", file=sys.stderr)
        sys.exit(1)
    tasks = load_tasks(FILENAME)
    task_to_show = [task for task in tasks if status_filter is None or task["status"] == status_filter]
    if not task_to_show and status_filter is not None:
        print(f"No tasks with status '{status_filter}' yet.")
        return
    elif not task_to_show and status_filter is None:
        print("No task yet. Add task now.")
        return
    for each_task in task_to_show:
        print_task(each_task)


def update_task(args):
    if len(args) != 2:
        print("Argument for update command must be exactly 2. Usage: update <id> <description>", file=sys.stderr)
        sys.exit(1)
    task_id = parse_id(args[0])
    description = args[1]
    description = description.strip()
    if len(description) == 0:
        print(f"Update description for task id {task_id} can not be empty", file=sys.stderr)
        sys.exit(1)
    tasks = load_tasks(FILENAME)
    task = find_task(tasks, task_id)
    task["description"] = description
    task["updatedAt"] = get_timestamp()
    #We don't need to write it back to the list because we are directly modifying the dictionary in the list.
    save_tasks(FILENAME, tasks)
    print(f"Task updated successfully, (ID: {task_id}).")
    print_task(task)

    
def delete_task(args):
    if len(args) != 1:
        print("Argument for delete command must be exactly 1. Usage: delete <id>", file=sys.stderr)
        sys.exit(1)
    task_id = parse_id(args[0])
    tasks = load_tasks(FILENAME)
    task = find_task(tasks, task_id)
    tasks.remove(task)
    save_tasks(FILENAME, tasks)
    print(f"Task deleted successfully, (ID: {task_id})")


def change_task_status(arg, command):
    if len(arg) != 1:
        print("Change of task status command must include only the id. Usage: mark-done <id> or mark-in-progress <id>", file=sys.stderr)
        sys.exit(1)
    task_id = parse_id(arg[0])
    if command == "mark-in-progress":
        new_status = STATUS_IN_PROGRESS
    elif command == "mark-done":
        new_status = STATUS_DONE
    tasks = load_tasks(FILENAME)
    task = find_task(tasks, task_id)
    if new_status == task["status"]:
        print(f"Task (ID: {task_id}) status already {new_status}")
        return
    task["status"] = new_status
    task["updatedAt"] = get_timestamp()
    save_tasks(FILENAME, tasks)
    print(f"Task marked as {new_status} (ID: {task_id})")
    


def main():
    command_info = """Usage: python3 task_cli.py <command> [arguments]
        add <task to add>
        update <taskId> <task description>
        mark-in-progress <id>
        mark-done <id>
        delete <id>
        list
        list done
        list todo
        list in-progress
        """
    if len(sys.argv) < 2:
        print("Incomplete number of arguments.\n", file=sys.stderr)
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
    elif command == "mark-done" or command == "mark-in-progress":
        change_task_status(args, command)
    else:
        print("Unknown command.\n", file=sys.stderr)
        print(command_info, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()