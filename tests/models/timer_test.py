from datetime import datetime

from src.models.task import Task
from src.models.timer import Timer


def test_create_timer():
    t = Timer()
    assert t.toDict() == {
        "id": None,
        "task": None,
        "startsAt": t.startsAt(),
        "endsAt": None,
        "createdAt": t.createdAt(),
    }


def test_assign_task_to_timer():
    t = Task("project-one", "Task One")
    tt = Timer()
    tt.assignTo(t)
    assert tt.toDict() == {
        "id": None,
        "task": t.toDict(),
        "startsAt": tt.startsAt(),
        "endsAt": None,
        "createdAt": tt.createdAt(),
    }


def test_getters_of_timer_without_task():
    t = Timer()
    assert t.project() is None and t.epic() is None and t.story() is None


def test_getters_of_timer_with_task():
    t = (
        Task("project-one", "Task One")
        .changeEpic("epic-one")
        .changeStory("story-one")
    )
    tt = Timer().assignTo(t)
    assert (
        tt.project() == "project-one"
        and tt.epic() == "epic-one"
        and tt.story() == "story-one"
    )


def test_can_close_timer():
    t = (
        Task("project-one", "Task One")
        .changeEpic("epic-one")
        .changeStory("story-one")
    )
    tt = Timer().assignTo(t).close()
    assert tt.endsAt() is not None


def test_applying_record_to_timer():
    n = int(datetime.now().timestamp())
    tt = Timer()
    r = {
        "timer_id": 1,
        "task_id": 1,
        "starts_at": n,
        "ends_at": None,
        "created_at": n,
    }

    tt.apply(r)
    assert tt.toDict() == {
        "id": 1,
        "task": None,
        "startsAt": n,
        "endsAt": None,
        "createdAt": n,
    }


def test_timer_valid_primary_key():
    s = Task("project-one", "Task One")
    assert s.primaryKey() == "task_id"
