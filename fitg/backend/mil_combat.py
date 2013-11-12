#Authored By Ben Cumber
#military_units.dat info format
#side, type, mobility, environ combat, space combat

def mil_combat(atk_id, def_id):
    session = Session()

    atk_stack = session.query(Stack).filterby(id = atk_id).one()
    def_stack = session.query(Stack).filterby(id = def_id).one()

    atk_mil_units = atk_stack.militaryunits
    def_mil_units = def_stack.militaryunits


def mil_combat_table(die_roll, combat_odds, is_attacker):
    defender_wounds = (
            (8, 7, 6, 5, 5, 4, 3, 3, 2, 2, 1),
            (7, 6, 5, 5, 4, 3, 2, 2, 1, 1, 1),
            (7, 5, 5, 4, 3, 2, 2, 2, 1, 1, 1),
            (6, 5, 4, 3, 3, 2, 1, 1, 1, 0, 0),
            (5, 4, 4, 3, 2, 1, 1, 0, 0, 0, 0),
            (4, 4, 3, 3, 1, 0, 0, 0, 0, 0, 0))
    
    attacker_wounds = (
            (0, 0, 0, 0, 0, 0, 1, 2, 2, 3, 4),
            (0, 0, 0, 0, 0, 1, 2, 3, 3, 4, 5),
            (0, 0, 0, 0, 1, 1, 2, 3, 4, 4, 5),
            (0, 0, 1, 1, 1, 2, 3, 3, 4, 5, 6),
            (1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 7),
            (1, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8))

