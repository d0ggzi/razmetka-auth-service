import psycopg2

from src.domain.exceptions import ResourceNotFound, ResourceAlreadyExist
from src.settings.config import settings
from src.utils.password import hash_password, check_password


class SQL:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            f"""
            host={settings.POSTGRES_HOST}
            port={settings.POSTGRES_PORT}
            dbname={settings.POSTGRES_DB}
            user={settings.POSTGRES_USER}
            password={settings.POSTGRES_PASSWORD}
        """
        )
        self.cursor = self.conn.cursor()

    def get_user(self, email: str):
        with self.conn:
            self.cursor.execute(
                "SELECT id, email, name, role.name FROM users JOIN role ON users.role_id = role.id WHERE email=%s", (email,)
            )
            result = self.cursor.fetchall()
            if bool(len(result)):
                return result[0][0], result[0][1], result[0][2], result[0][3]
            else:
                raise ResourceNotFound

    def reg_user(self, email: str, password: str, name: str, role_name: str) -> int:
        password = hash_password(password)
        with self.conn:
            self.cursor.execute(
                "SELECT email FROM users WHERE email=%s", (email,)
            )
            result = self.cursor.fetchall()
            if not bool(len(result)):
                try:
                    self.cursor.execute(
                        "SELECT id FROM role WHERE name=%s", (role_name,)
                    )
                    role_id = self.cursor.fetchone()[0]
                except Exception:
                    raise ResourceNotFound
                self.cursor.execute(
                    "INSERT INTO users (email, password, name, role_id) VALUES (%s, %s, %s, %s) "
                    "RETURNING id",
                    (email, password, name, role_id),
                )
                user_id = int(self.cursor.fetchall()[0][0])
                return user_id
            else:
                raise ResourceAlreadyExist


    def login(self, email: str, password: str) -> int:
        with self.conn:
            self.cursor.execute(
                "SELECT password, id FROM users WHERE email=%s", (email,)
            )
            result = self.cursor.fetchall()
            if bool(len(result)) and check_password(password, hashed_password=result[0][0]):
                return result[0][1]
            else:
                raise ResourceNotFound


db = SQL()
