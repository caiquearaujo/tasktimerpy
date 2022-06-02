from datetime import datetime
import pytest
from src.models.project import Project


def test_project_empty_name():
    with pytest.raises(Exception, match="Name must be set"):
        Project({})


def test_project_name():
    obj = Project({"name": "Project One"})
    assert obj.name() == "Project One"


def test_project_created_at():
    obj = Project({"name": "Project One"})
    assert isinstance(obj.createdAt(), int)


def test_project_id():
    obj = Project({"name": "Project One", "project_id": 1})
    assert obj.id() == 1


def test_project_has_not_id():
    obj = Project({"name": "Project One"})
    assert obj.hasId() == False


def test_project_has_id():
    obj = Project({"name": "Project One", "project_id": 1})
    assert obj.hasId() == True


def test_timer_custom_created_at():
    now = int(datetime.now().timestamp()) - 10
    p = Project({"name": "Project One", "created_at": now})
    assert p.createdAt() == now


def test_project_valid_primary_key():
    s = Project({"name": "Project One"})
    assert s.primaryKey() == "project_id"
