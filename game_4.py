#aligning the red line to blue line and score is recorded when the red line is clicked
import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
FULLSCREEN = False
if FULLSCREEN:
    WIDTH, HEIGHT = pygame.display.list_modes()[0]
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BUTTON_COLOR = (128, 128, 128)
LINE_WIDTH = 10
LINE_LENGTH = 300

# Calculate positions for centered blue line
blue_line_x = (WIDTH - LINE_LENGTH) // 2
blue_line_y = (HEIGHT - LINE_WIDTH) // 2

# Initialize the position of the red line
red_line_x = random.randint(0, WIDTH - LINE_LENGTH)
red_line_y = random.randint(0, HEIGHT - LINE_WIDTH)

# Score
score = 0

# Timer
start_time = None

# Initialize the font
font = pygame.font.Font(None, 36)
pygame.display.set_caption("Amblyopia Game")
def draw_lines():
    pygame.draw.rect(screen, BLUE, (blue_line_x, blue_line_y, LINE_LENGTH, LINE_WIDTH))
    pygame.draw.rect(screen, RED, (red_line_x, red_line_y, LINE_LENGTH, LINE_WIDTH))

def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

done_button_x = WIDTH - 120
done_button_y = HEIGHT - 50
done_button_width = 100
done_button_height = 40

done_button_rect = pygame.Rect(done_button_x, done_button_y, done_button_width, done_button_height)
done_button_clicked = False

red_line_clicked = False

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if done_button_rect.collidepoint(event.pos):
                if not red_line_clicked:
                    done_button_clicked = True
                    score += 1  # Increase the score by 1 when the button is clicked

                    if (blue_line_x <= red_line_x <= blue_line_x + LINE_LENGTH or
                        blue_line_x <= red_line_x + LINE_LENGTH <= blue_line_x + LINE_LENGTH) and \
                       (blue_line_y <= red_line_y <= blue_line_y + LINE_WIDTH or
                        blue_line_y <= red_line_y + LINE_WIDTH <= blue_line_y + LINE_WIDTH):
                        if start_time is None:
                            start_time = time.time()
                        elif time.time() - start_time <= 5:
                            score += 5
                        red_line_x = random.randint(0, WIDTH - LINE_LENGTH)
                        red_line_y = random.randint(0, HEIGHT - LINE_WIDTH)
                        start_time = None
                else:
                    done_button_clicked = False
            elif (red_line_x <= event.pos[0] <= red_line_x + LINE_LENGTH and
                  red_line_y <= event.pos[1] <= red_line_y + LINE_WIDTH):
                red_line_clicked = not red_line_clicked
                done_button_clicked = False

    if red_line_clicked:
        red_line_x, red_line_y = pygame.mouse.get_pos()

    # Clear the screen
    screen.fill(BLACK)

    # Draw lines
    draw_lines()

    # Draw score
    draw_text("Score: " + str(score), 20, 20, WHITE)

    # Draw Done button
    pygame.draw.rect(screen, BUTTON_COLOR, done_button_rect)
    draw_text("Done", done_button_x + 30, done_button_y + 10, WHITE)

    # Update the display
    pygame.display.update()
    clock.tick(60)

pygame.quit()
