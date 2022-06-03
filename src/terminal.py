import colorama
import sys
import gettext

from .database import Database

_ = gettext.gettext


class Terminal:
    def __init__(self, db: Database):
        self.db = db

    def askOption(self, title: str, options: dict):
        option = -1

        while option < 0:
            self.notice(title)

            for key, value in options.items():
                print(self.formatOption(key, value))

            try:
                print()

                option = input(
                    self.formatQuestion("Choose an option", required=True)
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

    def askInput(
        self,
        question: str,
        max: int = -1,
        required: bool = True,
        default: str = None,
    ):
        while True:
            response = input(
                self.formatQuestion(question, required, default)
            )

            if max < 0:
                max = len(response)

            if required:
                if len(response) == 0 and default != None:
                    return default

                if len(response) != 0 and len(response) <= max:
                    return response

                self.error(
                    _("Unexpected value"),
                    _("You must to provide an answer..."),
                )

                if len(response) > max:
                    self.error(
                        _("Unexpected value"),
                        _("Characters limit of {m} reached...\n").format(
                            m=max
                        ),
                    )
            else:
                if default != None:
                    return default

                return response or ""

    def askYN(self, question: str, default: str = "yes"):
        valid = {"yes": True, "y": True, "no": False, "n": False}

        if default is None:
            prompt = "y/n"
        elif default == "yes":
            prompt = "Y/n"
        elif default == "no":
            prompt = "y/N"
        else:
            default = "yes"
            prompt = "Y/n"

        while True:
            choice = input(
                self.formatQuestion(
                    question, required=True, default=prompt
                )
            ).lower()

            if default is not None and choice == "":
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                self.error(
                    _("Unexpected value"),
                    _(
                        "Please, you must to provide a valid answer: `y`, `n`, `yes` ou `no`."
                    ),
                )

    def shouldContinue(
        self,
    ):
        _continue = self.askYN(_("Do you want to continue?"))

        if _continue == False:
            self.exitWithSuccess(_("Operation aborted successfully..."))

    def error(self, error: str = "Error", message: str = None):
        print(
            self.applyInvertRed(error + " >")
            + " "
            + self.applyRed((message or _("Something went wrong...")))
        )

    def notice(self, message: str):
        print(self.applyYellow(message))

    def success(self, message: str = None):
        print(self.applyGreen((message or _("Everything is done..."))))

    def title(self, title: str):
        print(self.applyInvertYellow(title))
        print()

    def formatOption(self, key: str, value: str) -> str:
        return self.applyYellow("[" + str(key) + "]") + "\t" + value

    def formatQuestion(
        self, question: str, required=True, default=None
    ) -> str:
        message = ""

        if required:
            message += self.applyRed("[*] ")
        else:
            message += "[ ] "

        message += question + " "

        if default is not None:
            message += self.applyYellow("[" + default + "] ")

        message += self.applyGreen("> ")
        return message

    def applyGreen(self, message: str) -> str:
        return colorama.Fore.GREEN + message + colorama.Fore.RESET

    def applyRed(self, message: str) -> str:
        return colorama.Fore.RED + message + colorama.Fore.RESET

    def applyInvertRed(self, message: str) -> str:
        return colorama.Back.RED + message + colorama.Back.RESET

    def applyYellow(self, message: str) -> str:
        return colorama.Fore.YELLOW + message + colorama.Fore.RESET

    def applyInvertYellow(self, message: str) -> str:
        return (
            colorama.Back.YELLOW
            + colorama.Fore.BLACK
            + message
            + colorama.Back.RESET
            + colorama.Fore.RESET
        )

    def exitWithError(
        self, error: str = "Error", message: str = None, exitCode: int = 1
    ):
        """
        Terminate application with exit state
        """
        self.error(error, message)
        self.db.close()
        sys.exit(exitCode)

    def exitWithSuccess(self, message: str = None):
        """
        Terminate application with success state
        """
        self.success(message)
        self.db.close()
        sys.exit()
