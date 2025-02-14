import pygame, json, random
from pathlib import Path
from classes.classes_ import *

PATH = Path.cwd()

minecraft_font_small = pygame.font.Font(PATH / "bitcell_memesbruh03.ttf", 40)
minecraft_font_smaller = pygame.font.Font(PATH / "bitcell_memesbruh03.ttf", 24)
minecraft_font_book = pygame.font.Font(PATH / "bitcell_memesbruh03.ttf", 30)


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
    "play": {"eng": (render_small_text("Play"), 594), "hrv": ((render_small_text("Igraj"), 580))},
    "levels": {"eng": (render_small_text("Levels"), 580), "hrv": (render_small_text("Razine"), 580)},
    "tutorials": {"eng": (render_small_text("Tutorials"), 573), "hrv": (render_small_text("Vodiči"), 575)},
    "options": {"eng": (render_small_text("Options..."), 464), "hrv": (render_small_text("Opcije..."), 470)},
    "quit": {"eng": (render_small_text("Quit Game"), 659), "hrv": (render_small_text("Izađi iz igre"), 650)}
}

level_menu_text = {
    "lvl_builder": {"eng": (render_small_text("Level Builder"), 853), "hrv": (render_small_text("Graditelj Razina"), 810)},
    "your_levels": {"eng": (render_small_text("Your Levels"), 1063), "hrv": (render_small_text("Tvoje Razine"), 1040)},
    "debug_challenge": {"eng": (render_small_text("Debug Challenges"), 30), "hrv": (render_small_text("Izazovi za Debug"), 30)},
    "random_level": {"eng": (render_small_text("Random Level"), 627), "hrv": (render_small_text("Nasumična Razina"), 555)}
}

options_text = {
    "skins": {"eng": (render_small_text("Skins"), 587), "hrv": (render_small_text("Likovi"), 580)},
    "clear_progress": {"eng": (render_small_text("Clear Progress (Exits game)"), 452), "hrv": (render_small_text("Izbriši napredak (Zatvara igru)"), 427)},
    "audio_on": {"eng": (render_small_text("Audio: On"), 565), "hrv": (render_small_text("Zvuk: Uključeno"), 530)},
    "audio_off": {"eng": (render_small_text("Audio: Off"), 558), "hrv": (render_small_text("Zvuk: Isključeno"), 530)},
    "fx_on": {"eng": (render_small_text("FX: On"), 580), "hrv": (render_small_text("Efekti: Uključeno"), 530)},
    "fx_off": {"eng": (render_small_text("FX: Off"), 573), "hrv": (render_small_text("Efekti: Isključeno"), 530)},
    "python": {"eng": (render_small_text("Programming language: Python"), 425), "hrv": (render_small_text("Programski jezik: Python"), 480)},
    "c": {"eng": (render_small_text("Programming language: C"), 462), "hrv": (render_small_text("Programski jezik: C"), 520)},
    "c++": {"eng": (render_small_text("Programming language: C++"), 446), "hrv": (render_small_text("Programski jezik: C++"), 500)},
    "lang": {"eng": (render_small_text("Language: English"), 452), "hrv": (render_small_text("Jezik: Hrvatski"), 525)},
}

game_text = {
    "1.": render_smaller_text("1."),
    "2.": render_smaller_text("2."),
    "1v1": render_smaller_text("1v1"),
    0: render_smaller_text("Python"),
    1: render_smaller_text("C"),
    2: render_smaller_text("C++")
}

texts = {
    "Set start and end positions first!": {"eng": "Set start and end positions first!", "hrv": "Prvo postavi početnu i krajnju poziciju!"},
    "Set start position": {"eng": "Set start position", "hrv": "Postavi startnu poziciju"},
    "Set path block": {"eng": "Set path block", "hrv": "Postavi blok putanje"},
    "Save level": {"eng": "Save level", "hrv": "Spremi razinu"},
    "Unsaved": {"eng": "Unsaved", "hrv": "Nije spremljeno"},
    "Exit": {"eng": "Exit", "hrv": "Izlaz"},
    "Coming soon!": {"eng": "Coming soon!", "hrv": "Dolazi uskoro!"},
    "Buy Hint 1 first.": {"eng": "Buy Hint 1 first.", "hrv": "Najprije kupi Hint 1."},
    "You don't have enough emeralds!": {"eng": "You don't have enough emeralds!", "hrv": "Nemaš dovoljno smaragda!"},
    "Mob got out of bounds!": {"eng": "Mob got out of bounds!", "hrv": "Lik je izašao izvan granica!"},
    "Door is not unlocked!": {"eng": "Door is not unlocked!", "hrv": "Vrata nisu otvorena!"},
    "You can't go on this block!": {"eng": "You can't go on this block!", "hrv": "Ne možeš ići po ovom bloku!"},
    "You can only go on grass!": {"eng": "You can only go on grass!", "hrv": "Možeš ići jedino po travi!"},
    "You can only go on bedrock!": {"eng": "You can only go on bedrock!", "hrv": "Možeš ići jedino po temelju!"},
    "You can only go on purpur blocks!": {"eng": "You can only go on purpur blocks!", "hrv": "Možeš ići jedino po blokovima purpura!"},
}

def load_json_file(file):
    with open(file) as json_file:
        return json.load(json_file)

#music
current_song_index = 0
playlist = [PATH / "music" / "HelloWorld.mp3",
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