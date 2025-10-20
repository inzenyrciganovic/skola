import pygame
import sys

# Inicializace
pygame.init()

# Okno
WIDTH, HEIGHT = 1600, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Hry")

# Barvy
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# Font
FONT = pygame.font.Font(None, 60)

# FPS
clock = pygame.time.Clock()
FPS = 60


# ======================
#  TŘÍDA TLAČÍTKA
# ======================
class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.hovered = False

    def draw(self, screen):
        color = BLUE if self.hovered else GRAY
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=10)

        text_surface = FONT.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.callback()


# ======================
#  FUNKCE PRO HRY A MENU
# ======================
def start_game():
    """Spustí hru se skákáním po plošinách."""
    cube_size = 50
    player_x, player_y = 100, HEIGHT - cube_size - 20
    vy = 0
    speed = 7
    gravity = 0.8
    jump = -18
    on_ground = False

    # Plošiny
    platforms = [
        pygame.Rect(0, HEIGHT - 20, WIDTH, 20),       # zem
        pygame.Rect(300, 700, 300, 20),
        pygame.Rect(700, 600, 300, 20),
        pygame.Rect(1100, 500, 200, 20),
    ]

    # Cíl
    finish = pygame.Rect(1200, 450 - cube_size, cube_size, cube_size)

    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_running = False
        if keys[pygame.K_a]:
            player_x -= speed
        if keys[pygame.K_d]:
            player_x += speed
        if keys[pygame.K_SPACE] and on_ground:
            vy = jump
            on_ground = False

        # Gravitační logika
        vy += gravity
        if vy > 25:  # omezíme maximální pádovou rychlost
            vy = 25
        player_y += vy

        # Omezíme hráče uvnitř okna
        player_x = max(0, min(player_x, WIDTH - cube_size))
        if player_y > HEIGHT - cube_size:
            player_y = HEIGHT - cube_size
            vy = 0
            on_ground = True

        # Kontrola kolizí s plošinami
        on_ground = False
        player_rect = pygame.Rect(player_x, player_y, cube_size, cube_size)
        for plat in platforms:
            if player_rect.colliderect(plat):
                if vy >= 0 and player_rect.bottom - plat.top <= vy + 1:
                    player_y = plat.top - cube_size
                    vy = 0
                    on_ground = True
                    player_rect.y = player_y

        # Kontrola kolize s cílem
        if player_rect.colliderect(finish):
            SCREEN.fill(WHITE)
            win_text = FONT.render("Vyhrál jsi!", True, GREEN)
            rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            SCREEN.blit(win_text, rect)
            pygame.display.flip()
            pygame.time.delay(2000)
            game_running = False

        # Vykreslení
        SCREEN.fill(WHITE)
        for plat in platforms:
            pygame.draw.rect(SCREEN, DARK_GRAY, plat)
        pygame.draw.rect(SCREEN, RED, player_rect)
        pygame.draw.rect(SCREEN, GREEN, finish)

        info_text = pygame.font.Font(None, 36).render("Stiskni ESC pro návrat do menu", True, BLACK)
        SCREEN.blit(info_text, (20, 20))

        pygame.display.flip()
        clock.tick(FPS)


def open_settings():
    settings_running = True

    def close_settings():
        nonlocal settings_running
        settings_running = False

    back_button = Button("Back", WIDTH // 2 - 150, 400, 300, 80, close_settings)

    while settings_running:
        SCREEN.fill(DARK_GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            back_button.check_event(event)

        settings_text = FONT.render("Settings Menu", True, WHITE)
        text_rect = settings_text.get_rect(center=(WIDTH // 2, 150))
        SCREEN.blit(settings_text, text_rect)
        back_button.draw(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)


def exit_game():
    pygame.quit()
    sys.exit()


# ======================
#  HLAVNÍ MENU
# ======================
buttons = [
    Button("Start", WIDTH // 2 - 150, 200, 300, 80, start_game),
    Button("Settings", WIDTH // 2 - 150, 320, 300, 80, open_settings),
    Button("Exit", WIDTH // 2 - 150, 440, 300, 80, exit_game),
]

running = True
while running:
    SCREEN.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.check_event(event)
    for button in buttons:
        button.draw(SCREEN)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
