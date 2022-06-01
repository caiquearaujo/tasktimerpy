from models.namedrecord import NamedRecord


class Project(NamedRecord):
    def primaryKey() -> str:
        return "project_id"
