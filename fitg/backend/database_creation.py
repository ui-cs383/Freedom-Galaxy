#Created by: Greg Donaldson
#Purpose: Upload .dat files into a database using SQLAlchemy. For use by the Backend Team.

from sqlalchemy import *
from dataSnag import *

planetList = planets("planet.dat")
dictList = []
db = create_engine('sqlite://')

metadata = MetaData(db)

Planets = Table('Planets', metadata,
    Column('id', Integer),
    Column('name', String(40), primary_key=True),
    Column('race', String(40)),
    Column('sloyalty', Integer),
    Column('aloyalty', Integer),
    Column('numenvirons', Integer)
)

metadata.create_all()

for list in planetList:
    temp = {'id' : list[0], 'name' : list[1], 'race' : list[2], 
            'sloyalty' : list[3], 'aloyalty' : list[4], 'numenvirons' : list[5]}
    dictList.append(temp)

conn = db.connect()
conn.execute(Planets.insert(), dictList)

for row in conn.execute(select([Planets])):
    print row
