from datetime import datetime
from src.models.task import Task


def test_create_task():
    t = Task("project-one", "Task One")
    assert t.toDict() == {
        "id": None,
        "project": "project-one",
        "epic": None,
        "story": None,
        "name": "Task One",
        "done": 0,
        "createdAt": t.createdAt(),
    }


def test_mark_task_as_done():
    t = Task("project-one", "Task One")
    t.markAsDone()
    assert t.isDone()


def test_mark_task_as_undone():
    t = Task("project-one", "Task One")
    t.markAsDone().markAsUndone()
    assert not t.isDone()


def test_getters_of_task():
    t = Task("project-one", "Task One")
    t.changeEpic("Epic One")
    t.changeStory("Story One")
    assert t.toDict() == {
        "id": None,
        "project": "project-one",
        "epic": "epic-one",
        "story": "story-one",
        "name": "Task One",
        "done": 0,
        "createdAt": t.createdAt(),
    }


def test_setters_of_task():
    t = Task("project-one", "Task One")
    t.changeProject("Project Two")
    t.changeName("Task Two")
    t.changeEpic("Epic One")
    t.changeStory("Story One")
    assert t.toDict() == {
        "id": None,
        "project": "project-two",
        "epic": "epic-one",
        "story": "story-one",
        "name": "Task Two",
        "done": 0,
        "createdAt": t.createdAt(),
    }


def test_applying_record_to_task():
    n = int(datetime.now().timestamp())
    t = Task("project-one", "Task One")
    r = {
        "task_id": 1,
        "project": "project-one",
        "epic": "epic-one",
        "story": "story-one",
        "name": "Task One",
        "done": 1,
        "created_at": n,
    }

    t.apply(r)
    assert t.toDict() == {
        "id": 1,
        "project": "project-one",
        "epic": "epic-one",
        "story": "story-one",
        "name": "Task One",
        "done": 1,
        "createdAt": n,
    }


def test_task_valid_primary_key():
    s = Task("project-one", "Task One")
    assert s.primaryKey() == "task_id"
