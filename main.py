import pygame, random, json, time
from pygametextboxinput import *
from code_runner import *
from pathlib import Path
from def_codes import *

PATH = Path.cwd()

json_levels = open(PATH / "levels" / "levels.json")
levels = json.load(json_levels)

json_options = open(PATH / "options.json")
options = json.load(json_options)

json_data = open(PATH / "data.json")
data = json.load(json_data)

game_levels = []
game_skins = []

stevexy = [0, 510]

def move(grass_x, grass_y, level):
    steve = pygame.image.load(PATH / "skins" / f"{data["skin"]}.png")
    steve = pygame.transform.scale(steve, (85, 85))

    window.blit(steve, (stevexy[0], stevexy[1]))
    pygame.draw.rect(window, (0, 0, 0), (stevexy[0], stevexy[1], 85, 85), 1)

    window.blit(pygame.transform.scale(pygame.image.load(PATH / "blocks" / f"{levels[f"level{level}"][0]["blocks"][(stevexy[1]+grass_y)//85][(stevexy[0]+grass_x)//85]}"), (85, 85)), (stevexy[0]+grass_x, stevexy[1]+grass_y))
    pygame.draw.rect(window, (0, 0, 0), (stevexy[0]+grass_x, stevexy[1]+grass_y, 85, 85), 1)
    pygame.display.update()
    clock.tick(60)
    time.sleep(0.1)

class Level:
    def __init__(self, x, y, level, size, text_closed):
        self.x = x
        self.y = y
        self.level = level
        self.size = size
        self.unlocked = level <= levels["last_finished_level"]+1
        self.text_closed = text_closed
        self.text_page = 0
    def get_level(self):
        return self.level
    def hover(self, x2, y2):
        return self.x <= x2 <= self.x + self.size and self.y <= y2 <= self.y + self.size

for p in levels["level_p"]:
    game_levels.append(Level(p[0], p[1], p[2], p[3], p[4]))

class Skin:
    def __init__(self, name, x, y, price, unlocked):
        self.name = name
        self.x = x
        self.y = y
        self.price = price
        self.size = 80
        self.unlocked = unlocked
    def get_level(self):
        return self.level
    def hover(self, x2, y2):
        return self.x <= x2 <= self.x + self.size and self.y <= y2 <= self.y + self.size

for k in data["skins"]:
    game_skins.append(Skin(k, data["skins"][k][0], data["skins"][k][1], data["skins"][k][2], data["skins"][k][3]))

pygame.init()

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
random.shuffle(playlist)
pygame.mixer.music.load(playlist[current_song_index])
pygame.mixer.music.play()

music_on = options["music_on"]
fx_on = options["fx_on"]
if not music_on:
    pygame.mixer.music.pause()

def play_next_track():
    global current_song_index
    current_song_index = (current_song_index + 1) % len(playlist)
    pygame.mixer.music.load(playlist[current_song_index])
    pygame.mixer.music.play()

window = pygame.display.set_mode((1240, 620))
pygame.display.set_caption("Code_Craft")
pygame.display.set_icon(pygame.image.load(PATH / "drawable" / "crafting_table.png"))
clock = pygame.time.Clock()

def button(path, width, height, x, y):
    b_button = pygame.transform.scale(pygame.image.load(path), (width, height))
    window.blit(b_button, (x, y))

def menu_button(x, y, text_x, text, width, height, mouse):
    pygame.draw.rect(window, (130, 130, 130), (x, y, width, height))
    pygame.draw.rect(window, (0, 0, 0), (x, y, width, height), 1)

    window.blit(minecraft_font_small.render(text, True, (255, 255, 255)), (text_x, y+10))

    if x <= mouse[0] <= x+width and y <= mouse[1] <= y+height:
        pygame.draw.rect(window, (255, 255, 255), (x, y, width, height), 3)

def trans_surface(width, height, color, x, y):
    transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    transparent_surface.fill(color)
    window.blit(transparent_surface, (x, y))

def background():
    background = pygame.image.load(PATH / "drawable" / "background.png")
    background = pygame.transform.scale(background, (1240, 620))
    window.blit(background, (0, 0))

def bg_overlay():
    background_overlay = pygame.Surface((1240, 620), pygame.SRCALPHA)
    background_overlay.fill((0, 0, 0, 50))
    window.blit(background_overlay, (0, 0))

def minecraft_cmd(l):
    ll = len(l)
    y = 590 - ll*30
    index = 0
    while index < ll:
        color = (255, 255, 255)
        trans_surface(595, 30, (0, 0, 0, 100), 0, y)
        if l[index][0:7] == "Error: ":
            color = (255, 85, 85)
        if l[index] == "Player 1. won." or l[index] == "Player 2. won.":
            color = (0, 255, 0)
        window.blit(minecraft_font_small.render(l[index], True, color), (10, y+4))
        index += 1
        y += 30

code_input = Textbox(595, 0, 645, 620, PATH / "Minecraft.ttf")
pygame.key.set_repeat(200, 25)

languages = ["Python", "C"]
code_lang = 0

code_runned = False
level_finished = False
grades = [0, 0]

minecraft_font_big = pygame.font.Font(PATH / "Minecraft.ttf", 75)
minecraft_font_small = pygame.font.Font(PATH / "Minecraft.ttf", 25)
minecraft_font_smaller = pygame.font.Font(PATH / "Minecraft.ttf", 15)
minecraft_font_book = pygame.font.Font(PATH / "Minecraft.ttf", 20)

def description(string):
    length = 150
    x = 223
    if len(string) > 18:
        length = 300
        x = 147
    pygame.draw.rect(window, (194, 194, 194), (x, 598, length, 19))
    window.blit(minecraft_font_smaller.render(string, True, (255, 255, 255)), ((595-minecraft_font_smaller.size(string)[0])//2, 601))
    pygame.draw.rect(window, (0, 0, 0), (x, 598, length, 19), 1)

def menu():
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            play_next_track()

        mouse = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 420 <= mouse[0] <= 820 and 250 <= mouse[1] <= 290:
                    if levels["last_finished_level"] < 24:
                        game(levels["last_finished_level"]+1)
                elif 420 <= mouse[0] <= 820 and 300 <= mouse[1] <= 340:
                    level_menu()
                elif 420 <= mouse[0] <= 820 and 350 <= mouse[1] <= 390:
                    tutorial()
                elif 420 <= mouse[0] <= 615 and 420 <= mouse[1] <= 460:
                    options_win()
                elif 625 <= mouse[0] <= 820 and 420 <= mouse[1] <= 460:
                    exit()
        
        background()

        big_title = pygame.transform.scale(pygame.image.load(PATH / "drawable" / "Code_Craft.png"), (491, 127))
        window.blit(big_title, (374, 60))

        emerald = pygame.transform.scale(pygame.image.load(PATH / "drawable" / "emerald.png"), (32, 32))
        window.blit(emerald, (1210, 0))
        window.blit(minecraft_font_book.render(str(data["emeralds"]), True, (255, 255, 255)), (1213-minecraft_font_book.size(str(data["emeralds"]))[0], 8.8))

        menu_button(420, 250, 594, "Play", 400, 40, mouse)

        menu_button(420, 300, 580, "Levels", 400, 40, mouse)

        menu_button(420, 350, 573, "Tutorial", 400, 40, mouse)

        menu_button(420, 420, 464, "Options...", 195, 40, mouse)

        menu_button(625, 420, 659, "Quit Game", 195, 40, mouse)

        pygame.display.flip()     

def level_menu():
    for lvl in game_levels:
        lvl.unlocked = lvl.level <= levels["last_finished_level"]+1
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            play_next_track()
        mouse = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for lvl in game_levels:
                    if lvl.hover(mouse[0], mouse[1]) and lvl.unlocked:
                        game(lvl.level)
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    menu()
        
        background()
        bg_overlay()

        #back_button
        button(PATH / "drawable" / "unselect.png", 40, 40, 15, 565)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        #level_button
        for lvl in game_levels:
            if lvl.x != -1 and lvl.y != -1:
                pygame.draw.rect(window, (130, 130, 130), (lvl.x, lvl.y, lvl.size, lvl.size))
                pygame.draw.rect(window, (0, 0, 0), (lvl.x, lvl.y, lvl.size, lvl.size), 1)

                text_width = minecraft_font_small.size(str(lvl.level))[0]

                window.blit(minecraft_font_small.render(str(lvl.level), True, (255, 255, 255)), (lvl.x + (lvl.size-text_width)//2 + 1, lvl.y+30))

                if not lvl.unlocked:
                    trans_surface(lvl.size, lvl.size, (0, 0, 0, 50), lvl.x, lvl.y)

                if lvl.hover(mouse[0], mouse[1]) and lvl.unlocked:
                    pygame.draw.rect(window, (255, 255, 255), (lvl.x, lvl.y, lvl.size, lvl.size), 3)
                    button(PATH / "drawable" / "select.png", lvl.size, lvl.size, lvl.x, lvl.y)

        pygame.display.flip()

def tutorial():
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            play_next_track()
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    menu()
                    
        background()
        bg_overlay()

        #back_button
        button(PATH / "drawable" / "unselect.png", 40, 40, 15, 565)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        pygame.display.flip()

def options_win():
    global music_on, fx_on
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            play_next_track()
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    menu()
                if 420 <= mouse[0] <= 820 and 80 <= mouse[1] <= 120:
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
                    
        background()
        bg_overlay()

        menu_button(420, 80, 587, "Skins", 400, 40, mouse)

        music_state = "On" if music_on else "Off"
        menu_button(420, 130, 420+(400-minecraft_font_small.size(f"Audio: {music_state}")[0])//2, f"Audio: {music_state}", 400, 40, mouse)

        fx_state = "On" if fx_on else "Off"
        menu_button(420, 180, 444+(356-minecraft_font_small.size(f"FX: {fx_state}")[0])//2, f"FX: {fx_state}", 400, 40, mouse)

        menu_button(420, 230, 452, "Clear Progress (Exit's app)", 400, 40, mouse)

        #back_button
        button(PATH / "drawable" / "unselect.png", 40, 40, 15, 565)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        pygame.display.flip()

def skins():
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            play_next_track()
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
                    options_win()
                for skin in game_skins:
                    if skin.hover(mouse[0], mouse[1]):
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
                    
        background()
        bg_overlay()

        for skin in game_skins:
            pygame.draw.rect(window, (130, 130, 130), (skin.x, skin.y, skin.size, skin.size))
            pygame.draw.rect(window, (0, 0, 0), (skin.x, skin.y, skin.size, skin.size), 1)

            skin_image = pygame.transform.scale(pygame.image.load(PATH / "skins" / f"{skin.name}.png"), (skin.size, skin.size))

            window.blit(skin_image, (skin.x, skin.y))

            if not skin.unlocked:
                trans_surface(skin.size, skin.size, (0, 0, 0, 50), skin.x, skin.y)
                emerald = pygame.transform.scale(pygame.image.load(PATH / "drawable" / "emerald.png"), (32, 32))
                text_width = minecraft_font_small.size(str(skin.price))[0]
                window.blit(emerald, (skin.x + (skin.size-text_width)//2-17, skin.y+24))
                window.blit(minecraft_font_small.render(str(skin.price), True, (255, 255, 255)), (skin.x + (skin.size-text_width)//2 + 11, skin.y+30))

            if skin.name == data["skin"]:
                pygame.draw.rect(window, (0, 255, 0), (skin.x, skin.y, skin.size, skin.size), 2)

            if skin.hover(mouse[0], mouse[1]):
                pygame.draw.rect(window, (255, 255, 255), (skin.x, skin.y, skin.size, skin.size), 3)
                if skin.unlocked:
                    button(PATH / "drawable" / "select.png", skin.size, skin.size, skin.x, skin.y)

        #back_button
        button(PATH / "drawable" / "unselect.png", 40, 40, 15, 565)

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            trans_surface(30, 30, (170, 170, 170, 120), 14, 571)

        pygame.display.flip()

def game(level):
    global code_lang, code_runned, level_finished, grades
    global def_code_python, def_code_c
    messages = []
    restart_code = False
    one_v_one = False
    one_v_one_code = [False, False]
    one_v_one_time = [0, 0]
    player = 1
    code_input.i = 0
    code_input.cursor_pos = 0
    code_input.set_text(levels[f"level{level}"][0][f"input_text_{languages[code_lang]}"])
    if level >= 10:
        stevexy[0] = levels[f"level{level}"][0]["steve_xy"][0]*85
        stevexy[1] = (6-levels[f"level{level}"][0]["steve_xy"][1])*85
        def_code_python += f"\nmob = Mob({levels[f"level{level}"][0]["steve_xy"][0]}, {levels[f"level{level}"][0]["steve_xy"][1]})\n"         
        def_code_c += f"\n    struct Mob mob = {{{levels[f"level{level}"][0]["steve_xy"][0]}, {levels[f"level{level}"][0]["steve_xy"][1]}}};"
    while True:
        if not pygame.mixer.music.get_busy() and music_on:
            play_next_track()
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
                    menu()
                elif 30 <= mouse[0] <= 50 and 598 <= mouse[1] <= 618:
                    code_runned = True
                elif 595 <= mouse[0] <= 615 and 598 <= mouse[1] <= 618:
                    restart_code = True
                elif 566 <= mouse[0] <= 582 and 598 <= mouse[1] <= 618:
                    if level_finished and level < 24:
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
                            stevexy[0] = levels[f"level{level}"][0]["steve_xy"][0]*85
                            stevexy[1] = (6-levels[f"level{level}"][0]["steve_xy"][1])*85
                        level_finished = False
                        restart()
                        time.sleep(0.01)
                        restart()
                elif 630 <= mouse[0] <= 654 and 600 <= mouse[1] <= 615 and not one_v_one and level >= 10:
                    one_v_one = True
                    code_input_2 = Textbox(595, 0, 645, 620, PATH / "Minecraft.ttf")
                    code_input_2.set_text(levels[f"level{level}"][0][f"input_text_{languages[code_lang]}"])
                if 630 <= mouse[0] <= 640 and 600 <= mouse[1] <= 615 and level >= 10:
                    player = 1
                if 650 <= mouse[0] <= 660 and 600 <= mouse[1] <= 615 and level >= 10:
                    player = 2
                elif lang_text_x <= mouse[0] <= lang_text_x+lang_text_length and 600 <= mouse[1] <= 615:
                    code_lang = (code_lang + 1) % len(languages)
                    restart()
                elif not game_levels[level].text_closed:
                    if 375 <= mouse[0] <= 417 and 455 <= mouse[1] <= 479 and game_levels[level].text_page < levels[f"level{level}"][0]["pages"]-1:
                        game_levels[level].text_page += 1
                    if 165 <= mouse[0] <= 207 and 455 <= mouse[1] <= 479 and game_levels[level].text_page > 0:
                        game_levels[level].text_page -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_LMETA):
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
                code_input.set_text(levels[f"level{level}"][0][f"input_text_{languages[code_lang]}"])
                code_input.i = 0
                code_input.cursor_pos = 0
            elif player == 2:
                code_input_2.clear_text()
                code_input_2.set_text(levels[f"level{level}"][0][f"input_text_{languages[code_lang]}"])
                code_input_2.i = 0
                code_input_2.cursor_pos = 0
            if level >= 10:
                stevexy[0] = levels[f"level{level}"][0]["steve_xy"][0]*85
                stevexy[1] = (6-levels[f"level{level}"][0]["steve_xy"][1])*85

        pygame.draw.rect(window, (205, 205, 205), (0, 0, 595, 595))

        pygame.draw.rect(window, (0, 118, 197), (0, 595, 1240, 25))

        window.blit(minecraft_font_smaller.render(languages[code_lang], True, (255, 255, 255)), (lang_text_x, 600))

        if lang_text_x <= mouse[0] <= lang_text_x+lang_text_length and 600 <= mouse[1] <= 615:
            trans_surface(lang_text_length, 15, (170, 170, 170, 120), lang_text_x, 600)

        if 10 <= mouse[0] <= 30 and 597 <= mouse[1] <= 617:
            description("Exit")
            trans_surface(20, 20, (170, 170, 170, 120), 12, 597)
        
        #back_button
        button(PATH / "drawable" / "close.png", 22, 22, 10, 596)

        if 30 <= mouse[0] <= 50 and 598 <= mouse[1] <= 618:
            description("Run")
            trans_surface(20, 20, (170, 170, 170, 120), 34, 598)

        #run_button
        button(PATH / "drawable" / "select.png", 28, 28, 30, 593)

        if 595 <= mouse[0] <= 615 and 598 <= mouse[1] <= 618:
            description("Restart")
            trans_surface(20, 20, (170, 170, 170, 120), 599, 598)

        #restart_button
        button(PATH / "drawable" / "reject.png", 26, 26, 595, 595)

        #next_button and optimization warning
        if level_finished and level < 24:
            if 566 <= mouse[0] <= 582 and 598 <= mouse[1] <= 618:
                description("Next level")
                trans_surface(22, 20, (170, 170, 170, 120), 566, 598)
            button(PATH / "drawable" / "accept.png", 29, 29, 562, 592)

            if grades[0] > 0:
                if 630 <= mouse[0] <= 649 and 598 <= mouse[1] <= 617:
                    description("Your code can be more optimized!")
                    trans_surface(20, 20, (170, 170, 170, 120), 629, 597)
                button(PATH / "drawable" / "report_button.png", 19, 19, 630, 598)

        #1v1 button
        if level >= 10:
            if not one_v_one:
                window.blit(minecraft_font_smaller.render("1v1", True, (255, 255, 255)), (630, 600))
                if 630 <= mouse[0] <= 654 and 600 <= mouse[1] <= 615:
                    description("1 vs 1 with a friend")
                    trans_surface(24, 15, (170, 170, 170, 120), 630, 600)
            else:
                window.blit(minecraft_font_smaller.render("1.", True, (255, 255, 255)), (630, 600))
                if 630 <= mouse[0] <= 640 and 600 <= mouse[1] <= 615:
                    description("1st player")
                    trans_surface(10, 15, (170, 170, 170, 120), 630, 600)
                window.blit(minecraft_font_smaller.render("2.", True, (255, 255, 255)), (650, 600))
                if 650 <= mouse[0] <= 660 and 600 <= mouse[1] <= 615:
                    description("2nd player")
                    trans_surface(10, 15, (170, 170, 170, 120), 650, 600)

        

        #blocks
        i = 0
        j = 0
        while i < 595:
            while j < 595:
                block = pygame.image.load(PATH / "blocks" / f"{levels[f"level{level}"][0]["blocks"][j//85][i//85]}")
                block = pygame.transform.scale(block, (85, 85))
         
                window.blit(block, (i, j))
                pygame.draw.rect(window, (0, 0, 0), (i, j, 85, 85), 1)
                j += 85
            j = 0
            i += 85

        if not game_levels[level].text_closed:
            book = pygame.image.load(PATH / "drawable" / "book.png")
            book = pygame.transform.scale(book, (612, 612))

            window.blit(book, (80, 79))

            y = 122
            for el in levels[f"level{level}"][0]["text"][game_levels[level].text_page]:
                window.blit(minecraft_font_book.render(el, True, (0, 0, 0)), (165, y))
                y += 28.8

            if game_levels[level].text_page < levels[f"level{level}"][0]["pages"]-1:
                page_forward = pygame.image.load(PATH / "drawable" / "page_forward.png")
                page_forward = pygame.transform.scale(page_forward, (42, 24))

                window.blit(page_forward, (375, 455))

                if 375 <= mouse[0] <= 417 and 455 <= mouse[1] <= 479:
                    trans_surface(36, 19, (170, 170, 170, 120), 380, 459)
            
            if game_levels[level].text_page > 0:
                page_backward = pygame.image.load(PATH / "drawable" / "page_backward.png")
                page_backward = pygame.transform.scale(page_backward, (42, 24))

                window.blit(page_backward, (165, 455))

                if 165 <= mouse[0] <= 207 and 455 <= mouse[1] <= 479:
                    trans_surface(36, 19, (170, 170, 170, 120), 170, 459)

        if level >= 10:
            steve = pygame.image.load(PATH / "skins" / f"{data["skin"]}.png")
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
            print(cbd)
            if level < 10:
                if code_lang == 0:
                    executed_code = exec_code(code_input.get_text())
                elif code_lang == 1:
                    executed_code = exec_c_code(code_input.get_text(), "C")
                if executed_code["error"] != None:
                    messages.append("Error: " + executed_code['error'])
            else:
                input_code = code_input.get_text() if player == 1 else code_input_2.get_text()
                if code_lang == 0:
                    input_code = '\n'.join(input_code.split("\n")[14:])
                elif code_lang == 1:
                    input_code = '\n'.join(input_code.split("\n")[19:])
                start_time = time.time()
                if code_lang == 0:
                    executed_code = exec_code(def_code_python + input_code)
                elif code_lang == 1:
                    executed_code = exec_c_code(def_code_c + input_code, "C")
                if executed_code["error"] != None:
                    messages.append("Error: " + executed_code['error'])
                end_time = time.time()
                one_v_one_time[player-1] = end_time - start_time

            if code_lang == 0:
                messages += executed_code["out"]
                variables = executed_code["vars"]
                del variables["__builtins__"]
            elif code_lang == 1:
                for el in executed_code["out"]:
                    if el.split(" ")[0] not in ["right", "left", "up", "down"]:
                        messages += [el]

            #correct solution
            solution = False
            if level < 10 and levels[f"level{level}"][0][f"solution_{languages[code_lang]}"][0] == cbd:
                solution = True
            
            if level == 4:
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
                        elif el[0] == "char" and el[2] == "[" and el[3] == "]" and el[4] == "=":
                            c += 1
                    solution = c == 3
                    pass

            if level >= 10:
                stevexy[0] = levels[f"level{level}"][0]["steve_xy"][0]*85
                stevexy[1] = (6-levels[f"level{level}"][0]["steve_xy"][1])*85
                if level >= 14 and level < 17:
                    plate_activated = False
                try:
                    if code_lang == 0:
                        coms = variables["coms"]
                    elif code_lang == 1:
                        coms = []
                        for el in executed_code["out"]:
                            el_splited = el.split(" ")
                            if el_splited[0] in ["right", "left", "up", "down"]:
                                coms.append(el.split(" "))
                except Exception:
                    coms = []
                
                def check():
                    nonlocal plate_activated
                    if stevexy[1]//85 < 0 or stevexy[0]//85 < 0 or stevexy[1]//85 > 6 or stevexy[0]//85 > 6:
                        messages.append("You can only go on grass!")
                        restart()
                    elif levels[f"level{level}"][0]["blocks"][stevexy[1]//85][stevexy[0]//85] == "oak_trapdoor.png":
                        if level >= 14 and level < 17 and not plate_activated:
                            messages.append("Door is not unlocked!")
                            restart()
                        return True
                    elif levels[f"level{level}"][0]["blocks"][stevexy[1]//85][stevexy[0]//85] == "pressure_plate.png":
                        plate_activated = True
                    elif level < 17 and levels[f"level{level}"][0]["blocks"][stevexy[1]//85][stevexy[0]//85] != "grass_top.png":
                        messages.append("You can only go on grass!")
                        restart()
                        return False
                    elif level >= 17 and level < 21 and levels[f"level{level}"][0]["blocks"][stevexy[1]//85][stevexy[0]//85] != "bedrock.png":
                        messages.append("You can only go on bedrock!")
                        restart()
                        return False
                    elif level >= 21 and levels[f"level{level}"][0]["blocks"][stevexy[1]//85][stevexy[0]//85] != "purpur_block.png":
                        messages.append("You can only go on purpur blocks!")
                        restart()
                        return False
                    return False      
                for com in coms:
                    if com[0] == "right":
                        for _ in range(int(com[1])):
                            stevexy[0] += 85
                            move(-85, 0, level)
                            check()
                    elif com[0] == "left":
                        for _ in range(int(com[1])):
                            stevexy[0] -= 85
                            move(85, 0, level)
                            check()
                    elif com[0] == "up":
                        for _ in range(int(com[1])):
                            stevexy[1] -= 85
                            move(0, 85, level)
                            check()
                    elif com[0] == "down":
                        for _ in range(int(com[1])):
                            stevexy[1] += 85
                            move(0, -85, level)
                            check()

                if check():
                    if one_v_one:
                        one_v_one_code[player-1] = True
                        messages.append(f"Player {player}. finished the level!")
                    else:
                        if level >= 14 and level < 17 and plate_activated:
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
                messages.append(f"+{emeralds} Emeralds")
                data["emeralds"] += emeralds
                level_finished = True   
                with open(PATH / "data.json", 'w') as file:
                    json.dump(data, file, indent=4)

            code_runned = False

        minecraft_cmd(messages)

        cursor_pos = minecraft_font_smaller.render(f"Ln {code_input.i + 1}, Col {code_input.cursor_pos + 1}", True, (255, 255, 255))
        window.blit(cursor_pos, (1240 - cursor_pos.get_width() - 15, 600))
        
        pygame.display.update()
        clock.tick(60)

menu()

json_levels.close()
json_options.close()
json_data.close()