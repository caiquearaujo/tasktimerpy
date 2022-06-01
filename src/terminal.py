import colorama
import sys
import gettext

from database import Database

_ = gettext.gettext


class Terminal:
    @staticmethod
    def askOption(title: str, options: dict):
        option = -1
        print()

        while option < 0:
            print("== " + title)
            print()

            for key in options.keys:
                print(
                    colorama.Fore.YELLOW,
                    "[",
                    key,
                    "]",
                    colorama.Fore.RESET,
                    "\t",
                    options[key],
                )

            try:
                print()

                option = int(
                    input(
                        _("[*] Choose an option")
                        + colorama.Fore.GREEN
                        + " > "
                        + colorama.Fore.RESET
                    )
                )

                if option not in options:
                    option = -1
            except:
                option = -1

    @staticmethod
    def askInput(
        question: str,
        max: int = -1,
        required: bool = True,
        default: str = None,
    ):
        while True:
            message = question

            if default:
                message += (
                    colorama.Fore.YELLOW
                    + " ["
                    + default
                    + "]"
                    + colorama.Fore.RESET
                )

            print(message)
            response = input()

            if max < 0:
                max = len(response)

            if required:
                if len(response) == 0 and default != None:
                    return default

                if len(response) != 0 and len(response) <= max:
                    return response

                Terminal.printErr(
                    _("Unexpected value"),
                    _("You must to provide an answer..."),
                )

                if len(response) > max:
                    Terminal.printErr(
                        _("Unexpected value"),
                        _("Characters limit of {m} reached...\n").format(
                            m=max
                        ),
                    )
            else:
                if default != None:
                    return default

                return ""

    @staticmethod
    def askInputAsInt(
        question: str,
        max: int = -1,
        required: bool = True,
        default: int = None,
    ):
        while True:
            message = question

            if default:
                message += (
                    colorama.Fore.YELLOW
                    + " ["
                    + default
                    + "]"
                    + colorama.Fore.RESET
                )

            print(message)
            response = input()

            if max < 0:
                max = len(response)

            if required:
                if len(response) == 0 and default != None:
                    return default

                if len(response) != 0 and len(response) <= max:
                    try:
                        return int(response)
                    except ValueError:
                        Terminal.printErr(
                            _("Unexpected value"),
                            _("You must to provide an integer value..."),
                        )

                        continue

                Terminal.printErr(
                    _("Unexpected value"),
                    _("You must to provide an answer..."),
                )

                if len(response) > max:
                    Terminal.printErr(
                        _("Unexpected value"),
                        _("Characters limit of {m} reached...\n").format(
                            m=max
                        ),
                    )
            else:
                if default != None:
                    return default

                return ""

    @staticmethod
    def askYN(question: str, default: str = "yes"):
        valid = {"yes": True, "y": True, "no": False, "n": False}

        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            default = "yes"
            prompt = " [Y/n] "

        while True:
            choice = input(
                question
                + prompt
                + colorama.Fore.GREEN
                + "> "
                + colorama.Fore.RESET
            ).lower()

            if default is not None and choice == "":
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                Terminal.printErr(
                    _("Unexpected value"),
                    _(
                        "Please, you must to provide a valid answer: `y`, `n`, `yes` ou `no`."
                    ),
                )

    @staticmethod
    def shouldContinue():
        _continue = Terminal.askYN(_("Do you want to continue?"))

        if _continue == False:
            Terminal.success(_("Operation aborted successfully..."))

    @staticmethod
    def err(db: Database, err="Error", message=None):
        """Exibe uma mensagem de error e encerra o programa."""
        Terminal.printErr(err, (message or _("Something went wrong...")))
        db.close()
        sys.exit(2)

    @staticmethod
    def success(db: Database, message=None):
        """Exibe uma mensagem de sucesso e encerra o programa."""
        Terminal.printSuccess(
            "\n\n" + (message or _("Everything is done..."))
        )
        db.close()
        sys.exit()

    @staticmethod
    def printErr(err="Erro", message=None):
        print(
            colorama.Back.RED
            + err
            + " >"
            + colorama.Back.RESET
            + colorama.Fore.RED
            + " "
            + (message or _("Something went wrong..."))
            + colorama.Fore.RESET
        )

    @staticmethod
    def printWorking(message=None):
        print(
            colorama.Fore.YELLOW
            + (message or _("Wait a minute..."))
            + colorama.Fore.RESET
        )

    @staticmethod
    def printSuccess(message=None):
        print(
            colorama.Fore.GREEN
            + (message or _("Everything is done..."))
            + colorama.Fore.RESET
        )
