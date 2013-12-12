import pygame, string
import gui
import rpyc
import support.service as service
from startscreen.textbox import my_textbox
from startscreen.menubutton import my_button
from startscreen.listingbox import gamelistingbox

pygame.init()
        
def setscenario(scenarioflag):
    if scenarioflag is False:
        return 'egrix'
    else:
        return 'powder keg'
        
def setplayer( sideflag):
    if sideflag:
        return 'rebel'
    else:
        return 'imperial'
   
def main ():
    client = rpyc.connect("elegantgazelle.com", 55889, service.ClientService, config = {"allow_public_attrs" : True})

    background = pygame.image.load("data/freedom_galaxy.jpg")
    #background = pygame.transform.scale(background, (389, 489))

    start = my_button('Start Game')
    join = my_button('Join Game')
    allegiance = my_button('Rebel', 'Empire')
    single_player = my_button('Play AI', '2 Player')
    scenario = my_button('Flight', 'Powder')
    exit = my_button('Exit Game')
    gametextbox = my_textbox('Game Name')
    playertextbox = my_textbox('Your Name')
    screen = pygame.display.set_mode((536,720))
    listingbox = gamelistingbox()
    
    playerside = ''
    playerscenario = ''

    pygame.mixer.music.load('data/starwars-maintheme.mp3') 
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()

    redrawscreen = False
    screen.blit(background, background.get_rect())
    pygame.display.flip()
    
    gamelistasync = rpyc.async(client.root.list_games)
    
    selectedtextbox = gametextbox
    gametextbox.switchchar()
    
    run = True
    while run:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if selectedtextbox is not None:
                    if event.key == 9:
                        if selectedtextbox == gametextbox:
                            selectedtextbox.switchchar()
                            selectedtextbox = playertextbox
                            selectedtextbox.switchchar()
                        elif selectedtextbox == playertextbox:
                            selectedtextbox.switchchar()
                            selectedtextbox = gametextbox
                            selectedtextbox.switchchar()
                    elif event.key == pygame.K_RETURN:
                        run = False
                        #pygame.mixer.music.stop()
                        playerscenario = setscenario(scenario.is_alt)
                        playerside = setplayer( allegiance.is_alt)
                        gamesetup = client.root.start_game(id=gametextbox.input, player=playertextbox.input) #, scenario=playerscenario, ai=single_player.is_alt)
                        #print("Getting state of planets")
                        #planet = client.root.get_state(object_id=1, object_type="Planet")
                        #print planet
                        #print gamesetup
                        gui.main(client, gamesetup)
                    else:
                        selectedtextbox.addkey(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start.obj.collidepoint(mouse):
                    run = False
                    #pygame.mixer.music.stop()
                    playerscenario = setscenario(scenario.is_alt)
                    playerside = setplayer( allegiance.is_alt)
                    #gamesetup = client.root.start_game(id='test1', player=playertextbox.input) #id=gametextbox.input, scenario=playerscenario, ai=single_player.is_alt)
                    #print("Getting state of planets")
                    #planet = client.root.get_state(object_id=1, object_type="Planet")
                    #print planet
                    #print gamesetup
                    gui.main(client)#, gamesetup)
                    #fire request to server
                    print('my_button start game clicked')
                elif join.obj.collidepoint(mouse):
                    listingbox.visible = True
                    gamelisting = gamelistasync()
                    print('my_button join game clicked')
                elif allegiance.obj.collidepoint(mouse):
                    allegiance.switch_text()
                    if single_player.is_alt is False:
                        allegiance.is_alt = False
                    print('my_button rebel clicked')
                elif single_player.obj.collidepoint(mouse):
                    single_player.switch_text()
                    if single_player.is_alt is False:
                        allegiance.is_alt = False
                    print('my button player vs AI clicked')
                elif scenario.obj.collidepoint(mouse):
                    scenario.switch_text()
                    print('my button scenario clicked')
                elif exit.obj.collidepoint(mouse):
                    run = False
                    print('my button exit clicked')
                elif gametextbox.obj.collidepoint(mouse):
                    if selectedtextbox is not None:
                        selectedtextbox.switchchar()
                    selectedtextbox = gametextbox
                    selectedtextbox.switchchar()
                elif playertextbox.obj.collidepoint(mouse):
                    if selectedtextbox is not None:
                        selectedtextbox.switchchar()
                    selectedtextbox = playertextbox
                    selectedtextbox.switchchar()
                elif listingbox.visible is True:
                    if listingbox.obj.collidepoint(mouse):
                        if listingbox.cancelbutton.obj.collidepoint(mouse):
                            redrawscreen = True
                            listingbox.visible = False
                        elif listingbox.joinbutton.obj.collidepoint(mouse):
                            run = False
                            #pygame.mixer.music.stop()
                            playerscenario = setscenario(scenario.is_alt)
                            playerside = setplayer( allegiance.is_alt)
                            gamesetup = client.root.join_game(id=gametextbox.input, player=playertextbox.input) #scenario=playerscenario
                            print gamesetup
                            gui.main(gamesetup, client)
                        elif listingbox.refreshbutton.obj.collidepoint(mouse):
                            gamelisting = gamelistasync()
                        elif listingbox.gamebox.collidepoint(mouse):
                            listingbox.checkclick(mouse)
                            
                        
        if redrawscreen is True:
            screen.blit(background, background.get_rect())
            pygame.display.flip()
            redrawscreen = False
        
        if listingbox.visible is True:
            listingbox.draw(screen, mouse)
            if gamelisting is not None:
                if gamelisting.ready:
                    listingbox.setgamelist(gamelisting.value)
                    gamelisting = None
                else:
                    listingbox.drawloading(screen)
            single_player.is_alt = True
            if listingbox.selectedgame is not None:
                gametextbox.input = str(listingbox.selectedgame["id"])
                gametextbox.text = list(gametextbox.input)
                scenario.is_alt = listingbox.scenarioflag
                
        
        start.draw(screen, mouse, (13,650,170,40), (18,658))
        join.draw(screen, mouse, (196,650,155,40), (201,658))
        exit.draw(screen, mouse, (364,650,155,40), (369,658))
        
        single_player.draw(screen, mouse, (13,607,170,40), (18,611))
        allegiance.draw(screen, mouse, (196,607,155,40), (201,611))
        scenario.draw(screen, mouse, (364,607,155,40), (369,611))
        
        gametextbox.draw(screen, (13,560,250,42))
        playertextbox.draw(screen, (270,560,250,42))
        
        

        pygame.display.update()
        clock.tick(60)
   
if __name__ == '__main__':
    main()
