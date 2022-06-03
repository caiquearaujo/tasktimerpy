import colorama
import sys
import gettext

from .database import Database

_ = gettext.gettext


class Terminal:
    @staticmethod
    def askOption(title: str, options: dict):
        option = -1
        print()

        while option < 0:
            Terminal.printWorking(title)
            print()

            for key, value in options.items():
                print(
                    colorama.Fore.YELLOW,
                    "[",
                    key,
                    "]",
                    colorama.Fore.RESET,
                    "\t",
                    value,
                )

            try:
                print()

                option = input(
                    _("[*] Choose an option")
                    + colorama.Fore.GREEN
                    + " > "
                    + colorama.Fore.RESET
                )

                if option == "q":
                    return option
                else:
                    option = int(option)

                if options.get(option, None) is None:
                    option = -1
                    continue

                return option
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

            if required:
                message = "[*] " + message

            if default:
                message += (
                    colorama.Fore.YELLOW
                    + " ["
                    + default
                    + "]"
                    + colorama.Fore.RESET
                )

            response = input(
                message
                + colorama.Fore.GREEN
                + " > "
                + colorama.Fore.RESET
            )

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

                return response or ""

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
        Terminal.printErr(err, message)
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
    def printErr(err="Error", message=None):
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
    def printTitle(message: str):
        print(
            colorama.Back.YELLOW
            + colorama.Fore.BLACK
            + message
            + colorama.Fore.RESET
            + colorama.Back.RESET
            + "\n"
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
