import pygame, random, json, time
from classes.pygametextboxinput import *
from classes.code_runner import *
from pathlib import Path
from classes.def_codes import *
from classes.classes_ import *
from classes.utils import *

PATH = Path.cwd()

pygame.init()

window = pygame.display.set_mode((1240, 620))
pygame.display.set_caption("Code_Craft")
pygame.display.set_icon(pygame.image.load(PATH / "drawable" / "crafting_table.png"))
clock = pygame.time.Clock()

minecraft_font_big = pygame.font.Font(PATH / "Minecraft.ttf", 75)
minecraft_font_small = pygame.font.Font(PATH / "Minecraft.ttf", 25)
minecraft_font_smaller = pygame.font.Font(PATH / "Minecraft.ttf", 15)
minecraft_font_book = pygame.font.Font(PATH / "Minecraft.ttf", 20)

#music
current_song_index = 0
playlist = [PATH / "music" / "DryHands.mp3", 
            PATH / "music" / "Haggstrom.mp3", 
            PATH / "music" / "LivingMice.mp3",
            PATH / "music" / "MiceOnVenus.mp3",
            PATH / "music" / "Minecraft.mp3",
            PATH / "music" / "SubwooferLullaby.mp3",
            PATH / "music" / "Sweden.mp3",
            PATH / "music" / "WetHands.mp3"]

def load_json_file(file):
    with open(file) as json_file:
        return json.load(json_file)

levels = load_json_file(PATH / "levels" / "levels.json")

options = load_json_file(PATH / "options.json")

data = load_json_file(PATH / "data.json")

player_levels = load_json_file(PATH / "levels" / "player_levels.json")

stevexy = [0, 510]

game_utils = GameUtils(window, pygame, playlist, current_song_index, minecraft_font_small, minecraft_font_book, minecraft_font_smaller, clock, data, stevexy, levels, player_levels, time, PATH)

game_levels = []
for p in levels["level_p"]:
    game_levels.append(Level(p[0], p[1], p[2], p[3], p[4], levels))

player_game_levels = []
if player_levels["last_level"] > 0:
    for p in player_levels["level_p"]:
        player_game_levels.append(Level(p[0], p[1], p[2], p[3], p[4], levels))

game_skins = []
for k in data["skins"]:
    game_skins.append(Skin(k, data["skins"][k][0], data["skins"][k][1], data["skins"][k][2], data["skins"][k][3]))

random.shuffle(playlist)
pygame.mixer.music.load(playlist[current_song_index])
pygame.mixer.music.play()

music_on = options["music_on"]
fx_on = options["fx_on"]
if not music_on:
    pygame.mixer.music.pause()

code_input = Textbox(595, 0, 645, 620, PATH / "Minecraft.ttf")
pygame.key.set_repeat(200, 25)

languages = ["Python", "C", "C++"]
code_lang = 0

code_runned = False
level_finished = False
grades = [0, 0]

click_sound = pygame.mixer.Sound(PATH / "sounds" / "minecraft_click.mp3")

def menu():
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            game_utils.play_next_track()

        mouse = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 420 <= mouse[0] <= 820 and 250 <= mouse[1] <= 290:
                    if fx_on:
                        click_sound.play()
                    if levels["last_finished_level"] < 24:
                        game(levels["last_finished_level"]+1)
                elif 420 <= mouse[0] <= 820 and 300 <= mouse[1] <= 340:
                    if fx_on:
                        click_sound.play()
                    level_menu()
                elif 420 <= mouse[0] <= 820 and 350 <= mouse[1] <= 390:
                    if fx_on:
                        click_sound.play()
                    tutorial()
                elif 420 <= mouse[0] <= 615 and 420 <= mouse[1] <= 460:
                    if fx_on:
                        click_sound.play()
                    options_win()
                elif 625 <= mouse[0] <= 820 and 420 <= mouse[1] <= 460:
                    exit()
        
        game_utils.background()

        big_title = pygame.transform.scale(pygame.image.load(PATH / "drawable" / "Code_Craft.png"), (491, 127))
        window.blit(big_title, (374, 60))

        emerald = pygame.transform.scale(pygame.image.load(PATH / "drawable" / "emerald.png"), (32, 32))
        window.blit(emerald, (1210, 0))
        window.blit(minecraft_font_book.render(str(data["emeralds"]), True, (255, 255, 255)), (1213-minecraft_font_book.size(str(data["emeralds"]))[0], 8.8))

        game_utils.menu_button(420, 250, 594, "Play", 400, 40, mouse)

        game_utils.menu_button(420, 300, 580, "Levels", 400, 40, mouse)

        game_utils.menu_button(420, 350, 573, "Tutorial", 400, 40, mouse)

        game_utils.menu_button(420, 420, 464, "Options...", 195, 40, mouse)

        game_utils.menu_button(625, 420, 659, "Quit Game", 195, 40, mouse)

        pygame.display.flip()     

def level_menu():
    for lvl in game_levels:
        lvl.unlocked = lvl.level <= levels["last_finished_level"]+1
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            game_utils.play_next_track()
        mouse = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 830 <= mouse[0] <= 1030 and 550 <= mouse[1] <= 590:
                    if fx_on:
                        click_sound.play()
                    level_builder()
                if 1050 <= mouse[0] <= 1210 and 550 <= mouse[1] <= 590:
                    if fx_on:
                        click_sound.play()
                    your_levels_menu()
                for lvl in game_levels:
                    if lvl.hover(mouse[0], mouse[1]) and lvl.unlocked:
                        if fx_on:
                            click_sound.play()
                        game(lvl.level)
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    if fx_on:
                        click_sound.play()
                    menu()
        
        game_utils.background()
        game_utils.bg_overlay()

        #back_button
        game_utils.button(PATH / "drawable" / "unselect.png", 40, 40, 15, 565)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            game_utils.trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        #level_button
        for lvl in game_levels:
            if lvl.x != -1 and lvl.y != -1:
                pygame.draw.rect(window, (130, 130, 130), (lvl.x, lvl.y, lvl.size, lvl.size))
                pygame.draw.rect(window, (0, 0, 0), (lvl.x, lvl.y, lvl.size, lvl.size), 1)

                text_width = minecraft_font_small.size(str(lvl.level))[0]

                window.blit(minecraft_font_small.render(str(lvl.level), True, (255, 255, 255)), (lvl.x + (lvl.size-text_width)//2 + 1, lvl.y+30))

                if not lvl.unlocked:
                    game_utils.trans_surface(lvl.size, lvl.size, (0, 0, 0, 50), lvl.x, lvl.y)

                if lvl.hover(mouse[0], mouse[1]) and lvl.unlocked:
                    pygame.draw.rect(window, (255, 255, 255), (lvl.x, lvl.y, lvl.size, lvl.size), 3)
                    game_utils.button(PATH / "drawable" / "select.png", lvl.size, lvl.size, lvl.x, lvl.y)

        game_utils.menu_button(830, 550, 853, "Level builder", 200, 40, mouse)

        game_utils.menu_button(1050, 550, 1063, "Your levels", 160, 40, mouse)
        
        pygame.display.flip()

def your_levels_menu():
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            game_utils.play_next_track()
        mouse = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for lvl in player_game_levels:
                    if lvl.hover(mouse[0], mouse[1]) and lvl.level != -1:
                        if fx_on:
                            click_sound.play()
                        game(lvl.level, True)
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    if fx_on:
                        click_sound.play()
                    level_menu()
        
        game_utils.background()
        game_utils.bg_overlay()

        #back_button
        game_utils.button(PATH / "drawable" / "unselect.png", 40, 40, 15, 565)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            game_utils.trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        #level_button
        for lvl in player_game_levels:
            if lvl.x != -1 and lvl.y != -1:
                pygame.draw.rect(window, (130, 130, 130), (lvl.x, lvl.y, lvl.size, lvl.size))
                pygame.draw.rect(window, (0, 0, 0), (lvl.x, lvl.y, lvl.size, lvl.size), 1)

                text_width = minecraft_font_small.size(str(lvl.level))[0]

                window.blit(minecraft_font_small.render(str(lvl.level), True, (255, 255, 255)), (lvl.x + (lvl.size-text_width)//2 + 1, lvl.y+30))

                if lvl.hover(mouse[0], mouse[1]):
                    pygame.draw.rect(window, (255, 255, 255), (lvl.x, lvl.y, lvl.size, lvl.size), 3)
                    game_utils.button(PATH / "drawable" / "select.png", lvl.size, lvl.size, lvl.x, lvl.y)
        
        pygame.display.flip()

def level_builder():
    saved = False
    curr_level = player_levels["last_level"]+1
    plus_x_y = [0, 0]
    blocks = [["plus.png" for _ in range(7)] for _ in range(7)]
    block_file_names = [
        ["azalea_leaves.png", "bedrock.png", "cactus_top.png", "chorus_flower.png", "chorus_plant.png", "coal_ore.png"],
        ["crafting_table_top.png", "diamond_ore.png", "dirt.png", "emerald_ore.png", "end_stone_bricks.png", "end_stone.png"],
        ["farmland_moist.png", "farmland.png", "gold_ore.png", "grass_top.png", "hay_block_top.png", "melon_top.png"],
        ["nether_quartz.png", "nether_wart_block.png", "netherrack.png", "oak_log_top.png", "oak_trapdoor.png", "nether_gold_ore.png"],
        ["pumpkin_top.png", "purpur_block.png", "sand.png", "sandstone_top.png", "soul_sand.png", "soul_soil.png"],
        ["cobblestone.png"]
    ]
    start = []
    path_block = "plus.png"
    path_select = False
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            game_utils.play_next_track()
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse[0] <= 595 and mouse[1] <= 595:
                    plus_x_y = [mouse[0]//85, mouse[1]//85]
                elif 675 <= mouse[0] <= 1184 and 30 <= mouse[1] <= 540:
                    if (mouse[1]-32)//85 == 5 and (mouse[0]-675)//85 >= 1:
                        pass
                    else:
                        a = False
                        for el in blocks:
                            a = block_file_names[(mouse[1]-40)//85][(mouse[0]-675)//85] in el
                        if block_file_names[(mouse[1]-40)//85][(mouse[0]-675)//85] != "oak_trapdoor.png":
                            if path_select:
                                path_block = block_file_names[(mouse[1]-40)//85][(mouse[0]-675)//85]
                                path_select = False
                            else:
                                blocks[plus_x_y[1]][plus_x_y[0]] = block_file_names[(mouse[1]-40)//85][(mouse[0]-675)//85]
                        elif not a:
                            blocks[plus_x_y[1]][plus_x_y[0]] = block_file_names[(mouse[1]-40)//85][(mouse[0]-675)//85]
                elif 605 <= mouse[0] <= 625 and 20 <= mouse[1] <= 40:
                    start = plus_x_y.copy()
                elif 605 <= mouse[0] <= 633 and 60 <= mouse[1] <= 88:
                    path_select = True
                elif 609 <= mouse[0] <= 633 and 104 <= mouse[1] <= 129:
                    if start:
                        curr = new_level_curr
                        curr["steve_xy"] = [start[0], 6-start[1]]
                        curr["blocks"] = blocks
                        curr["path_block"] = path_block
                        player_levels[f"level{curr_level}"] = [curr]
                        with open(PATH / "levels" / "player_levels.json", 'w') as file:
                            json.dump(player_levels, file, indent=4)
                        saved = True
                elif 10 <= mouse[0] <= 30 and 597 <= mouse[1] <= 617:
                    if saved:
                        if curr_level > 1:
                            curr_level_p = [0] * 5
                            curr = player_levels["level_p"][-2]
                            curr_level_p[0] = curr[0]+100 if curr[0] < 1130 else 30
                            curr_level_p[1] = curr[1] if curr[0] < 1130 else curr[1]+110
                            curr_level_p[2] = curr_level
                            curr_level_p[3] = 80
                            curr_level_p[4] = True
                            player_levels["level_p"].insert(-1, curr_level_p)
                        player_levels["last_level"] += 1
                        if player_levels["last_level"] > 0:
                            for p in player_levels["level_p"]:
                                player_game_levels.append(Level(p[0], p[1], p[2], p[3], p[4], levels))
                        with open(PATH / "levels" / "player_levels.json", 'w') as file:
                            json.dump(player_levels, file, indent=4)
                    if fx_on:
                        click_sound.play()
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
            while j < 30 + 6 * 85:
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
            game_utils.description("Exit")
            game_utils.trans_surface(20, 20, (170, 170, 170, 120), 12, 597)
        
        #back_button
        game_utils.button(PATH / "drawable" / "close.png", 22, 22, 10, 596)

        if 605 <= mouse[0] <= 625 and 20 <= mouse[1] <= 40:
            game_utils.description("Set start position")
            game_utils.trans_surface(20, 20, (170, 170, 170, 120), 609, 20)

        #start button
        game_utils.button(PATH / "drawable" / "select.png", 28, 28, 605, 15)

        #path select
        game_utils.button(PATH / "blocks" / path_block, 28, 28, 605, 60)
        if 605 <= mouse[0] <= 633 and 60 <= mouse[1] <= 88:
            game_utils.description("Set path block")
            game_utils.trans_surface(28, 28, (170, 170, 170, 120), 605, 60)

        if 609 <= mouse[0] <= 633 and 104 <= mouse[1] <= 129:
            game_utils.description("Save level")
            game_utils.trans_surface(22, 21, (170, 170, 170, 120), 609, 104)

        #save button
        game_utils.button(PATH / "drawable" / "accept.png", 29, 29, 605, 100)

        pygame.display.flip()

def tutorial():
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            game_utils.play_next_track()
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    if fx_on:
                        click_sound.play()
                    menu()
                    
        game_utils.background()
        game_utils.bg_overlay()

        #back_button
        game_utils.button(PATH / "drawable" / "unselect.png", 40, 40, 15, 565)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            game_utils.trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        pygame.display.flip()

def options_win():
    global music_on, fx_on
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            game_utils.play_next_track()
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    if fx_on:
                        click_sound.play()
                    menu()
                if 420 <= mouse[0] <= 820 and 80 <= mouse[1] <= 120:
                    if fx_on:
                        click_sound.play()
                    skins()
                if 420 <= mouse[0] <= 820 and 130 <= mouse[1] <= 170:
                    if music_on:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    music_on = not music_on
                    options["music_on"] = music_on
                    with open(PATH / "options.json", 'w') as file:
                        json.dump(options, file, indent=4)
                if 420 <= mouse[0] <= 820 and 180 <= mouse[1] <= 220:
                    fx_on = not fx_on
                    options["fx_on"] = fx_on
                    with open(PATH / "options.json", 'w') as file:
                        json.dump(options, file, indent=4)
                if 420 <= mouse[0] <= 820 and 230 <= mouse[1] <= 270:
                    if fx_on:
                        click_sound.play()
                    levels["last_finished_level"] = 0
                    for k in data["skins"]:
                        if k != "steve":
                            data["skins"][k][3] = False
                    for i in range(1, 16):
                        game_skins[i].unlocked = False
                    data["emeralds"] = 0
                    data["skin"] = "steve"
                    with open(PATH / "levels" / "levels.json", 'w') as file:
                        json.dump(levels, file, indent=4)
                    with open(PATH / "data.json", 'w') as file:
                        json.dump(data, file, indent=4)
                    exit()
                    
        game_utils.background()
        game_utils.bg_overlay()

        game_utils.menu_button(420, 80, 587, "Skins", 400, 40, mouse)

        music_state = "On" if music_on else "Off"
        game_utils.menu_button(420, 130, 420+(400-minecraft_font_small.size(f"Audio: {music_state}")[0])//2, f"Audio: {music_state}", 400, 40, mouse)

        fx_state = "On" if fx_on else "Off"
        game_utils.menu_button(420, 180, 444+(356-minecraft_font_small.size(f"FX: {fx_state}")[0])//2, f"FX: {fx_state}", 400, 40, mouse)

        game_utils.menu_button(420, 230, 452, "Clear Progress (Exit's app)", 400, 40, mouse)

        #back_button
        game_utils.button(PATH / "drawable" / "unselect.png", 40, 40, 15, 565)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            game_utils.trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        pygame.display.flip()

def skins():
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            game_utils.play_next_track()
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    if fx_on:
                        click_sound.play()
                    options_win()
                for skin in game_skins:
                    if skin.hover(mouse[0], mouse[1]):
                        if fx_on:
                            click_sound.play()
                        if skin.unlocked:
                            data["skin"] = skin.name
                            with open(PATH / "data.json", 'w') as file:
                                json.dump(data, file, indent=4)
                        else:
                            if data["emeralds"] >= skin.price:
                                skin.unlocked = True
                                data["skins"][skin.name][3] = True
                                data["skin"] = skin.name
                                data["emeralds"] -= skin.price
                                with open(PATH / "data.json", 'w') as file:
                                    json.dump(data, file, indent=4)
                    
        game_utils.background()
        game_utils.bg_overlay()

        for skin in game_skins:
            pygame.draw.rect(window, (130, 130, 130), (skin.x, skin.y, skin.size, skin.size))
            pygame.draw.rect(window, (0, 0, 0), (skin.x, skin.y, skin.size, skin.size), 1)

            skin_image = pygame.transform.scale(pygame.image.load(PATH / "skins" / f"{skin.name}.png"), (skin.size, skin.size))

            window.blit(skin_image, (skin.x, skin.y))

            if not skin.unlocked:
                game_utils.trans_surface(skin.size, skin.size, (0, 0, 0, 50), skin.x, skin.y)
                emerald = pygame.transform.scale(pygame.image.load(PATH / "drawable" / "emerald.png"), (32, 32))
                text_width = minecraft_font_small.size(str(skin.price))[0]
                window.blit(emerald, (skin.x + (skin.size-text_width)//2-17, skin.y+24))
                window.blit(minecraft_font_small.render(str(skin.price), True, (255, 255, 255)), (skin.x + (skin.size-text_width)//2 + 11, skin.y+30))

            if skin.name == data["skin"]:
                pygame.draw.rect(window, (0, 255, 0), (skin.x, skin.y, skin.size, skin.size), 2)

            if skin.hover(mouse[0], mouse[1]):
                pygame.draw.rect(window, (255, 255, 255), (skin.x, skin.y, skin.size, skin.size), 3)
                if skin.unlocked:
                    game_utils.button(PATH / "drawable" / "select.png", skin.size, skin.size, skin.x, skin.y)

        #back_button
        game_utils.button(PATH / "drawable" / "unselect.png", 40, 40, 15, 565)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            game_utils.trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        pygame.display.flip()

def game(level, player_l = False):
    global code_lang, code_runned, level_finished, grades
    global def_code_python, def_code_c, def_code_cpp
    messages = []
    restart_code = False
    one_v_one = False
    one_v_one_code = [False, False]
    one_v_one_time = [0, 0]
    player = 1
    code_input.i = 0
    code_input.cursor_pos = 0
    text_path = levels[f"level{level}"][0][f"input_text_{languages[code_lang]}"] if not player_l else player_levels[f"level{level}"][0][f"input_text_{languages[code_lang]}"]
    code_input.set_text(text_path)
    if level >= 10:
        xy = levels[f"level{level}"][0]["steve_xy"] if not player_l else player_levels[f"level{level}"][0]["steve_xy"]
        stevexy[0] = xy[0]*85
        stevexy[1] = (6-xy[1])*85
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            game_utils.play_next_track()
        window.fill((30, 30, 30))

        mouse = pygame.mouse.get_pos()
        events = pygame.event.get()

        lang_text_x = (645-minecraft_font_smaller.size(languages[code_lang])[0])//2+595
        lang_text_length = minecraft_font_smaller.size(languages[code_lang])[0]

        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 10 <= mouse[0] <= 30 and 597 <= mouse[1] <= 617:
                    if fx_on:
                        click_sound.play()
                    if player_l:
                        your_levels_menu()
                    else:
                        level_menu()
                elif 30 <= mouse[0] <= 50 and 598 <= mouse[1] <= 618:
                    code_runned = True
                elif 595 <= mouse[0] <= 615 and 598 <= mouse[1] <= 618:
                    restart_code = True
                elif 566 <= mouse[0] <= 582 and 598 <= mouse[1] <= 618:
                    if not player_l and level_finished and level < 24:
                        one_v_one = False
                        player = 1
                        code_input.i = 0
                        code_input.cursor_pos = 0
                        if level > levels["last_finished_level"]:
                            levels["last_finished_level"] = level
                        level += 1
                        game_levels[level-1].unlocked = True
                        with open(PATH / "levels" / "levels.json", 'w') as file:
                            json.dump(levels, file, indent=4)
                        code_input.clear_text()
                        code_input.clear_text()
                        code_input.set_text(levels[f"level{level}"][0][f"input_text_{languages[code_lang]}"])
                        time.sleep(0.25)
                        messages = []
                        code_input.clear_text()
                        if level >= 10:
                            xy = levels[f"level{level}"][0]["steve_xy"]
                            stevexy[0] = xy[0]*85
                            stevexy[1] = (6-xy[1])*85
                        level_finished = False
                        restart()
                        time.sleep(0.01)
                        restart()
                elif 630 <= mouse[0] <= 654 and 600 <= mouse[1] <= 615 and not one_v_one and (level >= 10 or player_l):
                    one_v_one = True
                    code_input_2 = Textbox(595, 0, 645, 620, PATH / "Minecraft.ttf")
                    text_path = levels[f"level{level}"][0][f"input_text_{languages[code_lang]}"] if not player_l else player_levels[f"level{level}"][0][f"input_text_{languages[code_lang]}"]
                    code_input_2.set_text(text_path)
                elif one_v_one and 630 <= mouse[0] <= 640 and 600 <= mouse[1] <= 615 and (level >= 10 or player_l):
                    player = 1
                elif one_v_one and 650 <= mouse[0] <= 660 and 600 <= mouse[1] <= 615 and (level >= 10 or player_l):
                    player = 2
                elif one_v_one and 668 <= mouse[0] <= 684 and 598 <= mouse[1] <= 614:
                    player = 1
                    one_v_one = False
                elif lang_text_x <= mouse[0] <= lang_text_x+lang_text_length and 600 <= mouse[1] <= 615:
                    code_lang = (code_lang + 1) % len(languages)
                    restart()
                elif not player_l and 56 <= mouse[0] <= 67 and 597 <= mouse[1] <= 617:
                    print("hint 1")
                elif not player_l and 70 <= mouse[0] <= 84 and 597 <= mouse[1] <= 617:
                    print("hint 2")
                elif not game_levels[level].text_closed:
                    if 410 <= mouse[0] <= 452 and 515 <= mouse[1] <= 539 and game_levels[level].text_page < levels[f"level{level}"][0]["pages"]-1:
                        game_levels[level].text_page += 1
                    if 120 <= mouse[0] <= 162 and 515 <= mouse[1] <= 539 and game_levels[level].text_page > 0:
                        game_levels[level].text_page -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_LMETA):
                    if not player_l:
                        game_levels[level].text_closed = not game_levels[level].text_closed
                if event.key == pygame.K_k and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_LMETA):
                    messages = []

            if player == 1 and not one_v_one_code[0]:
                code_input.handle_events(event) 
            elif player == 2 and not one_v_one_code[1]:
                code_input_2.handle_events(event)

        if one_v_one:
            if player == 1:
                code_input.draw(window)
            elif player == 2:
                code_input_2.draw(window)
        else:
            code_input.draw(window)

        def restart():
            if player == 1:
                code_input.clear_text()
                text_path = levels[f"level{level}"][0][f"input_text_{languages[code_lang]}"] if not player_l else player_levels[f"level{level}"][0][f"input_text_{languages[code_lang]}"]
                code_input.set_text(text_path)
                code_input.i = 0
                code_input.cursor_pos = 0
            elif player == 2:
                code_input_2.clear_text()
                text_path = levels[f"level{level}"][0][f"input_text_{languages[code_lang]}"] if not player_l else player_levels[f"level{level}"][0][f"input_text_{languages[code_lang]}"]
                code_input_2.set_text(text_path)
                code_input_2.i = 0
                code_input_2.cursor_pos = 0
            if player_l or level >= 10:
                xy = levels[f"level{level}"][0]["steve_xy"] if not player_l else player_levels[f"level{level}"][0]["steve_xy"]
                stevexy[0] = xy[0]*85
                stevexy[1] = (6-xy[1])*85

        pygame.draw.rect(window, (205, 205, 205), (0, 0, 595, 595))

        pygame.draw.rect(window, (0, 118, 197), (0, 595, 1240, 25))

        #language
        window.blit(minecraft_font_smaller.render(languages[code_lang], True, (255, 255, 255)), (lang_text_x, 600))

        if lang_text_x <= mouse[0] <= lang_text_x+lang_text_length and 600 <= mouse[1] <= 615:
            game_utils.description("Change language")
            game_utils.trans_surface(lang_text_length, 15, (170, 170, 170, 120), lang_text_x, 600)

        if 10 <= mouse[0] <= 30 and 597 <= mouse[1] <= 617:
            game_utils.description("Exit")
            game_utils.trans_surface(20, 20, (170, 170, 170, 120), 12, 597)
        
        #back_button
        game_utils.button(PATH / "drawable" / "close.png", 22, 22, 10, 596)

        if 30 <= mouse[0] <= 50 and 598 <= mouse[1] <= 618:
            game_utils.description("Run")
            game_utils.trans_surface(20, 20, (170, 170, 170, 120), 34, 598)

        #run_button
        game_utils.button(PATH / "drawable" / "select.png", 28, 28, 30, 593)

        if 595 <= mouse[0] <= 615 and 598 <= mouse[1] <= 618:
            game_utils.description("Restart")
            game_utils.trans_surface(20, 20, (170, 170, 170, 120), 599, 598)

        #restart_button
        game_utils.button(PATH / "drawable" / "reject.png", 26, 26, 595, 595)

        if not player_l:
            #hint1_button
            hint_x = 56
            game_utils.button(PATH / "drawable" / "torch1.png", 31, 31, hint_x-11, 586)
            
            if hint_x <= mouse[0] <= hint_x+11 and 597 <= mouse[1] <= 617:
                game_utils.description("Hint 1. (5 emeralds)")
                game_utils.trans_surface(11, 20, (170, 170, 170, 120), hint_x, 597)
            
            #hint2_button
            game_utils.button(PATH / "drawable" / "torch2.png", 31, 31, hint_x+4, 586)

            if hint_x+14 <= mouse[0] <= hint_x+28 and 597 <= mouse[1] <= 617:
                game_utils.description("Hint 2. (15 emeralds)")
                game_utils.trans_surface(14, 20, (170, 170, 170, 120), hint_x+14, 597)

        #next_button
        if not player_l and level_finished and level < 24:
            if 566 <= mouse[0] <= 582 and 598 <= mouse[1] <= 618:
                game_utils.description("Next level")
                game_utils.trans_surface(22, 20, (170, 170, 170, 120), 566, 598)
            game_utils.button(PATH / "drawable" / "accept.png", 29, 29, 562, 592)

        #1v1 button
        if level >= 10 or player_l:
            if not one_v_one:
                window.blit(minecraft_font_smaller.render("1v1", True, (255, 255, 255)), (630, 600))
                if 630 <= mouse[0] <= 654 and 600 <= mouse[1] <= 615:
                    game_utils.description("1 vs 1 with a friend")
                    game_utils.trans_surface(24, 15, (170, 170, 170, 120), 630, 600)
            else:
                window.blit(minecraft_font_smaller.render("1.", True, (255, 255, 255)), (630, 600))
                if 630 <= mouse[0] <= 640 and 600 <= mouse[1] <= 615:
                    game_utils.description("1st player")
                    game_utils.trans_surface(10, 15, (170, 170, 170, 120), 630, 600)
                window.blit(minecraft_font_smaller.render("2.", True, (255, 255, 255)), (650, 600))
                if 650 <= mouse[0] <= 660 and 600 <= mouse[1] <= 615:
                    game_utils.description("2nd player")
                    game_utils.trans_surface(10, 15, (170, 170, 170, 120), 650, 600)

                if 668 <= mouse[0] <= 684 and 598 <= mouse[1] <= 614:
                    game_utils.description("Exit 1v1")
                    game_utils.trans_surface(16, 16, (170, 170, 170, 120), 668, 598)

                #exit_1v1_button
                game_utils.button(PATH / "drawable" / "close.png", 16, 16, 668, 598)

        #blocks
        i = 0
        j = 0
        while i < 595:
            while j < 595:
                level_key = f"level{level}"
                block_path = PATH / "blocks" / f"{levels[level_key][0]["blocks"][j//85][i//85]}" if not player_l else PATH / "blocks" / f"{player_levels[level_key][0]["blocks"][j//85][i//85]}"
                block = pygame.image.load(block_path)
                block = pygame.transform.scale(block, (85, 85))
         
                window.blit(block, (i, j))
                pygame.draw.rect(window, (0, 0, 0), (i, j, 85, 85), 1)
                j += 85
            j = 0
            i += 85

        #book
        if not player_l and not game_levels[level].text_closed:
            book = pygame.image.load(PATH / "drawable" / "book2.png")
            book = pygame.transform.scale(book, (800, 800))

            window.blit(book, (6, 12))

            game_utils.render_text(115, 63, levels[f"level{level}"][0][f"text_{languages[code_lang]}"][game_levels[level].text_page], 28.8)

            if game_levels[level].text_page < levels[f"level{level}"][0]["pages"]-1:
                game_utils.button(PATH / "drawable" / "page_forward.png", 42, 24, 410, 515)

                if 410 <= mouse[0] <= 452 and 515 <= mouse[1] <= 539:
                    game_utils.trans_surface(36, 19, (170, 170, 170, 120), 415, 519)
            
            if game_levels[level].text_page > 0:
                game_utils.button(PATH / "drawable" / "page_backward.png", 42, 24, 120, 515)

                if 120 <= mouse[0] <= 162 and 515 <= mouse[1] <= 539:
                    game_utils.trans_surface(36, 19, (170, 170, 170, 120), 125, 519)

        if level >= 10 or player_l:
            steve = pygame.image.load(PATH / "skins" / f"{data['skin']}.png")
            steve = pygame.transform.scale(steve, (85, 85))
        
            window.blit(steve, (stevexy[0], stevexy[1]))
            pygame.draw.rect(window, (0, 0, 0), (stevexy[0], stevexy[1], 85, 85), 1)

        if restart_code:
            restart()
            restart_code = False

        #code
        if code_runned:
            code = code_input.get_text().split("\n")
            cbd = []
            code_len = len(code)
            i = 0
            while i < code_len:
                cbdd = cbd_maker(code[i])     
                if cbdd:           
                    cbd.append(cbdd)
                i += 1
            if not player_l and level < 10:
                if code_lang == 0:
                    executed_code = exec_code(code_input.get_text())
                elif code_lang == 1:
                    executed_code = exec_c_code(code_input.get_text(), "C")
                elif code_lang == 2:
                    executed_code = exec_c_code(code_input.get_text(), "C++")
                if executed_code["error"] != None:
                    err = executed_code["error"]
                    if code_lang != 0:
                        try:
                            err = err.split("\n")[0].split(":", 1)[1].split(" ", 1)[1]
                        except Exception:
                            err = "?"
                    messages.append("Error: " + err)
            else:
                input_code = code_input.get_text() if player == 1 else code_input_2.get_text()
                if code_lang == 0:
                    input_code = '\n'.join(input_code.split("\n")[14:])
                elif code_lang == 1:
                    input_code = '\n'.join(input_code.split("\n")[19:])
                elif code_lang == 2:
                    input_code = '\n'.join(input_code.split("\n")[26:])
                start_time = time.time()
                if code_lang == 0:
                    executed_code = exec_code(def_code_python + input_code)
                elif code_lang == 1:
                    executed_code = exec_c_code(def_code_c + input_code, "C")
                elif code_lang == 2:
                    executed_code = exec_c_code(def_code_cpp + input_code, "C++")
                if executed_code["error"] != None:
                    messages.append("Error in code!")
                end_time = time.time()
                one_v_one_time[player-1] = end_time - start_time

            if code_lang == 0:
                messages += executed_code["out"]
                variables = executed_code["vars"]
                del variables["__builtins__"]
            elif code_lang == 1 or code_lang == 2:
                for el in executed_code["out"]:
                    if el.split(" ")[0] not in ["right", "left", "up", "down"]:
                        messages += [el]

            #correct solution
            solution = False
            if not player_l and level == 9:
                solution = True
            if not player_l and level < 10 and levels[f"level{level}"][0][f"solution_{languages[code_lang]}"][0] == cbd:
                solution = True
            
            if not player_l and level == 4:
                if code_lang == 0:
                    l = []
                    ll = ["<class 'bool'>", "<class 'float'>", "<class 'int'>", "<class 'str'>"]
                    for el in list(variables.keys()):
                        l.append(str(type(variables[el])))
                    l.sort()
                    if l == ll:
                        solution = True
                elif code_lang == 1:
                    c = 0
                    for el in cbd:
                        if el[0] == "int" and el[2] == "=":
                            c += 1
                        elif el[0] == "float" and el[2] == "=" and el[4] == ".":
                            c += 1
                        elif el[0] == "double" and el[2] == "=" and el[4] == ".":
                            c += 1
                        elif el[0] == "char" and el[2] == "[" and el[3] == "]" and el[4] == "=":
                            c += 1
                        elif el[0] == "char" and el[2] == "=":
                            c += 1
                    solution = c == 5
                    pass
                elif code_lang == 2:
                    c = 0
                    for el in cbd:
                        if el[0] == "int" and el[2] == "=":
                            c += 1
                        elif el[0] == "float" and el[2] == "=" and el[4] == ".":
                            c += 1
                        elif el[0] == "double" and el[2] == "=" and el[4] == ".":
                            c += 1
                        elif el[0] == "string" and el[2] == "=":
                            c += 1
                        elif el[0] == "bool" and el[2] == "=":
                            c += 1
                        elif el[0] == "char" and el[2] == "=":
                            c += 1
                    solution = c == 6
                    pass

            if player_l or level >= 10:
                xy = levels[f"level{level}"][0]["steve_xy"] if not player_l else player_levels[f"level{level}"][0]["steve_xy"]
                stevexy[0] = xy[0]*85
                stevexy[1] = (6-xy[1])*85
                if not player_l and level >= 14 and level < 17:
                    plate_activated = False
                try:
                    if code_lang == 0:
                        coms = variables["coms"]
                    elif code_lang == 1 or code_lang == 2:
                        coms = []
                        for el in executed_code["out"]:
                            el_splited = el.split(" ")
                            if el_splited[0] in ["right", "left", "up", "down"]:
                                coms.append(el.split(" "))
                except Exception:
                    coms = []
                
                def check():
                    nonlocal plate_activated, player_l
                    block = levels[f"level{level}"][0]["blocks"][stevexy[1]//85][stevexy[0]//85] if not player_l else player_levels[f"level{level}"][0]["blocks"][stevexy[1]//85][stevexy[0]//85]
                    if stevexy[1]//85 < 0 or stevexy[0]//85 < 0 or stevexy[1]//85 > 6 or stevexy[0]//85 > 6:
                        messages.append("You can only go on grass!")
                        restart()
                    elif block == "oak_trapdoor.png":
                        if level >= 14 and level < 17 and not plate_activated:
                            messages.append("Door is not unlocked!")
                            restart()
                        return True
                    elif block == "pressure_plate.png":
                        plate_activated = True
                    elif player_l:
                        if block != player_levels[f"level{level}"][0]["path_block"]:
                            messages.append("You can't go on this block!")
                            restart()
                            return False
                    elif level < 17 and block != "grass_top.png":
                        messages.append("You can only go on grass!")
                        restart()
                        return False
                    elif level >= 17 and level < 21 and block != "bedrock.png":
                        messages.append("You can only go on bedrock!")
                        restart()
                        return False
                    elif level >= 21 and block != "purpur_block.png":
                        messages.append("You can only go on purpur blocks!")
                        restart()
                        return False
                    return False      
                for com in coms:
                    if com[0] == "right":
                        for _ in range(int(com[1])):
                            stevexy[0] += 85
                            game_utils.move(-85, 0, level, player_l)
                            check()
                    elif com[0] == "left":
                        for _ in range(int(com[1])):
                            stevexy[0] -= 85
                            game_utils.move(85, 0, level, player_l)
                            check()
                    elif com[0] == "up":
                        for _ in range(int(com[1])):
                            stevexy[1] -= 85
                            game_utils.move(0, 85, level, player_l)
                            check()
                    elif com[0] == "down":
                        for _ in range(int(com[1])):
                            stevexy[1] += 85
                            game_utils.move(0, -85, level, player_l)
                            check()

                if check():
                    if one_v_one:
                        one_v_one_code[player-1] = True
                        messages.append(f"Player {player}. finished the level!")
                        if not (one_v_one_code[0] and one_v_one_code[1]):
                            xy = levels[f"level{level}"][0]["steve_xy"] if not player_l else player_levels[f"level{level}"][0]["steve_xy"]
                            stevexy[0] = xy[0]*85
                            stevexy[1] = (6-xy[1])*85
                    else:
                        if player_l:
                            solution = True
                        elif level >= 14 and level < 17 and plate_activated:
                            solution = True
                        elif level >= 10 and level < 14 or level >= 17:
                            solution = True
                else:
                    messages.append("Wrong solution! Try again.")
                    restart()
            
            if one_v_one:
                if one_v_one_code[0] and one_v_one_code[1]:
                    grades = grade_code(code_input.get_text(), code_input_2.get_text(), one_v_one_time)
                    messages.append(f"Player 1. scored: {grades[0]}/3")
                    messages.append(f"Player 2. scored: {grades[1]}/3")
                    won = 0
                    if grades[0] > grades[1]:
                        won = 1
                    elif grades[1] > grades[0]:
                        won = 2
                    messages.append(f"Player {won}. won.")

            if solution:
                if level >= 10:
                    if fx_on:
                        sound = pygame.mixer.Sound(PATH / "sounds" / "trapdoor.mp3")
                        sound.play()
                                        
                messages.append("Great job!")
                emeralds = 5
                if level >= 10:
                    emeralds = 10
                if level >= 14:
                    emeralds = 15
                if not player_l:
                    messages.append(f"+{emeralds} Emeralds")
                    data["emeralds"] += emeralds
                level_finished = True   
                with open(PATH / "data.json", 'w') as file:
                    json.dump(data, file, indent=4)

            code_runned = False

        game_utils.minecraft_cmd(messages)

        cursor_pos = minecraft_font_smaller.render(f"Ln {code_input.i + 1}, Col {code_input.cursor_pos + 1}", True, (255, 255, 255))
        window.blit(cursor_pos, (1240 - cursor_pos.get_width() - 15, 600))
        
        pygame.display.update()
        clock.tick(60)

menu()