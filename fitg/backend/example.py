#Created by: Greg Donaldson
#Purpose: Educating the Backend Team on SQLAlchemy.

from sqlalchemy import *                    #This will import pretty much everything you might need. Of course, you need to install SQLAlchemy.
from sqlalchemy.orm import sessionmaker     #This allows you access to a created database file.
from database_creation import loadDatabase  #And this allows you to create a database file.
import os                                   #For file cleanup later on.

#Make sure you have all the .dat files from the 383 site.

loadDatabase()  #This function takes all the .dat files and creates a database. 
                #You can actually see the database (Freedom.db) at C:\Python27.
                
#Now we connect to the database using the following command:

db = create_engine('sqlite:///C:\\Python27\\Freedom.db') #Keep in mind that anything after the 'sqlite:///' is the address of the database. Also note the '\\' in the path.

#Next we create a Session. This is a class that allows us to manipulate the database.

Session = sessionmaker(bind=db)

#And now we instantiate the Session.

session = Session()

#Now, to retrieve data from the database depends on what you are calling. First, we need to load the metadata from the database.
meta = MetaData()
meta.reflect(bind=db) #Reflect loads the metadata from the existing database into the meta object. From here, we create our tables.

#Now we set up our table objects to call queries and update the database.
#I create an object for every table currently in the database. You probably won't need to.

Action = meta.tables['Action']
charCombat = meta.tables['charCombat']
Characters = meta.tables['Characters']
Detection = meta.tables['Detection']
Environ = meta.tables['Environ']
milCombat = meta.tables['milCombat']
Planets = meta.tables['Planets']
Possessions = meta.tables['Possessions']
Races = meta.tables['Races']

#Now that we have every object available, we need to select a table to work with. 
#For instance, we want to know more information about the character Zina Adora.

#First, connect to the database.
conn = db.connect()

#Then select the Characters table.
s = select([Characters])

#Now, we tell the database to send us the selection.

result = conn.execute(s)

#The data is actually stored in a list of tuples, where each tuple is its own row. So, a for loop displays everything.
#However, we just want information on Zina Adora. Since we know the first value is the character names...

for row in result:
    if row[0] == 'Zina Adora':
        print row
        
#Its important to note that each time you use result, its closed after the first use.
    
#Now that we have seen how to get data from the database, how do we update the database?
#For instance, Zina Adora has been detected as the result of a mission.

#All we have to do is tell our conn object to execute an update.
conn.execute(Characters.update().where(Characters.c.name=='Zina Adora').values(detected=True))

#Lots of stuff going on in the above statement. Taking it one step at a time...

#conn is our database object.
#.execute( is telling our database object to do something, dependent on what is inside the paranthesis.
#Characters.update() is telling our Characters table to update. update() works on any table.
#.where(Characters.c.name=='Zina Adora') This compound statement tells the database which row to look at.
#In this case, we want to look at the Characters table, and at the name value (indicated by Characters.c.name),
#and that we are looking for Zina Adora.
#.values(detected=True) is telling the database to change the row that has the name Zina Adora,
#and to change the detected value to be True.

#Now, to check this statement, all we need to do is pull out the information from the Characters table again.
#As a quick reminder on how to do that:
s = select([Characters])
result = conn.execute(s)
for row in result:
    if row[0] == 'Zina Adora':
        print row
        
#Running the above code, you will notice that Zina Adora's second to last value has changed to True from where it was before.
#This completes the SQLAlchemy tutorial. If you have any questions, let me know.