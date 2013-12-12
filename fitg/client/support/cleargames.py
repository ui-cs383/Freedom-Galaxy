import rpyc
import service

client = rpyc.connect("elegantgazelle.com", 55889, service.ClientService, config = {"allow_public_attrs" : True})

c = client.root

for game in c.list_games()["response"]["games"]:
    print game["id"]
    if str(game["id"]) != "test1":
        c.delete_game(str(game["id"]))