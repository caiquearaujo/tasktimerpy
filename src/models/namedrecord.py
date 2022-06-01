from typing import Union
from datetime import datetime
from slugify import slugify
from models.record import Record


class NamedRecord(Record):
    def __init__(self, record: dict):
        super().__init__(record)

        if "name" not in record:
            raise Exception("Name must be set")

        self.__name = record.get("name")
        self.__slug = record.get("slug", None)
        self.__created_at = record.get(
            "created_at", int(datetime.now().timestamp())
        )

        if self.__slug != None:
            self.__slug = slugify(self.__slug)

    def name(self) -> Union[str, None]:
        return self.__name

    def slug(self) -> Union[str, None]:
        return self.__slug

    def createdAt(self) -> int:
        return self.__created_at
