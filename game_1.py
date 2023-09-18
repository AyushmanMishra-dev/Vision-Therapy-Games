#in this game choose the blue box with transparency effect
import pygame
import pygame_gui
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)  # Black background
SHAPE_COLOR = (0, 0, 255)     # Blue shape color
DISTRACTION_COLOR = (255, 0, 0)  # Red distraction color
SHAPE_SIZE = 50
DISTRACTION_COUNT = 10
DISTRACTION_MIN_DISTANCE = SHAPE_SIZE * 2  # Minimum distance between distractions

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Amblyopia Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Create a UI manager
ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Create a slider for setting transparency
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((WIDTH // 4, HEIGHT - 50), (WIDTH // 2, 20)),
    start_value=255,  # Initial transparency (255 is fully opaque)
    value_range=(0, 255),  # Transparency range
    manager=ui_manager
)

# Font for displaying the score and time
font = pygame.font.Font(None, 36)

def create_shape(transparency):
    x = random.randint(0, WIDTH - SHAPE_SIZE)
    y = random.randint(0, HEIGHT - SHAPE_SIZE)
    shape_surface = pygame.Surface((SHAPE_SIZE, SHAPE_SIZE), pygame.SRCALPHA)
    shape_color_with_transparency = (0, 0, 255, transparency)
    pygame.draw.rect(shape_surface, shape_color_with_transparency, (0, 0, SHAPE_SIZE, SHAPE_SIZE))
    return shape_surface, pygame.Rect(x, y, SHAPE_SIZE, SHAPE_SIZE)

def create_distraction(distractions):
    while True:
        x = random.randint(0, WIDTH - SHAPE_SIZE)
        y = random.randint(0, HEIGHT - SHAPE_SIZE)
        rect = pygame.Rect(x, y, SHAPE_SIZE, SHAPE_SIZE)

        # Check if the new distraction has enough space between existing distractions
        if all(rect.colliderect(existing) is False for existing in distractions):
            distractions.append(rect)  # Add the new distraction to the list
            return rect, distractions

def main():
    running = True
    game_started = False
    transparency = 255  # Initial transparency
    score = 0  # Initial score
    start_time = None

    shape_to_trace, shape_rect = None, None
    distractions = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle UI events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_started and shape_rect.collidepoint(event.pos):
                    score += int(transparency / 10)  # Increase score based on transparency
                    shape_to_trace, shape_rect = create_shape(transparency)
                elif slider.rect.collidepoint(event.pos):
                    # If the slider is clicked, start the timer and the game
                    game_started = True
                    shape_to_trace, shape_rect = create_shape(transparency)
                    distractions = []
                    score = 0  # Reset score when starting a new game
                    start_time = time.time()

            if game_started:
                ui_manager.process_events(event)

        screen.fill(BACKGROUND_COLOR)

        if game_started:
            # Create distractions as needed
            while len(distractions) < DISTRACTION_COUNT:
                new_distraction, distractions = create_distraction(distractions)
                pygame.draw.rect(screen, DISTRACTION_COLOR, new_distraction)

            # Draw the shape to be traced
            screen.blit(shape_to_trace, shape_rect)

            # Display the score and time
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (20, 20))

            if start_time:
                elapsed_time = int(time.time() - start_time)
                time_text = font.render(f"Time: {elapsed_time} sec", True, (255, 255, 255))
                screen.blit(time_text, (WIDTH - 200, 20))

        # Draw the UI elements
        ui_manager.update(1 / 60)
        ui_manager.draw_ui(screen)

        # Update transparency based on the slider value
        transparency = int(slider.get_current_value())

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
