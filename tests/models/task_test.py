from src.models.project import Project
from src.models.epic import Epic
from src.models.story import Story
from src.models.task import Task


def test_task_with_story():
    p = Project({"name": "Project One"})
    e = Epic({"name": "Epic One"})
    e.assignTo(p)
    s = Story({"name": "Story One"})
    s.assignTo(e)
    t = Task({"name": "Task One"})
    t.assignTo(s)
    assert t.story() == s


def test_task_same_project_of_story():
    p = Project({"name": "Project One"})
    e = Epic({"name": "Epic One"})
    e.assignTo(p)
    s = Story({"name": "Story One"})
    s.assignTo(e)
    t = Task({"name": "Task One"})
    t.assignTo(s)
    assert t.project() == p


def test_task_same_epic_of_story():
    p = Project({"name": "Project One"})
    e = Epic({"name": "Epic One"})
    e.assignTo(p)
    s = Story({"name": "Story One"})
    s.assignTo(e)
    t = Task({"name": "Task One"})
    t.assignTo(s)
    assert t.epic() == e


def test_task_can_mark_as_done():
    s = Task({"name": "Task One"})
    s.done()
    assert s.isDone()


def test_task_is_done():
    s = Task({"name": "Task One", "done": 1})
    assert s.isDone()


def test_task_valid_primary_key():
    s = Task({"name": "Task One"})
    assert s.primaryKey() == "task_id"
