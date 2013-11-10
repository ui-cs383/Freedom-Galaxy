"""
Authored by Ben Cumber
Currently just the Detection Routine in the Combat Class.
"""
import random
from orm import *
from database_creation import loadDatabase
class Combat:

    def __init__(self):
        #The following detection table is exactly the same as the one from FitG with
        # E = -2, Dd = -1, D = 0, U = 1
        self.detection_table = ((-1, 0, 1, 1, 1, 1, 1, 1),
                                (-1, 0, 0, 0, 1, 1, 1, 1),
                                (-1, -1, 0, 0, 0, 1, 1, 1),
                                (-2, -1, -1, 0, 0, 0, 1, 1),
                                (-2, -1, -1, -1, 0, 0, 0, 1),
                                (-2, -2, -2, -1, -1, 0, 0, 0) )
        #self.detection_table = (('Dd', 'D', 'U', 'U', 'U', 'U', 'U', 'U'),
    #                            ('Dd', 'D', 'D', 'D', 'U', 'U', 'U', 'U'),
    #                            ('Dd', 'Dd', 'D', 'D', 'D', 'U', 'U', 'U'),
    #                            ('E', 'Dd', 'Dd', 'D', 'D', 'D', 'U', 'U'),
    #                            ('E', 'Dd', 'Dd', 'Dd', 'D', 'D', 'D', 'U'),
    #                            ('E', 'E', 'E', 'Dd', 'Dd', 'D', 'D', 'D') )
    def detection_routine(self, Stackid, pdb_level):
        session = Session()
        evasion_val = 0 #can be 0-7
        die_roll = 0    #can be 0-5


        stack1 = session.query(Stack).filter_by(id = Stackid).one()
        characters = stack1.characters
        navigation_rating = characters[0].navigation
        for char in characters:                         #Find the character in the stack
            if char.navigation > navigation_rating:     #with the highest navigation ratings
                navigation_rating = char.navigation

        spaceship = stack1.Spaceship()

        manuever_rating = spaceship.stat3

        print "navigation_rating", navigation_rating
        print "manuever_rating", manuever_rating
        #Determine the Evasion Value.
        #If the difference between the navigation_rating and the
        #manuever_rating is greater than 1, then add 1 to the lowest rating and
        #add those values together.

        if (abs(navigation_rating - manuever_rating) > 1):
            if navigation_rating < manuever_rating:
                evasion_val = 2 * navigation_rating + 1
            else:
                evasion_val = 2 * manuever_rating + 1
        else:
            evasion_val = navigation_rating + manuever_rating

        #Make sure we are reading from the correct column.
        if(evasion_val == 6):
            evasion_val = 5
        elif(evasion_val == 7 or evasion_val == 8):
            evasion_val = 6
        elif(evasion_val >= 9):
            evasion_val = 7

        die_roll = random.randint(0, 5)

        previously_detected = stack1.stack_detection()  #Is the stack already detected?
        if previously_detected == True:                 #modifier for when the
            evasion_val = evasion_val - 1               #stack is detected shift 1
                                                        #to the left

        if(pdb_level == 2):                             #modifier for when pdb is 2
            evasion_val = evasion_val - 2               #shift two to the left

        result = self.detection_table[die_roll][evasion_val]

        if(pdb_level == 0):                             #modifier for when pdb is 0
            if(result < 0):                             #if the result was Dd or E its just D.
                result = 0

        print "Die roll is ", die_roll
        print "Evasion value is", evasion_val
        print "The result is", result
        print

        
loadDatabase()
test = Combat()
test.detection_routine(1, 0)
