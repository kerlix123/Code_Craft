import pygame
PATH = None

class Loaders:
    def __init__(self, window, minecraft_font_small, clock, time, path):
        global PATH
        self.window = window
        self.minecraft_font_small = minecraft_font_small
        self.clock = clock
        self.time = time
        PATH = path

    def loading_screen(self):
        background = pygame.image.load(PATH / "drawable" / "logo.png")
        background = pygame.transform.scale(background, (1484, 620))

        loading_bar_width = 600
        loading_bar_height = 30
        loading_bar_x = (1240 - loading_bar_width) // 2
        loading_bar_y = 500
        loading_progress = 0

        padding = 5

        fade_out = False
        loading_bar_alpha = 255

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.window.blit(background, (-122, 0))

            if loading_progress < loading_bar_width:
                loading_progress += 10
            else:
                fade_out = True

            if fade_out:
                if loading_bar_alpha > 0:
                    loading_bar_alpha -= 5

                border_surface = pygame.Surface((loading_bar_width + 2 * (padding + 2), loading_bar_height + 2 * (padding + 2)), pygame.SRCALPHA)
                border_surface.fill((0, 0, 0, loading_bar_alpha))
                self.window.blit(border_surface, (loading_bar_x - padding - 2, loading_bar_y - padding - 2))

                pygame.draw.rect(self.window, (255, 255, 255), 
                                    (loading_bar_x - padding, loading_bar_y - padding, 
                                    loading_bar_width + 2 * padding, loading_bar_height + 2 * padding))

                loading_bar_surface = pygame.Surface((loading_progress, loading_bar_height), pygame.SRCALPHA)
                loading_bar_surface.fill((0, 0, 0, loading_bar_alpha))
                self.window.blit(loading_bar_surface, (loading_bar_x, loading_bar_y))

            else:
                pygame.draw.rect(self.window, (0, 0, 0), 
                                    (loading_bar_x - padding - 2, loading_bar_y - padding - 2,
                                    loading_bar_width + 2 * (padding + 2), loading_bar_height + 2 * (padding + 2)))

                pygame.draw.rect(self.window, (255, 255, 255), 
                                    (loading_bar_x - padding, loading_bar_y - padding, 
                                    loading_bar_width + 2 * padding, loading_bar_height + 2 * padding))

                pygame.draw.rect(self.window, (0, 0, 0), (loading_bar_x, loading_bar_y, loading_progress, loading_bar_height))

            if fade_out and loading_bar_alpha <= 0:
                break

            pygame.display.flip()
            self.clock.tick(60)

    def render_text_with_background(self, text, position, font, color, padding=5, bg_alpha=150):
        """Render text with a background."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=position)

        bg_surface = pygame.Surface((text_rect.width + padding * 2, text_rect.height + padding * 2))
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

        big_title = pygame.image.load(PATH / "drawable" / "Code_Craft.png")
        big_title = pygame.transform.scale(big_title, (491, 127))

        fade_alpha = 0
        title_fade_in = False

        fade_out_alpha = 255

        background = pygame.image.load(PATH / "drawable" / "background.png")
        background = pygame.transform.scale(background, (1240, 620))

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if finished_typing and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                    start_fade_out = True

            self.window.blit(background, (0, 0))
            background_overlay = pygame.Surface((1240, 620), pygame.SRCALPHA)
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

            pygame.display.flip()
            self.clock.tick(60)