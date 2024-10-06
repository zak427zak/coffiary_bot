from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int = 3306

    # For SQLAlchemy
    def construct_sqlalchemy_url(self, driver="pymysql", host=None, port=None) -> str:
        """
        Constructs and returns a SQLAlchemy URL for this database configuration.
        """
        from sqlalchemy.engine.url import URL

        if not host:
            host = self.host
        if not port:
            port = self.port

        uri = URL.create(
            drivername=f"mysql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)

    @staticmethod
    def from_env(env: Env):
        """
        Creates the DbConfig object from environment variables.
        """
        host = env.str("DB_HOST")
        password = env.str("MYSQL_PASSWORD")  # измените на переменную окружения для пароля MySQL
        user = env.str("MYSQL_USER")  # измените на переменную окружения для пользователя MySQL
        database = env.str("MYSQL_DATABASE")  # измените на переменную окружения для базы данных MySQL
        port = env.int("DB_PORT", 3306)  # измените порт на стандартный порт MySQL
        return DbConfig(
            host=host, password=password, user=user, database=database, port=port
        )


@dataclass
class TgBot:
    token: str
    admin_ids: int
    use_redis: bool
    server_token: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=env.int("ADMINS"),
            use_redis=env.bool("USE_REDIS"),
            server_token=env.str("SERVER_TOKEN")
        ),
        db=DbConfig(
            host=env.str('MYSQL_HOST'),
            password=env.str('MYSQL_PASSWORD'),
            user=env.str('MYSQL_USER'),
            database=env.str('MYSQL_DATABASE')
        ),
        misc=Miscellaneous()
    )
