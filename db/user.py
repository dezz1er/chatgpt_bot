from sqlalchemy import Integer, VARCHAR, BigInteger, Enum
from sqlalchemy.orm import mapped_column
from structures.role import Role
from .base import Base


class User(Base):
    """ Класс пользователя """
    __tablename__ = 'users'
    user_id = mapped_column(BigInteger, unique=True, nullable=False,
                            primary_key=True)
    username = mapped_column(VARCHAR(32), unique=False, nullable=True)
    balance = mapped_column(Integer, default=0)
    locale = mapped_column(VARCHAR(2), default='ru')
    role = mapped_column(Enum(Role), default=Role.USER)

    def __str__(self) -> str:
        return f"<User:{self.user_id}>"

    def __repr__(self):
        return self.__str__()
