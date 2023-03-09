from dataclasses import dataclass


@dataclass
class DBConnection:
    HOST: str = 'localhost'
    PORT: int = 5455
    DB_NAME: str = 'postgres'
    USER: str = 'postgres'
    PASSWORD: str = '121212'
