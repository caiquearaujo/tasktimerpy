#!/usr/bin/env python
import gettext
import sys

from src.database import Database
from src.commands import Commands
from src.terminal import Terminal

_ = gettext.gettext


def main():
    Terminal.printTitle(_("Task timer manager"))

    db = Database(".")
    command = None
    argv = sys.argv[1:]

    if len(argv) == 0:
        Terminal.err(
            db,
            _("Invalid arguments"),
            _("You must insert a command before continue..."),
        )

    cd = Commands(db)

    command = argv[0]
    switcher = {
        "start": lambda: cd.start(),
        "close": lambda: cd.close(),
    }

    func = switcher.get(command, False)

    if func == False:
        Terminal.err(
            db,
            "Invalid command",
            'The command "{i}" was not found.'.format(i=command),
        )

    func()


if __name__ == "__main__":
    main()
