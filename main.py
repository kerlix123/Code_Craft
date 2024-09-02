import pygame, random, json, time
from pygametextboxinput import *
from code_runner import *

json_levels = open("/Users/antoniomatijevic/Documents/CodeCraft/levels/levels.json")
levels = json.load(json_levels)

json_options = open("/Users/antoniomatijevic/Documents/CodeCraft/options.json")
options = json.load(json_options)

json_data = open("/Users/antoniomatijevic/Documents/CodeCraft/data.json")
data = json.load(json_data)

game_levels = []
game_skins = []

stevexy = [0, 510]

def move(grass_x, grass_y, level):
    steve = pygame.image.load(f"/Users/antoniomatijevic/Documents/CodeCraft/skins/{data["skin"]}.png")
    steve = pygame.transform.scale(steve, (85, 85))

    window.blit(steve, (stevexy[0], stevexy[1]))
    pygame.draw.rect(window, (0, 0, 0), (stevexy[0], stevexy[1], 85, 85), 1)

    window.blit(pygame.transform.scale(pygame.image.load(f"/Users/antoniomatijevic/Documents/CodeCraft/blocks/{levels[f"level{level}"][0]["blocks"][(stevexy[1]+grass_y)//85][(stevexy[0]+grass_x)//85]}"), (85, 85)), (stevexy[0]+grass_x, stevexy[1]+grass_y))
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
playlist = ["/Users/antoniomatijevic/Documents/CodeCraft/music/DryHands.mp3", 
            "/Users/antoniomatijevic/Documents/CodeCraft/music/Haggstrom.mp3", 
            "/Users/antoniomatijevic/Documents/CodeCraft/music/LivingMice.mp3",
            "/Users/antoniomatijevic/Documents/CodeCraft/music/MiceOnVenus.mp3",
            "/Users/antoniomatijevic/Documents/CodeCraft/music/Minecraft.mp3",
            "/Users/antoniomatijevic/Documents/CodeCraft/music/SubwooferLullaby.mp3",
            "/Users/antoniomatijevic/Documents/CodeCraft/music/Sweden.mp3",
            "/Users/antoniomatijevic/Documents/CodeCraft/music/WetHands.mp3"]
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
pygame.display.set_icon(pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/crafting_table.png"))
clock = pygame.time.Clock()

def menu_button(x, y, text_x, text, width, height, mouse):
    pygame.draw.rect(window, (130, 130, 130), (x, y, width, height))
    pygame.draw.rect(window, (0, 0, 0), (x, y, width, height), 1)

    window.blit(minecraft_font_small.render(text, True, (255, 255, 255)), (text_x, y+10))

    if x <= mouse[0] <= x+width and y <= mouse[1] <= y+height:
        pygame.draw.rect(window, (255, 255, 255), (x, y, width, height), 3)

def minecraft_cmd(l):
    ll = len(l)
    y = 590 - ll*30
    index = 0
    while index < ll:
        transparent_surface = pygame.Surface((595, 30), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 100))
        window.blit(transparent_surface, (0, y))
        window.blit(minecraft_font_small.render(l[index], True, (255, 255, 255)), (10, y+4))
        index += 1
        y += 30

class Function:
    def __init__(self, params, fun_code):
        self.params = params
        self.fun_code = fun_code


code_input = TextInputBox(605, 10, font_family="/Users/antoniomatijevic/Documents/CodeCraft/Minecraft.ttf", font_size=24, max_width=620, max_height=620)
font = pygame.font.Font(pygame.font.match_font("/Users/antoniomatijevic/Documents/CodeCraft/Minecraft.ttf"), 20)
pygame.key.set_repeat(200, 25)

languages = ["Python"]
code_lang = 0

code_runned = False

level_finished = False

minecraft_font_big = pygame.font.Font("/Users/antoniomatijevic/Documents/CodeCraft/Minecraft.ttf", 75)
minecraft_font_small = pygame.font.Font("/Users/antoniomatijevic/Documents/CodeCraft/Minecraft.ttf", 25)
minecraft_font_smaller = pygame.font.Font("/Users/antoniomatijevic/Documents/CodeCraft/Minecraft.ttf", 15)
minecraft_font_book = pygame.font.Font("/Users/antoniomatijevic/Documents/CodeCraft/Minecraft.ttf", 20)

def description(string):
    pygame.draw.rect(window, (194, 194, 194), (223, 598, 150, 19))
    window.blit(minecraft_font_smaller.render(string, True, (255, 255, 255)), ((595-minecraft_font_smaller.size(string)[0])//2, 601))
    pygame.draw.rect(window, (0, 0, 0), (223, 598, 150, 19), 1)

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
                    game(levels["last_finished_level"]+1)
                elif 420 <= mouse[0] <= 820 and 300 <= mouse[1] <= 340:
                    level_menu()
                elif 420 <= mouse[0] <= 820 and 350 <= mouse[1] <= 390:
                    tutorial()
                elif 420 <= mouse[0] <= 615 and 420 <= mouse[1] <= 460:
                    options_win()
                elif 625 <= mouse[0] <= 820 and 420 <= mouse[1] <= 460:
                    exit()
        
        background = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/background.png")
        background = pygame.transform.scale(background, (1240, 620))
        
        window.blit(background, (0, 0))

        big_title = pygame.transform.scale(pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/Code_Craft.png"), (491, 127))
        
        window.blit(big_title, (374, 60))

        emerald = pygame.transform.scale(pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/emerald.png"), (32, 32))

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
        background = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/background.png")
        background = pygame.transform.scale(background, (1240, 620))
        
        window.blit(background, (0, 0))

        background_overlay = pygame.Surface((1240, 620), pygame.SRCALPHA)
        background_overlay.fill((0, 0, 0, 50))
        window.blit(background_overlay, (0, 0))

        #back_button
        back_button = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/unselect.png")
        back_button = pygame.transform.scale(back_button, (40, 40))

        window.blit(back_button, (15, 565))

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            transparent_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            transparent_surface.fill((170, 170, 170, 120))
            window.blit(transparent_surface, (14, 571))

        #level_button
        for lvl in game_levels:
            if lvl.x != -1 and lvl.y != -1:
                pygame.draw.rect(window, (130, 130, 130), (lvl.x, lvl.y, lvl.size, lvl.size))
                pygame.draw.rect(window, (0, 0, 0), (lvl.x, lvl.y, lvl.size, lvl.size), 1)

                text_width = minecraft_font_small.size(str(lvl.level))[0]

                window.blit(minecraft_font_small.render(str(lvl.level), True, (255, 255, 255)), (lvl.x + (lvl.size-text_width)//2 + 1, lvl.y+30))

                if not lvl.unlocked:
                    transparent_surface = pygame.Surface((lvl.size, lvl.size), pygame.SRCALPHA)
                    transparent_surface.fill((0, 0, 0, 50))
                    window.blit(transparent_surface, (lvl.x, lvl.y))

                if lvl.hover(mouse[0], mouse[1]) and lvl.unlocked:
                    pygame.draw.rect(window, (255, 255, 255), (lvl.x, lvl.y, lvl.size, lvl.size), 3)
                    play_button = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/select.png")
                    play_button = pygame.transform.scale(play_button, (lvl.size, lvl.size))
                    window.blit(play_button, (lvl.x, lvl.y))

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
                    
        background = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/background.png")
        background = pygame.transform.scale(background, (1240, 620))
        
        window.blit(background, (0, 0))

        background_overlay = pygame.Surface((1240, 620), pygame.SRCALPHA)
        background_overlay.fill((0, 0, 0, 50))
        window.blit(background_overlay, (0, 0))

        #back_button
        back_button = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/unselect.png")
        back_button = pygame.transform.scale(back_button, (40, 40))

        window.blit(back_button, (15, 565))

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            transparent_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            transparent_surface.fill((170, 170, 170, 120))
            window.blit(transparent_surface, (14, 571))

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
                    with open("/Users/antoniomatijevic/Documents/CodeCraft/options.json", 'w') as file:
                        json.dump(options, file, indent=4)
                if 420 <= mouse[0] <= 820 and 180 <= mouse[1] <= 220:
                    fx_on = not fx_on
                    options["fx_on"] = fx_on
                    with open("/Users/antoniomatijevic/Documents/CodeCraft/options.json", 'w') as file:
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
                    with open("/Users/antoniomatijevic/Documents/CodeCraft/levels/levels.json", 'w') as file:
                        json.dump(levels, file, indent=4)
                    with open("/Users/antoniomatijevic/Documents/CodeCraft/data.json", 'w') as file:
                        json.dump(data, file, indent=4)
                    exit()
                    
        background = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/background.png")
        background = pygame.transform.scale(background, (1240, 620))
        
        window.blit(background, (0, 0))

        background_overlay = pygame.Surface((1240, 620), pygame.SRCALPHA)
        background_overlay.fill((0, 0, 0, 50))
        window.blit(background_overlay, (0, 0))

        menu_button(420, 80, 587, "Skins", 400, 40, mouse)

        music_state = "On" if music_on else "Off"
        menu_button(420, 130, 420+(400-minecraft_font_small.size(f"Audio: {music_state}")[0])//2, f"Audio: {music_state}", 400, 40, mouse)

        fx_state = "On" if fx_on else "Off"
        menu_button(420, 180, 444+(356-minecraft_font_small.size(f"FX: {fx_state}")[0])//2, f"FX: {fx_state}", 400, 40, mouse)

        menu_button(420, 230, 452, "Clear Progress (Exit's app)", 400, 40, mouse)

        #back_button
        back_button = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/unselect.png")
        back_button = pygame.transform.scale(back_button, (40, 40))

        window.blit(back_button, (15, 565))

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            transparent_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            transparent_surface.fill((170, 170, 170, 120))
            window.blit(transparent_surface, (14, 571))

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
                            with open("/Users/antoniomatijevic/Documents/CodeCraft/data.json", 'w') as file:
                                json.dump(data, file, indent=4)
                        else:
                            if data["emeralds"] >= skin.price:
                                skin.unlocked = True
                                data["skins"][skin.name][3] = True
                                data["skin"] = skin.name
                                data["emeralds"] -= skin.price
                                with open("/Users/antoniomatijevic/Documents/CodeCraft/data.json", 'w') as file:
                                    json.dump(data, file, indent=4)
                    
        background = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/background.png")
        background = pygame.transform.scale(background, (1240, 620))
        
        window.blit(background, (0, 0))

        background_overlay = pygame.Surface((1240, 620), pygame.SRCALPHA)
        background_overlay.fill((0, 0, 0, 50))
        window.blit(background_overlay, (0, 0))

        for skin in game_skins:
            pygame.draw.rect(window, (130, 130, 130), (skin.x, skin.y, skin.size, skin.size))
            pygame.draw.rect(window, (0, 0, 0), (skin.x, skin.y, skin.size, skin.size), 1)

            skin_image = pygame.transform.scale(pygame.image.load(f"/Users/antoniomatijevic/Documents/CodeCraft/skins/{skin.name}.png"), (skin.size, skin.size))

            window.blit(skin_image, (skin.x, skin.y))

            if not skin.unlocked:
                transparent_surface = pygame.Surface((skin.size, skin.size), pygame.SRCALPHA)
                transparent_surface.fill((0, 0, 0, 50))
                window.blit(transparent_surface, (skin.x, skin.y))
                emerald = pygame.transform.scale(pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/emerald.png"), (32, 32))
                text_width = minecraft_font_small.size(str(skin.price))[0]
                window.blit(emerald, (skin.x + (skin.size-text_width)//2-17, skin.y+24))
                window.blit(minecraft_font_small.render(str(skin.price), True, (255, 255, 255)), (skin.x + (skin.size-text_width)//2 + 11, skin.y+30))

            if skin.name == data["skin"]:
                pygame.draw.rect(window, (0, 255, 0), (skin.x, skin.y, skin.size, skin.size), 2)

            if skin.hover(mouse[0], mouse[1]):
                pygame.draw.rect(window, (255, 255, 255), (skin.x, skin.y, skin.size, skin.size), 3)
                if skin.unlocked:
                    play_button = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/select.png")
                    play_button = pygame.transform.scale(play_button, (skin.size, skin.size))
                    window.blit(play_button, (skin.x, skin.y))

        #back_button
        back_button = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/unselect.png")
        back_button = pygame.transform.scale(back_button, (40, 40))

        window.blit(back_button, (15, 565))

        if 15 <= mouse[0] <= 55 and 565 <= mouse[1] <= 605:
            transparent_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            transparent_surface.fill((170, 170, 170, 120))
            window.blit(transparent_surface, (14, 571))

        pygame.display.flip()

def game(level):
    global code_lang, code_runned, level_finished
    messages = []
    restart_code = False
    code_input.set_text(levels[f"level{level}"][0]["input_text"])
    if level >= 10:
        stevexy[0] = levels[f"level{level}"][0]["steve_xy"][0]*85
        stevexy[1] = (6-levels[f"level{level}"][0]["steve_xy"][1])*85
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
                    if level_finished:
                        if level > levels["last_finished_level"]:
                            levels["last_finished_level"] = level
                        level += 1
                        with open("/Users/antoniomatijevic/Documents/CodeCraft/data.json", 'w') as file:
                            json.dump(data, file, indent=4)
                        game_levels[level-1].unlocked = True
                        with open("/Users/antoniomatijevic/Documents/CodeCraft/levels/levels.json", 'w') as file:
                            json.dump(levels, file, indent=4)
                        code_input.clear_text()
                        code_input.clear_text()
                        code_input.set_text(levels[f"level{level}"][0]["input_text"])
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
                elif lang_text_x <= mouse[0] <= lang_text_x+lang_text_length and 600 <= mouse[1] <= 615:
                    code_lang = (code_lang + 1) % len(languages)
                elif not game_levels[level].text_closed:
                    if 375 <= mouse[0] <= 417 and 455 <= mouse[1] <= 479 and game_levels[level].text_page < levels[f"level{level}"][0]["pages"]-1:
                        game_levels[level].text_page += 1
                    if 165 <= mouse[0] <= 207 and 455 <= mouse[1] <= 479 and game_levels[level].text_page > 0:
                        game_levels[level].text_page -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    game_levels[level].text_closed = not game_levels[level].text_closed
                if event.key == pygame.K_k and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    messages = []
                if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    code_runned = True

        code_input.update(events)
        code_input.render(window)

        def restart():
            code_input.clear_text()
            code_input.set_text(levels[f"level{level}"][0]["input_text"])
            if level >= 10:
                stevexy[0] = levels[f"level{level}"][0]["steve_xy"][0]*85
                stevexy[1] = (6-levels[f"level{level}"][0]["steve_xy"][1])*85

        pygame.draw.rect(window, (205, 205, 205), (0, 0, 595, 595))

        pygame.draw.rect(window, (0, 118, 197), (0, 595, 1240, 25))

        window.blit(minecraft_font_smaller.render(languages[code_lang], True, (255, 255, 255)), (lang_text_x, 600))

        if lang_text_x <= mouse[0] <= lang_text_x+lang_text_length and 600 <= mouse[1] <= 615:
            transparent_surface = pygame.Surface((lang_text_length, 15), pygame.SRCALPHA)
            transparent_surface.fill((170, 170, 170, 120))
            window.blit(transparent_surface, (lang_text_x, 600))

        #back_button
        back_button = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/close.png")
        back_button = pygame.transform.scale(back_button, (22, 22))

        if 10 <= mouse[0] <= 30 and 597 <= mouse[1] <= 617:
            description("Exit")

            transparent_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            transparent_surface.fill((170, 170, 170, 120))
            window.blit(transparent_surface, (12, 597))

        window.blit(back_button, (10, 596))

        #run_button
        run_button = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/select.png")
        run_button = pygame.transform.scale(run_button, (28, 28))

        if 30 <= mouse[0] <= 50 and 598 <= mouse[1] <= 618:
            description("Run")

            transparent_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            transparent_surface.fill((170, 170, 170, 120))
            window.blit(transparent_surface, (34, 598))
        window.blit(run_button, (30, 593))

        #restart_button
        restart_button = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/reject.png")
        restart_button = pygame.transform.scale(restart_button, (26, 26))

        if 595 <= mouse[0] <= 615 and 598 <= mouse[1] <= 618:
            description("Restart")
            
            transparent_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            transparent_surface.fill((170, 170, 170, 120))
            window.blit(transparent_surface, (599, 598))
        window.blit(restart_button, (595, 595))

        #next_button
        if level_finished:
            next_button = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/accept.png")
            next_button = pygame.transform.scale(next_button, (29, 29))

            if 566 <= mouse[0] <= 582 and 598 <= mouse[1] <= 618:
                description("Next level")
                
                transparent_surface = pygame.Surface((22, 20), pygame.SRCALPHA)
                transparent_surface.fill((170, 170, 170, 120))
                window.blit(transparent_surface, (566, 598))
            window.blit(next_button, (562, 592))

        #blocks
        i = 0
        j = 0
        while i < 595:
            while j < 595:
                block = pygame.image.load(f"/Users/antoniomatijevic/Documents/CodeCraft/blocks/{levels[f"level{level}"][0]["blocks"][j//85][i//85]}")
                block = pygame.transform.scale(block, (85, 85))
         
                window.blit(block, (i, j))
                pygame.draw.rect(window, (0, 0, 0), (i, j, 85, 85), 1)
                j += 85
            j = 0
            i += 85

        if not game_levels[level].text_closed:
            book = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/book.png")
            book = pygame.transform.scale(book, (612, 612))

            window.blit(book, (80, 79))

            y = 122
            for el in levels[f"level{level}"][0]["text"][game_levels[level].text_page]:
                window.blit(minecraft_font_book.render(el, True, (0, 0, 0)), (165, y))
                y += 28.8

            if game_levels[level].text_page < levels[f"level{level}"][0]["pages"]-1:
                page_forward = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/page_forward.png")
                page_forward = pygame.transform.scale(page_forward, (42, 24))

                window.blit(page_forward, (375, 455))

                if 375 <= mouse[0] <= 417 and 455 <= mouse[1] <= 479:
                    transparent_surface = pygame.Surface((36, 19), pygame.SRCALPHA)
                    transparent_surface.fill((170, 170, 170, 120))
                    window.blit(transparent_surface, (380, 459))
            
            if game_levels[level].text_page > 0:
                page_backward = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/page_backward.png")
                page_backward = pygame.transform.scale(page_backward, (42, 24))

                window.blit(page_backward, (165, 455))

                if 165 <= mouse[0] <= 207 and 455 <= mouse[1] <= 479:
                    transparent_surface = pygame.Surface((36, 19), pygame.SRCALPHA)
                    transparent_surface.fill((170, 170, 170, 120))
                    window.blit(transparent_surface, (170, 459))

        if level >= 10:
            steve = pygame.image.load(f"/Users/antoniomatijevic/Documents/CodeCraft/skins/{data["skin"]}.png")
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

            if level < 10:
                executed_code = exec_code(code_input.get_text())
            else:
                def_code = f"""coms = []
class Mob:
    global coms
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def go_up(self, n):
        self.y += n
        coms.append(("up", n))
    def go_down(self, n):
        self.y -= n
        coms.append(("down", n))
    def go_right(self, n):
        self.x += n
        coms.append(("right", n))
    def go_left(self, n):
        self.x -= n
        coms.append(("left", n))
mob = Mob({levels[f"level{level}"][0]["steve_xy"][0]}, {levels[f"level{level}"][0]["steve_xy"][1]})
"""
                input_code = '\n'.join(code_input.get_text().split("\n")[13:])
                executed_code = exec_code(def_code + input_code)

            messages += executed_code["out"]
            variables = executed_code["vars"]

            #correct solution
            solution = False
            if levels[f"level{level}"][0]["solution"][0] == cbd:
                solution = True
            
            if level == 4:
                l = []
                ll = ["<class 'bool'>", "<class 'float'>", "<class 'int'>", "<class 'str'>"]
                for el in list(variables.values()):
                    l.append(str(type(el)))
                l.sort()
                if l == ll:
                    solution = True

            if level >= 10:
                if level >= 14:
                    plate_activated = False
                coms = variables["coms"]

                print(grade_code("mob = Mob(0, 0)\nmob.go_right(6)\nmob.go_up(6)", [('right', 6), ('up', 6)], '\n'.join(code_input.get_text().split("\n")[13:]), coms))
                
                def check():
                    nonlocal plate_activated
                    if stevexy[1]//85 < 0 or stevexy[0]//85 < 0 or stevexy[1]//85 > 6 or stevexy[0]//85 > 6:
                        messages.append("You can only go on grass!")
                        restart()
                    elif levels[f"level{level}"][0]["blocks"][stevexy[1]//85][stevexy[0]//85] == "oak_trapdoor.png":
                        if level >= 14 and not plate_activated:
                            messages.append("Door is not unlocked!")
                            restart()
                        return True
                    elif levels[f"level{level}"][0]["blocks"][stevexy[1]//85][stevexy[0]//85] == "pressure_plate.png":
                        plate_activated = True
                    elif levels[f"level{level}"][0]["blocks"][stevexy[1]//85][stevexy[0]//85] != "grass_top.png":
                        messages.append("You can only go on grass!")
                        restart()
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
                    if level >= 14 and plate_activated:
                        solution = True
                    elif level >= 10 and level < 14:
                        solution = True
                else:
                    messages.append("Wrong solution! Try again.")
                    restart()
                
            if solution:
                if level >= 10:
                    if fx_on:
                        sound = pygame.mixer.Sound("/Users/antoniomatijevic/Documents/CodeCraft/sounds/trapdoor.mp3")
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

            code_runned = False

        minecraft_cmd(messages)

        cursor_pos = font.render(f"Ln {code_input.cursor_y_pos + 1}, Col {code_input.cursor_x_pos + 1}", True, (255, 255, 255))
        window.blit(cursor_pos, (1240 - cursor_pos.get_width() - 15, 600))
        
        pygame.display.update()
        clock.tick(60)

menu()

json_levels.close()
json_options.close()
json_data.close()