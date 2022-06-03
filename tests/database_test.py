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


# def test_can_create_a_project():
#     db = Database("./tests", "tasktimerpy_test")

#     io = Project({"name": "Project One"})
#     project = db.createProject(io)

#     db.close()
#     assert project.name() == io.name() and project.hasId()


# def test_can_get_a_project():
#     db = Database("./tests", "tasktimerpy_test")

#     io = Project({"name": "Project One"})
#     project = db.createProject(io)

#     read = db.getProject(project.id())
#     db.close()
#     assert read.name() == project.name() and read.id() == project.id()


# def test_can_create_an_epic():
#     db = Database("./tests", "tasktimerpy_test")

#     io = Epic({"name": "Epic One"})
#     io.assignTo(db.getProject(1))
#     epic = db.createEpic(io)

#     db.close()
#     assert epic.name() == io.name() and epic.hasId()


# def test_can_get_an_epic():
#     db = Database("./tests", "tasktimerpy_test")

#     io = Epic({"name": "Epic One"})
#     io.assignTo(db.getProject(1))
#     epic = db.createEpic(io)

#     read = db.getEpic(epic.id())
#     db.close()
#     assert read.name() == epic.name() and read.id() == epic.id()


# def test_can_create_a_story():
#     db = Database("./tests", "tasktimerpy_test")

#     io = Story({"name": "Story One"})
#     io.assignTo(db.getEpic(1))
#     story = db.createStory(io)

#     db.close()
#     assert story.name() == io.name() and story.hasId()


# def test_can_get_a_story():
#     db = Database("./tests", "tasktimerpy_test")

#     io = Story({"name": "Story One"})
#     io.assignTo(db.getEpic(1))
#     story = db.createStory(io)

#     read = db.getStory(story.id())
#     db.close()
#     assert read.name() == story.name() and read.id() == story.id()


# def test_can_create_a_task():
#     db = Database("./tests", "tasktimerpy_test")

#     io = Task({"name": "Task One"})
#     io.assignTo(db.getStory(1))
#     task = db.createTask(io)

#     db.close()
#     assert task.name() == io.name() and task.hasId()


# def test_can_get_a_task():
#     db = Database("./tests", "tasktimerpy_test")

#     io = Task({"name": "Task One"})
#     io.assignTo(db.getStory(1))
#     task = db.createTask(io)

#     read = db.getTask(task.id())
#     db.close()
#     assert read.name() == task.name() and read.id() == task.id()


# def test_can_get_undone_projects():
#     db = Database("./tests", "tasktimerpy_test")
#     projects = db.getUndoneProjects()
#     db.close()
#     assert len(projects) == 2 and isinstance(projects[0], Project)


# def test_can_get_undone_epics():
#     db = Database("./tests", "tasktimerpy_test")
#     epics = db.getUndoneEpics(db.getProject(1))
#     db.close()
#     assert len(epics) == 2 and isinstance(epics[0], Epic)


# def test_can_get_undone_stories():
#     db = Database("./tests", "tasktimerpy_test")
#     stories = db.getUndoneStories(db.getEpic(1))
#     db.close()
#     assert len(stories) == 2 and isinstance(stories[0], Story)


# def test_can_get_undone_tasks():
#     db = Database("./tests", "tasktimerpy_test")
#     tasks = db.getUndoneTasks()
#     db.close()
#     assert len(tasks) == 2 and isinstance(tasks[0], Task)


# def test_can_create_a_timer():
#     db = Database("./tests", "tasktimerpy_test")
#     timer = db.timerOpen(db.getTask(1))
#     db.close()
#     assert timer.hasId() and not timer.isDone()


# def test_can_get_an_active_timer():
#     db = Database("./tests", "tasktimerpy_test")
#     timer = db.timerActive()
#     db.close()
#     assert timer.hasId() and not timer.isDone()


# def test_can_close_a_timer():
#     db = Database("./tests", "tasktimerpy_test")
#     timer = db.getTimer(1)
#     timer = db.timerClose(timer)
#     db.close()
#     assert timer.hasId() and timer.isDone()


# def test_cannot_get_an_active_timer():
#     db = Database("./tests", "tasktimerpy_test")
#     timer = db.timerActive()
#     db.close()
#     assert timer is None


# def test_cannot_close_an_empty_timer():
#     db = Database("./tests", "tasktimerpy_test")

#     with pytest.raises(sqlite3.Error, match="You must start timer first"):
#         db.timerClose(Timer())


# def test_cannot_close_an_unknown_timer():
#     db = Database("./tests", "tasktimerpy_test")

#     with pytest.raises(sqlite3.Error, match="Timer does not exists"):
#         db.timerClose(Timer({"timer_id": 999999}))


# def test_can_create_a_timer_without_task():
#     db = Database("./tests", "tasktimerpy_test")

#     with pytest.raises(sqlite3.Error, match="You must create task first"):
#         timer = db.timerOpen(Task({"name": "Task One"}))


# def test_can_create_a_timer_with_invalid_task():
#     db = Database("./tests", "tasktimerpy_test")

#     with pytest.raises(sqlite3.Error, match="Task does not exists"):
#         db.timerOpen(Timer({"name": "Task One", "timer_id": 999999}))


# def test_can_mark_a_task_as_done():
#     db = Database("./tests", "tasktimerpy_test")

#     task = db.taskDone(db.getTask(1))
#     task = db.getTask(1)
#     db.close()
#     assert task.isDone()


# def test_cannot_mark_invalid_task_as_done():
#     db = Database("./tests", "tasktimerpy_test")

#     with pytest.raises(sqlite3.Error, match="You must create task first"):
#         db.taskDone(Task({"name": "Task One"}))


# def test_cannot_mark_unknown_task_as_done():
#     db = Database("./tests", "tasktimerpy_test")

#     with pytest.raises(sqlite3.Error, match="Task does not exists"):
#         db.taskDone(Task({"name": "Task One", "task_id": 999999}))
