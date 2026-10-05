import sys

args = sys.argv[:]
try:
    if args[1] == "done":
        print("Successfully done!")
except IndexError:
    print(args)