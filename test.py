import pygame
from pathlib import Path
import time

# Paths and initialization
PATH = Path.cwd()
pygame.init()

# Screen and font setup
window = pygame.display.set_mode((1240, 620))
pygame.display.set_caption("Code_Craft")
pygame.display.set_icon(pygame.image.load(PATH / "drawable" / "crafting_table.png"))
clock = pygame.time.Clock()

# Fonts
minecraft_font_big = pygame.font.Font(PATH / "Minecraft.ttf", 75)
minecraft_font_small = pygame.font.Font(PATH / "Minecraft.ttf", 25)
minecraft_font_smaller = pygame.font.Font(PATH / "Minecraft.ttf", 15)
minecraft_font_book = pygame.font.Font(PATH / "Minecraft.ttf", 20)

def loading_screen():
    # Load background image
    background = pygame.image.load(PATH / "drawable" / "logo.png")

    # Get original dimensions of the image
    original_width, original_height = background.get_size()

    # Calculate the scale factors for both dimensions
    scale_width = window.get_width() / original_width
    scale_height = window.get_height() / original_height

    # Use the smaller scale factor to maintain aspect ratio
    scale_factor = max(scale_width, scale_height)

    # Calculate new dimensions
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)

    # Scale the image to fill the screen while maintaining aspect ratio
    background = pygame.transform.scale(background, (new_width, new_height))

    # Get the position to center the image (if it overflows the window)
    background_rect = background.get_rect(center=(window.get_width() // 2, window.get_height() // 2))

    # Loading bar parameters
    loading_bar_width = 600
    loading_bar_height = 30
    loading_bar_x = (window.get_width() - loading_bar_width) // 2  # Center horizontally
    loading_bar_y = 500  # Fixed Y position for loading bar
    loading_progress = 0  # Initial loading progress

    # Padding for the border
    padding = 5  # Padding around the loading bar

    # Main loop for the loading screen
    while True:
        # Event handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Draw the background image
        window.fill((0, 0, 0))  # Fill the window with black
        window.blit(background, background_rect)

        # Update the loading progress
        if loading_progress < loading_bar_width:
            loading_progress += 6  # Increase this value to speed up the loading

        # Draw the loading bar background (transparent)
        # Draw the border around the loading bar
        pygame.draw.rect(window, (0, 0, 0), (loading_bar_x - padding - 2, loading_bar_y - padding - 2,
                                               loading_bar_width + 2 * (padding + 2), loading_bar_height + 2 * (padding + 2)), 3)  # Black border

        # Draw the actual loading bar (filled)
        if loading_progress > 0:  # Only draw if there's progress
            pygame.draw.rect(window, (0, 0, 0), (loading_bar_x, loading_bar_y, loading_progress, loading_bar_height))  # Black progress fill

        # Check if loading is complete
        if loading_progress >= loading_bar_width:
            break  # Exit the loading loop to go back to main program

        # Update the display
        pygame.display.flip()
        clock.tick(60)

def render_text_with_background(text, position, font, color, padding=5, bg_alpha=150):
    """Render text with a background."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=position)

    # Create a background surface with padding
    bg_surface = pygame.Surface((text_rect.width + padding * 2, text_rect.height + padding * 2))
    bg_surface.fill((0, 0, 0))  # Solid black
    bg_surface.set_alpha(bg_alpha)  # Set transparency
    window.blit(bg_surface, (text_rect.x - padding, text_rect.y - padding))  # Draw the background

    # Draw the text on top of the background
    window.blit(text_surface, text_rect.topleft)

def display_intro_text():
    # Text and counters
    text1 = "Welcome to:"
    counter1 = 0

    text2 = "Game made by Antonio - NEX in which you can learn basics of programming."
    counter2 = 0
    text2_type = False

    text3 = "I hope you will enjoy playing it as much as I enjoyed making it."
    counter3 = 0
    text3_type = False

    text4 = "You can learn Python, C or C++."
    counter4 = 0
    text4_type = False

    text5 = "And if you ever find yourself stuck or unsure how to do something, just ask Google."
    counter5 = 0
    text5_type = False

    text6 = "I lost count of how many times I did that while making this game! ;)"
    counter6 = 0
    text6_type = False

    text7 = "Remember, programming is all about experimenting and learning from mistakes."
    counter7 = 0
    text7_type = False

    text8 = "So don't worry if you don't get it right the first time-just keep trying!"
    counter8 = 0
    text8_type = False

    text10 = "And who knows? Maybe one day you'll be building your own games and applications!"
    counter10 = 0
    text10_type = False

    text11 = "So, let's dive in and see what you can do. Good luck, and most importantly-have fun!"
    counter11 = 0
    text11_type = False

    # Load background and title image
    background = pygame.image.load(PATH / "drawable" / "background.png")
    background = pygame.transform.scale(background, (1240, 620))
    big_title = pygame.image.load(PATH / "drawable" / "Code_Craft.png")
    big_title = pygame.transform.scale(big_title, (491, 127))

    # Fade-in control
    fade_alpha = 0  # Start with full transparency for big_title
    title_fade_in = False  # Track whether to start fading in big_title

    # Main loop
    while True:
        # Event handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Draw background with overlay
        window.blit(background, (0, 0))
        background_overlay = pygame.Surface((1240, 620), pygame.SRCALPHA)
        background_overlay.fill((0, 0, 0, 50))
        window.blit(background_overlay, (0, 0))

        # Text typing effect
        if counter1 < 4 * len(text1):
            counter1 += 1
        elif not title_fade_in:
            time.sleep(0.5)
            title_fade_in = True  # Start the fade-in animation for big_title once text is done

        # Render text gradually with the specified color (130, 130, 130)
        color = (194, 194, 194)

        render_text_with_background(text1[:counter1 // 4], (540, 20), minecraft_font_small, color)

        # Fade-in effect for big_title
        if title_fade_in:
            title_surface = big_title.copy()
            title_surface.set_alpha(fade_alpha)  # Set transparency
            window.blit(title_surface, (374, 60))

            # Gradually increase alpha until fully opaque
            if fade_alpha < 255:
                fade_alpha += 3  # Adjust for fade speed
            else:
                text2_type = True

        # Sequentially display each text with typing effect, adjusting Y positions for 45-pixel spacing
        if text2_type:
            if counter2 < 3 * len(text2):
                counter2 += 1
            else:
                text2_type = False
                text3_type = True
            render_text_with_background(text2[:counter2 // 3], (140, 200), minecraft_font_small, color)

        if text3_type:
            if counter3 < 3 * len(text3):
                counter3 += 1
            else:
                text3_type = False
                text4_type = True
            render_text_with_background(text3[:counter3 // 3], (140, 245), minecraft_font_small, color)  # 45 pixels below text2

        if text4_type:
            if counter4 < 3 * len(text4):
                counter4 += 1
            else:
                text4_type = False
                text5_type = True
            render_text_with_background(text4[:counter4 // 3], (140, 290), minecraft_font_small, color)  # 45 pixels below text3

        if text5_type:
            if counter5 < 3 * len(text5):
                counter5 += 1
            else:
                text5_type = False
                text6_type = True
            render_text_with_background(text5[:counter5 // 3], (140, 335), minecraft_font_small, color)  # 45 pixels below text4

        if text6_type:
            if counter6 < 3 * len(text6):
                counter6 += 1
            else:
                text6_type = False
                text7_type = True
            render_text_with_background(text6[:counter6 // 3], (140, 380), minecraft_font_small, color)  # 45 pixels below text5

        if text7_type:
            if counter7 < 3 * len(text7):
                counter7 += 1
            else:
                text7_type = False
                text8_type = True
            render_text_with_background(text7[:counter7 // 3], (140, 425), minecraft_font_small, color)  # 45 pixels below text6

        if text8_type:
            if counter8 < 3 * len(text8):
                counter8 += 1
            else:
                text8_type = False
                text10_type = True
            render_text_with_background(text8[:counter8 // 3], (140, 470), minecraft_font_small, color)  # 45 pixels below text7

        if text10_type:
            if counter10 < 3 * len(text10):
                counter10 += 1
            else:
                text10_type = False
                text11_type = True
            render_text_with_background(text10[:counter10 // 3], (140, 515), minecraft_font_small, color)  # 45 pixels below text8

        if text11_type:
            if counter11 < 3 * len(text11):
                counter11 += 1  
            render_text_with_background(text11[:counter11 // 3], (140, 560), minecraft_font_small, color)  # 45 pixels below text10

        # Update the display
        pygame.display.flip()
        clock.tick(60)

# Call the loading screen function
loading_screen()

# Call the display text function after loading
display_intro_text()

pygame.quit()
