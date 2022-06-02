from .namedrecord import NamedRecord


class Project(NamedRecord):
    def primaryKey(self) -> str:
        return "project_id"
