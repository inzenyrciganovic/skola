import pygame
import sys
# Ponecháno, i když v tomto souboru nevidíme definici game_loop
from main import game_loop 

# Inicializace Pygame
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu s hover efektem")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 200, 0) # Přidáno pro stav zvuku

# Font
font = pygame.font.SysFont(None, 60)

# Položky menu
menu_items = ["Start", "Options", "Quit"]

# Globální nastavení (musí být globální pro použití v obou funkcích)
sound_enabled = True 

# Funkce pro vykreslení menu s hover efektem
def draw_menu(mouse_pos):
    screen.fill(BLACK)
    for i, item in enumerate(menu_items):
        text = font.render(item, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 80))
        if text_rect.collidepoint(mouse_pos):
            text = font.render(item, True, RED)
        screen.blit(text, text_rect)
    pygame.display.update()

# --- NOVÁ FUNKCE PRO NASTAVENÍ ---

def options_menu():
    """Vstupní bod a smyčka pro obrazovku nastavení."""
    global sound_enabled
    options_running = True
    
    while options_running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Vykreslení nastavení
        screen.fill(BLACK)
        
        # --- Položka Zvuk ---
        sound_status = "ZAPNUTO" if sound_enabled else "VYPNUTO"
        sound_label = font.render("Zvuk:", True, WHITE)
        sound_label_rect = sound_label.get_rect(center=(WIDTH // 2 - 100, HEIGHT // 2 - 40))
        
        sound_text = font.render(sound_status, True, (GREEN if sound_enabled else RED))
        sound_rect = sound_text.get_rect(center=(WIDTH // 2 + 100, HEIGHT // 2 - 40))
        
        # Hover efekt na ovládací prvky
        is_hovering_sound = sound_label_rect.collidepoint(mouse_pos) or sound_rect.collidepoint(mouse_pos)
        if is_hovering_sound:
            sound_text = font.render(sound_status, True, RED)
            
        screen.blit(sound_label, sound_label_rect)
        screen.blit(sound_text, sound_rect)
        
        # --- Položka Zpět ---
        back_text = font.render("Zpět do menu", True, WHITE)
        back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        
        # Hover efekt
        if back_rect.collidepoint(mouse_pos):
            back_text = font.render("Zpět do menu", True, BLUE)
            
        screen.blit(back_text, back_rect)
        
        pygame.display.update()

        # Zpracování událostí v nastavení
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                # Kontrola kliknutí na Zvuk
                if sound_label_rect.collidepoint(mouse_pos) or sound_rect.collidepoint(mouse_pos):
                    sound_enabled = not sound_enabled # Přepnutí stavu
                    print(f"Zvuk přepnut na: {'ZAPNUTO' if sound_enabled else 'VYPNUTO'}")
                
                # Kontrola kliknutí na Zpět
                elif back_rect.collidepoint(mouse_pos):
                    options_running = False # Ukončí smyčku a vrátí se do main_menu
            
            # Návrat pomocí ESC
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                options_running = False
                
# --- KONEC FUNKCE PRO NASTAVENÍ ---

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
                            # 💡 Zde voláme novou funkci pro nastavení
                            options_menu() 
                            # Po návratu z options_menu se automaticky pokračuje ve smyčce main_menu
                            print("Návrat z nastavení do menu.")

if __name__ == "__main__":
    main_menu()