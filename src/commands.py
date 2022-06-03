from datetime import datetime
import gettext
from typing import Callable

from .database import Database
from .models.task import Task
from .models.timer import Timer
from .terminal import Terminal

_ = gettext.gettext


class Commands:
    def __init__(self, db: Database, terminal: Terminal) -> None:
        self.db = db
        self.term = terminal

    def start(self):
        self.term.title(_("Starting a timer"))

        try:
            current_timer = self.db.timerActive()

            if current_timer is None:
                current_timer = self.__unactiveTimer()
            else:
                self.term.notice(
                    _(
                        'A timer is already started, working on "{i}" task...'
                    ).format(i=current_timer.task().name())
                )
                self.term.notice(
                    _("You must finish it before continue...")
                )
                self.term.exitWithSuccess()

            print()
            self.term.notice(
                _('Timer started to "{i}"...').format(
                    i=current_timer.task().name()
                )
            )
            self.term.exitWithSuccess()

        except Exception as e:
            self.term.exitWithError(_("Exception"), str(e))

    def stats(self):
        self.term.notice(_("Stats of current timer"))

        try:
            current_timer = self.db.timerActive()

            if current_timer is None:
                self.term.notice(
                    _("You must start a timer before continue...")
                )
                self.term.exitWithSuccess()

            now = datetime.now()
            start = datetime.fromtimestamp(current_timer.startsAt())
            delta = now - start

            days = delta.days
            total_seconds = delta.seconds
            mins, secs = divmod(total_seconds, 60)
            hours, mins = divmod(mins, 60)

            msg = _(
                "{d} day(s) {h} hour(s) {m} minute(s) {s} second(s)"
            ).format(d=days, h=hours, m=mins, s=secs)

            print(
                self.term.applyGreen("Project: ")
                + current_timer.project()
            )

            print(
                self.term.applyGreen("Epic: ")
                + (current_timer.epic() or "--")
            )

            print(
                self.term.applyGreen("Story: ")
                + (current_timer.story() or "--")
            )

            print(
                self.term.applyGreen("Task: ")
                + current_timer.task().name()
            )

            print(msg)
            self.term.exitWithSuccess(" ")

        except Exception as e:
            self.term.exitWithError(_("Exception"), e)

    def close(self):
        self.term.title(_("Closing a timer"))

        try:
            current_timer = self.db.timerActive()

            if current_timer is None:
                self.term.notice(
                    _("You must start a timer before continue...")
                )
                self.term.exitWithSuccess()

            self.db.timerClose(current_timer)
            self.term.notice(
                _('Timer closed to "{i}"...').format(
                    i=current_timer.task().name()
                )
            )

            done = self.term.askYN(
                _("Do you want mark task as done?"), "no"
            )

            if done:
                self.db.taskDone(current_timer.task())

            self.term.exitWithSuccess()

        except Exception as e:
            self.term.exitWithError(_("Exception"), e)

    def __unactiveTimer(self) -> Timer:
        self.term.notice(_("No active timer found..."))

        switcher = {
            "q": lambda: self.term.exitWithSuccess(),
            0: lambda: self.__create(),
            1: lambda: self.__load(),
        }

        task = self.__trigger("task", switcher)
        timer = self.db.timerOpen(task)

        if timer is None:
            self.term.exitWithError(
                _("Error"), _("Cannot open timer to task...")
            )

        return timer

    def __create(self) -> Task:
        self.term.title(_("Creating Task"))
        print()

        project = self.term.askInput(
            _("Type the project name for task"),
        )

        epic = self.term.askInput(
            _("Type the epic name for task"), required=False
        )
        story = self.term.askInput(
            _("Type the story name for task"), required=False
        )
        name = self.term.askInput(_("Type the task name"))

        e = Task(project, name).apply({"epic": epic, "story": story})
        return self.db.createTask(e)

    def __load(self) -> Task:
        return self.__loadTemplate(
            self.db.getUndoneTasks, _("task"), _("tasks")
        )

    def __trigger(self, name: str, switcher: dict):
        option = self.term.askOption(
            _("What do you want to do?"),
            {
                "q": _("Quit"),
                0: _("Create a new {x}").format(x=name),
                1: _("Load an existing {x}").format(x=name),
            },
        )

        return switcher.get(option, switcher.get(0))()

    def __loadTemplate(self, data: Callable, singular: str, plural: str):
        self.term.title(_("Listing current active {x}").format(x=plural))
        self.term.notice(_("Finding {x}...").format(x=plural))
        print()

        datas = data()

        if datas is None or len(datas) == 0:
            self.term.error(
                _("Empty data"),
                _("No {x} were found...").format(x=plural),
            )

            create = self.term.askYN(
                _("Do you want to create a new task?")
            )

            if create:
                return self.__create()

            self.term.exitWithSuccess()

        options = {}

        for t in datas:
            options[t.id()] = t.name()

        option = self.term.askOption(
            _("What {x} do want to start right now?").format(x=singular),
            options,
        )

        return filter(lambda t: t.id() == option, datas)[0]
