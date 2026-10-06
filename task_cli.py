import helper, sys
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
        helper.add_task(args)
    elif command == "update":
        helper.update_task(args)
    elif command == "delete":
        helper.delete_task(args)
    elif command == "list":
        helper.list_tasks(args)
    elif command == "mark-done" or command == "mark-in-progress":
        helper.change_task_status(args, command)
    else:
        print("Unknown command.\n", file=sys.stderr)
        print(command_info, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()