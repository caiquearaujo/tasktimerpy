#!/usr/bin/env python
import gettext
import sys

from src.database import Database
from src.commands import Commands
from src.terminal import Terminal

_ = gettext.gettext


def main():
    db = Database(".")
    term = Terminal(db)

    term.title(_("Task timer manager"))

    command = None
    argv = sys.argv[1:]

    if len(argv) == 0:
        term.exitWithError(
            _("Invalid arguments"),
            _("You must insert a command before continue..."),
        )

    cd = Commands(db, term)

    command = argv[0]
    switcher = {
        "start": lambda: cd.start(),
        "close": lambda: cd.close(),
        "stats": lambda: cd.stats(),
    }

    func = switcher.get(command, False)

    if func == False:
        term.exitWithError(
            "Invalid command",
            'The command "{i}" was not found.'.format(i=command),
        )

    func()


if __name__ == "__main__":
    main()
