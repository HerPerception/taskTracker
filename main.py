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
