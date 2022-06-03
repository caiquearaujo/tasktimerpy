import gettext
from pathlib import Path, PurePath
from typing import List, Union
from pypika import Query, Table
import sqlite3

from .models.task import Task
from .models.timer import Timer

_ = gettext.gettext


class Database:
    def __init__(self, path: str, db_name: str = "tasktimerpy"):
        self.db_file = (
            Path(PurePath(path, db_name + ".sqlite3"))
            .joinpath()
            .absolute()
        )
        self.conn = None
        self.last_err = None

        self.mount()

    def mount(self):
        """
        Mount a connection to a SQLite Database.
        """

        try:
            self.conn = sqlite3.connect(self.db_file)
            self.__create(self.conn)
        except sqlite3.Error as e:
            self.conn.rollback()
            raise e

    def close(self):
        if self.conn != None:
            self.conn.close()

    def createTask(self, r: Task) -> Union[Task, None]:
        t = Table("tasks")
        q = (
            Query.into(t)
            .columns(
                t.project,
                t.epic,
                t.story,
                t.name,
                t.created_at,
            )
            .insert(
                r.project(),
                r.epic(),
                r.story(),
                r.name(),
                r.createdAt(),
            )
        )
        i = self.__commit(str(q))

        if i is None:
            return None

        return self.getTask(i)

    def getTask(self, id: int) -> Union[Task, None]:
        t = Table("tasks")
        q = Query.from_(t).select("*").where(t.task_id == id)
        r = self.__one(str(q))

        if r is None:
            return None

        return Task(r.get("project"), r.get("name")).apply(r)

    def getUndoneTasks(self) -> Union[List[Task], None]:
        t = Table("tasks")
        q = (
            Query.from_(t)
            .select("*")
            .where(t.done == 0)
            .orderby(t.created_at)
            .limit(15)
        )
        r = self.__all(str(q))

        if r is None:
            return None

        tasks = []

        for i in r:
            tasks.append(Task(i.get("project"), i.get("name")).apply(i))

        return tasks

    def getTimer(self, id: int) -> Union[Task, None]:
        t = Table("timers")
        q = Query.from_(t).select("*").where(t.task_id == id)
        r = self.__one(str(q))

        if r is None:
            return None

        o = Timer().apply(r)
        o.assignTo(self.getTask(r.get("task_id", -1)))
        return o

    def taskDone(self, r: Task) -> Task:
        if r.hasId() == False:
            raise sqlite3.Error(Exception("You must create task first"))

        r = self.getTask(r.id())

        if r is None:
            raise sqlite3.Error(Exception("Task does not exists"))

        r.markAsDone()

        t = Table("tasks")
        q = Query.update(t).set(t.done, 1).where(t.task_id == r.id())
        self.__commit(str(q))
        return r

    def timerOpen(self, r: Task) -> Union[Timer, None]:
        if r.hasId() == False:
            raise sqlite3.Error(Exception("You must create task first"))

        r = self.getTask(r.id())

        if r is None:
            raise sqlite3.Error(Exception("Task does not exists"))

        x = Timer()
        x.assignTo(r)

        t = Table("timers")
        q = (
            Query.into(t)
            .columns(
                t.task_id,
                t.starts_at,
                t.created_at,
            )
            .insert(
                x.task().id(),
                x.startsAt(),
                x.createdAt(),
            )
        )
        i = self.__commit(str(q))

        if i is None:
            return None

        return self.getTimer(i)

    def timerClose(self, r: Timer) -> Timer:
        if r.hasId() == False:
            raise sqlite3.Error(Exception("You must start timer first"))

        r = self.getTimer(r.id())

        if r is None:
            raise sqlite3.Error(Exception("Timer does not exists"))

        r.close()

        t = Table("timers")
        q = (
            Query.update(t)
            .set(t.ends_at, r.endsAt())
            .where(t.timer_id == r.id())
        )
        self.__commit(str(q))
        return r

    def timerActive(self) -> Union[Timer, None]:
        t = Table("timers")
        q = Query.from_(t).select("*").where(t.ends_at.isnull())
        r = self.__one(str(q))

        if r is None:
            return None

        o = Timer().apply(r)
        o.assignTo(self.getTask(r.get("task_id", -1)))
        return o

    def __one(self, query: str) -> Union[dict, None]:
        self.last_err = None

        try:
            c = self.conn.cursor()
            c.execute(query)
            fields = [field[0] for field in c.description]
            values = c.fetchone()
            return dict(zip(fields, values))
        except sqlite3.Error as e:
            self.last_err = e
            return None
        except TypeError as e:
            self.last_err = e
            return None

    def __all(self, query: str) -> Union[list, None]:
        self.last_err = None

        try:
            c = self.conn.cursor()
            c.execute(query)
            columns = [col[0] for col in c.description]
            rows = [dict(zip(columns, row)) for row in c.fetchall()]
            return rows
        except sqlite3.Error as e:
            self.last_err = e
            return None
        except TypeError as e:
            self.last_err = e
            return None

    def __commit(self, query: str) -> Union[int, None]:
        self.last_err = None

        try:
            c = self.conn.cursor()
            c.execute(query)
            self.conn.commit()
            return c.lastrowid
        except sqlite3.Error as e:
            self.conn.rollback()
            self.last_err = e
            return None

    def __create(self, conn: sqlite3.Connection):
        """
        Create tables if them does not exist.
        """

        tasks = """
		CREATE TABLE IF NOT EXISTS tasks (
			task_id integer PRIMARY KEY,
			project text NOT NULL,
			epic text NULL,
			story text NULL,
			done integer NOT NULL DEFAULT 0,
			name text NOT NULL,
			created_at integer NOT NULL
		);"""

        timers = """
		CREATE TABLE IF NOT EXISTS timers (
			timer_id integer PRIMARY KEY,
			task_id integer NOT NULL,
			starts_at integer NOT NULL,
			ends_at integer NULL,
			created_at integer NOT NULL,
			FOREIGN KEY (task_id) REFERENCES tasks (task_id) ON DELETE CASCADE
		);"""

        cursor = conn.cursor()
        cursor.execute(tasks)
        cursor.execute(timers)

        conn.commit()
