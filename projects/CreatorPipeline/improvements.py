from CreatorPipeline.constants import DEFAULTS




def main():
    """Prints a list of things to improve from the dev notes improvements list"""
    todofile = DEFAULTS.docs_root / "docs" / "_devnotes"/ "improvements.txt"

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
    print("{:-^120}".format(f" Things to Improve - List || {count} items "))

    for i in output[:3]:
        print(i)
    print("{:-^120}".format("Completed - List"))

    for x in complete[:4]:
        print(x)

if __name__ == "__main__":
    main()