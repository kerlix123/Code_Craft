import pygame, json
class GameUtils:
    def __init__(self, window, playlist, current_song_index, minecraft_font_small, minecraft_font_book, minecraft_font_smaller, clock, data, stevexy, levels, player_levels, time, path, languages):
        self.window = window
        self.playlist = playlist
        self.current_song_index = current_song_index
        self.minecraft_font_small = minecraft_font_small
        self.minecraft_font_book = minecraft_font_book
        self.minecraft_font_smaller = minecraft_font_smaller
        self.clock = clock
        self.data = data
        self.stevexy = stevexy
        self.levels = levels
        self.player_levels = player_levels
        self.time = time
        self.PATH = path
        self.languages = languages
        self.background_photo = pygame.transform.scale(pygame.image.load(self.PATH / "drawable" / "background.png"), (1240, 620))
        self.background_overlay = pygame.Surface((1240, 620), pygame.SRCALPHA)
        self.background_overlay.fill((0, 0, 0, 50))
        self.click_sound = pygame.mixer.Sound(self.PATH / "sounds" / "minecraft_click.mp3")
        self.steve = pygame.transform.scale(pygame.image.load(self.PATH / "skins" / f"{self.data['skin']}.png"), (85, 85))

    def set_skin(self):
        self.steve = pygame.transform.scale(pygame.image.load(self.PATH / "skins" / f"{self.data['skin']}.png"), (85, 85))
        
    def play_next_track(self, music_on):
        if not pygame.mixer.music.get_busy() and music_on:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            pygame.mixer.music.load(self.playlist[self.current_song_index])
            pygame.mixer.music.play()
    
    def button(self, b_button, x, y):
        self.window.blit(b_button, (x, y))

    def menu_button(self, x, y, text_x, text, width, height, mouse):
        pygame.draw.rect(self.window, (130, 130, 130), (x, y, width, height))
        pygame.draw.rect(self.window, (0, 0, 0), (x, y, width, height), 1)

        self.window.blit(text, (text_x, y+10))

        if x <= mouse[0] <= x+width and y <= mouse[1] <= y+height:
            pygame.draw.rect(self.window, (255, 255, 255), (x, y, width, height), 3)

    def trans_surface(self, width, height, color, x, y):
        transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        transparent_surface.fill(color)
        self.window.blit(transparent_surface, (x, y))

    def background(self):
        self.window.blit(self.background_photo, (0, 0))
    
    def bg_overlay(self):
        self.window.blit(self.background_overlay, (0, 0))

    def render_text(self, x, y, text, inc):
        for el in text:
            self.window.blit(el, (x, y))
            y += inc

    def minecraft_cmd(self, l, x, length, start_y):
        ll = len(l)
        y = start_y - ll*30
        index = 0
        while index < ll:
            color = (255, 255, 255)
            self.trans_surface(length, 30, (0, 0, 0, 100), x, y)
            if l[index][0:7] == "Error: ":
                color = (255, 85, 85)
            if l[index] == "Player 1. won." or l[index] == "Player 2. won.":
                color = (0, 255, 0)
            self.window.blit(self.minecraft_font_small.render(l[index], True, color), (x+10, y+4))
            index += 1
            y += 30

    def description(self, string):
        length = 150
        x = 223
        if len(string) > 18:
            length = 300
            x = 147
        pygame.draw.rect(self.window, (194, 194, 194), (x, 598, length, 19))
        self.window.blit(self.minecraft_font_smaller.render(string, True, (255, 255, 255)), ((595-self.minecraft_font_smaller.size(string)[0])//2, 601))
        pygame.draw.rect(self.window, (0, 0, 0), (x, 598, length, 19), 1)

    def move(self, grass_x, grass_y, level, player_l=False):
        self.window.blit(self.steve, (self.stevexy[0], self.stevexy[1]))
        pygame.draw.rect(self.window, (0, 0, 0), (self.stevexy[0], self.stevexy[1], 85, 85), 1)

        block_path = self.levels[f"level{level}"][0]["blocks"] if not player_l else self.player_levels[f"level{level}"][0]["blocks"]

        self.window.blit(pygame.transform.scale(pygame.image.load(self.PATH / "blocks" / f"{block_path[(self.stevexy[1]+grass_y)//85][(self.stevexy[0]+grass_x)//85]}"), (85, 85)), (self.stevexy[0]+grass_x, self.stevexy[1]+grass_y))
        pygame.draw.rect(self.window, (0, 0, 0), (self.stevexy[0]+grass_x, self.stevexy[1]+grass_y, 85, 85), 1)
        pygame.display.update()
        self.clock.tick(60)
        self.time.sleep(0.1)

    def render_blocks(self, level, player_l):
        blocks = []
        level_key = f"level{level}"
        block_size = 85
        block_paths = {}

        # Preload all unique block images
        for row in range(7):
            blocks.append([])
            for col in range(7):
                # Select the correct block based on the level and player context
                if not player_l:
                    block_type = self.levels[level_key][0]['blocks'][row][col]
                else:
                    block_type = self.player_levels[level_key][0]['blocks'][row][col]
                
                block_path = self.PATH / "blocks" / f"{block_type}"
                
                # Cache the block images to avoid loading and scaling every time
                if block_path not in block_paths:
                    block_image = pygame.image.load(block_path)
                    block_image = pygame.transform.scale(block_image, (block_size, block_size))
                    block_paths[block_path] = block_image
                
                blocks[row].append(block_paths[block_path])
        return blocks

    def render_book_text(self, level, code_lang):
        return [
            [self.minecraft_font_book.render(row, True, (0, 0, 0)) for row in page]
            for page in self.levels[f"level{level}"][0][f"text_{self.languages[code_lang]}"]
        ]
    
    def play_click_sound(self, fx_on):
        if fx_on:
            self.click_sound.play()

    def write_to_json(self, file, input_dict):
        with open(file, 'w') as json_file:
            json.dump(input_dict, json_file, indent=4)