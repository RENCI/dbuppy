from dataclasses import dataclass
from pathlib import PurePath


@dataclass
class SQLScript:
    """Contains SQLScript"""
    name: str
    path: PurePath
    # statements: tuple[str] = ()
    content: str = ""


class SQLScriptReader:
    """Reads file content into ScriptInfo.content"""

    @staticmethod
    def read(si: SQLScript):
        with open(si.path) as file:
            si.content = file.read()

    # @staticmethod
    # def set_statements(si: SQLScript):
    #     statements = si.content.split(";\n")
    #     res = []
    #     for s in statements:
    #         trimmed = s.strip()
    #         if trimmed != "":
    #             res.append(trimmed + ";")
    #     si.statements = res
    #




