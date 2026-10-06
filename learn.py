import sys

# args = sys.argv[:]
# try:
#     if args[1] == "done":
#         print("Successfully done!")
# except IndexError:
#     print(args)


# print(load_tasks("tasks.json"))
# print(generate_id([]))
# items = [
#     {"id": 1, "name": "Alice", "role": "admin"},
#     #{"id": 2, "name": "Bob", "role": "editor"},
#     {"id": 3, "name": "Charlie", "role": "viewer"},
#     {"id": 4, "name": "Bob", "role": "editor"},
# ]
# print(get_timestamp())
# print(generate_id(items))
# print(find_task(items, 4))
# print(find_task([], 1))
# print(parse_id("7"))
# print(parse_id("int"))

systemarg = sys.argv[2:]
print(systemarg)


# An implementation of delete_task I don't want to lose.
# def delete_task(args):
#     if len(args) != 1:
#         print("Argument for delete command must be exactly 1. Usage: delete <id>", file=sys.stderr)
#         sys.exit(1)
#     task_id = parse_id(args[0])
#     task = find_task(tasks, task_id)
#     if task is None:
#         print(f"No task with ID: {task_id}", file=sys.stderr)
#         sys.exit(1)
#     tasks = load_tasks(FILENAME)
    #tasks = [included_task for included_task in tasks if included_task["id"] != task_id]
    #I used the loop instead of list comprehension because this way I can control the iteration and break the loop once a match is found.
    # List comprehension would check every single dictionary in the list even after the match is found.
    # for index, task_dict in enumerate(tasks):
    #     if task_dict.get("id") == task_id:
    #         del tasks[index]
    #         id_found = True
    #         break
    # save_tasks(FILENAME, tasks)
    # print(f"Task deleted successfully, (ID: {task_id})")
