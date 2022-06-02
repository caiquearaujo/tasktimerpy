from typing import Union
from .epic import Epic


class Story(Epic):
    def __init__(self, record: dict):
        super().__init__(record)
        self.__epic = None

    def assignTo(self, epic: Epic):
        self.__epic = epic
        super().assignTo(epic.project())

    def epic(self) -> Union[Epic, None]:
        return self.__epic

    def primaryKey(self) -> str:
        return "story_id"
