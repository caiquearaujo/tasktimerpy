import gettext
from typing import Union
from datetime import datetime
from .record import Record

_ = gettext.gettext


class NamedRecord(Record):
    def __init__(self, record: dict):
        super().__init__(record)

        if "name" not in record:
            raise Exception(_("Name must be set"))

        self.__name = record.get("name")
        self.__created_at = record.get(
            "created_at", int(datetime.now().timestamp())
        )

    def name(self) -> Union[str, None]:
        return self.__name

    def createdAt(self) -> int:
        return self.__created_at
