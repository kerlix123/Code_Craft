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
        steve = self.pygame.image.load(PATH / "skins" / f"{self.data['skin']}.png")
        steve = self.pygame.transform.scale(steve, (85, 85))

        self.window.blit(steve, (self.stevexy[0], self.stevexy[1]))
        self.pygame.draw.rect(self.window, (0, 0, 0), (self.stevexy[0], self.stevexy[1], 85, 85), 1)

        block_path = self.levels[f"level{level}"][0]["blocks"] if not player_l else self.player_levels[f"level{level}"][0]["blocks"]

        self.window.blit(self.pygame.transform.scale(self.pygame.image.load(PATH / "blocks" / f"{block_path[(self.stevexy[1]+grass_y)//85][(self.stevexy[0]+grass_x)//85]}"), (85, 85)), (self.stevexy[0]+grass_x, self.stevexy[1]+grass_y))
        self.pygame.draw.rect(self.window, (0, 0, 0), (self.stevexy[0]+grass_x, self.stevexy[1]+grass_y, 85, 85), 1)
        self.pygame.display.update()
        self.clock.tick(60)
        self.time.sleep(0.1)

    def loading_screen(self):
        background = self.pygame.image.load(PATH / "drawable" / "logo.png")
        background = self.pygame.transform.scale(background, (1484, 620))

        loading_bar_width = 600
        loading_bar_height = 30
        loading_bar_x = (1240 - loading_bar_width) // 2
        loading_bar_y = 500
        loading_progress = 0

        padding = 5

        fade_out = False
        loading_bar_alpha = 255

        while True:
            events = self.pygame.event.get()
            for event in events:
                if event.type == self.pygame.QUIT:
                    self.pygame.quit()
                    exit()

            self.window.blit(background, (-122, 0))

            if loading_progress < loading_bar_width:
                loading_progress += 10
            else:
                fade_out = True

            if fade_out:
                if loading_bar_alpha > 0:
                    loading_bar_alpha -= 5

                border_surface = self.pygame.Surface((loading_bar_width + 2 * (padding + 2), loading_bar_height + 2 * (padding + 2)), self.pygame.SRCALPHA)
                border_surface.fill((0, 0, 0, loading_bar_alpha))
                self.window.blit(border_surface, (loading_bar_x - padding - 2, loading_bar_y - padding - 2))

                self.pygame.draw.rect(self.window, (255, 255, 255), 
                                    (loading_bar_x - padding, loading_bar_y - padding, 
                                    loading_bar_width + 2 * padding, loading_bar_height + 2 * padding))

                loading_bar_surface = self.pygame.Surface((loading_progress, loading_bar_height), self.pygame.SRCALPHA)
                loading_bar_surface.fill((0, 0, 0, loading_bar_alpha))
                self.window.blit(loading_bar_surface, (loading_bar_x, loading_bar_y))

            else:
                self.pygame.draw.rect(self.window, (0, 0, 0), 
                                    (loading_bar_x - padding - 2, loading_bar_y - padding - 2,
                                    loading_bar_width + 2 * (padding + 2), loading_bar_height + 2 * (padding + 2)))

                self.pygame.draw.rect(self.window, (255, 255, 255), 
                                    (loading_bar_x - padding, loading_bar_y - padding, 
                                    loading_bar_width + 2 * padding, loading_bar_height + 2 * padding))

                self.pygame.draw.rect(self.window, (0, 0, 0), (loading_bar_x, loading_bar_y, loading_progress, loading_bar_height))

            if fade_out and loading_bar_alpha <= 0:
                break

            self.pygame.display.flip()
            self.clock.tick(60)

    def render_text_with_background(self, text, position, font, color, padding=5, bg_alpha=150):
        """Render text with a background."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=position)

        bg_surface = self.pygame.Surface((text_rect.width + padding * 2, text_rect.height + padding * 2))
        bg_surface.fill((0, 0, 0))
        bg_surface.set_alpha(bg_alpha)
        self.window.blit(bg_surface, (text_rect.x - padding, text_rect.y - padding))

        self.window.blit(text_surface, text_rect.topleft)

    def display_intro_text(self):
        text1 = "Welcome to:"
        counter1 = 0

        texts = [
            "Game made by Antonio - NEX in which you can learn basics of programming.",
            "I hope you will enjoy playing it as much as I enjoyed making it.",
            "You can learn Python, C, or C++.",
            "And if you ever find yourself stuck or unsure how to do something, just ask Google.",
            "I lost count of how many times I did that while making this game! ;)",
            "Remember, programming is all about experimenting and learning from mistakes.",
            "So don't worry if you don't get it right the first time-just keep trying!",
            "And who knows? Maybe one day you'll be building your own games and applications!",
            "So, let's dive in and see what you can do. Good luck, and most importantly-have fun!"
        ]

        text_index = 0
        counter = 0
        finished_typing = False
        start_fade_out = False

        big_title = self.pygame.image.load(PATH / "drawable" / "Code_Craft.png")
        big_title = self.pygame.transform.scale(big_title, (491, 127))

        fade_alpha = 0
        title_fade_in = False

        fade_out_alpha = 255

        while True:
            events = self.pygame.event.get()
            for event in events:
                if event.type == self.pygame.QUIT:
                    exit()
                if finished_typing and (event.type == self.pygame.KEYDOWN or event.type == self.pygame.MOUSEBUTTONDOWN):
                    start_fade_out = True

            self.background()
            background_overlay = self.pygame.Surface((1240, 620), self.pygame.SRCALPHA)
            background_overlay.fill((0, 0, 0, 50 if not start_fade_out else fade_out_alpha // 5))
            self.window.blit(background_overlay, (0, 0))

            color = (194, 194, 194)
            if not (start_fade_out and text_index <= 0):
                self.render_text_with_background(text1[:(counter1 // 3)+1], (540, 20), self.minecraft_font_small, color)

            if counter1 < 3 * len(text1):
                counter1 += 1
            else:
                if not title_fade_in:
                    self.time.sleep(0.5)
                    title_fade_in = True

            if title_fade_in:
                title_surface = big_title.copy()
                title_surface.set_alpha(fade_alpha)
                self.window.blit(title_surface, (374, 60))

                if fade_alpha < 255:
                    fade_alpha += 3
                else:
                    if not start_fade_out and text_index < len(texts):
                        if counter < 2 * len(texts[text_index]):
                            counter += 1
                        else:
                            self.time.sleep(0.45)
                            counter = 0
                            text_index += 1
                            if text_index >= len(texts):
                                finished_typing = True
                    else:
                        finished_typing = True

                    for i in range(text_index):
                        self.render_text_with_background(texts[i], (140, 200 + i * 45), self.minecraft_font_small, color)

                    if not finished_typing:
                        self.render_text_with_background(texts[text_index][:counter // 2], (140, 200 + text_index * 45), self.minecraft_font_small, color)

            if start_fade_out:
                fade_out_alpha -= 15
                text_index -= 1
                if fade_out_alpha <= 0:
                    return

            self.pygame.display.flip()
            self.clock.tick(60)