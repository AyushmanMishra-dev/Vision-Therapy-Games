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
WHITE = (255, 255, 255)
ROAD_COLOR = (100, 100, 100)
BALL_COLOR = (0, 0, 255)
OBSTACLE_COLOR = (255, 0, 0)
FONT_NAME = 'Arial'

# Ball properties
ball_radius = 20
ball_x = 100
ball_y = HEIGHT - ball_radius * 2
ball_speed_x = 5
ball_speed_y = 0
gravity = 1
is_jumping = False
can_score = True

# Obstacle properties
obstacle_width = 40
obstacle_height = 40
obstacle_x = WIDTH
obstacle_y = HEIGHT - obstacle_height
obstacle_speed = 5

# Score
score = 0

# Timer
start_time = time.time()

# Camera properties
camera_x = 0
pygame.display.set_caption("Lazy Eye Therapy Game")
# Initialize the font
font = pygame.font.Font(None, 36)

def draw_ball(x, y):
    pygame.draw.circle(screen, BALL_COLOR, (x - camera_x, y), ball_radius)

def draw_obstacle(x, y):
    pygame.draw.rect(screen, OBSTACLE_COLOR, (x - camera_x, y, obstacle_width, obstacle_height))

def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def check_collision():
    global is_jumping, ball_y, ball_speed_y, score, can_score

    if ball_y >= HEIGHT - ball_radius * 2:
        ball_y = HEIGHT - ball_radius * 2
        ball_speed_y = 0
        is_jumping = False
        can_score = True

    if ball_x + ball_radius > obstacle_x and ball_x - ball_radius < obstacle_x + obstacle_width:
        if ball_y + ball_radius > obstacle_y:
            is_jumping = False
            if can_score:
                score -= 1
                can_score = False
        else:
            if can_score:
                score += 1
                can_score = False

    return False

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                ball_speed_y = -15

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    ball_speed_y += gravity

    # Update obstacle position
    obstacle_x -= obstacle_speed

    # Check for collision
    check_collision()

    # Reset obstacle when it goes off-screen
    if obstacle_x < camera_x:
        obstacle_x = camera_x + WIDTH
        obstacle_y = HEIGHT - obstacle_height
        can_score = True

    # Calculate camera position to keep the ball centered
    camera_x = ball_x - WIDTH // 2

    # Clear the screen
    screen.fill(BLACK)

    # Draw road
    pygame.draw.rect(screen, ROAD_COLOR, (0, HEIGHT - 100, WIDTH, 100))

    # Draw obstacle
    draw_obstacle(obstacle_x, obstacle_y)

    # Draw ball
    draw_ball(ball_x, ball_y)

    # Draw score
    draw_text("Score: " + str(score), 20, 20, WHITE)

    # Draw timer
    elapsed_time = time.time() - start_time
    draw_text("Time: {:.2f}".format(elapsed_time), 20, 60, WHITE)

    # Update the display
    pygame.display.update()
    clock.tick(60)

pygame.quit()
