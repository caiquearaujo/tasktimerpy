import sqlite3;
import pathlib;
import pypika;

class Database:
	def __init__(self, path: str, db_name: str = 'tasktimerpy'):
		self.db_file = pathlib.Path(pathlib.PurePath(path, db_name+'.sqlite3')).joinpath().absolute();
		self.conn = None;

		self.mount();

	def mount (self):
		"""
		Mount a connection to a SQLite Database.
		"""

		try:
			self.conn = sqlite3.connect(self.db_file);
			self.__create(self.conn);
		except sqlite3.Error as e:
			print(e);

	def close (self):
		if (self.conn != None) :
			self.conn.close();

	def __create (self, conn: sqlite3.Connection):
		"""
		Create tables if them does not exist.
		"""
		projects = """
		CREATE TABLE IF NOT EXISTS projects ( 
			project_id integer PRIMARY KEY,
			name text NOT NULL,
			slug text NULL,
			created_at integer NOT NULL
		);""";

		epics = """
		CREATE TABLE IF NOT EXISTS epics (
			epic_id integer PRIMARY KEY,
			project_id integer NOT NULL,
			name text NOT NULL,
			slug text NULL,
			created_at integer NOT NULL,
			FOREIGN KEY (project_id) REFERENCES projects (project_id)
		);""";

		stories = """
		CREATE TABLE IF NOT EXISTS stories (
			story_id integer PRIMARY KEY,
			project_id integer NOT NULL,
			epic_id integer NULL,
			name text NOT NULL,
			slug text NULL,
			created_at integer NOT NULL,
			FOREIGN KEY (project_id) REFERENCES projects (project_id),
			FOREIGN KEY (epic_id) REFERENCES epics (epic_id)
		);""";

		tasks = """
		CREATE TABLE IF NOT EXISTS tasks (
			task_id integer PRIMARY KEY,
			project_id integer NOT NULL,
			epic_id integer NULL,
			story_id integer NULL,
			name text NOT NULL,
			slug text NULL,
			created_at integer NOT NULL,
			FOREIGN KEY (project_id) REFERENCES projects (project_id),
			FOREIGN KEY (epic_id) REFERENCES epics (epic_id),
			FOREIGN KEY (story_id) REFERENCES stories (story_id)
		);""";

		timers = """
		CREATE TABLE IF NOT EXISTS timers (
			project_id integer NOT NULL,
			epic_id integer NULL,
			story_id integer NULL,
			task_id integer NULL,
			starts_at integer NOT NULL,
			ends_at integer NULL,
			created_at integer NOT NULL,
			FOREIGN KEY (project_id) REFERENCES projects (project_id),
			FOREIGN KEY (epic_id) REFERENCES epics (epic_id),
			FOREIGN KEY (story_id) REFERENCES stories (story_id),
			FOREIGN KEY (task_id) REFERENCES tasks (task_id)
		);""";

		cursor = conn.cursor();
		cursor.execute(projects);
		cursor.execute(epics);
		cursor.execute(stories);
		cursor.execute(tasks);
		cursor.execute(timers);
		
		conn.commit();

