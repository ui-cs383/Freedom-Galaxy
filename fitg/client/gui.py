'''
Created on Nov 28, 2013

@author: Sean
'''

import pygame
#from hud.buttons import
import rpyc
from sys import exit as sysexit
from entities.system import System
from support.custommouse import MouseCursor
from support.loadimage import load_image
import hud.buttons as Menu_Buttons

pygame.init()

def main(client, setupinfo=None):
    gameid = 'test1'#setupinfo["request"]["parameters"]["id"]
    height = 720
    width = 1024
    screensize = (width, height)
    screen = pygame.display.set_mode(screensize)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(0)
    animate = True
    running = True

    background, background_rect = load_image("stars.jpg")
    screen.blit(background, background_rect)
    mouse_ptr = MouseCursor("pointer2.png")
    mouse_sel = MouseCursor("selected2.png")
    mouse = pygame.sprite.RenderUpdates((mouse_ptr))
    mouse.draw(screen)
    pygame.display.flip()
    #===========================================================================
    # Object Initialization:
    #===========================================================================
    characterlist = client.root.get_state(game_id = gameid, object_type="Character")["response"]["character"]
    planetlist = client.root.get_state(game_id = gameid, object_type="Planet")["response"]["planet"]
    environlist = client.root.get_state(game_id = gameid, object_type="Environ")["response"]["environ"]
    militarylist = client.root.get_state(game_id = gameid, object_type="Unit")["response"]["unit"]
    stacklist = client.root.get_state(game_id = gameid, object_type="Stack")["response"]["stack"]
    star_system = System(screen, background, animate, characterlist, planetlist, environlist, militarylist, stacklist)
    #print characterlist
    menu = Menu_Buttons.Menu(screen)
    
    
    selected_unit = None

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sysexit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sysexit()
            if not mouse_ptr.down:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if selected_unit:
                        hover_unit = left_mouse_select_check(client, mouse_sel, star_system)
                        if hover_unit != selected_unit:
                            #mergeresponse = client.root.merge_stack(unit.stack_id, selected_unit.stack_id)
                            #if mergeresponse["Success"]:
                            selected_unit.add_unit(hover_unit)
                            star_system.unit_list.remove(hover_unit)
                    print "SPACE BAR"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_ptr.pressed = mouse_sel.pressed = True
                        mouse_ptr.released = mouse_sel.released = False
                        selected_unit = left_mouse_select_check(client, mouse_ptr, star_system)
                        # while the mouse button is down, change its cursor
                        mouse.remove(mouse_ptr)
                        mouse.add(mouse_sel)
						#Update Buttons and menu status
                        menu.update_buttons(mouse_ptr.rect)
                    elif event.button == 3:
                        key_mod = pygame.key.get_mods()
                        if key_mod == 4097 or key_mod == 1:
                            hover_unit = star_system.unit_list.get_sprites_at(mouse_ptr.pos)
                            print "STACK REMOVING FROM", hover_unit
                            if hover_unit:
                                #splitresponse = client.root.split_stack(hover_unit[0].stack_id, hover_unit[0].unit_list[-1].id)
                                #if splitresponse["Success"]:
                                #   sprite.set_stack_id(splitresponse["response"]["stack id"])
                                sprite = hover_unit[0].remove_unit()
                                if sprite:
                                    #splitresponse = client.root.split_stack(hover_unit[0].stack_id, sprite.id)
                                    #if splitresponse["Success"]:
                                    #   sprite.set_stack_id(splitresponse["response"]["stack id"])
                                    star_system.unit_list.add(sprite)
                                    #else:
                                    #   hover_unit[0].add_unit(sprite)
                            print "SHIFT RIGHT CLICK"
                        else:
                            hover_unit = star_system.unit_list.get_sprites_at(mouse_ptr.pos)
                            if hover_unit:
                                hover_unit[0].cycle_unit()
                            print "RIGHT CLICK"

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_ptr.released = mouse_sel.released = True
                selected_unit = left_mouse_unselect_check(client, mouse, selected_unit, star_system)
                # while the mouse button is up, change its cursor
                mouse.remove(mouse_sel)
                mouse.add(mouse_ptr)

        screen.blit(background, background_rect)
        star_system.update()
        if selected_unit:
            selected_unit.update(True)
        mouse.update()
        star_system.draw()
		#Draw buttons and menus
        menu.draw_buttons(screen, height, width, selected_unit)
        mouse.draw(screen)
        pygame.display.flip()


def left_mouse_select_check(client, mouse, star_system):
    for unit in star_system.unit_list:
        if unit.rect.collidepoint(mouse.pos) and unit.visible == 1:
            star_system.unit_list.move_to_front(unit)
            return unit
    for planet in star_system.planet_list:
        if planet.rect.collidepoint(mouse.pos):
            star_system.planets_move(planet)
            return None


def left_mouse_unselect_check(client, mouse, selected_unit, star_system):
    if selected_unit:
        for planet in star_system.planet_list:
            new_location_id = planet.location * 10
            if planet.collide_rect.colliderect(selected_unit.rect):
                #moveresponse = client.root.move(stack_id=selected_unit.stack_id, location_id=new_location_id)
                selected_unit.loc_id = new_location_id #=moveresponse["response"]["location"]
                return None
            for environ in planet.environment.environ_list:
                new_location_id = new_location_id + environ.location
                new_environ_id = environ.id
                for point in environ.collision_points:
                    if selected_unit.rect.colliderect(pygame.Rect((point), (10, 10))):
                        moveresponse = client.root.move(stack_id=selected_unit.stack_id, location_id=environ.id)
                        print moveresponse
                        if moveresponse["request"]["success"] is True:
                            selected_unit.set_loc_id (new_location_id )
                            selected_unit.set_environ_id (new_environ_id)
                        return None
    '''    for unit in star_system.unit_list:
            if unit is not selected_unit:
                if unit.rect.colliderect(selected_unit.rect):
                    mergeresponse = client.root.merge_stack(unit.stack_id, selected_unit.stack_id)
                    if mergeresponse["Success"]:
                        unit.add_unit(selected_unit)
                        star_system.unit_list.remove(selected_unit)
    '''


if __name__ == '__main__':
    main()
