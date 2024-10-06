from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import func
from typing_extensions import Annotated

# Создаем экземпляр SQLAlchemy
db = SQLAlchemy()

# Настройка сессии
Session = scoped_session(sessionmaker())


# Базовый класс для всех моделей
class Base(DeclarativeBase):
    query = db.session.query_property()  # Настройка query для доступа через модели


# Миксин для автоматического определения имени таблицы
class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


# Миксин для автоматического добавления метаданных о времени создания
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())


# Тип для идентификатора
int_pk = Annotated[int, mapped_column(primary_key=True)]
