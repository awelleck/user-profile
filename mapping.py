import os
import sqlalchemy
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

version = sqlalchemy.__version__
print(version)

engine = create_engine('postgresql+psycopg2://' + os.environ['USER'] +
                       ':' + os.environ['PASS'] + '@localhost/practice',
                       echo=True)
print(engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'practice'

    username = Column(String(80), primary_key=True, unique=True)
    password = Column(String(100))
    email = Column(String(25), unique=True)
    first_name = Column(String(25))
    last_name = Column(String(25))

    def __repr__(self):
        return ("<User(username='%s', password='%s', email='%s', " +
                "first_name='%s', last_name='%s')>") % (self.username,
                                                        self.password,
                                                        self.email,
                                                        self.first_name,
                                                        self.last_name)
