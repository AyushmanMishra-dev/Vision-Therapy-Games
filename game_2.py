import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)       # Black background
OBJECT_COLOR = (255, 0, 0)         # Blue objects
CHARACTER_COLOR = (0, 0, 255)      # Black character
OBSTACLE_COLOR = (255, 255, 255)   # Red obstacles
TEXT_COLOR = (255, 255, 255)       # White text
OBJECT_SIZE = 30
CHARACTER_SIZE = 50
FONT_SIZE = 36

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lazy Eye Therapy Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()
def create_object():
    x = random.randint(0, WIDTH - OBJECT_SIZE)
    y = 0
    return pygame.Rect(x, y, OBJECT_SIZE, OBJECT_SIZE)

def display_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main():
    running = True
    objects = []

    character_x = (WIDTH - CHARACTER_SIZE) // 2
    character_y = HEIGHT - CHARACTER_SIZE

    score = 0

    # Start the timer
    start_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Move the character left and right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character_x -= 5
        if keys[pygame.K_RIGHT]:
            character_x += 5

        # Create falling objects
        if len(objects) < 5:
            objects.append(create_object())

        # Update object positions
        for obj in objects:
            obj.y += 5

        # Check for collisions and update score
        for obj in objects:
            if obj.colliderect((character_x, character_y, CHARACTER_SIZE, CHARACTER_SIZE)):
                score += 1
                objects.remove(obj)

            if obj.y > HEIGHT:
                objects.remove(obj)

        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, CHARACTER_COLOR, (character_x, character_y, CHARACTER_SIZE, CHARACTER_SIZE))
        for obj in objects:
            pygame.draw.rect(screen, OBJECT_COLOR, obj)

        # Display the score and time taken
        elapsed_time = int(time.time() - start_time)
        display_text(f"Score: {score}", FONT_SIZE, TEXT_COLOR, WIDTH // 2, 20)
        display_text(f"Time: {elapsed_time} seconds", FONT_SIZE, TEXT_COLOR, WIDTH // 2, 60)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print(f"Game Over! Score: {score}, Time Taken: {elapsed_time} seconds")

if __name__ == "__main__":
    main()
