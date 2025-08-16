import pygame
import random
import sys
import colorsys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Stones - Retro Gradient Edition")

# Clock
clock = pygame.time.Clock()

# Player settings
player_size = 50
player_speed = 8

# Enemy settings
enemy_size = 50
boss_size = 100

# Fonts
retro_font = pygame.font.SysFont("Courier New", 28, bold=True)
title_font = pygame.font.SysFont("Courier New", 40, bold=True)

# High score tracker
high_score = 0

# Gradient settings
gradient_speed = 0.00005  # slower background hue shift

def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r*255), int(g*255), int(b*255)

def get_gradient_colors(time):
    hue_top = (time * gradient_speed) % 1.0
    hue_bottom = (hue_top + 0.1) % 1.0
    top_color = hsv_to_rgb(hue_top, 0.5, 0.7)
    bottom_color = hsv_to_rgb(hue_bottom, 0.5, 0.7)
    return top_color, bottom_color

def draw_gradient(top_color, bottom_color):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_player(x, y):
    pygame.draw.rect(screen, (0, 0, 0), (x + player_size//4, y + player_size//3, player_size//2, player_size//1.5))
    pygame.draw.circle(screen, (255, 255, 255), (x + player_size//2, y + player_size//4), player_size//4)

def drop_enemies(enemy_list, spawn_chance, level):
    if len(enemy_list) < 12 and random.random() < spawn_chance:
        x_pos = random.randint(0, WIDTH - enemy_size)
        enemy_list.append([x_pos, 0, enemy_size, "normal"])  # type: normal

    # Boss every 5 levels
    if level % 5 == 0 and not any(e[-1] == "boss" for e in enemy_list):
        x_pos = random.randint(0, WIDTH - boss_size)
        enemy_list.append([x_pos, 0, boss_size, "boss"])

def draw_enemies(enemy_list):
    for enemy in enemy_list:
        color = (50, 50, 50) if enemy[3] == "normal" else (200, 0, 0)
        pygame.draw.ellipse(screen, color, (enemy[0], enemy[1], enemy[2], enemy[2]-10))

def update_enemy_positions(enemy_list, score, speed):
    for enemy in enemy_list[:]:
        if 0 <= enemy[1] < HEIGHT:
            enemy[1] += speed if enemy[3] == "normal" else speed * 0.7  # boss slower
        else:
            enemy_list.remove(enemy)
            if enemy[3] == "normal":
                score += 1
    return score

def collision_check(enemy_list, player_pos):
    px, py = player_pos
    for ex, ey, size, typ in enemy_list:
        if (ex < px < ex + size or ex < px + player_size < ex + size) and \
           (ey < py < ey + player_size < ey + size or ey < py < ey + player_size):
            return True
    return False

def get_player_name():
    player_name = ""
    input_active = True
    while input_active:
        top_color, bottom_color = get_gradient_colors(pygame.time.get_ticks())
        draw_gradient(top_color, bottom_color)
        title = title_font.render("Enter Your Name", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        name_display = retro_font.render(player_name, True, (255, 255, 255))
        screen.blit(name_display, (WIDTH//2 - name_display.get_width()//2, HEIGHT//2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name.strip() != "":
                    return player_name
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 12 and event.unicode.isprintable():
                    player_name += event.unicode

def start_screen():
    while True:
        top_color, bottom_color = get_gradient_colors(pygame.time.get_ticks())
        draw_gradient(top_color, bottom_color)

        # Game title
        title1 = title_font.render("Dodge", True, (255, 255, 255))
        title2 = title_font.render("the Falling", True, (255, 255, 255))
        title3 = title_font.render("Stones", True, (255, 255, 255))
        screen.blit(title1, (WIDTH//2 - title1.get_width()//2, HEIGHT//3 - 60))
        screen.blit(title2, (WIDTH//2 - title2.get_width()//2, HEIGHT//3))
        screen.blit(title3, (WIDTH//2 - title3.get_width()//2, HEIGHT//3 + 60))

        # Author tag
        author_text = retro_font.render("@CODEWITHAS_31", True, (255, 255, 255))
        screen.blit(author_text, (WIDTH//2 - author_text.get_width()//2, HEIGHT//3 + 150))

        # Start prompt
        prompt_text = retro_font.render("Press ENTER to Start", True, (255, 255, 255))
        screen.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, HEIGHT//3 + 220))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def game_over_screen(score, player_name):
    global high_score
    if score > high_score:
        high_score = score
    while True:
        top_color, bottom_color = get_gradient_colors(pygame.time.get_ticks())
        draw_gradient(top_color, bottom_color)
        over_text = title_font.render("GAME OVER", True, (255, 255, 255))
        score_text = retro_font.render(f"{player_name}'s Score: {score}", True, (255, 255, 255))
        high_score_text = retro_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        restart1 = retro_font.render("Press R to Restart", True, (255, 255, 255))
        restart2 = retro_font.render("or", True, (255, 255, 255))
        restart3 = retro_font.render("Q to Quit", True, (255, 255, 255))
        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//3))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
        screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 10))
        screen.blit(restart1, (WIDTH//2 - restart1.get_width()//2, HEIGHT//2 + 80))
        screen.blit(restart2, (WIDTH//2 - restart2.get_width()//2, HEIGHT//2 + 110))
        screen.blit(restart3, (WIDTH//2 - restart3.get_width()//2, HEIGHT//2 + 140))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    return

# --- Main Program ---
start_screen()
player_name = get_player_name()

while True:
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 10
    enemies = []
    score = 0
    level = 1
    enemy_speed = 6  # slower speed
    spawn_chance = 0.04  # lower spawn chance

    running = True
    while running:
        # Background
        current_time = pygame.time.get_ticks()
        top_color, bottom_color = get_gradient_colors(current_time)
        draw_gradient(top_color, bottom_color)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Level logic
        level = score // 20 + 1
        enemy_speed = 6 + (level - 1) * 0.3
        spawn_chance = 0.04 + (level - 1) * 0.005

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        # Enemies
        drop_enemies(enemies, spawn_chance, level)
        score = update_enemy_positions(enemies, score, enemy_speed)

        # Collision
        if collision_check(enemies, (player_x, player_y)):
            game_over_screen(score, player_name)
            running = False

        # Draw
        draw_player(player_x, player_y)
        draw_enemies(enemies)

        # HUD
        score_text = retro_font.render(f"Score: {score}", True, (255, 255, 255))
        high_text = retro_font.render(f"High: {high_score}", True, (255, 255, 255))
        level_text = retro_font.render(f"Level: {level}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(high_text, (10, 40))
        screen.blit(level_text, (10, 70))

        pygame.display.flip()
        clock.tick(30)
