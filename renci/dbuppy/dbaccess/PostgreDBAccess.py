import logging
from typing import NamedTuple

import psycopg2

from renci.dbuppy.dbaccess.DBAccess import DBAccess
from renci.dbuppy.dbaccess.DBConnection import DBConnection
from renci.dbuppy.dbaccess.ExecutionResults import ExecutedScriptsResult
from renci.dbuppy.sqlscripts.SQLScript import SQLScript, SQLScriptReader


class PostgreDBAccess(DBAccess):
    """Provides connection to Postgresql DB"""

    def __init__(self, connection: DBConnection):
        self.connection = connection

    def _get_connection(self):
        conn = psycopg2.connect(host=self.connection.HOST,
                                port=self.connection.PORT,
                                database=self.connection.DB_NAME,
                                user=self.connection.USER,
                                password=self.connection.PASSWORD)
        return conn

    def _execute_cmd(self, sqlcommand: str, params: dict = None):
        """
        This method is used to execute SQL commands.
        :param sqlcommand: string that contains SQL command
        :param params: dictionary with parameters for SQL command
        :param transaction: True (default) to execute SQl command in a transaction
        :return: None
        """
        conn = None

        try:
            conn = self._get_connection()
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

            with conn.cursor() as cur:
                cur.execute(sqlcommand, params)
                cur.close()
                conn.commit()

        except Exception as ex:
            raise DBAccess.Exception(ex)
        finally:
            if conn is not None:
                conn.close()

    def _execute_query(self, sqlquery: str, params: tuple = None) -> list[list]:
        """
        This method is used to execute SQL commands.
        :param sqlcommand: string that contains SQL command
        :param params: dictionary with parameters for SQL command
        :return: None
        """
        rows = None

        with self._get_connection() as conn:
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

            with conn.cursor() as cur:
                cur.execute(sqlquery, params)
                rows = cur.fetchall()

        return rows

    def check_connection_to_DB(self):
        logging.info(f'Checking connection to [{self.connection.HOST}:{self.connection.PORT}] {self.connection.DB_NAME}')
        self._execute_query('SELECT version()')
        logging.info(f'Connection ok')

    def is_versioned(self) -> bool:
        res = self._execute_query('''
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name='dbuppy' 
        ''')

        return len(res) > 0

    def add_version_table(self):
        self._execute_cmd('''create table dbuppy
                            (
                                "scriptname" text not null,
                                "haderror"   bool not null,
                                "created"  timestamptz not null
                            );''')

    def get_executed_scripts(self) -> list[ExecutedScriptsResult]:
        rows = self._execute_query('''select scriptname, haderror from "dbuppy" order by created''')
        res = [ExecutedScriptsResult(r[0], r[1]) for r in rows]
        return res

    def add_executed_script(self, script: str, haderror: bool):
        res = self._execute_query ('''insert into "dbuppy" (scriptname, haderror, created) values (%s, %s, CURRENT_TIMESTAMP); SELECT 1;''',
                            (script, haderror))

    def execute(self, script: SQLScript):
        SQLScriptReader.read(script)
        self._execute_cmd(script.content)

