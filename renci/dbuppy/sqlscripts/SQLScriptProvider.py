from pathlib import Path

from renci.dbuppy.sqlscripts.SQLScript import SQLScript


"""Provides lists of SQL scripts"""
class SQLScriptProvider:
    IGNORE_PREFIX = '_'
    CREATE_DIR = 'CREATE'
    UPDATE_DIR = 'UPDATE'

    def __init__(self, path_to_dir: str):
        self.create_dir = Path(path_to_dir, self.CREATE_DIR)
        self.update_dir = Path(path_to_dir, self.UPDATE_DIR)

    def _get_files_in_dir(self, dir: Path) -> list[Path]:
        res = []
        for i in dir.iterdir():
            if i.is_file() and not i.name.startswith(self.IGNORE_PREFIX):
                res.append(i)
        return res

    def _get_SQLScripts_from_paths(self, files):
        res = [SQLScript(name=f.name, path=f) for f in files]
        res.sort(key=lambda r: r.name)
        return res

    def get_create_scripts(self) -> list[SQLScript]:
        """Returns CREATE scripts"""
        files = self._get_files_in_dir(self.create_dir)
        res = self._get_SQLScripts_from_paths(files)
        return res

    def get_update_scripts(self) -> list[SQLScript]:
        """Returns UPDATE scripts"""
        files = self._get_files_in_dir(self.update_dir)
        res = self._get_SQLScripts_from_paths(files)
        return res


