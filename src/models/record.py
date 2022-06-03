from typing import Union
from datetime import datetime


class Record(object):
    def __init__(self):
        self.__id = None
        self.__created_at = int(datetime.now().timestamp())

    def apply(self, record: dict):
        self.__id = record.get(self.primaryKey(), None)
        self.__created_at = record.get("created_at", self.createdAt())
        return self

    def id(self) -> Union[int, None]:
        return self.__id

    def hasId(self):
        return self.__id is not None

    def createdAt(self) -> int:
        return self.__created_at

    def primaryKey(self) -> str:
        pass

    def toDict(self) -> dict:
        pass
