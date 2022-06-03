import colorama
from src.database import Database
from src.terminal import Terminal

db = Database("./tests", "tasktimerpy_test")


def test_apply_green():
    assert Terminal(db).applyGreen("Green") == "\x1b[32mGreen\x1b[39m"


def test_apply_invert_red():
    assert Terminal(db).applyInvertRed("Red") == "\x1b[41mRed\x1b[49m"


def test_apply_invert_yellow():
    assert (
        Terminal(db).applyInvertYellow("Yellow")
        == "\x1b[43m\x1b[30mYellow\x1b[49m\x1b[39m"
    )


def test_apply_red():
    assert Terminal(db).applyRed("Red") == "\x1b[31mRed\x1b[39m"


def test_apply_yellow():
    assert Terminal(db).applyYellow("Yellow") == "\x1b[33mYellow\x1b[39m"


def test_format_option():
    assert (
        Terminal(db).formatOption("1", "Option")
        == "\x1b[33m[1]\x1b[39m\tOption"
    )


def test_format_question():
    assert (
        Terminal(db).formatQuestion("Question")
        == "\x1b[31m[*] \x1b[39mQuestion \x1b[32m> \x1b[39m"
    )


def test_format_question_not_required():
    assert (
        Terminal(db).formatQuestion("Question", required=False)
        == "[ ] Question \x1b[32m> \x1b[39m"
    )


def test_format_question_with_default():
    assert (
        Terminal(db).formatQuestion("Question", default="default")
        == "\x1b[31m[*] \x1b[39mQuestion \x1b[33m[default] \x1b[39m\x1b[32m> \x1b[39m"
    )


def test_error(capsys):
    Terminal(db).error("Error", "Unknown")
    captured = capsys.readouterr()
    assert (
        "\x1b[41mError >\x1b[49m \x1b[31mUnknown\x1b[39m\n"
        == captured.out
    )


def test_notice(capsys):
    Terminal(db).notice("Notice")
    captured = capsys.readouterr()
    assert "\x1b[33mNotice\x1b[39m\n" == captured.out


def test_success(capsys):
    Terminal(db).success("Success")
    captured = capsys.readouterr()
    assert "\x1b[32mSuccess\x1b[39m\n" == captured.out


def test_title(capsys):
    Terminal(db).title("Title")
    captured = capsys.readouterr()
    assert "\x1b[43m\x1b[30mTitle\x1b[49m\x1b[39m\n\n" == captured.out
