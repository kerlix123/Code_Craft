import pygame, json, random
from pathlib import Path
from classes.classes_ import *

PATH = Path.cwd()

minecraft_font_small = pygame.font.Font(PATH / "Minecraft.ttf", 25)
minecraft_font_smaller = pygame.font.Font(PATH / "Minecraft.ttf", 15)
minecraft_font_book = pygame.font.Font(PATH / "Minecraft.ttf", 20)

def get_scaled_img(img, size):
    return pygame.transform.scale(pygame.image.load(img), size)

back_button = get_scaled_img(PATH / "drawable" / "unselect.png", (40, 40))
play_level_button = get_scaled_img(PATH / "drawable" / "select.png", (80, 80))
close_button = get_scaled_img(PATH / "drawable" / "close.png", (22, 22))
run_button = get_scaled_img(PATH / "drawable" / "select.png", (28, 28))
accept_button = get_scaled_img(PATH / "drawable" / "accept.png", (29, 29))
restart_button = get_scaled_img(PATH / "drawable" / "reject.png", (26, 26))
torch1_button = get_scaled_img(PATH / "drawable" / "torch1.png", (31, 31))
torch2_button = get_scaled_img(PATH / "drawable" / "torch2.png", (31, 31))
close_1v1_button = get_scaled_img(PATH / "drawable" / "close.png", (16, 16))
clock_button = get_scaled_img(PATH / "drawable" / "clock.png", (20, 20))
book = get_scaled_img(PATH / "drawable" / "book.png", (800, 800))
page_forward_button = get_scaled_img(PATH / "drawable" / "page_forward.png", (42, 24))
page_backward_button = get_scaled_img(PATH / "drawable" / "page_backward.png", (42, 24))
not_saved = get_scaled_img(PATH / "drawable" / "not_saved.png", (15, 15)).convert_alpha()

def render_small_text(text):
    return minecraft_font_small.render(text, True, (255, 255, 255))

def render_smaller_text(text):
    return minecraft_font_smaller.render(text, True, (255, 255, 255))

menu_text = {
    "play": render_small_text("Play"),
    "levels": render_small_text("Levels"),
    "tutorials": render_small_text("Tutorials"),
    "options": render_small_text("Options..."),
    "quit": render_small_text("Quit Game")
}

level_menu_text = {
    "lvl_builder": render_small_text("Level Builder"),
    "your_levels": render_small_text("Your levels"),
    "debug_challenge": render_small_text("Debug challenges"),
    "random_level": render_small_text("Random level")
}

options_text = {
    "skins": render_small_text("Skins"),
    "clear_progress": render_small_text("Clear Progress (Exit's app)"),
    "audio_on": render_small_text("Audio: On"),
    "audio_off": render_small_text("Audio: Off"),
    "fx_on": render_small_text("FX: On"),
    "fx_off": render_small_text("FX: Off"),
    "python": render_small_text("Programming language: Python"),
    "c": render_small_text("Programming language: C"),
    "c++": render_small_text("Programming language: C++"),
}

game_text = {
    "1.": render_smaller_text("1."),
    "2.": render_smaller_text("2."),
    "1v1": render_smaller_text("1v1"),
    0: render_smaller_text("Python"),
    1: render_smaller_text("C"),
    2: render_smaller_text("C++")
}


def load_json_file(file):
    with open(file) as json_file:
        return json.load(json_file)

#music
current_song_index = 0
playlist = [PATH / "music" / "HelloWorld.mp3",
            PATH / "music" / "Me.mp3", 
            PATH / "music" / "Valley.mp3",
            PATH / "music" / "Croatia.mp3",
            PATH / "music" / "Peace.mp3"]
random.shuffle(playlist)

levels = load_json_file(PATH / "levels" / "levels.json")

data = load_json_file(PATH / "data.json")

player_levels = load_json_file(PATH / "levels" / "player_levels.json")

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

stevexy = [0, 510]

languages = ["Python", "C", "C++"]
code_lang = data["code_lang"]

code_runned = False
level_finished = False
grades = [0, 0]