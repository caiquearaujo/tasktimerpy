import gettext
from pathlib import Path, PurePath
from typing import List, Union
from pypika import Query, Table, JoinType
import sqlite3

from .models.epic import Epic
from .models.project import Project
from .models.story import Story
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

    def createProject(self, r: Project) -> Union[Project, None]:
        t = Table("projects")
        q = (
            Query.into(t)
            .columns(t.name, t.created_at)
            .insert(r.name(), r.createdAt())
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
            .columns(t.project_id, t.name, t.created_at)
            .insert(r.project().id(), r.name(), r.createdAt())
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
            .columns(t.project_id, t.epic_id, t.name, t.created_at)
            .insert(
                r.project().id(),
                r.epic().id(),
                r.name(),
                r.createdAt(),
            )
        )
        i = self.__commit(str(q))

        if i is None:
            return None

        return self.getStory(i)

    def createTask(self, r: Task) -> Union[Task, None]:
        if r.story() is None or r.story().hasId() == False:
            raise sqlite3.Error(
                Exception(_("You must create story first"))
            )

        t = Table("tasks")
        q = (
            Query.into(t)
            .columns(
                t.project_id,
                t.epic_id,
                t.story_id,
                t.name,
                t.created_at,
            )
            .insert(
                r.project().id(),
                r.epic().id(),
                r.story().id(),
                r.name(),
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
        o.assignTo(self.getProject(r.get("project_id", -1)))
        return o

    def getStory(self, id: int) -> Union[Story, None]:
        t = Table("stories")
        q = Query.from_(t).select("*").where(t.story_id == id)
        r = self.__one(str(q))

        if r is None:
            return None

        o = Story(r)
        o.assignTo(self.getEpic(r.get("epic_id", -1)))
        return o

    def getTask(self, id: int) -> Union[Task, None]:
        t = Table("tasks")
        q = Query.from_(t).select("*").where(t.task_id == id)
        r = self.__one(str(q))

        if r is None:
            return None

        o = Task(r)
        o.assignTo(self.getStory(r.get("story_id", -1)))
        return o

    def getUndoneProjects(self) -> Union[List[Project], None]:
        t = Table("projects")
        i = Table("tasks")
        q = (
            Query.from_(t)
            .join(i, JoinType.left)
            .on(t.project_id == i.project_id)
            .select(t.project_id, t.name, t.created_at)
            .where((i.done == 0) | (i.done.isnull()))
            .orderby(i.created_at)
            .groupby(t.project_id)
            .limit(15)
        )
        r = self.__all(str(q))

        if r is None:
            return None

        projects = []

        for i in r:
            projects.append(Project(i))

        return projects

    def getUndoneEpics(self, project: Project) -> Union[List[Epic], None]:
        t = Table("epics")
        i = Table("tasks")
        q = (
            Query.from_(t)
            .join(i, JoinType.left)
            .on(t.epic_id == i.epic_id)
            .select(t.epic_id, t.project_id, t.name, t.created_at)
            .where(
                (i.project_id == project.id()) | (i.project_id.isnull())
            )
            .where((i.done == 0) | (i.done.isnull()))
            .orderby(i.created_at)
            .groupby(t.epic_id)
            .limit(15)
        )
        r = self.__all(str(q))

        if r is None:
            return None

        epics = []

        for i in r:
            o = Epic(i)
            o.assignTo(self.getProject(i.get("project_id", -1)))
            epics.append(o)

        return epics

    def getUndoneStories(self, epic: Epic) -> Union[List[Story], None]:
        t = Table("stories")
        i = Table("tasks")
        q = (
            Query.from_(t)
            .join(i, JoinType.left)
            .on(t.story_id == i.story_id)
            .select(
                t.story_id, t.project_id, t.epic_id, t.name, t.created_at
            )
            .where((i.epic_id == epic.id()) | (i.epic_id.isnull()))
            .where((i.done == 0) | (i.done.isnull()))
            .orderby(i.created_at)
            .groupby(t.story_id)
            .limit(15)
        )
        r = self.__all(str(q))

        if r is None:
            return None

        stories = []

        for i in r:
            o = Story(i)
            o.assignTo(self.getEpic(i.get("epic_id", -1)))
            stories.append(o)

        return stories

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
            o = Task(i)
            o.assignTo(self.getStory(i.get("story_id", -1)))
            tasks.append(o)

        return tasks

    def getTimer(self, id: int) -> Union[Task, None]:
        t = Table("timers")
        q = Query.from_(t).select("*").where(t.task_id == id)
        r = self.__one(str(q))

        if r is None:
            return None

        o = Timer(r)
        o.assignTo(self.getTask(r.get("task_id", -1)))
        return o

    def taskDone(self, r: Task) -> Task:
        if r.hasId() == False:
            raise sqlite3.Error(Exception("You must create task first"))

        r = self.getTask(r.id())

        if r is None:
            raise sqlite3.Error(Exception("Task does not exists"))

        r.done()

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
                t.project_id,
                t.epic_id,
                t.story_id,
                t.task_id,
                t.starts_at,
                t.created_at,
            )
            .insert(
                x.project().id(),
                x.epic().id(),
                x.story().id(),
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

        o = Timer(r)
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
        projects = """
		CREATE TABLE IF NOT EXISTS projects (
			project_id integer PRIMARY KEY,
			name text NOT NULL,
			created_at integer NOT NULL
		);"""

        epics = """
		CREATE TABLE IF NOT EXISTS epics (
			epic_id integer PRIMARY KEY,
			project_id integer NOT NULL,
			name text NOT NULL,
			created_at integer NOT NULL,
			FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE
		);"""

        stories = """
		CREATE TABLE IF NOT EXISTS stories (
			story_id integer PRIMARY KEY,
			project_id integer NOT NULL,
			epic_id integer NOT NULL,
			name text NOT NULL,
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
			done integer NOT NULL DEFAULT 0,
			name text NOT NULL,
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
