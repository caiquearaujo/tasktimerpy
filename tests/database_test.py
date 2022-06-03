import os
from pathlib import Path, PurePath
import sqlite3
import pytest
from src.database import Database

from src.models.task import Task
from src.models.timer import Timer


def test_database_is_created():
    path = Path(PurePath("./tests", "tasktimerpy_test.sqlite3"))

    try:
        os.unlink(path)
    except:
        pass

    db = Database("./tests", "tasktimerpy_test")
    db.close()
    assert path.is_file()


def test_can_create_a_task():
    db = Database("./tests", "tasktimerpy_test")

    io = Task("Project One", "Task One")
    oo = db.createTask(io)

    db.close()
    assert oo.name() == io.name() and oo.hasId()


def test_can_get_a_task():
    db = Database("./tests", "tasktimerpy_test")

    io = Task("Project One", "Task One")
    oo = db.createTask(io)

    read = db.getTask(oo.id())
    db.close()
    assert read.name() == oo.name() and read.id() == oo.id()


def test_can_get_undone_tasks():
    db = Database("./tests", "tasktimerpy_test")
    tasks = db.getUndoneTasks()
    db.close()
    assert len(tasks) == 2 and isinstance(tasks[0], Task)


def test_can_create_a_timer():
    db = Database("./tests", "tasktimerpy_test")
    timer = db.timerOpen(db.getTask(1))
    db.close()
    assert timer.hasId() and not timer.isDone()


def test_can_get_an_active_timer():
    db = Database("./tests", "tasktimerpy_test")
    timer = db.timerActive()
    db.close()
    assert timer.hasId() and not timer.isDone()


def test_can_close_a_timer():
    db = Database("./tests", "tasktimerpy_test")
    timer = db.getTimer(1)
    timer = db.timerClose(timer)
    db.close()
    assert timer.hasId() and timer.isDone()


def test_cannot_get_an_active_timer():
    db = Database("./tests", "tasktimerpy_test")
    timer = db.timerActive()
    db.close()
    assert timer is None


def test_cannot_close_an_empty_timer():
    db = Database("./tests", "tasktimerpy_test")

    with pytest.raises(sqlite3.Error, match="You must start timer first"):
        db.timerClose(Timer())


def test_cannot_close_an_unknown_timer():
    db = Database("./tests", "tasktimerpy_test")

    with pytest.raises(sqlite3.Error, match="Timer does not exists"):
        db.timerClose(Timer().apply({"timer_id": 9999999}))


def test_can_create_a_timer_without_task():
    db = Database("./tests", "tasktimerpy_test")

    with pytest.raises(sqlite3.Error, match="You must create task first"):
        timer = db.timerOpen(Task("Project One", "Task One"))


def test_can_create_a_timer_with_invalid_task():
    db = Database("./tests", "tasktimerpy_test")

    with pytest.raises(sqlite3.Error, match="Task does not exists"):
        db.timerOpen(
            Task("Project One", "Task One").apply({"task_id": 99999})
        )


def test_can_mark_a_task_as_done():
    db = Database("./tests", "tasktimerpy_test")

    task = db.taskDone(db.getTask(1))
    task = db.getTask(1)
    db.close()
    assert task.isDone()


def test_cannot_mark_invalid_task_as_done():
    db = Database("./tests", "tasktimerpy_test")

    with pytest.raises(sqlite3.Error, match="You must create task first"):
        db.taskDone(Task("Project One", "Task One"))


def test_cannot_mark_unknown_task_as_done():
    db = Database("./tests", "tasktimerpy_test")

    with pytest.raises(sqlite3.Error, match="Task does not exists"):
        db.taskDone(
            Task("Project One", "Task One").apply({"task_id": 99999})
        )
