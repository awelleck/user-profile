from sqlalchemy import Column, Integer, String
from sqlalchemy.extdeclarative import declarative_base

Base = declarative_base()

class Profiles(Base):
	__tablename__ = 'practice'

	username = Column(String(80), primary_key=True)
	password = Column(String(100))
	email = Column(String(25), primary_key=True)
	first_name = Column(String(25))
	last_name = Column(String(25))

	def __repr__(self):
		return "<User(username='%s', password='%s', email='%s', first_name='%s', last_name='%s')>" %
			(self.username, self.password, self.email, self.first_name, self.last_name)
