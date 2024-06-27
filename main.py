import pygame, random, json
from pygametextboxinput import *

json_file = open('/Users/antoniomatijevic/Documents/CodeCraft/levels/levels.json')
levels = json.load(json_file)  

game_levels = []

class Level:
    def __init__(self, x, y, level, size, text_closed):
        self.x = x
        self.y = y
        self.level = level
        self.size = size
        self.unlocked = level <= levels["last_finished_level"]+1
        self.text_closed = text_closed
    def get_level(self):
        return self.level
    def hover(self, x2, y2):
        return self.x <= x2 <= self.x + self.size and self.y <= y2 <= self.y + self.size

for p in levels["level_p"]:
    game_levels.append(Level(p[0], p[1], p[2], p[3], p[4]))

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

music_on = True

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

code_input = TextInputBox(605, 10, font_family="/Users/antoniomatijevic/Documents/CodeCraft/Minecraft.ttf", font_size=24, max_width=620, max_height=620)
font = pygame.font.Font(pygame.font.match_font("/Users/antoniomatijevic/Documents/CodeCraft/Minecraft.ttf"), 20)
pygame.key.set_repeat(200, 25)

languages = ["Python", "Kotlin"]
code_lang = 0

minecraft_font_big = pygame.font.Font("/Users/antoniomatijevic/Documents/CodeCraft/Minecraft.ttf", 75)
minecraft_font_small = pygame.font.Font("/Users/antoniomatijevic/Documents/CodeCraft/Minecraft.ttf", 25)
minecraft_font_smaller = pygame.font.Font("/Users/antoniomatijevic/Documents/CodeCraft/Minecraft.ttf", 15)
minecraft_font_book = pygame.font.Font("/Users/antoniomatijevic/Documents/CodeCraft/Minecraft.ttf", 20)

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
                    options()
                elif 625 <= mouse[0] <= 820 and 420 <= mouse[1] <= 460:
                    exit()
        
        background = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/background.png")
        background = pygame.transform.scale(background, (1240, 620))
        
        window.blit(background, (0, 0))

        big_title = pygame.transform.scale(pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/Code_Craft.png"), (491, 127))
        
        window.blit(big_title, (374, 60))

        menu_button(420, 250, 594, "Play", 400, 40, mouse)

        menu_button(420, 300, 580, "Levels", 400, 40, mouse)

        menu_button(420, 350, 573, "Tutorial", 400, 40, mouse)

        menu_button(420, 420, 464, "Options...", 195, 40, mouse)

        menu_button(625, 420, 659, "Quit Game", 195, 40, mouse)

        pygame.display.flip()     

def level_menu():
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
    global music_on
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

def options():
    global music_on
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
                    if music_on:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    music_on = not music_on
        background = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/background.png")
        background = pygame.transform.scale(background, (1240, 620))
        
        window.blit(background, (0, 0))

        background_overlay = pygame.Surface((1240, 620), pygame.SRCALPHA)
        background_overlay.fill((0, 0, 0, 50))
        window.blit(background_overlay, (0, 0))

        music_state = "On" if music_on else "Off"
        menu_button(420, 80, 420+(400-minecraft_font_small.size(f"Audio: {music_state}")[0])//2, f"Audio: {music_state}", 400, 40, mouse)

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
    global code_lang
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
                    print(code_input.get_text())
                elif lang_text_x <= mouse[0] <= lang_text_x+lang_text_length and 600 <= mouse[1] <= 615:
                    if code_lang < 1:
                        code_lang += 1
                    else:
                        code_lang = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    game_levels[level].text_closed = not game_levels[level].text_closed
                        
        code_input.update(events)
        code_input.render(window)

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
            transparent_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            transparent_surface.fill((170, 170, 170, 120))
            window.blit(transparent_surface, (12, 597))

        window.blit(back_button, (10, 596))

        #run_button
        run_button = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/select.png")
        run_button = pygame.transform.scale(run_button, (28, 28))
        
        window.blit(run_button, (30, 593))

        if 30 <= mouse[0] <= 50 and 598 <= mouse[1] <= 618:
            transparent_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            transparent_surface.fill((170, 170, 170, 120))
            window.blit(transparent_surface, (34, 598))
        window.blit(run_button, (30, 593))

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
            for el in levels[f"level{level}"][0]["text"]:
                window.blit(minecraft_font_book.render(el, True, (0, 0, 0)), (165, y))
                y += 28.8

            page_forward = pygame.image.load("/Users/antoniomatijevic/Documents/CodeCraft/drawable/page_forward.png")
            page_forward = pygame.transform.scale(page_forward, (42, 24))

            window.blit(page_forward, (375, 455))

            if 375 <= mouse[0] <= 417 and 455 <= mouse[1] <= 479:
                transparent_surface = pygame.Surface((36, 19), pygame.SRCALPHA)
                transparent_surface.fill((170, 170, 170, 120))
                window.blit(transparent_surface, (380, 459))

        

        cursor_pos = font.render(f"Ln {code_input.cursor_y_pos + 1}, Col {code_input.cursor_x_pos + 1}", True, (255, 255, 255))
        window.blit(cursor_pos, (1240 - cursor_pos.get_width() - 15, 600))
        
        pygame.display.update()
        clock.tick(60)

menu()

json_file.close()