import pygame
import sys
import random
import math
import os

pygame.init()

# === OKNO ===
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animace pohybu + dash")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# === FUNKCE NAČTENÍ ANIMACÍ ===
def load_animation(path):
    frames = []
    if not os.path.exists(path):
        return frames
    for filename in sorted(os.listdir(path)):
        if filename.endswith(".png"):
            frame = pygame.image.load(os.path.join(path, filename)).convert_alpha()
            frames.append(frame)
    return frames

# === NAČTENÍ ANIMACÍ ===
animations = {
    "up": load_animation("C:/Users/tomas/Desktop/programecko/projekt/assets/Hráč nahoru"),
    "down": load_animation("C:/Users/tomas/Desktop/programecko/projekt/assets/Hráč dolu"),
    "left": load_animation("C:/Users/tomas/Desktop/programecko/projekt/assets/Hráč nalevo"),
    "right": load_animation("C:/Users/tomas/Desktop/programecko/projekt/assets/Hráč napravo"),
    "idle": load_animation("C:/Users/tomas/Desktop/programecko/projekt/assets/Hráč Idle")
}

# === HRÁČ ===
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
dash_distance = 200
dash_cooldown = 1000
last_dash_time = -dash_cooldown

direction = "down"
state = "idle"
current_frame = 0
frame_delay = 100
last_frame_update = pygame.time.get_ticks()

# === ENEMIES ===
enemy_size = 40
enemies = []
enemy_spawn_delay = 1000
last_spawn_time = pygame.time.get_ticks()
enemy_speed = 2

# === TEXT ===
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()
running = True
def update_animation():
    global current_frame, last_frame_update
    now = pygame.time.get_ticks()
    if now - last_frame_update > frame_delay:
        frames = animations.get(direction, [])
        if len(frames) > 0:
            current_frame = (current_frame + 1) % len(frames)
        last_frame_update = now
    
# === HLAVNÍ SMYČKA ===
while running:
    current_time = pygame.time.get_ticks()

    # --- Události ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Pohyb hráče ---
    keys = pygame.key.get_pressed()
    moving = False
    dx, dy = 0, 0
    old_direction = direction

    if keys[pygame.K_a]:
        dx -= 1
        moving = True
    if keys[pygame.K_d]:
        dx += 1
        moving = True
    if keys[pygame.K_w]:
        dy -= 1
        moving = True
    if keys[pygame.K_s]:
        dy += 1
        moving = True

    # Normalizace diagonálního pohybu
    if dx != 0 or dy != 0:
        length = math.hypot(dx, dy)
        dx, dy = dx / length, dy / length
        player_x += dx * player_speed
        player_y += dy * player_speed

    # --- Výběr směru animace ---
    if moving:
        if abs(dx) >= abs(dy):
            direction = "right" if dx > 0 else "left"
        else:
            direction = "down" if dy > 0 else "up"
        state = "walk"
    else:
        state = "idle"

    # Reset snímku při změně směru
    if direction != old_direction:
        current_frame = 0

    # --- DASH ---
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0] and current_time - last_dash_time >= dash_cooldown:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dash_dx = mouse_x - player_x
        dash_dy = mouse_y - player_y
        distance = math.hypot(dash_dx, dash_dy)
        if distance != 0:
            dash_dx, dash_dy = dash_dx / distance, dash_dy / distance
            start_x, start_y = player_x, player_y
            player_x += dash_dx * dash_distance
            player_y += dash_dy * dash_distance
            last_dash_time = current_time

            # Omez hráče na obrazovku
            player_x = max(0, min(WIDTH - 64, player_x))
            player_y = max(0, min(HEIGHT - 64, player_y))

            # Dash zóna zabíjí enemy
            dash_rect = pygame.Rect(min(start_x, player_x), min(start_y, player_y),
                                    abs(player_x - start_x) + 64,
                                    abs(player_y - start_y) + 64)

            for enemy in enemies[:]:
                if dash_rect.colliderect(enemy['rect']):
                    enemies.remove(enemy)

    # --- OMEZENÍ POHYBU ---
    player_x = max(0, min(WIDTH - 64, player_x))
    player_y = max(0, min(HEIGHT - 64, player_y))

    # --- SPAWN ENEMY ---
    if current_time - last_spawn_time > enemy_spawn_delay:
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            x = random.randint(0, WIDTH - enemy_size)
            y = -enemy_size
        elif side == 'bottom':
            x = random.randint(0, WIDTH - enemy_size)
            y = HEIGHT
        elif side == 'left':
            x = -enemy_size
            y = random.randint(0, HEIGHT - enemy_size)
        else:
            x = WIDTH
            y = random.randint(0, HEIGHT - enemy_size)
        enemies.append({'rect': pygame.Rect(x, y, enemy_size, enemy_size)})
        last_spawn_time = current_time

    # === VYKRESLENÍ ===
    screen.fill(WHITE)

    # --- ANIMACE PODLE STAVU (idle / walk) ---
    if state == "idle":
        idle_frames = animations.get("idle", [])
        if idle_frames:
            image = idle_frames[min(current_frame, len(idle_frames) - 1)]
        else:
            image = animations[direction][0]
    else:
        update_animation()
        image = animations[direction][current_frame]

    player_rect = pygame.Rect(player_x, player_y, image.get_width(), image.get_height())
    screen.blit(image, (player_x, player_y))

    # --- ENEMY POHYB ---
    for enemy in enemies[:]:
        enemy_rect = enemy['rect']
        ex, ey = player_x - enemy_rect.x, player_y - enemy_rect.y
        dist = math.hypot(ex, ey)
        if dist != 0:
            ex, ey = ex / dist, ey / dist
        enemy_rect.x += ex * enemy_speed
        enemy_rect.y += ey * enemy_speed

        pygame.draw.rect(screen, BLUE, enemy_rect)

        if player_rect.colliderect(enemy_rect):
            print("Game Over!")
            running = False

    # --- DASH COOLDOWN ---
    time_since_dash = max(0, dash_cooldown - (current_time - last_dash_time))
    cooldown_text = font.render(f"Dash cooldown: {time_since_dash//1000 + 1}s", True, (0, 0, 0))
    screen.blit(cooldown_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
