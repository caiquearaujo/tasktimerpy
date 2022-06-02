from datetime import datetime

from src.models.project import Project
from src.models.epic import Epic
from src.models.story import Story
from src.models.task import Task
from src.models.timer import Timer


def test_timer_with_task():
    p = Project({"name": "Project One"})
    e = Epic({"name": "Epic One"})
    e.assignTo(p)
    s = Story({"name": "Story One"})
    s.assignTo(e)
    t = Task({"name": "Task One"})
    t.assignTo(s)
    tt = Timer()
    tt.assignTo(t)
    assert tt.task() == t


def test_timer_same_project_of_task():
    p = Project({"name": "Project One"})
    e = Epic({"name": "Epic One"})
    e.assignTo(p)
    s = Story({"name": "Story One"})
    s.assignTo(e)
    t = Task({"name": "Task One"})
    t.assignTo(s)
    tt = Timer()
    tt.assignTo(t)
    assert tt.project() == p


def test_timer_same_epic_of_task():
    p = Project({"name": "Project One"})
    e = Epic({"name": "Epic One"})
    e.assignTo(p)
    s = Story({"name": "Story One"})
    s.assignTo(e)
    t = Task({"name": "Task One"})
    t.assignTo(s)
    tt = Timer()
    tt.assignTo(t)
    assert tt.epic() == e


def test_timer_same_story_of_task():
    p = Project({"name": "Project One"})
    e = Epic({"name": "Epic One"})
    e.assignTo(p)
    s = Story({"name": "Story One"})
    s.assignTo(e)
    t = Task({"name": "Task One"})
    t.assignTo(s)
    tt = Timer()
    tt.assignTo(t)
    assert tt.story() == s


def test_timer_custom_starts_at():
    now = int(datetime.now().timestamp()) - 10
    t = Timer({"starts_at": now})
    assert t.startsAt() == now


def test_timer_custom_created_at():
    now = int(datetime.now().timestamp()) - 10
    t = Timer({"created_at": now})
    assert t.createdAt() == now


def test_timer_custom_ends_at():
    now = int(datetime.now().timestamp()) - 10
    t = Timer({"ends_at": now})
    assert t.endsAt() == now


def test_timer_empty_ends_at():
    t = Timer()
    assert t.endsAt() == None


def test_timer_can_be_closed():
    t = Timer()
    t.close()
    assert t.endsAt() is not None


def test_timer_valid_primary_key():
    s = Timer()
    assert s.primaryKey() == "timer_id"
