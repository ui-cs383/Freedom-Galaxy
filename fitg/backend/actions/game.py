import yaml
import orm
from sqlalchemy.orm import exc
from sqlalchemy import or_

def start(session, id, player, scenario="egrix"):
    try:
        session.query(orm.Game).filter_by(id = id).one()
    except exc.NoResultFound:
        pass
    else:
        return False, "FATAL: A game with that id already exists."

    f = 'scenarios/' + scenario + '.yaml'

    with open (f, "r") as scenario_file:
        game_data = scenario_file.read()

    game_data = yaml.load(game_data)

    game = orm.Game(id = id, player1 = player, player2 = None, scenario = scenario)
    rebel = orm.Stack()
    imperial = orm.Stack()

    for objects, values in game_data.items():
        if objects == 'characters':
            for attributes in values:
                character = orm.Character(**attributes)

                possessions = game_data['possessions']

                for possession_attribute, possession in enumerate(possessions):
                    if character.name == possession['owner_name']:
                        item = orm.Possession(**possession)
                        character.possessions.append(item)

                if attributes['side'] == 'Rebel':
                    rebel.characters.append(character)
                else:
                    imperial.characters.append(character)

        elif objects == 'units':
            for attributes in values:
                count = attributes['count']
                attributes.pop('count', None)

                for x in range(0, count):
                    unit = orm.Unit(**attributes)
                    #stack.units.append(unit)

                if attributes['side'] == 'Rebel':
                    rebel.units.append(unit)
                else:
                    imperial.units.append(unit)

        elif objects == 'planets':
            for attributes in values:
                planet = orm.Planet(**attributes)

                environs = game_data['environs']

                for environ_attribute, environ in enumerate(environs):
                    if 'planet_location' in environ:
                        location = environ['planet_location']

                        if planet.location == location:
                            environ.pop('planet_location', None)
                            area = orm.Environ(**environ)
                            planet.environs.append(area)

                game.planets.append(planet)


    game.stacks.append(rebel)
    game.stacks.append(imperial)

    try:
        session.add(game)
    except:
        success = False
    else:
        success = True

    return success, { 'game': game.__dict__ }
    
def join(session, id, player):
    game = session.query(orm.Game).filter_by(id = id).filter(or_(player1 = None, player2 = None)).one()
    session.add(game)

    if game.player1 is None:
        game.player1 = player
    elif game.player2 is None:
        game.player2 = player
    else:
        return False, { 'game': game.__dict__ }

    session.add(game)
    session.commit()

    return True, { 'game': game.__dict__ }


def list(session):
    games = session.query(orm.Game).filter((orm.Game.player1 == None) | (orm.Game.player2 == None)).all()
    glist = [ x.__dict__ for x in games ]

    return True, { 'games': glist }


def get_object(session, table, id=None):

    orm_name = getattr(orm, table)

    if id is None:
        print("Getting all of the stuff")
        items = session.query(orm_name).all()
        items = [ x.__dict__ for x in items ]
    else:
        items = session.query(orm_name).filter_by(id=id).one()

    return True, { table: items }
