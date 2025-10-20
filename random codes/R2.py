import pygame
import sys

pygame.init()

# Okno
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dash Die Repeat Demo")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)
GRAY = (180, 180, 180)
GREEN = (0, 200, 0)

# Font
FONT = pygame.font.Font(None, 36)

# FPS
clock = pygame.time.Clock()
FPS = 60

# ======================
#  Hráč
# ======================
class Player:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = False
        self.dash_cooldown = 0
        self.dash_power = 15
        self.size = size

    def handle_input(self, keys):
        self.vx = 0
        if keys[pygame.K_a]:
            self.vx = -self.speed
        if keys[pygame.K_d]:
            self.vx = self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False
        if keys[pygame.K_LSHIFT] and self.dash_cooldown == 0:
            if keys[pygame.K_a]:
                self.vx = -self.dash_power
            elif keys[pygame.K_d]:
                self.vx = self.dash_power
            self.dash_cooldown = 20  # frames cooldown

    def apply_gravity(self):
        self.vy += self.gravity
        if self.vy > 25:
            self.vy = 25
        self.rect.y += self.vy

    def move_horizontal(self):
        self.rect.x += self.vx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def update_dash(self):
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

# ======================
#  Platformy a hazardy
# ======================
platforms = [
    pygame.Rect(0, HEIGHT-20, WIDTH, 20),
    pygame.Rect(200, 450, 200, 20),
    pygame.Rect(500, 350, 200, 20),
    pygame.Rect(700, 250, 100, 20),
]

hazards = [
    pygame.Rect(400, HEIGHT-30, 50, 20),
    pygame.Rect(650, HEIGHT-30, 50, 20)
]

finish = pygame.Rect(750, 200, 50, 50)

# ======================
#  Hlavní smyčka hry
# ======================
def game_loop():
    player = Player(50, HEIGHT-70, 25)
    best_time = None
    start_time = pygame.time.get_ticks()
    
    running = True
    while running:
        dt = clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if keys[pygame.K_r]:  # restart level
                return game_loop()

        # ---- Hráč ----
        player.handle_input(keys)
        player.apply_gravity()
        player.move_horizontal()
        player.update_dash()

        # ---- Kolize s platformami ----
        player.on_ground = False
        for plat in platforms:
            if player.rect.colliderect(plat) and player.vy >= 0:
                if player.rect.bottom - plat.top <= player.vy + 1:
                    player.rect.bottom = plat.top
                    player.vy = 0
                    player.on_ground = True

        # ---- Smrt (hazard) ----
        dead = False
        if player.rect.top > HEIGHT:
            dead = True
        for hazard in hazards:
            if player.rect.colliderect(hazard):
                dead = True
        if dead:
            return game_loop()  # okamžitý respawn

        # ---- Cíl ----
        if player.rect.colliderect(finish):
            elapsed_time = (pygame.time.get_ticks() - start_time)/1000
            if best_time is None or elapsed_time < best_time:
                best_time = elapsed_time
            pygame.time.delay(500)
            return game_loop()

        # ---- Čas ----
        elapsed_time = (pygame.time.get_ticks() - start_time)/1000

        # ---- Vykreslení ----
        SCREEN.fill(WHITE)
        for plat in platforms:
            pygame.draw.rect(SCREEN, GRAY, plat)
        for hazard in hazards:
            pygame.draw.rect(SCREEN, RED, hazard)
        pygame.draw.rect(SCREEN, BLUE, player.rect)
        pygame.draw.rect(SCREEN, GREEN, finish)

        time_text = FONT.render(f"Time: {elapsed_time:.2f}s", True, BLACK)
        SCREEN.blit(time_text, (10,10))
        if best_time:
            best_text = FONT.render(f"Best: {best_time:.2f}s", True, BLACK)
            SCREEN.blit(best_text, (10, 40))

        pygame.display.flip()

# ======================
# Spuštění hry pouze pokud je main.py spuštěn přímo
# ======================
if __name__ == "__main__":
    game_loop()
