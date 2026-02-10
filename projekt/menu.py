<<<<<<< HEAD
import pygame
import sys
# Ponecháno, i když v tomto souboru nevidíme definici game_loop
from main import game_loop 
=======
import tkinter as tk
import random
import math
import time
>>>>>>> 0a4f2d9 (pokus)

WIDTH, HEIGHT = 1920, 1080
PARTICLE_COUNT = 1000
FOV = 500

<<<<<<< HEAD
# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 200, 0) # Přidáno pro stav zvuku
=======
PASTEL_COLORS = [
    "#FFB6C1","#FFA07A","#E0FFFF","#FFFACD","#D8BFD8",
    "#B0E0E6","#98FB98","#FFD700","#FF69B4","#BA55D3"
]
>>>>>>> 0a4f2d9 (pokus)

WORDS = [
    "BUMBAC", "TWINK", "CHAOS", "BLINK", "OMG", "LOL", "PULSE", 
    "FIRE", "WTF", "BOOM", "PSYCHO", "FREAK", "HYPE", "MADNESS"
]

class Particle:
    __slots__ = ['x','y','z','dx','dy','dz','size','color']
    def __init__(self):
        self.x = random.uniform(-WIDTH/2, WIDTH/2)
        self.y = random.uniform(-HEIGHT/2, HEIGHT/2)
        self.z = random.uniform(50,2000)
        self.dx = random.uniform(-6,6)
        self.dy = random.uniform(-6,6)
        self.dz = random.uniform(-12,12)
        self.size = random.uniform(2,5)
        self.color = random.choice(PASTEL_COLORS)

<<<<<<< HEAD
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
=======
    def update(self, mouse):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz

        if self.z < 50: self.z = 2000
        if self.z > 2000: self.z = 50

        if mouse:
            mx,my = mouse
            self.dx += (mx - WIDTH/2 - self.x)/600
            self.dy += (my - HEIGHT/2 - self.y)/600

        self.color = random.choice(PASTEL_COLORS)

    def project(self):
        f = FOV / (FOV + self.z)
        return WIDTH/2 + self.x*f, HEIGHT/2 + self.y*f, self.size*f*2

class TextChaos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes("-fullscreen", True)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.particles = [Particle() for _ in range(PARTICLE_COUNT)]
        self.mouse = None
        self.start = time.time()

        self.bind("<Motion>", self.mouse_move)
        self.bind("<Escape>", lambda e:self.quit())

        self.loop()

    def mouse_move(self,e):
        self.mouse = (e.x, e.y)

    def loop(self):
        t = time.time() - self.start

        delay = random.choice([16, 24, 33, 40])
        self.canvas.configure(bg=random.choice(["#FFE4E1","#FFF0F5","#E6E6FA","#F0FFF0","#FFFFE0"]))
        self.canvas.delete("all")

        jitter_x = random.randint(-15,15)
        jitter_y = random.randint(-15,15)

        # PARTICLES
        for p in self.particles:
            p.update(self.mouse)
            x,y,s = p.project()
            self.canvas.create_rectangle(
                x+jitter_x, y+jitter_y,
                x+s+jitter_x, y+s+jitter_y,
                fill=p.color, outline=""
            )
            # Mirror
            self.canvas.create_rectangle(
                WIDTH-x, y,
                WIDTH-x+s, y+s,
                fill=p.color, outline=""
            )
            self.canvas.create_rectangle(
                x, HEIGHT-y,
                x+s, HEIGHT-y+s,
                fill=p.color, outline=""
            )

            # TEXT EVERYWHERE
            if random.random() < 0.1:
                word = random.choice(WORDS)
                self.canvas.create_text(
                    x+jitter_x+random.randint(-20,20),
                    y+jitter_y+random.randint(-20,20),
                    text=word,
                    fill=random.choice(PASTEL_COLORS),
                    font=("Arial", random.randint(10,30), "bold")
                )

        # Abstract neon walls
        for _ in range(30):
            x1 = random.randint(0, WIDTH)
            y1 = random.randint(0, HEIGHT)
            x2 = x1 + random.randint(-50,50)
            y2 = y1 + random.randint(-50,50)
            self.canvas.create_line(x1, y1, x2, y2, fill=random.choice(PASTEL_COLORS), width=2)

        # Floating rainbow chaotic title
        size = int(40 + math.sin(t*4)*30)
        self.canvas.create_text(
            WIDTH/2 + math.sin(t*2)*250,
            120 + math.cos(t*3)*60,
            text="TWINK TEXT CHAOS – BUMBAC MODE",
            fill=random.choice(PASTEL_COLORS),
            font=("Arial", size, "bold")
        )

        # BUMBAC EFFECT: big random flash + text spam
        if random.random() < 0.05:
            self.canvas.create_rectangle(0,0,WIDTH,HEIGHT, fill=random.choice(["#FFFFFF","#F0F8FF","#FFFACD"]), outline="")
            for _ in range(50):
                self.canvas.create_text(
                    random.randint(0,WIDTH),
                    random.randint(0,HEIGHT),
                    text=random.choice(WORDS),
                    fill=random.choice(PASTEL_COLORS),
                    font=("Arial", random.randint(10,40), "bold")
                )

        self.after(delay, self.loop)
>>>>>>> 0a4f2d9 (pokus)

if __name__ == "__main__":
    TextChaos().mainloop()
