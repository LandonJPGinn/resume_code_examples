import argparse
import os

from CreatorPipeline.constants import DEFAULTS


def main():
    """Main function for todo list."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        nargs="?",
        const=True,
        default=False,
    )
    args = parser.parse_args()


    todofile = DEFAULTS.docs_root / "docs" / "_devnotes"/ "todo.txt"

    output = []
    complete = []
    with open(todofile, "r") as f:
        for line in f.readlines():
            if line.startswith("[ ] - "):
                output.append(line.strip())

            if line.startswith("[x] - "):
                complete.append(" " + line.strip())

    output = list(filter(None, output))
    complete = list(filter(None, complete))
    count = len(output)
    print("{:-^120}".format(f" ToDo - List || {count} items "))

    for i in output:
        print(i.title())
    print("{:-^120}".format("Completed - List"))

    for x in complete[:-9:-1]:
        print(x.lower())


    if args.o:
        os.system(f"subl {todofile}")

if __name__ == "__main__":
    main()