import gettext
from typing import Callable

from database import Database
from models.epic import Epic
from models.project import Project
from models.record import Record
from models.story import Story
from models.task import Task
from models.timer import Timer
from terminal import Terminal

_ = gettext.gettext


class Commands:
    def __init__(self, path: str, db_name: str = "tasktimerpy") -> None:
        self.db = Database(path, db_name)

    def start(self):
        try:
            current_timer = self.db.timerActive()

            if current_timer is None:
                current_timer = self.__unactiveTimer()
            else:
                Terminal.printWorking(
                    _(
                        "A timer is already started to task id {i}..."
                    ).format(i=current_timer.task().id())
                )
                Terminal.printWorking(
                    _("You must finish it before continue...")
                )
                Terminal.success(self.db)

            Terminal.printWorking(
                _("Timer started to task id {i}...").format(
                    i=current_timer.task().id()
                )
            )
            Terminal.success(self.db)

        except Exception as e:
            Terminal.err(self.db, _("Exception"), e)

    def close(self):
        try:
            current_timer = self.db.timerActive()

            if current_timer is None:
                Terminal.printWorking(
                    _("You must start a timer before continue...")
                )
                Terminal.success(self.db)

            self.db.timerClose(current_timer)
            Terminal.printWorking(
                _("Timer closed to task id {i}...").format(
                    i=current_timer.task().id()
                )
            )

            done = Terminal.askYN(
                _("Do you want mark task as done?"), "no"
            )

            if done:
                self.db.taskDone(current_timer.task())

            Terminal.success(self.db)

        except Exception as e:
            Terminal.err(self.db, _("Exception"), e)

    def __unactiveTimer(self) -> Timer:
        switcher = {
            0: lambda: self.__create(),
            1: lambda: self.__load(),
        }

        task = self.__trigger("task", switcher)
        timer = self.db.timerOpen(Timer().assignTo(task))

        if timer is None:
            Terminal.err(self.db, _("Error"), "Cannot open timer to task...")

        return timer

    def __create(self) -> Task:
        switcher = {
            0: lambda: self.__createProject(),
            1: lambda: self.__loadProjects(),
        }

        project = self.__trigger("project", switcher)

        switcher = {
            0: lambda: self.__createEpic(project),
            1: lambda: self.__loadEpics(project),
        }

        epic = self.__trigger("epic", switcher)

        switcher = {
            0: lambda: self.__createStory(epic),
            1: lambda: self.__loadStories(epic),
        }

        story = self.__trigger("story", switcher)
        return self.__createTask(story)

    def __trigger(self, name: str, switcher: dict):
        option = Terminal.askOption(
            _("What do you want to do?"),
            {
                0: _("Create a new {x}").format(x=name),
                1: _("Load an existing {x}").format(x=name),
            },
        )

        return switcher.get(option, switcher[0])()

    def __createProject(self) -> Project:
        Terminal.printWorking(_("Starting to create a new project"))
        print()

        name = Terminal.askInput(
            _("What is the project name?"),
        )

        return self.db.createProject(Project({"name": name}))

    def __loadProjects(self) -> Project:
        return self.__loadTemplate(
            self.db.getUndoneProjects, _("project"), _("projects")
        )

    def __createEpic(self, project: Project) -> Epic:
        Terminal.printWorking(
            _("Starting to create a new epic to project id {i}").format(
                i=project.id()
            )
        )
        print()

        name = Terminal.askInput(
            _("What is the epic name?"),
        )

        e = Epic({"name": name})
        e.assignTo(project)
        return self.db.createEpic(e)

    def __loadEpics(self, project: Project) -> Epic:
        return self.__loadTemplate(
            lambda: self.db.getUndoneEpics(project), _("epic"), _("epics")
        )

    def __createStory(self, epic: Epic) -> Story:
        Terminal.printWorking(
            _("Starting to create a new story to epic id {i}").format(
                i=epic.id()
            )
        )
        print()

        name = Terminal.askInput(
            _("What is the story name?"),
        )

        e = Story({"name": name})
        e.assignTo(epic)
        return self.db.createStory(e)

    def __loadStories(self, epic: Epic) -> Story:
        return self.__loadTemplate(
            lambda: self.db.getUndoneStories(epic),
            _("story"),
            _("stories"),
        )

    def __createTask(self, story: Story) -> Task:
        Terminal.printWorking(
            _("Starting to create a new task to story id {i}").format(
                i=story.id()
            )
        )
        print()

        name = Terminal.askInput(
            _("What is the task name?"),
        )

        e = Task({"name": name})
        e.assignTo(story)
        return self.db.createTask(e)

    def __load(self) -> Task:
        return self.__loadTemplate(
            self.db.getUndoneTasks, _("task"), _("tasks")
        )

    def __loadTemplate(self, data: Callable, singular: str, plural: str):
        Terminal.printWorking(_("Finding {x}...").format(x=plural))
        print()

        datas = data()

        if datas is None:
            Terminal.printErr(
                _("Empty data"),
                _("No {x} were found...").format(x=plural),
            )
            return self.__create()

        options = {}

        for t in datas:
            options[t.id()] = t.name()

        option = Terminal.askOption(
            _("What {x} do want to start right now?").format(x=plural),
            options,
        )

        return filter(lambda t: t.id() == option, datas)[0]
