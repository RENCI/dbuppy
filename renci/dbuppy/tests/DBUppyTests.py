import unittest
from unittest.mock import Mock

from renci.dbuppy import DBUppy
from renci.dbuppy.dbaccess.ExecutionResults import ExecutedScriptsResult
from renci.dbuppy.sqlscripts.SQLScript import SQLScript



class DBUppyTests(unittest.TestCase):

    def get_Script(self, name):
        s = SQLScript(name=name, path= '/pathtoscripts/' + name)
        return s

    def get_fake_ScriptProvider_with_no_history(self):
        scriptprovider = Mock()
        scriptprovider.get_update_scripts = Mock()
        scriptprovider.get_update_scripts.return_value = []
        return scriptprovider

    def get_fake_DBAccess(self):
        dba = Mock()
        dba.get_executed_scripts = Mock()
        dba.get_executed_scripts.return_value = []
        dba.execute = Mock()
        return dba

    def test_get_scripts_to_execute(self):
        script_provider = self.get_fake_ScriptProvider_with_no_history()
        script_provider.get_update_scripts.return_value = [self.get_Script('20200101_s1.sql'), self.get_Script('20200102_s2.sql')]

        dbaccess = self.get_fake_DBAccess()
        dbaccess.get_executed_scripts.return_value = [ExecutedScriptsResult('20200101_s1.sql', False)]

        dbu = DBUppy(dbaccess=dbaccess, scriptprovider=script_provider)
        list_to_execute = dbu.get_scripts_for_update()
        self.assertEqual(1, len(list_to_execute))
        self.assertEqual('20200102_s2.sql', list_to_execute[0].name)


    def test_update(self):
        script_provider = self.get_fake_ScriptProvider_with_no_history()
        script_provider.get_update_scripts.return_value = [self.get_Script('20200101_s1.sql')]
        dbaccess = self.get_fake_DBAccess()
        dbu = DBUppy(dbaccess=dbaccess, scriptprovider=script_provider)
        dbu.update()
        dbaccess.execute.assert_called_once()




if __name__ == '__main__':
    unittest.main()
