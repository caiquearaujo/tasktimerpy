from src.models.project import Project
from src.models.epic import Epic


def test_epic_with_project():
    p = Project({"name": "Project One"})
    e = Epic({"name": "Epic One"})
    e.assignTo(p)
    assert e.project() == p


def test_epic_valid_primary_key():
    s = Epic({"name": "Epic One"})
    assert s.primaryKey() == "epic_id"
