from database_creation import *
from random import randint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Session = sessionmaker(bind=db)

class Character(Base):
	__tablename__ = 'Characters'

	name = Column(String(40), primary_key=True)
	gif = Column(String(40))
	title = Column(String(40))
	location = Column(String(40))
	side = Column(String(40))
	combat = Column(Integer)
	endurance = Column(Integer)
	intelligence = Column(Integer)
	leadership = Column(Integer)
	diplomacy = Column(Integer)
	navigation = Column(Integer)
	homeworld = Column(String(40))
	bonuses = Column(String(40))
	wounds = Column(Integer)

	def __repr__(self):
		return "%s, %s." % (self.name, self.wounds)

class Stack(Base):
	__tablename__ = 'Stacks'

	id = Column(Integer, primary_key=True)
	size = Column(Integer)
	combatrating = Column(Integer)
	location = Column(String(40))
	active = Column(PickleType)
	inactive = Column(PickleType)

	# function to add unit to stack, check if not already in another stack, if so, remove?


class Environ(Base):
	__tablename__ = 'Environs'

	id = Column(Integer, primary_key=True)
	type = Column(String(40))
	size = Column(Integer)
	race = Column(Integer)
	starfaring = Column(Boolean)
	resources = Column(Integer)
	mystery = Column(Integer)
	monster = Column(String(40))
	mystery2 = Column(Integer)

class Planet(Base):
	__tablename__ = 'Planets'

	id = Column(Integer, primary_key=True)
	name = Column(String(40))
	race = Column(String(40))
	sloyalty = Column(Integer)
	aloyalty = Column(Integer)
	numenvirons = Column(Integer)

