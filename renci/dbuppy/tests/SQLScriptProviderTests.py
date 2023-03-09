import unittest

from renci.dbuppy.sqlscripts.SQLScriptProvider import SQLScriptProvider


class SQLScriptProviderTests(unittest.TestCase):
    def test_get_create_scripts(self):
        p = SQLScriptProvider('./testdata/test1')
        createscripts = p.get_create_scripts()
        expected_names = ['20200101_0800_CreateAllTables.sql', '20200101_1520_AddRemovedItemsTable.sql']
        got_names = [n.name for n in createscripts]

        self.assertListEqual(expected_names, got_names)

        for cs in createscripts:
            self.assertIsNotNone(cs.path)


    def test_get_update_scripts(self):
        p = SQLScriptProvider('./testdata/test1')
        scripts = p.get_update_scripts()
        expected_names = ['20200201_0914_AddTables.sql', '20200202_1014_AddPermissions.sql']
        got_names = [n.name for n in scripts]

        self.assertListEqual(expected_names, got_names)


