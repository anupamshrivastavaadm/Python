import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# Clock for controlling FPS
clock = pygame.time.Clock()

# Player settings
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 7

# Enemy settings
enemy_size = 50
enemy_speed = 5
enemies = []

# Score
score = 0
font = pygame.font.SysFont("Arial", 24)

def drop_enemies(enemy_list):
    """Spawn enemies randomly at the top."""
    if len(enemy_list) < 10 and random.random() < 0.03:
        x_pos = random.randint(0, WIDTH - enemy_size)
        enemy_list.append([x_pos, 0])

def draw_enemies(enemy_list):
    for enemy in enemy_list:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
    """Move enemies down and remove those off screen."""
    for enemy in enemy_list[:]:
        if enemy[1] >= 0 and enemy[1] < HEIGHT:
            enemy[1] += enemy_speed
        else:
            enemy_list.remove(enemy)
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    """Check for collisions between enemies and player."""
    px, py = player_pos
    for ex, ey in enemy_list:
        if (ex < px < ex + enemy_size or ex < px + player_size < ex + enemy_size) and \
           (ey < py < ey + player_size < ey + enemy_size or ey < py < ey + player_size):
            return True
    return False

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # Enemy logic
    drop_enemies(enemies)
    score = update_enemy_positions(enemies, score)

    # Collision
    if collision_check(enemies, (player_x, player_y)):
        print(f"Game Over! Final Score: {score}")
        pygame.quit()
        sys.exit()

    # Draw player & enemies
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    draw_enemies(enemies)

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display & tick
    pygame.display.flip()
    clock.tick(30)
