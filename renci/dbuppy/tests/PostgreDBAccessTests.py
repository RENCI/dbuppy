import unittest


from renci.dbuppy.dbaccess.DBConnection import DBConnection
from renci.dbuppy.dbaccess.PostgreDBAccess import PostgreDBAccess


class PostgreDBAccessTests(unittest.TestCase):

    CONNECTION = DBConnection(DB_NAME="dbuppy222")


    def test_is_Versioned_returns_false_when_table_not_exist(self):
        self.recreate_db()
        dba = PostgreDBAccess(self.CONNECTION)
        res = dba.is_versioned()
        self.assertFalse(res)


    def test_add_version_table(self):

        self.recreate_db()

        dba = PostgreDBAccess(self.CONNECTION)
        dba.add_version_table()
        res = dba.is_versioned()
        self.assertTrue(res)

    def recreate_db(self):
        postgresdbcoonn = DBConnection(DB_NAME="postgres")
        dba = PostgreDBAccess(postgresdbcoonn)
        dba._execute_cmd(f'DROP DATABASE IF EXISTS {self.CONNECTION.DB_NAME};')
        dba._execute_cmd(f'CREATE DATABASE {self.CONNECTION.DB_NAME};')

    def test_add_executed_script(self):
        self.recreate_db()
        dba = PostgreDBAccess(self.CONNECTION)
        dba.add_version_table()
        dba.add_executed_script("script1", False)
        res = dba.get_executed_scripts()
        self.assertTrue(len(res) == 1)
