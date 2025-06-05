#!/usr/bin/env python3
"""
DB class for user operations
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """Database connection class"""

    def __init__(self):
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        if self.__session is None:
            Session = sessionmaker(bind=self._engine)
            self.__session = Session()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user and returns the User object"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find user by arbitrary keyword arguments"""
        if not kwargs:
            raise InvalidRequestError
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound
        except Exception:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user’s attributes"""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
