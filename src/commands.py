import gettext
from typing import Callable

from .database import Database
from .models.task import Task
from .models.timer import Timer
from .terminal import Terminal

_ = gettext.gettext


class Commands:
    def __init__(self, db: Database) -> None:
        self.db = db

    def start(self):
        Terminal.printTitle(_("Task timer manager"))

        try:
            current_timer = self.db.timerActive()

            if current_timer is None:
                current_timer = self.__unactiveTimer()
            else:
                Terminal.printWorking(
                    _(
                        'A timer is already started, working on "{i}" task...'
                    ).format(i=current_timer.task().name())
                )
                Terminal.printWorking(
                    _("You must finish it before continue...")
                )
                Terminal.success(self.db)

            print()
            Terminal.printWorking(
                _('Timer started to "{i}"...').format(
                    i=current_timer.task().name()
                )
            )
            Terminal.success(self.db)

        except Exception as e:
            Terminal.err(self.db, _("Exception"), str(e))

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
                _('Timer closed to "{i}"...').format(
                    i=current_timer.task().name()
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
        Terminal.printWorking(_("No active timer found..."))

        switcher = {
            "q": lambda: Terminal.success(self.db),
            0: lambda: self.__create(),
            1: lambda: self.__load(),
        }

        task = self.__trigger("task", switcher)
        timer = self.db.timerOpen(task)

        if timer is None:
            Terminal.err(
                self.db, _("Error"), _("Cannot open timer to task...")
            )

        return timer

    def __create(self) -> Task:
        Terminal.printTitle(_("Creating Task"))
        print()

        project = Terminal.askInput(
            _("Type the project name for task"),
        )

        epic = Terminal.askInput(
            _("Type the epic name for task"), required=False
        )
        story = Terminal.askInput(
            _("Type the story name for task"), required=False
        )
        name = Terminal.askInput(_("Type the task name"))

        e = Task(project, name).apply({"epic": epic, "story": story})
        return self.db.createTask(e)

    def __load(self) -> Task:
        return self.__loadTemplate(
            self.db.getUndoneTasks, _("task"), _("tasks")
        )

    def __trigger(self, name: str, switcher: dict):
        option = Terminal.askOption(
            _("What do you want to do?"),
            {
                "q": _("Quit"),
                0: _("Create a new {x}").format(x=name),
                1: _("Load an existing {x}").format(x=name),
            },
        )

        return switcher.get(option, switcher.get(0))()

    def __loadTemplate(self, data: Callable, singular: str, plural: str):
        Terminal.printTitle(
            _("Listing current active {x}").format(x=plural)
        )
        Terminal.printWorking(_("Finding {x}...").format(x=plural))
        print()

        datas = data()

        if datas is None or len(datas) == 0:
            Terminal.printErr(
                _("Empty data"),
                _("No {x} were found...").format(x=plural),
            )

            create = Terminal.askYN(
                _("Do you want to create a new task?")
            )

            if create:
                return self.__create()

            Terminal.success(self.db)

        options = {}

        for t in datas:
            options[t.id()] = t.name()

        option = Terminal.askOption(
            _("What {x} do want to start right now?").format(x=singular),
            options,
        )

        return filter(lambda t: t.id() == option, datas)[0]
