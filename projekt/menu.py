import pygame
import sys
from main import game_loop

# Inicializace Pygame
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu s hover efektem")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GRAY = (150, 150, 150)

# Font
font = pygame.font.SysFont(None, 60)

# Položky menu
menu_items = ["Start", "Options", "Quit"]

# Funkce pro vykreslení menu s hover efektem
def draw_menu(mouse_pos):
    screen.fill(BLACK)
    for i, item in enumerate(menu_items):
        text = font.render(item, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 80))
        if text_rect.collidepoint(mouse_pos):
            text = font.render(item, True, BLUE)
        screen.blit(text, text_rect)
    pygame.display.update()

# Hlavní smyčka menu
def main_menu():
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        draw_menu(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, item in enumerate(menu_items):
                    text = font.render(item, True, WHITE)
                    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 80))
                    if text_rect.collidepoint(mouse_pos):
                        if item == "Quit":
                            pygame.quit()
                            sys.exit()
                        elif item == "Start":
                            game_loop()  # spustí hru
                        elif item == "Options":
                            screen.fill(BLACK)

if __name__ == "__main__":
    main_menu()