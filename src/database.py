from asyncio import Task
from datetime import datetime
from pathlib import Path, PurePath
from typing import Union
from pypika import Query, Table
from slugify import slugify
import sqlite3
from models.epic import Epic

from models.project import Project
from models.story import Story
from models.timer import Timer


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
            print(e)

    def close(self):
        if self.conn != None:
            self.conn.close()

    def createProject(self, r: Project) -> Union[Project, None]:
        t = Table("projects")
        q = (
            Query.into(t)
            .columns(t.name, t.slug, t.created_at)
            .insert(r.name(), r.slug(), r.createdAt())
        )
        i = self.__commit(str(q))

        if i is None:
            return None

        return self.getProject(i)

    def createEpic(self, r: Epic) -> Union[Epic, None]:
        if r.project() is None or r.project().hasId() == False:
            raise sqlite3.Error(
                Exception("You must create project first")
            )

        t = Table("epics")
        q = (
            Query.into(t)
            .columns(t.project_id, t.name, t.slug, t.created_at)
            .insert(r.project().id(), r.name(), r.slug(), r.createdAt())
        )
        i = self.__commit(str(q))

        if i is None:
            return None

        return self.getEpic(i)

    def createStory(self, r: Story) -> Union[Story, None]:
        if r.epic() is None or r.epic().hasId() == False:
            raise sqlite3.Error(Exception("You must create epic first"))

        t = Table("stories")
        q = (
            Query.into(t)
            .columns(
                t.project_id, t.epic_id, t.name, t.slug, t.created_at
            )
            .insert(
                r.project().id(),
                r.epic().id(),
                r.name(),
                r.slug(),
                r.createdAt(),
            )
        )
        i = self.__commit(str(q))

        if i is None:
            return None

        return self.getStory(i)

    def createTask(self, r: Task) -> Union[Task, None]:
        if r.story() is None or r.story().hasId() == False:
            raise sqlite3.Error(Exception("You must create story first"))

        t = Table("task")
        q = (
            Query.into(t)
            .columns(
                t.project_id,
                t.epic_id,
                t.story_id,
                t.name,
                t.slug,
                t.created_at,
            )
            .insert(
                r.project().id(),
                r.epic().id(),
                r.story().id(),
                r.name(),
                r.slug(),
                r.createdAt(),
            )
        )
        i = self.__commit(str(q))

        if i is None:
            return None

        return self.getTask(i)

    def getProject(self, id: int) -> Union[Project, None]:
        t = Table("projects")
        q = Query.from_(t).select("*").where(t.project_id == id)
        r = self.__one(str(q))

        if r is None:
            return None

        o = Project(r)
        return o

    def getEpic(self, id: int) -> Union[Epic, None]:
        t = Table("epics")
        q = Query.from_(t).select("*").where(t.epic_id == id)
        r = self.__one(str(q))

        if r is None:
            return None

        o = Epic(r)
        o.assignTo(self.getProject(r.project_id or -1))
        return o

    def getStory(self, id: int) -> Union[Story, None]:
        t = Table("stories")
        q = Query.from_(t).select("*").where(t.story_id == id)
        r = self.__one(str(q))

        if r is None:
            return None

        o = Story(r)
        o.assignTo(self.getEpic(r.epic_id or -1))
        return o

    def getTask(self, id: int) -> Union[Task, None]:
        t = Table("tasks")
        q = Query.from_(t).select("*").where(t.task_id == id)
        r = self.__one(str(q))

        if r is None:
            return None

        o = Task(r)
        o.assignTo(self.getStory(r.story_id or -1))
        return o

    def getTimer(self, id: int) -> Union[Task, None]:
        t = Table("timers")
        q = Query.from_(t).select("*").where(t.task_id == id)
        r = self.__one(str(q))

        if r is None:
            return None

        o = Timer(r)
        o.assignTo(self.getTask(r.task_id or -1))
        return o

    def timerOpen(self, r: Timer) -> Union[Timer, None]:
        if r.task() is None or r.task().hasId() == False:
            raise sqlite3.Error(Exception("You must create task first"))

        t = Table("timers")
        q = (
            Query.into(t)
            .columns(
                t.project_id,
                t.epic_id,
                t.story_id,
                t.task_id,
                t.starts_at,
                t.created_at,
            )
            .insert(
                r.project().id(),
                r.epic().id(),
                r.story().id(),
                r.task().id(),
                r.startsAt(),
                r.createdAt(),
            )
        )
        i = self.__commit(str(q))

        if i is None:
            return None

        return self.getTimer(i)

    def timerClose(self, r: Timer) -> Timer:
        if r.hasId() == False:
            raise sqlite3.Error(Exception("You must start timer first"))

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
        q = Query.from_(t).select("*").where(t.ends_at.null())
        r = self.__one(str(q))

        if r is None:
            return None

        o = Timer(r)
        o.assignTo(self.getTask(r.task_id or -1))
        return o

    def existsProject(self, id: int) -> int:
        if (
            self.__exists("projects", "project_id", "project_id", id)
            == False
        ):
            raise sqlite3.Error(
                Exception(
                    "Cannot find project by project_id {id}".format(id=id)
                )
            )

        return id

    def existsEpic(self, id: int) -> int:
        if self.__exists("epics", "epic_id", "epic_id", id) == False:
            raise sqlite3.Error(
                Exception(
                    "Cannot find epic by epic_id {id}".format(id=id)
                )
            )

        return id

    def existsStory(self, id: int) -> int:
        if self.__exists("stories", "story_id", "story_id", id) == False:
            raise sqlite3.Error(
                Exception(
                    "Cannot find story by story_id {id}".format(id=id)
                )
            )

        return id

    def existsTask(self, id: int) -> int:
        if self.__exists("tasks", "task_id", "task_id", id) == False:
            raise sqlite3.Error(
                Exception(
                    "Cannot find task by task_id {id}".format(id=id)
                )
            )

        return id

    def existstimer(self, id: int) -> int:
        if self.__exists("timers", "timer_id", "timer_id", id) == False:
            raise sqlite3.Error(
                Exception(
                    "Cannot find timer by timer_id {id}".format(id=id)
                )
            )

        return id

    def __exists(
        self, table: str, pk: str, column: str, value: str
    ) -> bool:
        self.last_err = None

        try:
            r = self.conn.cursor().execute(
                "SELECT * FROM {t} WHERE {c} = '{v}'".format(
                    pk=pk, t=table, c=column, v=value
                )
            )

            if r.fetchone():
                return True

            return False
        except sqlite3.Error as e:
            self.conn.rollback()
            self.last_err = e
            return False

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

    def __commit(self, query: str) -> Union[int, None]:
        self.last_err = None

        try:
            c = self.conn.cursor()
            c.execute(query)
            return c.lastrowid
        except sqlite3.Error as e:
            self.conn.rollback()
            self.last_err = e
            return None

    def __create(self, conn: sqlite3.Connection):
        """
        Create tables if them does not exist.
        """
        projects = """
		CREATE TABLE IF NOT EXISTS projects (
			project_id integer PRIMARY KEY,
			name text NOT NULL,
			slug text NULL,
			created_at integer NOT NULL
		);"""

        epics = """
		CREATE TABLE IF NOT EXISTS epics (
			epic_id integer PRIMARY KEY,
			project_id integer NOT NULL,
			name text NOT NULL,
			slug text NULL,
			created_at integer NOT NULL,
			FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE
		);"""

        stories = """
		CREATE TABLE IF NOT EXISTS stories (
			story_id integer PRIMARY KEY,
			project_id integer NOT NULL,
			epic_id integer NOT NULL,
			name text NOT NULL,
			slug text NULL,
			created_at integer NOT NULL,
			FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE,
			FOREIGN KEY (epic_id) REFERENCES epics (epic_id) ON DELETE CASCADE
		);"""

        tasks = """
		CREATE TABLE IF NOT EXISTS tasks (
			task_id integer PRIMARY KEY,
			project_id integer NOT NULL,
			epic_id integer NOT NULL,
			story_id integer NOT NULL,
			name text NOT NULL,
			slug text NULL,
			created_at integer NOT NULL,
			FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE,
			FOREIGN KEY (epic_id) REFERENCES epics (epic_id) ON DELETE CASCADE,
			FOREIGN KEY (story_id) REFERENCES stories (story_id) ON DELETE CASCADE
		);"""

        timers = """
		CREATE TABLE IF NOT EXISTS timers (
			timer_id integer PRIMARY KEY,
			project_id integer NOT NULL,
			epic_id integer NOT NULL,
			story_id integer NOT NULL,
			task_id integer NOT NULL,
			starts_at integer NOT NULL,
			ends_at integer NULL,
			created_at integer NOT NULL,
			FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE,
			FOREIGN KEY (epic_id) REFERENCES epics (epic_id) ON DELETE CASCADE,
			FOREIGN KEY (story_id) REFERENCES stories (story_id) ON DELETE CASCADE,
			FOREIGN KEY (task_id) REFERENCES tasks (task_id) ON DELETE CASCADE
		);"""

        cursor = conn.cursor()
        cursor.execute(projects)
        cursor.execute(epics)
        cursor.execute(stories)
        cursor.execute(tasks)
        cursor.execute(timers)

        conn.commit()
