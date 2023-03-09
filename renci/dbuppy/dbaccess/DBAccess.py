import abc

from renci.dbuppy.dbaccess.DBConnection import DBConnection
from renci.dbuppy.dbaccess.ExecutionResults import ExecutedScriptsResult
from renci.dbuppy.sqlscripts.SQLScript import SQLScript


class DBAccess(metaclass=abc.ABCMeta):
    """This class provides basic interface to run queries/commands against database"""

    @abc.abstractmethod
    def __init__(self,  connection: DBConnection):
        pass

    @abc.abstractmethod
    def check_connection_to_DB(self) -> bool:
        """Checks if application can connect to DB"""
        pass

    @abc.abstractmethod
    def execute(self, cmd: SQLScript):
        """Executes SQL command"""
        pass

    @abc.abstractmethod
    def is_versioned(self) -> bool:
        """Checks if a database contains version table"""
        pass

    @abc.abstractmethod
    def add_version_table(self):
        """Adds version table to a database"""
        pass

    @abc.abstractmethod
    def get_executed_scripts(self) -> list[ExecutedScriptsResult]:
        """Returns executed scripts"""
        pass

    @abc.abstractmethod
    def add_executed_script(self, script: str, haderror: bool):
        """Adds executed script"""
        pass

    class Exception(Exception):
        """High level exception wrapper for exceptions happened while interracting with DB"""
        pass
