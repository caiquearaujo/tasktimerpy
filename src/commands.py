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
            Terminal.err(
                self.db, _("Error"), "Cannot open timer to task..."
            )

        return timer

    def __create(self) -> Task:
        return self.__createTask()

    def __trigger(self, name: str, switcher: dict):
        option = Terminal.askOption(
            _("What do you want to do?"),
            {
                0: _("Create a new {x}").format(x=name),
                1: _("Load an existing {x}").format(x=name),
            },
        )

        return switcher.get(option, switcher.get(0))()

    def __createTask(self) -> Task:
        print()

        name = Terminal.askInput(
            _("What is the task name?"),
        )

        e = Task({"name": name})
        return self.db.createTask(e)

    def __load(self) -> Task:
        return self.__loadTemplate(
            self.db.getUndoneTasks, _("task"), _("tasks")
        )

    def __loadTemplate(self, data: Callable, singular: str, plural: str):
        Terminal.printWorking(_("Finding {x}...").format(x=plural))
        print()

        datas = data()

        if datas is None or len(data) == 0:
            Terminal.printErr(
                _("Empty data"),
                _("No {x} were found...").format(x=plural),
            )
            return self.__create()

        options = {}

        for t in datas:
            options[t.id()] = t.name()

        option = Terminal.askOption(
            _("What {x} do want to start right now?").format(x=singular),
            options,
        )

        return filter(lambda t: t.id() == option, datas)[0]
