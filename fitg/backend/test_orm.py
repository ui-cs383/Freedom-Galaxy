import orm

session = orm.Session()

game = orm.Game('test_game', 'Jeff', 'Ben', 'Demo')

## create a planet
planet = orm.Planet(111, "Mimulus", "Kayns", -2, 1)

## create an enviorn
environ = orm.Environ(1, "W", 4, "Kayns", 1, 4, 0, "Prox", 0, 0)

## create a stack
stack = orm.Stack()

## create a character
character = orm.Character("Zina Adora", "izina.gif", "Princess of Adare", "Rhone", "Rebel", 1, 1, 1, 2, 3, 2, "Adare", "RI")

## create a unit
unit = orm.Unit("Ninja", "Rebel", 5, 5, 1)

## add a character to the stack
stack.characters.append(character)

## add a unit to the stack
stack.units.append(unit)

## add the stack to the enviorn
environ.stacks.append(stack)

## add the enivorn to the planet
planet.environs.append(environ)

## add the planet to the game
game.planets.append(planet)

## complete the session
session.add(game)

## commit the session
session.commit()