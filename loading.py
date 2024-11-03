import pygame
from pathlib import Path

# Paths and initialization
PATH = Path.cwd()
pygame.init()

# Screen and font setup
window = pygame.display.set_mode((1240, 620))
pygame.display.set_caption("Code_Craft")
pygame.display.set_icon(pygame.image.load(PATH / "drawable" / "crafting_table.png"))
clock = pygame.time.Clock()

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

# Call the loading screen function
loading_screen()

# After loading is done, continue with the rest of your program
# For example, you can start your main game loop here
# ...

pygame.quit()
