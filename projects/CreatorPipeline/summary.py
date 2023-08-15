from CreatorPipeline.constants import DEFAULTS

from rich.console import Console
from rich.table import Table
import ast
import sys
import json
import pprint
import subprocess

pp = pprint.PrettyPrinter(indent=4)

def main():
    """Prints a list of things to improve from the dev notes improvements list"""
    console = Console(width=120, no_color=False)
    print("\n\n")
    # Episode Schedule 10
    table = Table(show_header=True, header_style="bold magenta", expand=True, min_width=300,)
    table.add_column("#", style="dim", width=2)
    table.add_column("Date", style="dim", width=7)
    table.add_column("Episode Title", width=54)
    table.add_column("Status", justify="center", width=6)
    table.add_column("ID", justify="right", width=8)

    with open(DEFAULTS.episode_log_path, "r") as f:
        data = {i: x.split("\t\t")[-1] for i, x in enumerate(f.readlines())}

    table.add_row("", "", "Active Episodes", "", end_section=True)
    for i, episode in data.items():
        episode = ast.literal_eval(rf'{episode}')
        dt = episode.get("date_publish")
        tl = episode.get("Title")
        st = episode.get("Status")
        nm = episode.get("abbrv_title")
        table.add_row(
            str(i),
            f"[bold]{dt}[/bold]",
            f"{tl}",
            f"{st}",
            f"{nm}",
        )
    table.add_row("", "", "", end_section=True)
    table.add_row("q", "quit", "Quit Menu")
    table.add_row("b", "back", "Go Back to Main Menu")

    console.clear()
    console.print(table)
    choice = input("\n\nWhat episode do you want to work on?")

    if "q" in choice.lower():
        sys.exit()

    elif "b" in choice.lower():
        print("\n"*100)
        return

    choice = int(choice)
    details = data.get(choice).replace("\n", "").replace("\t\t", "").replace("\t", "").replace("'", '"')
    details = json.loads(details)

    pp.pprint(details)

    gotopath = DEFAULTS.show_episode_root / details.get("abbrv_title")

    print(f"\n\nRun the following to open episode:\n\n\ncd \"{gotopath}\"")
    subprocess.call(str(gotopath), shell=True)
    sys.exit()

if __name__ == "__main__":
    main()