import json

PATH = None

class GameUtils:
    def __init__(self, window, pygame, playlist, current_song_index, minecraft_font_small, minecraft_font_book, minecraft_font_smaller, clock, data, stevexy, levels, player_levels, time, path):
        global PATH
        self.window = window
        self.pygame = pygame
        self.playlist = playlist
        self.current_song_index = current_song_index
        self.minecraft_font_small = minecraft_font_small
        self.minecraft_font_book = minecraft_font_book
        self.minecraft_font_smaller = minecraft_font_smaller
        self.current_song_index = 0
        self.clock = clock
        self.data = data
        self.stevexy = stevexy
        self.levels = levels
        self.player_levels = player_levels
        self.time = time
        PATH = path
        
    def play_next_track(self):
        self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
        self.pygame.mixer.music.load(self.playlist[self.current_song_index])
        self.pygame.mixer.music.play()
    
    def button(self, path, width, height, x, y):
        b_button = self.pygame.transform.scale(self.pygame.image.load(path), (width, height))
        self.window.blit(b_button, (x, y))

    def menu_button(self, x, y, text_x, text, width, height, mouse):
        self.pygame.draw.rect(self.window, (130, 130, 130), (x, y, width, height))
        self.pygame.draw.rect(self.window, (0, 0, 0), (x, y, width, height), 1)

        self.window.blit(self.minecraft_font_small.render(text, True, (255, 255, 255)), (text_x, y+10))

        if x <= mouse[0] <= x+width and y <= mouse[1] <= y+height:
            self.pygame.draw.rect(self.window, (255, 255, 255), (x, y, width, height), 3)

    def trans_surface(self, width, height, color, x, y):
        transparent_surface = self.pygame.Surface((width, height), self.pygame.SRCALPHA)
        transparent_surface.fill(color)
        self.window.blit(transparent_surface, (x, y))

    def background(self):
        background = self.pygame.image.load(PATH / "drawable" / "background.png")
        background = self.pygame.transform.scale(background, (1240, 620))
        self.window.blit(background, (0, 0))
    
    def bg_overlay(self):
        background_overlay = self.pygame.Surface((1240, 620), self.pygame.SRCALPHA)
        background_overlay.fill((0, 0, 0, 50))
        self.window.blit(background_overlay, (0, 0))

    def render_text(self, x, y, text, inc):
        for el in text:
            self.window.blit(self.minecraft_font_book.render(el, True, (0, 0, 0)), (x, y))
            y += inc

    def minecraft_cmd(self, l):
        ll = len(l)
        y = 590 - ll*30
        index = 0
        while index < ll:
            color = (255, 255, 255)
            self.trans_surface(595, 30, (0, 0, 0, 100), 0, y)
            if l[index][0:7] == "Error: ":
                color = (255, 85, 85)
            if l[index] == "Player 1. won." or l[index] == "Player 2. won.":
                color = (0, 255, 0)
            self.window.blit(self.minecraft_font_small.render(l[index], True, color), (10, y+4))
            index += 1
            y += 30

    def description(self, string):
        length = 150
        x = 223
        if len(string) > 18:
            length = 300
            x = 147
        self.pygame.draw.rect(self.window, (194, 194, 194), (x, 598, length, 19))
        self.window.blit(self.minecraft_font_smaller.render(string, True, (255, 255, 255)), ((595-self.minecraft_font_smaller.size(string)[0])//2, 601))
        self.pygame.draw.rect(self.window, (0, 0, 0), (x, 598, length, 19), 1)

    def move(self, grass_x, grass_y, level, player_l=False):
        steve = self.pygame.image.load(PATH / "skins" / f"{self.data["skin"]}.png")
        steve = self.pygame.transform.scale(steve, (85, 85))

        self.window.blit(steve, (self.stevexy[0], self.stevexy[1]))
        self.pygame.draw.rect(self.window, (0, 0, 0), (self.stevexy[0], self.stevexy[1], 85, 85), 1)

        block_path = self.levels[f"level{level}"][0]["blocks"] if not player_l else self.player_levels[f"level{level}"][0]["blocks"]

        self.window.blit(self.pygame.transform.scale(self.pygame.image.load(PATH / "blocks" / f"{block_path[(self.stevexy[1]+grass_y)//85][(self.stevexy[0]+grass_x)//85]}"), (85, 85)), (self.stevexy[0]+grass_x, self.stevexy[1]+grass_y))
        self.pygame.draw.rect(self.window, (0, 0, 0), (self.stevexy[0]+grass_x, self.stevexy[1]+grass_y, 85, 85), 1)
        self.pygame.display.update()
        self.clock.tick(60)
        self.time.sleep(0.1)