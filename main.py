import pygame, time, math, sys

pygame.init()
window = pygame.display.set_mode((1240, 620))

from classes.pygametextboxinput import *
from classes.code_runner import *
from classes.def_codes import *
from classes.classes_ import *
from classes.utils import *
from classes.loaders import *
from classes.vars import *
from classes.ccrpg import *

#!!!
#!!!Most of the global variables are declared in the vars.py file!
#!!!

pygame.display.set_caption("Code_Craft")
pygame.display.set_icon(pygame.image.load(PATH / "drawable" / "villager_hq.png"))
pygame.key.set_repeat(200, 25)
clock = pygame.time.Clock()

pygame.mixer.music.load(playlist[current_song_index])
pygame.mixer.music.play()

music_on = data["music_on"]
fx_on = data["fx_on"]
lang = data["lang"]
if not music_on:
    pygame.mixer.music.pause()

game_utils = GameUtils(window, playlist, current_song_index, minecraft_font_small, minecraft_font_book, minecraft_font_smaller, clock, data, stevexy, levels, player_levels, time, PATH, languages)
loaders = Loaders(window, minecraft_font_small, clock, time, PATH)
rpg = RandomPathGenerator(7)
code_input = Textbox(595, 0, 645, 620, PATH / "fonts" / "Minecraft.ttf")

def menu():
    big_title = get_scaled_img(PATH / "drawable" / "Code_Craft.png", (491, 127))
    emerald = get_scaled_img(PATH / "drawable" / "emerald.png", (32, 32))
    
    game_utils.background()
    window.blit(big_title, (374, 60))
    window.blit(emerald, (1210, 0))

    while True:
        game_utils.play_next_track(music_on)

        mouse = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 420 <= mouse[0] <= 820 and 250 <= mouse[1] <= 290:
                    #Opens current level if Play button is clicked
                    game_utils.play_click_sound(fx_on)
                    if levels["last_finished_level"] < 36:
                        game(levels["last_finished_level"]+1)
                elif 420 <= mouse[0] <= 820 and 300 <= mouse[1] <= 340:
                    #Opens level menu if Levels button is clicked
                    game_utils.play_click_sound(fx_on)
                    level_menu()
                elif 420 <= mouse[0] <= 820 and 350 <= mouse[1] <= 390:
                    #Opens tutorial window if Tutorial button is clicked
                    game_utils.play_click_sound(fx_on)
                    tutorial()
                elif 420 <= mouse[0] <= 615 and 420 <= mouse[1] <= 460:
                    #Opens options window if Options... button is clicked
                    game_utils.play_click_sound(fx_on)
                    options_win()
                elif 625 <= mouse[0] <= 820 and 420 <= mouse[1] <= 460:
                    #Exits the game if Quit Game button is clicked
                    pygame.quit()
                    sys.exit()

        #Emerald count
        window.blit(minecraft_font_book.render(str(data["emeralds"]), True, (255, 255, 255)), (1213-minecraft_font_book.size(str(data["emeralds"]))[0], 2.6))

        game_utils.menu_button(420, 250, menu_text["play"][lang], 400, 40, mouse)

        game_utils.menu_button(420, 300, menu_text["levels"][lang], 400, 40, mouse)

        game_utils.menu_button(420, 350, menu_text["tutorials"][lang], 400, 40, mouse)

        game_utils.menu_button(420, 420, menu_text["options"][lang], 195, 40, mouse)

        game_utils.menu_button(625, 420, menu_text["quit"][lang], 195, 40, mouse)

        pygame.display.update()
        clock.tick(60)    

def level_menu():
    while True:
        game_utils.play_next_track(music_on)
        mouse = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 550 <= mouse[0] <= 785 and 550 <= mouse[1] <= 590:
                    # Generate and save a new level using GridPathfinder
                    rpg.generate_points()

                    curr_level = player_levels["last_level"] + 1
                    new_level = new_level_curr.copy()

                    new_level["steve_xy"] = rpg.get_start()
                    new_level["blocks"] = rpg.random_path(rpg.start, rpg.end)
                    new_level["path_block"] = "grass_top.png"
                    player_levels[f"level{curr_level}"] = [new_level]

                    curr_level_p = [0] * 5
                    curr = player_levels["level_p"][-1] if player_levels["level_p"] else [-70, 30, None, None, None]
                    curr_level_p[0] = curr[0]+100 if curr[0] < 1130 else 30
                    curr_level_p[1] = curr[1] if curr[0] < 1130 else curr[1]+110
                    curr_level_p[2] = curr_level
                    curr_level_p[3] = 80
                    curr_level_p[4] = True
                    player_levels["level_p"].append(curr_level_p)

                    player_levels["last_level"] += 1

                    if player_levels["last_level"] > 0:
                        for p in player_levels["level_p"]:
                            player_game_levels.append(Level(p[0], p[1], p[2], p[3], p[4], levels))

                    game_utils.write_to_json(PATH / "levels" / "player_levels.json", player_levels)
                    game(curr_level, player_l=True, random_l=True)
                if 810 <= mouse[0] <= 1015 and 550 <= mouse[1] <= 590:
                    #Opens level builder if Level Builder button is clicked
                    game_utils.play_click_sound(fx_on)
                    level_builder()
                if 1035 <= mouse[0] <= 1210 and 550 <= mouse[1] <= 590:
                    #Opens players level menu if Your levels button is clicked
                    game_utils.play_click_sound(fx_on)
                    your_levels_menu()
                for lvl in game_levels:
                    #Opens level on which player clicked
                    if lvl.hover(mouse[0], mouse[1]) and lvl.unlocked:
                        game_utils.play_click_sound(fx_on)
                        game(lvl.level)
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    #Retuns to main menu if Back button is clicked
                    game_utils.play_click_sound(fx_on)
                    menu()
        
        game_utils.background()
        game_utils.bg_overlay()

        #back_button
        game_utils.button(back_button, 10, 565)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            game_utils.trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        #level_button
        for lvl in game_levels:
            pygame.draw.rect(window, (130, 130, 130), (lvl.x, lvl.y, lvl.size, lvl.size))
            pygame.draw.rect(window, (0, 0, 0), (lvl.x, lvl.y, lvl.size, lvl.size), 1)

            text_width = minecraft_font_small.size(str(lvl.level))[0]

            window.blit(render_small_text(str(lvl.level)), (lvl.x + (lvl.size-text_width)//2 + 1, lvl.y+20))

            if not lvl.unlocked:
                game_utils.trans_surface(lvl.size, lvl.size, (0, 0, 0, 50), lvl.x, lvl.y)

            if lvl.hover(mouse[0], mouse[1]) and lvl.unlocked:
                pygame.draw.rect(window, (255, 255, 255), (lvl.x, lvl.y, lvl.size, lvl.size), 3)
                game_utils.button(play_level_button, lvl.x, lvl.y)

        window.blit(level_menu_text["debug_challenge"][lang][0], (level_menu_text["debug_challenge"][lang][1], 240))

        game_utils.menu_button(550, 550, level_menu_text["random_level"][lang], 235, 40, mouse)

        game_utils.menu_button(805, 550, level_menu_text["lvl_builder"][lang], 210, 40, mouse)

        game_utils.menu_button(1035, 550, level_menu_text["your_levels"][lang], 175, 40, mouse)
        
        pygame.display.update()
        clock.tick(60)

def your_levels_menu():
    while True:
        game_utils.play_next_track(music_on)
        mouse = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for lvl in player_game_levels:
                    #Opens level on which player clicked
                    if lvl.hover(mouse[0], mouse[1]) and lvl.level != -1:
                        game_utils.play_click_sound(fx_on)
                        game(lvl.level, True)
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    #Retuns to Level menu if Back button is clicked
                    game_utils.play_click_sound(fx_on)
                    level_menu()
        
        game_utils.background()
        game_utils.bg_overlay()

        #back_button
        game_utils.button(back_button, 10, 565)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            game_utils.trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        #level_button
        for lvl in player_game_levels:
            pygame.draw.rect(window, (130, 130, 130), (lvl.x, lvl.y, lvl.size, lvl.size))
            pygame.draw.rect(window, (0, 0, 0), (lvl.x, lvl.y, lvl.size, lvl.size), 1)

            text_width = minecraft_font_small.size(str(lvl.level))[0]

            window.blit(render_small_text(str(lvl.level)), (lvl.x + (lvl.size-text_width)//2 + 1, lvl.y+20))

            if lvl.hover(mouse[0], mouse[1]):
                pygame.draw.rect(window, (255, 255, 255), (lvl.x, lvl.y, lvl.size, lvl.size), 3)
                game_utils.button(play_level_button, lvl.x, lvl.y)
        
        pygame.display.update()
        clock.tick(60)

def level_builder():
    messages = []
    saved = False
    curr_level = player_levels["last_level"]+1
    plus_x_y = [0, 0]
    blocks = [["plus.png" for _ in range(7)] for _ in range(7)]
    block_file_names = [
        ["dirt.png", "farmland.png", "farmland_moist.png", "grass_top.png", "sand.png", "sandstone_top.png"],
        ["oak_log_top.png", "oak_trapdoor.png", "cobblestone.png", "coal_ore.png", "gold_ore.png", "emerald_ore.png"],
        ["diamond_ore.png", "bedrock.png", "netherrack.png", "nether_quartz.png", "nether_gold_ore.png", "nether_wart_block.png"],
        ["end_stone.png", "end_stone_bricks.png", "purpur_block.png", "chorus_plant.png", "soul_sand.png", "soul_soil.png"]
    ]
    start = []
    path_block = "plus.png"
    path_select = False
    end = None
    time = 0
    while True:
        game_utils.play_next_track(music_on)
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_LMETA):
                    #Clears the messages if Ctrl+K/Cmd+K is clicked
                    messages.clear()
                key = pygame.key.name(event.key)
                if key == "up":
                    plus_x_y[1] = (plus_x_y[1] - 1) % 7  
                elif key == "down":
                    plus_x_y[1] = (plus_x_y[1] + 1) % 7  
                elif key == "left":
                    plus_x_y[0] = (plus_x_y[0] - 1) % 7  
                elif key == "right":
                    plus_x_y[0] = (plus_x_y[0] + 1) % 7  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse[0] <= 595 and mouse[1] <= 595:
                    #Changes the block that is going to be edited if user clicked on it
                    plus_x_y = [mouse[0]//85, mouse[1]//85]
                elif 675 <= mouse[0] <= 1184 and 30 <= mouse[1] <= 380:
                    saved = False
                    #Sets the block at plus_x_y to block from right side that is clicked
                    a = False
                    for el in blocks:
                        a = block_file_names[(mouse[1]-40)//85][(mouse[0]-675)//85] in el
                    if block_file_names[(mouse[1]-40)//85][(mouse[0]-675)//85] != "oak_trapdoor.png":
                        if path_select:
                            #Sets the path block if editor is in mode for setting the path
                            path_block = block_file_names[(mouse[1]-40)//85][(mouse[0]-675)//85]
                            path_select = False
                        else:
                            if end and plus_x_y == end[::-1]:
                                end = None
                            blocks[plus_x_y[1]][plus_x_y[0]] = block_file_names[(mouse[1]-40)//85][(mouse[0]-675)//85]
                    elif not a:
                        #if block is trapdoor
                        if end:
                            blocks[end[0]][end[1]] = "plus.png"
                            blocks[plus_x_y[1]][plus_x_y[0]] = block_file_names[(mouse[1]-40)//85][(mouse[0]-675)//85]
                        else:
                            blocks[plus_x_y[1]][plus_x_y[0]] = block_file_names[(mouse[1]-40)//85][(mouse[0]-675)//85]
                        end = [plus_x_y[1], plus_x_y[0]]
                elif 605 <= mouse[0] <= 625 and 20 <= mouse[1] <= 40:
                    saved = False
                    #Sets the start at plus_x_y if Set start position button is clicked
                    start = plus_x_y.copy()
                elif 605 <= mouse[0] <= 633 and 60 <= mouse[1] <= 88:
                    #Sets the editor in mode for setting the path if Set path block button is clicked
                    path_select = True
                elif 609 <= mouse[0] <= 633 and 104 <= mouse[1] <= 129:
                    #Saves the level if Save level button is clicked
                    if start and end:
                        curr = new_level_curr.copy()
                        curr["steve_xy"] = [start[0], 6-start[1]]
                        curr["blocks"] = blocks
                        curr["path_block"] = path_block
                        player_levels[f"level{curr_level}"] = [curr]
                        game_utils.write_to_json(PATH / "levels" / "player_levels.json", player_levels)
                        saved = True
                    else:
                        messages.append(texts["Set start and end positions first!"][lang])
                elif 10 <= mouse[0] <= 30 and 597 <= mouse[1] <= 617:
                    #Exits and updates the player_levels.json to fully save level if Exit button is clicked
                    if saved:
                        curr_level_p = [0] * 5
                        curr = player_levels["level_p"][-1] if player_levels["level_p"] else [-70, 30, None, None, None]
                        curr_level_p[0] = curr[0]+100 if curr[0] < 1130 else 30
                        curr_level_p[1] = curr[1] if curr[0] < 1130 else curr[1]+110
                        curr_level_p[2] = curr_level
                        curr_level_p[3] = 80
                        curr_level_p[4] = False
                        player_levels["level_p"].append(curr_level_p)
                        player_levels["last_level"] += 1
                        if player_levels["last_level"] > 0:
                            for p in player_levels["level_p"]:
                                player_game_levels.append(Level(p[0], p[1], p[2], p[3], p[4], levels))
                        game_utils.write_to_json(PATH / "levels" / "player_levels.json", player_levels)
                    game_utils.play_click_sound(fx_on)
                    level_menu()
        game_utils.background()
        game_utils.bg_overlay()

        pygame.draw.rect(window, (205, 205, 205), (0, 0, 1240, 595))

        pygame.draw.rect(window, (0, 118, 197), (0, 595, 1240, 25))
        pygame.draw.rect(window, (0, 118, 197), (595, 0, 50, 620))

        i = 0
        j = 0
        while i < 595:
            while j < 595:
                block = pygame.image.load(PATH / "blocks" / blocks[j//85][i//85])
                block = pygame.transform.scale(block, (85, 85))
         
                window.blit(block, (i, j))
                pygame.draw.rect(window, (0, 0, 0), (i, j, 85, 85), 1)
                j += 85
            j = 0
            i += 85
        

        i = 675
        j = 30

        while i < 1184:
            while j < 30 + 4 * 85:
                if (i - 645) // 85 < len(block_file_names[j // 85]):
                    block = pygame.image.load(PATH / "blocks" / block_file_names[j // 85][(i - 645) // 85])
                    block = pygame.transform.scale(block, (85, 85))

                    window.blit(block, (i, j))
                    pygame.draw.rect(window, (0, 0, 0), (i, j, 85, 85), 1)

                j += 90
            
            j = 30
            i += 90

        pygame.draw.rect(window, (0, 255, 0), (plus_x_y[0]*85, plus_x_y[1]*85, 85, 85), 2)

        if start:
            pygame.draw.rect(window, (255, 0, 0), (start[0]*85, start[1]*85, 85, 85), 2)
        
        if 10 <= mouse[0] <= 30 and 597 <= mouse[1] <= 617:
            game_utils.description(texts["Exit"][lang])
            game_utils.trans_surface(20, 20, (170, 170, 170, 120), 12, 597)
        
        #back_button
        game_utils.button(close_button, 10, 596)

        if 605 <= mouse[0] <= 625 and 20 <= mouse[1] <= 40:
            game_utils.description(texts["Set start position"][lang])
            game_utils.trans_surface(20, 20, (170, 170, 170, 120), 609, 20)

        #start button
        game_utils.button(run_button, 605, 15)

        #path select
        path_button = get_scaled_img(PATH / "blocks" / path_block, (28, 28))
        window.blit(path_button, (605, 60))
        if 605 <= mouse[0] <= 633 and 60 <= mouse[1] <= 88:
            game_utils.description(texts["Set path block"][lang])
            game_utils.trans_surface(28, 28, (170, 170, 170, 120), 605, 60)

        if 609 <= mouse[0] <= 633 and 104 <= mouse[1] <= 129:
            game_utils.description(texts["Save level"][lang])
            game_utils.trans_surface(22, 21, (170, 170, 170, 120), 609, 104)

        #save button
        game_utils.button(accept_button, 605, 100)

        #not saved
        if not saved:
            time += 0.03
            alpha = 240 + 127 * math.sin(time)

            # Create a new surface with the image and apply alpha
            faded_image = not_saved.copy()
            faded_image.set_alpha(alpha)

            # Draw the faded image
            window.blit(faded_image, (613, 145))

            if 613 <= mouse[0] <= 628 and 145 <= mouse[1] <= 160:
                game_utils.description(texts["Unsaved"][lang])
                game_utils.trans_surface(17, 17, (170, 170, 170, 120), 612, 144)

        game_utils.minecraft_cmd(messages, 0, 595, 590)

        pygame.display.update()
        clock.tick(60)

def tutorial():
    text = texts["Coming soon!"][lang]
    text_index = 0
    while True:
        game_utils.play_next_track(music_on)
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    #Retuns to main menu if Back button is clicked
                    game_utils.play_click_sound(fx_on)
                    menu()
                    
        game_utils.background()
        game_utils.bg_overlay()

        if text_index < len(text):
            text_index += 1
            time.sleep(0.05)

        window.blit(render_small_text(text[:text_index]), (540, 300))

        #back_button
        game_utils.button(back_button, 10, 565)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            game_utils.trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        pygame.display.update()
        clock.tick(60)

def options_win():
    global music_on, fx_on, code_lang, lang
    while True:
        game_utils.play_next_track(music_on)
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    #Retuns to main menu if Back button is clicked
                    game_utils.play_click_sound(fx_on)
                    menu()
                if 420 <= mouse[0] <= 820 and 80 <= mouse[1] <= 120:
                    #Opens Skins menu if Skins button is clicked
                    game_utils.play_click_sound(fx_on)
                    skins()
                if 420 <= mouse[0] <= 820 and 130 <= mouse[1] <= 170:
                    #Turns music on/off and writes it to options if Audio: button is clicked
                    if music_on:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    music_on = not music_on
                    data["music_on"] = music_on
                    game_utils.write_to_json(PATH / "data.json", data)
                if 420 <= mouse[0] <= 820 and 180 <= mouse[1] <= 220:
                    #Turns fx on/off and writes it to options if FX: button is clicked
                    fx_on = not fx_on
                    data["fx_on"] = fx_on
                    game_utils.write_to_json(PATH / "data.json", data)
                if 420 <= mouse[0] <= 820 and 230 <= mouse[1] <= 270:
                    #Changes main programming language and writes it to options if Programming language: button is clicked
                    data["code_lang"] = (data["code_lang"] + 1) % 3
                    code_lang = data["code_lang"]
                    game_utils.write_to_json(PATH / "data.json", data)
                if 420 <= mouse[0] <= 820 and 280 <= mouse[1] <= 320:
                    #Changes game language eng/hrv
                    lang = "hrv" if lang == "eng" else "eng"
                    data["lang"] = lang
                    game_utils.write_to_json(PATH / "data.json", data)
                if 420 <= mouse[0] <= 820 and 330 <= mouse[1] <= 370:
                    #Clears game progress if Clear Progress button is clicked
                    game_utils.play_click_sound(fx_on)
                    data["music_on"] = True
                    data["fx_on"] = True
                    data["code_lang"] = 0
                    data["lang"] = "eng"
                    levels["last_finished_level"] = 0
                    for k in data["skins"]:
                        if k != "stevo":
                            data["skins"][k][3] = False
                    for i in range(1, 12):
                        game_skins[i].unlocked = False
                    for lvl in range(1, 37):
                        levels[f"level{lvl}"][0]["hint1_unlocked"] = False
                        levels[f"level{lvl}"][0]["hint2_unlocked"] = False
                    data["emeralds"] = 20
                    data["skin"] = "stevo"
                    data["first_play"] = True
                    player_levels["level_p"].clear()
                    player_levels["last_level"] = 0
                    keys_to_remove = [key for key in player_levels if key.startswith("level") and key[5:].isdigit()]
                    for key in keys_to_remove:
                        del player_levels[key]
                    game_utils.write_to_json(PATH / "levels" / "levels.json", levels)
                    game_utils.write_to_json(PATH / "levels" / "player_levels.json", player_levels)
                    game_utils.write_to_json(PATH / "data.json", data)
                    pygame.quit()
                    sys.exit()
                    
        game_utils.background()
        game_utils.bg_overlay()

        game_utils.menu_button(420, 80, options_text["skins"][lang], 400, 40, mouse)

        if music_on:
            game_utils.menu_button(420, 130, options_text["audio_on"][lang], 400, 40, mouse)
        else:
            game_utils.menu_button(420, 130, options_text["audio_off"][lang], 400, 40, mouse)

        if fx_on:
            game_utils.menu_button(420, 180, options_text["fx_on"][lang], 400, 40, mouse)
        else:
            game_utils.menu_button(420, 180, options_text["fx_off"][lang], 400, 40, mouse)

        if data["code_lang"] == 0:
            game_utils.menu_button(420, 230, options_text["python"][lang], 400, 40, mouse)
        elif data["code_lang"] == 1:
            game_utils.menu_button(420, 230, options_text["c"][lang], 400, 40, mouse)
        else:
            game_utils.menu_button(420, 230, options_text["c++"][lang], 400, 40, mouse)

        game_utils.menu_button(420, 280, options_text["lang"][lang], 400, 40, mouse)

        game_utils.menu_button(420, 330, options_text["clear_progress"][lang], 400, 40, mouse)

        #back_button
        game_utils.button(back_button, 10, 565)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            game_utils.trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        pygame.display.update()
        clock.tick(60)

def skins():
    messages = []

    skins_imgs = {
        skin.name: get_scaled_img(PATH / "skins" / f"{skin.name}.png", (skin.size, skin.size))
        for skin in game_skins
    }

    while True:
        game_utils.play_next_track(music_on)
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    #Retuns to Options menu if Back button is clicked
                    game_utils.play_click_sound(fx_on)
                    options_win()
                for skin in game_skins:
                    #Makes the clicked skin default if skin is clicked
                    if skin.hover(mouse[0], mouse[1]):
                        game_utils.play_click_sound(fx_on)
                        if skin.unlocked:
                            data["skin"] = skin.name
                            game_utils.write_to_json(PATH / "data.json", data)
                            game_utils.set_skin()
                        else:
                            if data["emeralds"] >= skin.price:
                                skin.unlocked = True
                                data["skins"][skin.name][3] = True
                                data["skin"] = skin.name
                                data["emeralds"] -= skin.price
                                game_utils.write_to_json(PATH / "data.json", data)
                                game_utils.set_skin()
                            else:
                                messages.append(texts["Not enough emeralds!"][lang])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_LMETA):
                    #Clears the output if Ctrl+K/Cmd+K is clicked
                    messages.clear()
                    
        game_utils.background()
        game_utils.bg_overlay()

        for skin in game_skins:
            pygame.draw.rect(window, (0, 0, 0), (skin.x, skin.y, skin.size, skin.size), 1)

            skin_image = skins_imgs[skin.name]

            window.blit(skin_image, (skin.x, skin.y))

            if not skin.unlocked:
                game_utils.trans_surface(skin.size, skin.size, (0, 0, 0, 50), skin.x, skin.y)
                emerald = get_scaled_img(PATH / "drawable" / "emerald.png", (32, 32))
                text_width = minecraft_font_small.size(str(skin.price))[0]
                window.blit(emerald, (skin.x + (skin.size-text_width)//2-17, skin.y+24))
                window.blit(render_small_text(str(skin.price)), (skin.x + (skin.size-text_width)//2 + 11, skin.y+20))

            if skin.name == data["skin"]:
                pygame.draw.rect(window, (0, 255, 0), (skin.x, skin.y, skin.size, skin.size), 2)

            if skin.hover(mouse[0], mouse[1]):
                pygame.draw.rect(window, (255, 255, 255), (skin.x, skin.y, skin.size, skin.size), 3)
                if skin.unlocked:
                    game_utils.button(play_level_button, skin.x, skin.y)

        #back_button
        game_utils.button(back_button, 10, 565)

        game_utils.minecraft_cmd(messages, 0, 1240, 620)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            game_utils.trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        pygame.display.update()
        clock.tick(60)

def game(level, player_l = False, random_l = False):
    global code_lang
    global def_code_python, def_code_c, def_code_cpp
    global book, lang
    code_lang = data["code_lang"]
    messages = []
    restart_code = False
    code_runned = False
    level_finished = False
    one_v_one = False
    one_v_one_code = [False, False]
    one_v_one_time = [0, 0]
    fun_calls = [0, 0]
    grades = [0, 0]
    stop_moving = False

    timed_start = 0
    timed_time = 0
    minutes = 0
    seconds = 0

    lang_text_x = (645-minecraft_font_smaller.size(languages[code_lang])[0])//2+595
    lang_text_length = minecraft_font_smaller.size(languages[code_lang])[0]

    level_object = (game_levels if not player_l else player_game_levels)[level-1]
    level_data = (levels if not player_l else player_levels)[f"level{level}"][0]

    player = 1
    def get_text_path():
        return level_data[f"input_text_{languages[code_lang]}"]
    code_input.set_text(get_text_path())

    book_text = game_utils.render_book_text(level_data[f"text_{languages[code_lang]}_{lang}"])

    blocks = game_utils.render_blocks(level_data["blocks"])

    def restart_mob():
        if player_l or level >= 10:
            xy = level_data["steve_xy"]
            stevexy[0] = xy[0]*85
            stevexy[1] = (6-xy[1])*85

    restart_mob()

    def restart_text():
        text_path = get_text_path()
        code_input_object = code_input if player == 1 else code_input_2
        code_input_object.set_text(text_path)

    def buy_hint(hint, price):
        if level_data[f"hint{hint}_unlocked"]:
            messages.append((level_data[f"hint{hint}_{languages[code_lang]}_{lang}"]))
        elif hint == 2 and not level_data["hint1_unlocked"]:
            messages.append(texts["Buy Hint 1 first."][lang])
        else:
            if data["emeralds"] >= price:
                data["emeralds"] -= price
                messages.append((level_data[f"hint{hint}_{languages[code_lang]}_{lang}"]))
                level_data[f"hint{hint}_unlocked"] = True
                game_utils.write_to_json(PATH / "levels" / "levels.json", levels)
                game_utils.write_to_json(PATH / "data.json", data)
            else:
                messages.append(texts["You don't have enough emeralds!"][lang])

    def del_random_l():
        if random_l:
            player_levels.pop(f"level{level}")
            player_levels["level_p"].pop()
            player_levels["last_level"] -= 1
            player_game_levels.pop()
            game_utils.write_to_json(PATH / "levels" / "player_levels.json", player_levels)
            return True
        
    def check():
        nonlocal plate_activated, player_l
        if stevexy[1]//85 < 0 or stevexy[0]//85 < 0 or stevexy[1]//85 > 6 or stevexy[0]//85 > 6:
            messages.append(texts["Mob got out of bounds!"][lang])
            restart_mob()
            return False
            
        block = level_data["blocks"][stevexy[1]//85][stevexy[0]//85]
    
        if block == "oak_trapdoor.png":
            if level >= 14 and level < 17 and not plate_activated:
                messages.append(texts["Door is not unlocked!"][lang])
                restart_mob()
            return True
        elif block == "pressure_plate.png":
            plate_activated = True
        elif player_l:
            if block != level_data["path_block"]:
                messages.append(texts["You can't go on this block!"][lang])
                restart_mob()
                return False
        elif (level < 17 or level == 33 or level == 34) and block != "grass_top.png":
            messages.append(texts["You can only go on grass!"][lang])
            restart_mob()
            return False
        elif (level >= 17 and level < 21 or level == 35) and block != "bedrock.png":
            messages.append(texts["You can only go on bedrock!"][lang])
            restart_mob()
            return False
        elif (level >= 21 and level < 33 or level == 36) and block != "purpur_block.png":
            messages.append(texts["You can only go on purpur blocks!"][lang])
            restart_mob()
            return False

    while True:
        game_utils.play_next_track(music_on)
        window.fill((30, 30, 30))

        mouse = pygame.mouse.get_pos()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                del_random_l()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 10 <= mouse[0] <= 30 and 597 <= mouse[1] <= 617:
                    #Returns to Main menu, Level menu or Player levels menu if Back button is clicked
                    game_utils.play_click_sound(fx_on)
                    if del_random_l():
                        level_menu()
                    elif player_l:
                        your_levels_menu()
                    else:
                        menu()
                elif 30 <= mouse[0] <= 50 and 598 <= mouse[1] <= 618:
                    if player_l or level >= 10:
                        game_levels[level-1].text_closed = True
                    code_runned = True
                    restart_mob()
                elif 595 <= mouse[0] <= 615 and 598 <= mouse[1] <= 618:
                    #Restarts code if Restart button is clicked
                    restart_code = True
                elif 566 <= mouse[0] <= 582 and 598 <= mouse[1] <= 618:
                    #Goes to the next level if current level is finished
                    if not player_l and level_finished and level < 36:
                        one_v_one = False
                        timed_start = 0
                        player = 1
                        if level > levels["last_finished_level"]:
                            levels["last_finished_level"] = level
                        level += 1
                        level_object = game_levels[level-1]
                        level_data = levels[f"level{level}"][0]
                        level_object.unlocked = True
                        game_utils.write_to_json(PATH / "levels" / "levels.json", levels)
                        messages.clear()
                        level_finished = False
                        blocks = game_utils.render_blocks(level_data["blocks"])
                        if not player_l:
                            book_text = game_utils.render_book_text(level_data[f"text_{languages[code_lang]}_{lang}"])
                        text_path = get_text_path()
                        restart_text()
                        restart_mob()
                elif 630 <= mouse[0] <= 654 and 600 <= mouse[1] <= 615 and not one_v_one and (10 <= level <= 24 or player_l):
                    #Enters the 1v1 mode if 1v1 button is clicked
                    one_v_one = True
                    code_input_2 = Textbox(595, 0, 645, 620, PATH / "Minecraft.ttf")
                    text_path = get_text_path()
                    code_input_2.set_text(text_path)
                elif one_v_one and 630 <= mouse[0] <= 640 and 600 <= mouse[1] <= 615 and (10 <= level <= 24  or player_l):
                    #Opens first player's code editor if 1. button is clicked in 1v1 mode
                    player = 1
                elif one_v_one and 650 <= mouse[0] <= 660 and 600 <= mouse[1] <= 615 and (10 <= level <= 24  or player_l):
                    #Opens second player's code editor if 2. button is clicked in 1v1 mode
                    player = 2
                elif one_v_one and 668 <= mouse[0] <= 684 and 598 <= mouse[1] <= 614:
                    #Exits 1v1 mode if Exit 1v1 button is clicked in 1v1 mode
                    player = 1
                    one_v_one = False
                elif lang_text_x <= mouse[0] <= lang_text_x+lang_text_length and 600 <= mouse[1] <= 615:
                    #Changes the current programming language if Programming language is pressed
                    code_lang = (code_lang + 1) % 3
                    lang_text_x = (645-minecraft_font_smaller.size(languages[code_lang])[0])//2+595
                    lang_text_length = minecraft_font_smaller.size(languages[code_lang])[0]
                    book_text = game_utils.render_book_text(level_data[f"text_{languages[code_lang]}_{lang}"])
                    restart_text()
                elif not player_l and 56 <= mouse[0] <= 67 and 597 <= mouse[1] <= 617:
                    #Buys and displays or just displays first hint when first Hint button is clicked
                    buy_hint(1, 5)
                elif not player_l and 70 <= mouse[0] <= 84 and 597 <= mouse[1] <= 617:
                    #Buys and displays or just displays second hint when second Hint button is clicked
                    buy_hint(2, 15)  
                elif 90 <= mouse[0] <= 110 and 598 <= mouse[1] <= 618:
                    if not player_l:
                        restart_text()
                        restart_mob()
                        timed_start = time.time()
                elif not level_object.text_closed:
                    #Changes showed page if Book is not closed
                    if 410 <= mouse[0] <= 452 and 515 <= mouse[1] <= 539 and level_object.text_page < level_data["pages"]-1:
                        #Goes to next page of the book if it exists
                        level_object.text_page += 1
                    if 120 <= mouse[0] <= 162 and 515 <= mouse[1] <= 539 and level_object.text_page > 0:
                        #Goes to previous page of the book if it exists
                        level_object.text_page -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_LMETA):
                    #Closes or opens the book if Ctrl+E/Cmd+E is clicked
                    level_object.text_closed = not level_object.text_closed
                if event.key == pygame.K_k and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_LMETA):
                    #Clears the output if Ctrl+K/Cmd+K is clicked
                    messages.clear()

            #Feeds the events to the current Textbox object
            if player == 1 and not one_v_one_code[0]:
                code_input.handle_events(event) 
            elif player == 2 and not one_v_one_code[1]:
                code_input_2.handle_events(event)

        if player == 1:
            code_input.draw(window)
        elif player == 2:
            code_input_2.draw(window)

        pygame.draw.rect(window, (205, 205, 205), (0, 0, 595, 595))

        pygame.draw.rect(window, (0, 118, 197), (0, 595, 1240, 25))

        #language
        window.blit(game_text[code_lang], (lang_text_x, 596))

        if lang_text_x <= mouse[0] <= lang_text_x+lang_text_length and 600 <= mouse[1] <= 615:
            game_utils.description(texts["Change language"][lang])
            game_utils.trans_surface(lang_text_length, 15, (170, 170, 170, 120), lang_text_x, 600)

        if 10 <= mouse[0] <= 30 and 597 <= mouse[1] <= 617:
            game_utils.description(texts["Exit"][lang])
            game_utils.trans_surface(20, 20, (170, 170, 170, 120), 12, 597)
        
        #back_button
        game_utils.button(close_button, 10, 596)

        if 30 <= mouse[0] <= 50 and 598 <= mouse[1] <= 618:
            game_utils.description(texts["Run"][lang])
            game_utils.trans_surface(20, 20, (170, 170, 170, 120), 34, 598)

        #run_button
        game_utils.button(run_button, 30, 593)

        if 595 <= mouse[0] <= 615 and 598 <= mouse[1] <= 618:
            game_utils.description(texts["Restart"][lang])
            game_utils.trans_surface(20, 20, (170, 170, 170, 120), 599, 598)

        #restart_button
        game_utils.button(restart_button, 596, 595)

        if not player_l:
            #hint1_button
            hint_x = 56
            game_utils.button(torch1_button, hint_x-11, 586)
            
            if hint_x <= mouse[0] <= hint_x+11 and 597 <= mouse[1] <= 617:
                if level_data["hint1_unlocked"]:
                    game_utils.description("Hint 1.")
                else:
                    game_utils.description(f"Hint 1. (5 {texts["emeralds"][lang]})")
                game_utils.trans_surface(11, 20, (170, 170, 170, 120), hint_x, 597)
            
            #hint2_button
            game_utils.button(torch2_button, hint_x+4, 586)

            if hint_x+14 <= mouse[0] <= hint_x+28 and 597 <= mouse[1] <= 617:
                if level_data["hint2_unlocked"]:
                    game_utils.description("Hint 2.")
                else:
                    game_utils.description(f"Hint 2. (15 {texts["emeralds"][lang]})")
                game_utils.trans_surface(14, 20, (170, 170, 170, 120), hint_x+14, 597)

            if 90 <= mouse[0] <= 110 and 598 <= mouse[1] <= 618:
                game_utils.description(texts["Timed challenge"][lang])
                game_utils.trans_surface(20, 20, (170, 170, 170, 120), 90, 598)

            #clock_button
            game_utils.button(clock_button, 90, 598)

        #next_button
        if not player_l and level_finished and level < 36:
            if 566 <= mouse[0] <= 582 and 598 <= mouse[1] <= 618:
                game_utils.description(texts["Next level"][lang])
                game_utils.trans_surface(22, 20, (170, 170, 170, 120), 566, 598)
            game_utils.button(accept_button, 562, 592)

        #1v1 button
        if 10 <= level <= 24 or player_l:
            if not one_v_one:
                window.blit(game_text["1v1"], (630, 596))
                if 630 <= mouse[0] <= 654 and 600 <= mouse[1] <= 615:
                    game_utils.description(texts["1 vs 1 with a friend"][lang])
                    game_utils.trans_surface(24, 15, (170, 170, 170, 120), 630, 600)
            else:
                window.blit(game_text["1."], (630, 596))
                if 630 <= mouse[0] <= 640 and 600 <= mouse[1] <= 615:
                    game_utils.description(texts["1st player"][lang])
                    game_utils.trans_surface(10, 15, (170, 170, 170, 120), 630, 600)
                window.blit(game_text["2."], (650, 596))
                if 650 <= mouse[0] <= 660 and 600 <= mouse[1] <= 615:
                    game_utils.description(texts["2nd player"][lang])
                    game_utils.trans_surface(10, 15, (170, 170, 170, 120), 650, 600)

                if 668 <= mouse[0] <= 684 and 598 <= mouse[1] <= 614:
                    game_utils.description(texts["Exit 1v1"][lang])
                    game_utils.trans_surface(16, 16, (170, 170, 170, 120), 668, 598)

                #exit_1v1_button
                game_utils.button(close_1v1_button, 668, 598)


        #blocks
        i = 0
        j = 0
        while i < 595:
            while j < 595:
                window.blit(blocks[j//85][i//85], (i, j))
                pygame.draw.rect(window, (0, 0, 0), (i, j, 85, 85), 1)
                j += 85
            j = 0
            i += 85

        if 10 <= level <= 24 or level >= 33 or player_l:
            steve = pygame.image.load(PATH / "skins" / f"{data['skin']}.png")
            steve = pygame.transform.scale(steve, (85, 85))
        
            window.blit(steve, (stevexy[0], stevexy[1]))
            pygame.draw.rect(window, (0, 0, 0), (stevexy[0], stevexy[1], 85, 85), 1)
        #book
        if not level_object.text_closed:
            window.blit(book, (6, 12))
            game_utils.render_text(115, 63, book_text[level_object.text_page], 28.8)

            if level_object.text_page < level_data["pages"]-1:
                game_utils.button(page_forward_button, 410, 515)

                if 410 <= mouse[0] <= 452 and 515 <= mouse[1] <= 539:
                    game_utils.trans_surface(36, 19, (170, 170, 170, 120), 415, 519)
            
            if level_object.text_page > 0:
                game_utils.button(page_backward_button, 120, 515)

                if 120 <= mouse[0] <= 162 and 515 <= mouse[1] <= 539:
                    game_utils.trans_surface(36, 19, (170, 170, 170, 120), 125, 519)

        if restart_code:
            restart_text()
            restart_mob()
            restart_code = False

        if timed_start != 0:
            timed_time = time.time() - timed_start
            minutes = int(timed_time // 60)
            seconds = int(timed_time % 60)

            window.blit(render_small_text(f"{minutes:02}:{seconds:02}"), (1165, 0))

        #code
        if code_runned:
            code = code_input.get_text().split("\n")
            cbd = []
            for el in code:
                cbdd = cbd_maker(el)     
                if cbdd:           
                    cbd.append(cbdd)

            #Get and execute the inputted code
            input_code = code_input.get_text() if player == 1 else code_input_2.get_text()
            start_time = time.time()
            if code_lang == 0:
                executed_code = exec_code(def_code_python + input_code)
            else:
                c_lang = "C" if code_lang == 1 else "C++"
                executed_code = exec_c_code(def_code_c + input_code if code_lang == 1 else def_code_cpp + input_code, c_lang)
            end_time = time.time()
            one_v_one_time[player-1] = end_time - start_time
            if executed_code["error"]:
                err = executed_code["error"]
                if code_lang != 0:
                    try:
                        err = err.split("\n")[0].split(":", 1)[1].split(" ", 1)[1]
                    except Exception:
                        err = "?"
                messages.append("Error: " + err)

            if code_lang == 0:
                messages += executed_code["out"]
                variables = executed_code["vars"]
                del variables["__builtins__"]
            else:
                for el in executed_code["out"]:
                    if el.split(" ")[0] not in ("right", "left", "up", "down"):
                        messages += [el]

            #correct solution
            solution = False
            if not player_l and level == 9:
                solution = True
            if not player_l and (level < 10 or level > 24 and level < 33) and level_data[f"solution_{languages[code_lang]}"][0] == cbd:
                solution = True
            
            if not player_l and level == 4:
                if code_lang == 0:
                    s = {int, float, bool, str}
                    for el in variables.keys():
                        s.discard(type(variables[el]))
                    solution = not s
                elif code_lang in [1, 2]:
                    c = 0
                    valid_types = {
                        1: {"int", "float", "double", "char"},
                        2: {"int", "float", "double", "string", "bool", "char"}
                    }
                    for el in cbd:
                        if el[0] in valid_types[code_lang]:
                            if el[0] == "char" and el[2] == "[" and el[3] == "]" and el[4] == "=":
                                c += 1
                            elif el[2] == "=":
                                c += 1
                    solution = c == (5 if code_lang == 1 else 6)
            if player_l or level >= 10 and level <= 24 or level >= 33 and level <= 36:
                stop_moving = False
                if not player_l and level >= 14 and level < 17:
                    plate_activated = False
                try:
                    if code_lang == 0:
                        coms = variables["coms"]
                    else:
                        coms = []
                        for el in executed_code["out"]:
                            el_splited = el.split(" ")
                            if el_splited[0] in ["right", "left", "up", "down"]:
                                coms.append(el.split(" "))
                except Exception:
                    coms = []
                if len(coms) > 50:
                    coms = []

                for com in coms:
                    if stop_moving:
                        break
                    direction, steps = com[0], int(com[1])
                    dx, dy = moves[direction]
                    for _ in range(steps):
                        stevexy[0] += dx
                        stevexy[1] += dy
                        game_utils.move(-dx, -dy, level_data["blocks"])
                        if check() == False:
                            stop_moving = True
                            break

                if check():
                    if one_v_one:
                        fun_calls[player-1] = len(coms)
                        one_v_one_code[player-1] = True
                        messages.append(f"{texts["Player"][lang]} {player}. {texts["finished the level"][lang]}!")
                        if not (one_v_one_code[0] and one_v_one_code[1]):
                            restart_mob()
                    else:
                        if player_l:
                            solution = True
                        elif level >= 14 and level < 17 and plate_activated:
                            solution = True
                        elif level >= 17 and level < 21:
                            if "for" in input_code:
                                solution = True
                            else:
                                messages.append(f"{texts["Your code should include a"][lang]} for {texts["loop"][lang]}!")
                                restart_mob()
                        elif level >= 21 and level <= 24:
                            if "while" in input_code:
                                solution = True
                            else:
                                messages.append(f"{texts["Your code should include a"][lang]} while {texts["loop"][lang]}!")
                                restart_mob()
                        elif level >= 10 and level < 14 or level >= 33:
                            solution = True
                else:
                    messages.append(texts["Wrong solution! Try again."][lang])
                    restart_mob()
            
            if one_v_one:
                if one_v_one_code[0] and one_v_one_code[1]:
                    grades = grade_code(code_input.get_text(), code_input_2.get_text(), one_v_one_time, fun_calls)
                    messages.append(f"{texts["1st player"][lang]} {texts["scored"][lang]}: {grades[0]}/4")
                    messages.append(f"{texts["2nd player"][lang]} {texts["scored"][lang]}: {grades[1]}/4")
                    if grades[0] == grades[1]:
                        messages.append(texts["It's a draw!"][lang])
                    else:
                        messages.append(f"{texts["Player"][lang]} {1 if grades[0] > grades[1] else 2}. {texts["won"][lang]}.")

            if solution and not executed_code["error"]:
                if player_l or level >= 10 and level <= 24 or level >= 33 and level <= 36:
                    if fx_on:
                        sound = pygame.mixer.Sound(PATH / "sounds" / "trapdoor.mp3")
                        sound.play()
                                        
                messages.append(texts["Great job!"][lang])
                emeralds = 5
                if level >= 10:
                    emeralds = 10
                elif level >= 14:
                    emeralds = 15
                if not player_l:
                    messages.append(f"+{emeralds} {texts["Emeralds"][lang]}")
                if timed_time:
                    timed_start = 0
                    messages.append(f"{texts["Your time"][lang]}: {minutes:02}:{seconds:02}")
                    if timed_time < 10:
                        messages.append(f"< 10 {texts["seconds"][lang]}: +20 {texts["Emeralds"][lang]}")
                        emeralds += 20
                    elif timed_time < 15:
                        messages.append(f"< 15 {texts["seconds"][lang]}: +15 {texts["Emeralds"][lang]}")
                        emeralds += 15
                    elif timed_time < 20:
                        messages.append(f"< 20 {texts["seconds"][lang]}: +10 {texts["Emeralds"][lang]}")
                        emeralds += 10
                    elif timed_time < 30:
                        messages.append(f"< 30 {texts["seconds"][lang]}: +5 {texts["Emeralds"][lang]}")
                        emeralds += 5

                data["emeralds"] += emeralds
                level_finished = True   
                game_utils.write_to_json(PATH / "data.json", data)

            code_runned = False

        game_utils.minecraft_cmd(messages, 0, 595, 590)

        cursor_pos = minecraft_font_smaller.render(f"Ln {code_input.i + 1}, Col {code_input.cursor_pos + 1}", True, (255, 255, 255))
        window.blit(cursor_pos, (1240 - cursor_pos.get_width() - 15, 596))
        
        pygame.display.update()
        clock.tick(60)

loaders.loading_screen()
if data["first_play"]:
    data["first_play"] = False
    game_utils.write_to_json(PATH / "data.json", data)
    loaders.display_intro_text()
menu()