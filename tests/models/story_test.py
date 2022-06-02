from src.models.project import Project
from src.models.epic import Epic
from src.models.story import Story


def test_story_with_epic():
    p = Project({"name": "Project One"})
    e = Epic({"name": "Epic One"})
    e.assignTo(p)
    s = Story({"name": "Story One"})
    s.assignTo(e)
    assert s.epic() == e


def test_story_same_project_of_epic():
    p = Project({"name": "Project One"})
    e = Epic({"name": "Epic One"})
    e.assignTo(p)
    s = Story({"name": "Story One"})
    s.assignTo(e)
    assert s.project() == p


def test_story_valid_primary_key():
    s = Story({"name": "Story One"})
    assert s.primaryKey() == "story_id"
