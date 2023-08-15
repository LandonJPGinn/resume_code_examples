import os
import sys
from CreatorPipeline.constants import DEFAULTS, STATUS
from CreatorPipeline.database import ActiveEpisodeDatabase as AED
from CreatorPipeline.episode import Episode
from CreatorPipeline import todolist
from CreatorPipeline import improvements
from CreatorPipeline import summary
from CreatorPipeline.phase import PhaseRunner
from functools import partial


def clear():
    """Clears the console"""
    print("\n" * 120)

class FunctionItem:
    """A menu item that calls a Python function when selected"""
    def __init__(self, text:str, function, args=None, kwargs=None):
        self.text = text
        self.function = function
        self.args = args or []
        self.kwargs = kwargs or {}

    def __call__(self):
        self.function(*self.args, **self.kwargs)


class ConsoleMenu:
    """A Console Menu"""
    def __init__(self, title, items):
        self.title = title
        self.text = title
        self.items = items

    def show(self):
        """Show the menu and respond to choices when selected."""
        while True:
            print("\n"*4)
            print(self.title)
            print("=" * len(self.title))
            for i, item in enumerate(self.items):
                print(f"{i + 1} - {item.text}")
            print("0 - Exit")
            choice = input("Enter your choice: ")
            clear()
            if choice == "0":
                break
            try:
                choice = int(choice)
                if choice < 1 or choice > len(self.items):
                    raise ValueError
            except ValueError:
                print("Invalid choice")
            else:
                try:
                    self.items[choice - 1]()
                except TypeError:
                    self.items[choice - 1].show()
            print("\n"*4)
    
    def add_item(self, item):
        """Add an item to the menu"""
        self.items.append(item)


class Navigator:
    """A Console Menu"""
    def __init__(self):
        self.ep = None
        agenda_submenu_items = [
            FunctionItem("Go To Folder", self.event_open_episode_directory),
            FunctionItem("Build Initial", self.phase_build),
            FunctionItem("Research", self.phase_research),
            FunctionItem("Plan", self.phase_plan),
            FunctionItem("Edit Setup", self.phase_edit_setup),
            FunctionItem("Edit Finish", self.phase_edit_finish),
            FunctionItem("Package", self.phase_package),
            FunctionItem("Release", self.phase_release),
            FunctionItem("Analytics", self.phase_analytics),
        ]
        self.agenda_submenu = ConsoleMenu("Agenda", agenda_submenu_items)

        main_menu_items = [
            self.active_submenu(),
            FunctionItem("Agenda", self.event_agenda),
            FunctionItem("ToDo", self.event_todo),
            FunctionItem("CBB", self.event_cbb),
            FunctionItem("Open Episodes Directory", self.event_open_episodes_directory),
            FunctionItem("Open Repo Directory", self.event_open_repo_directory),
            FunctionItem("Edit Repo", self.event_edit_repo),
        ]

        main_menu = ConsoleMenu("Main Menu", main_menu_items)
        clear()

        main_menu.show()



    def get_active_episodes(self):
        """Gets the active episodes from the database"""
        return AED().active.get("active")

    def get_episodes_from_hash(self):
        """Gets the episodes from the hash"""
        selected_episodes = []

        for episode in self.get_active_episodes():
            print(f"individual ep: {episode}")
            current_episode = Episode(episode)
            print(current_episode)
            if not current_episode:
                print(
                    f"{episode} failed to find an Episode. Make sure the hash provided is in the database.\nStopping"
                )
                sys.exit()
            selected_episodes.append(current_episode)
        
        return selected_episodes

    def event_agenda(self,*args):
        """Event for the Agenda submenu"""
        summary.main()

    def event_todo(self,*args):
        """Event for the ToDo submenu"""
        todolist.main()

    def event_cbb(self,*args):
        """Event for the CBB submenu"""
        improvements.main()
    
    def event_open_episode_directory(self,*args):
        """Event for opening the episode directory"""
        path = DEFAULTS.show_episode_root / self.ep.abbrv_title
        os.system(f"explorer {path}")

    def event_open_episodes_directory(self,*args):
        """Event for opening the episode directory"""
        os.system(f"explorer {DEFAULTS.show_episode_root}")

    def event_open_repo_directory(self,*args):
        """Event for opening the repo directory"""
        os.system(f"explorer {DEFAULTS.code_root}")

    def event_edit_repo(self,*args):
        """Event for opening the repo directory"""
        os.system(f"code {DEFAULTS.code_root}")

    def submenu_per_episode(self, *args):
        """Event for opening the repo directory"""
        self.ep = args[0]
        self.ep.summarize()
        print("\n"*3)
        print(f"Epsiode Status is currently: {self.ep.Status}")
        nxt = STATUS.next_step(current_step=self.ep.Status)
        print(f"Please Run: {nxt}")
        self.agenda_submenu.show()

    def active_submenu_items(self):
        """Gets the active submenu items"""
        return [FunctionItem(f"{x.ID} - {x.Title}", partial(self.submenu_per_episode, x)) for x in self.get_episodes_from_hash() ]

    def active_submenu(self):
        """Gets the active submenu"""
        submenu_items = self.active_submenu_items()
        return ConsoleMenu("Active", submenu_items)

    def phase_build(self):
        """Run the build phase"""
        PhaseRunner(self.ep, skip=True).Build()

    def phase_research(self):
        """Run the research phase"""
        PhaseRunner(self.ep).Research()
    
    def phase_plan(self):
        """Run the plan phase"""
        PhaseRunner(self.ep).Plan()

    def phase_edit_setup(self):
        """Run the edit setup phase"""
        PhaseRunner(self.ep).Edit_Setup()

    def phase_edit_finish(self):
        """Run the edit finish phase"""
        PhaseRunner(self.ep).Edit_Finish()

    def phase_package(self):
        """Run the package phase"""
        PhaseRunner(self.ep).Package()

    def phase_release(self):
        """Run the release phase"""
        PhaseRunner(self.ep).Release()

    def phase_analytics(self):
        """Run the analytics phase"""
        PhaseRunner(self.ep).Analytics

if __name__ == "__main__":
    Navigator()