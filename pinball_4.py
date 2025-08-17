import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()

# Screen settings (9:16 aspect ratio)
WIDTH, HEIGHT = 450, 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pinball Game")

# Fonts and colors
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 48)
title_font = pygame.font.SysFont("Arial", 60, bold=True)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Global variables
high_score_file = "highscore.txt"
player_name = ""
level = 1
score = 0
high_score = 0

# Load high score
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as f:
        try:
            high_score = int(f.read().split(',')[1])
        except:
            high_score = 0

# Paddle settings
paddle_width = 100
paddle_height = 15
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 50
paddle_speed = 10

# Ball template
ball_radius = 10
initial_ball_speed = 5

# Game states
game_state = "home"  # home, name_input, instructions, playing, game_over

# Ball list
balls = []

def draw_text(text, font, color, x, y, center=False):
    render = font.render(text, True, color)
    rect = render.get_rect()
    if center:
        rect.center = (x, y)
        screen.blit(render, rect)
    else:
        screen.blit(render, (x, y))

def draw_gradient_background(top_color, bottom_color):
    """Draw a vertical gradient background"""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def show_home_screen():
    draw_gradient_background((0, 50, 100), (0, 0, 0))
    draw_text("Pinball", title_font, YELLOW, WIDTH//2, HEIGHT//3, center=True)
    draw_text("A Retro Game is Back", big_font, WHITE, WIDTH//2, HEIGHT//3 + 100, center=True)
    draw_text("Press ENTER to Start", font, GREEN, WIDTH//2, HEIGHT//2 + 150, center=True)
    draw_text("@codewithas_31", font, WHITE, WIDTH//2, HEIGHT-50, center=True)
    pygame.display.flip()

def show_instructions():
    draw_gradient_background((0, 50, 100), (0, 0, 0))
    instructions = [
        "Instructions:",
        "- Use LEFT and RIGHT arrows to move paddle",
        "- Keep the balls in play",
        "- Score points by bouncing balls",
        "- Each 50 points -> level up (new balls spawn, speed increases)",
        "- Press R to restart or Q to quit",
        "",
        "Press any key to start..."
    ]
    for i, line in enumerate(instructions):
        draw_text(line, font, WHITE, 20, 50 + i*40)
    pygame.display.flip()

def game_over_screen():
    draw_gradient_background((100, 0, 50), (0, 0, 0))
    draw_text("GAME OVER", title_font, RED, WIDTH//2, HEIGHT//3, center=True)
    draw_text(f"Score: {score}", big_font, WHITE, WIDTH//2, HEIGHT//2, center=True)
    draw_text(f"High Score: {high_score}", font, YELLOW, WIDTH//2, HEIGHT//2 + 60, center=True)
    draw_text("Press R to Restart or Q to Quit", font, GREEN, WIDTH//2, HEIGHT//2 + 120, center=True)
    pygame.display.flip()

def save_high_score():
    global high_score
    if score > high_score:
        high_score = score
        with open(high_score_file, "w") as f:
            f.write(f"{player_name},{high_score}")

def create_ball():
    """Create a new ball with random initial direction"""
    angle = random.choice([-1, 1])
    ball = {
        "x": WIDTH // 2,
        "y": HEIGHT // 2,
        "dx": initial_ball_speed * angle,
        "dy": -initial_ball_speed,
        "hit": False  # collision flag
    }
    return ball

def reset_game():
    global balls, level, score, paddle_x
    balls = [create_ball()]
    level = 1
    score = 0
    paddle_x = WIDTH // 2 - paddle_width // 2

# Start with one ball
reset_game()

# Main game loop
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "home":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "name_input"
        elif game_state == "name_input":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = "instructions"
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 10:
                        player_name += event.unicode
        elif game_state == "instructions":
            if event.type == pygame.KEYDOWN:
                game_state = "playing"
        elif game_state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    initial_ball_speed = 5
                    reset_game()
                    game_state = "playing"
                elif event.key == pygame.K_q:
                    running = False

    keys = pygame.key.get_pressed()
    if game_state == "playing":
        # Move paddle
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
            paddle_x += paddle_speed

        # Update all balls
        for ball in balls[:]:
            ball["x"] += ball["dx"]
            ball["y"] += ball["dy"]

            # Collisions with walls
            if ball["x"] <= 0 or ball["x"] >= WIDTH - ball_radius:
                ball["dx"] *= -1
            if ball["y"] <= 0:
                ball["dy"] *= -1

            # Paddle collision
            if paddle_y < ball["y"] + ball_radius < paddle_y + paddle_height and paddle_x < ball["x"] < paddle_x + paddle_width:
                if not ball["hit"]:
                    ball["dy"] *= -1
                    score += 10
                    ball["hit"] = True
            else:
                ball["hit"] = False

            # Ball falls below paddle
            if ball["y"] >= HEIGHT - ball_radius:
                balls.remove(ball)

        # Level up every 50 points
        new_level = score // 50 + 1
        if new_level > level:
            level = new_level
            # Spawn new balls equal to current level-1
            for _ in range(level - 1):
                new_ball = create_ball()
                # Slight random direction for each new ball
                new_ball["dx"] = random.choice([-1, 1]) * (initial_ball_speed + 1)
                new_ball["dy"] = -initial_ball_speed
                balls.append(new_ball)
            # Increase speed slightly
            initial_ball_speed += 1
            # Update all balls' speed
            for ball in balls:
                ball["dx"] = (ball["dx"]/abs(ball["dx"])) * initial_ball_speed
                ball["dy"] = (ball["dy"]/abs(ball["dy"])) * initial_ball_speed

        # Check game over
        if len(balls) == 0:
            save_high_score()
            game_state = "game_over"

        # Draw paddle
        pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
        # Draw all balls
        for ball in balls:
            pygame.draw.circle(screen, RED, (int(ball["x"]), int(ball["y"])), ball_radius)

        # Draw score and info
        draw_text(f"Player: {player_name}", font, WHITE, 10, 10)
        draw_text(f"Score: {score}", font, WHITE, 10, 40)
        draw_text(f"High Score: {high_score}", font, WHITE, 10, 70)
        draw_text(f"Level: {level}", font, WHITE, WIDTH-150, 10)
        draw_text(f"Balls: {len(balls)}", font, WHITE, WIDTH-150, 40)

    elif game_state == "home":
        show_home_screen()
    elif game_state == "name_input":
        draw_gradient_background((0, 50, 100), (0, 0, 0))
        draw_text("Enter Your Name:", big_font, WHITE, WIDTH//2, HEIGHT//3, center=True)
        draw_text(player_name, big_font, GREEN, WIDTH//2, HEIGHT//2, center=True)
        pygame.display.flip()
    elif game_state == "instructions":
        show_instructions()
    elif game_state == "game_over":
        game_over_screen()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
