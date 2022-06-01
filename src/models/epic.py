from typing import Union
from models.namedrecord import NamedRecord
from models.project import Project


class Epic(NamedRecord):
    def __init__(self, record: dict):
        super().__init__(record)
        self.__project = None

    def assignTo(self, project: Project):
        self.__project = project

    def project(self) -> Union[Project, None]:
        return self.__project

    def primaryKey() -> str:
        return "epic_id"
