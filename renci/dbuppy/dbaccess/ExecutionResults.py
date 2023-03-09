from dataclasses import dataclass


@dataclass
class ExecutedScriptsResult:
    name: str
    haderror: bool