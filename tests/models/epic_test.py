from src.models.project import Project
from src.models.epic import Epic


def test_epic_with_project():
    p = Project({"name": "Project One"})
    e = Epic({"name": "Epic One"})
    e.assignTo(p)
    assert e.project() == p
