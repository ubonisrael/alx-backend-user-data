#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, and_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """
    valid_query_args = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        # self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def add_user(self, email: str, hashed_password: str) -> User:
        """adds a user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user
    
    def find_user_by(self, **kwargs) -> User:
        """
        returns the first row found in the users
        table as filtered by the method's input arguments
        """
        for k in kwargs:
            if k not in self.valid_query_args:
                raise InvalidRequestError()
        # filters = [getattr(User, key) == value for key, value in kwargs.items()]
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound()
        return user
    
    def update_user(self, user_id: str, **kwargs) -> None:
        """
        takes as argument a required user_id
        integer and arbitrary keyword arguments,
        and returns None"""
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if k not in self.valid_query_args:
                raise ValueError()
            setattr(user, k, v)
        self._session.commit()
