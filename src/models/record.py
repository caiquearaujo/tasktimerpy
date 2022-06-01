from typing import Union


class Record:
    def __init__(self, record: dict):
        self.__id = record.get(self.primaryKey(), None)

    def id(self) -> Union[int, None]:
        return self.__id

    def hasId(self):
        return self.__id is not None
