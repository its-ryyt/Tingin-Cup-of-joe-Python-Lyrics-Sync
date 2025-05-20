import time
import threading
import pygame
import math
import os

# Lyrics with timestamps
lyrics = [
    (1.69, "Tingin - Cup of Joe"),
    (5.69, "Dahan-dahan lang sa gitna man ng daan"),
    (9.54, "Mga saglit na inilikha"),
    (13.39, "Kakaiba ang tama"),
    (17.87, "Ng sinag sa 'yong kutis na kayumanggi"),
    (23.08, "Oh, sa'n ba 'ko dinadala?"),
    (27.58, "Bawat ngiting biglaang nabura"),
    (31.70, "Iyong naipinta"),
    (36.03, "Hiwaga ng 'yong tingin, nang-aalipin"),
    (41.37, "Kahit sa'n man madala"),
    (46.16, "'Di pinapansin, ingay sa tabi"),
    (50.56, "Magulong kapaligiran, sa 'yo lang ang tingin"),
    (55.31, "'Di pinapansin, ika'y paiikutin"),
    (60.14, "Nang dahan-dahan lang sa gitna man ng daan"),
    (65.32, "Sa bawat sandaling ikaw ay pinagmamasdan"),
    (69.87, "May dumadapong kiliti na 'di maunawaan"),
    (74.51, "Walang imik, 'di mabanggit na sa aking isip"),
    (78.05, "Ikaw lang ang nagmamarka"),
    (83.28, "Kahit mabitin aking salita"),
    (87.73, "Mata'y ibinubunyag na"),
    (90.99, "Sa 'yo lang magpapaangkin, 'di palalampasin"),
    (96.05, "'Wag ka sanang kumawala"),
    (101.56, "'Di mawawala"),
    (105.51, "'Di pinapansin, ingay sa tabi"),
    (110.08, "Magulong kapaligiran, sa 'yo lang ang tingin"),
    (114.67, "'Di pinapansin, ako'y paiikutin"),
    (119.49, "Nang dahan-dahan lang sa gitna man ng daan"),
    (124.22, "Oh"),
    (128.91, "Oh"),
    (133.52, "Oh"),
    (138.30, "Oh"),
    (142.96, "'Di man alam ang darating"),
    (147.63, "Sa dulo at sa gitna ng dilim"),
    (152.23, "Sa liwanag mo nakatingin"),
    (156.45, "Sa 'yo nakatingin, sa 'yo lang ang tingin"),
    (161.40, "'Di man alam ang darating"),
    (166.01, "Sa dulo at sa gitna ng dilim"),
    (170.44, "Sa liwanag mo nakatingin"),
    (174.80, "Sa 'yo nakatingin, sa 'yo lang ang tingin"),
    (183.24, "'Di pinapansin, ingay sa tabi"),
    (187.72, "Magulong kapaligiran, sa 'yo lang ang tingin"),
    (192.27, "'Di pinapansin, ika'y paiikutin"),
    (197.21, "Nang dahan-dahan lang (dahan-dahan lang) sa gitna man ng daan"),
    (201.53, "'Di pinapansin, ingay sa tabi"),
    (206.02, "Magulong kapaligiran, sa 'yo lang ang tingin"),
    (210.53, "'Di pinapansin, ika'y paiikutin"),
    (215.61, "Nang dahan-dahan lang sa gitna man ng daan"),
    (219.32, "Thanks for watching!"),
    (224.32, "Please like and follow for more!"),
]

# File paths
MUSIC_PATH = r"D:\PYTHON - Songs\Tingin-Cup of Joe\mp3\Tingin.mp3"
BG_IMAGE_PATH = r"D:\PYTHON - Songs\Tingin-Cup of Joe\bg\bg.jpg"

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1000, 300), pygame.RESIZABLE)
pygame.display.set_caption("Tingin - Cup of Joe")

# Fonts and colors
font = pygame.font.SysFont("Arial", 24)
TEXT_COLOR = (255, 255, 255)
CHAR_DELAY = 0.05
OVERLAY_ALPHA = 190

# Load background image
if os.path.exists(BG_IMAGE_PATH):
    background_raw = pygame.image.load(BG_IMAGE_PATH).convert()
else:
    raise FileNotFoundError("Background image not found at specified path.")

def draw_overlay(surface, alpha=240):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    surface.blit(overlay, (0, 0))

def draw_wave_text_centered(surface, text, start_time, current_time):
    elapsed = current_time - start_time
    amplitude = 12
    y_base = surface.get_height() // 2

    # Word wrap
    words = text.split()
    lines = []
    line = ""
    max_width = surface.get_width() * 0.9  # 90% width

    for word in words:
        test_line = line + " " + word if line else word
        test_width = font.size(test_line)[0]
        if test_width <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)

    total_height = len(lines) * font.get_height()
    y = y_base - total_height // 2

    for line_text in lines:
        x = (surface.get_width() - font.size(line_text)[0]) // 2
        for i, char in enumerate(line_text):
            char_elapsed = elapsed - i * CHAR_DELAY
            if char_elapsed < 0:
                offset_y = 0
            elif char_elapsed < 0.3:
                offset_y = -math.sin(char_elapsed * math.pi / 0.3) * amplitude
            else:
                offset_y = 0
            char_surf = font.render(char, True, TEXT_COLOR)
            surface.blit(char_surf, (x, y + offset_y))
            x += char_surf.get_width()
        y += font.get_height()

def draw_play_button(surface):
    w, h = surface.get_size()
    center = (w // 2, h // 2)
    size = 40
    points = [
        (center[0] - size // 2, center[1] - size),
        (center[0] - size // 2, center[1] + size),
        (center[0] + size, center[1])
    ]
    pygame.draw.polygon(surface, TEXT_COLOR, points)

    return pygame.Rect(center[0] - size // 2, center[1] - size, size + size // 2, size * 2)

def wait_for_play_button():
    global screen
    global play_button_rect
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return

        window_width, window_height = screen.get_size()
        bg_scaled = pygame.transform.smoothscale(background_raw, (window_width, window_height))
        screen.blit(bg_scaled, (0, 0))
        draw_overlay(screen, OVERLAY_ALPHA)
        play_button_rect = draw_play_button(screen)
        pygame.display.flip()
        clock.tick(60)

def play_music():
    pygame.mixer.music.load(MUSIC_PATH)
    pygame.mixer.music.play()

def sync_lyrics():
    global screen
    start_time = time.time()
    lyric_index = 0
    clock = pygame.time.Clock()
    running = True

    while running and lyric_index < len(lyrics):
        current_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
                return
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        timestamp, line = lyrics[lyric_index]
        if current_time >= timestamp:
            next_timestamp = lyrics[lyric_index + 1][0] if lyric_index + 1 < len(lyrics) else timestamp + 5
            line_start_time = time.time()
            while time.time() - start_time < next_timestamp and running:
                now = time.time()
                window_width, window_height = screen.get_size()
                bg_scaled = pygame.transform.smoothscale(background_raw, (window_width, window_height))
                screen.blit(bg_scaled, (0, 0))
                draw_overlay(screen, OVERLAY_ALPHA)
                draw_wave_text_centered(screen, line, line_start_time, now)
                pygame.display.flip()
                clock.tick(60)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.mixer.music.stop()
                        return
                    elif event.type == pygame.VIDEORESIZE:
                        screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            lyric_index += 1
        else:
            window_width, window_height = screen.get_size()
            bg_scaled = pygame.transform.smoothscale(background_raw, (window_width, window_height))
            screen.blit(bg_scaled, (0, 0))
            draw_overlay(screen, OVERLAY_ALPHA)
            pygame.display.flip()
            clock.tick(60)

def main():
    wait_for_play_button()
    threading.Thread(target=play_music).start()
    sync_lyrics()
    pygame.quit()

if __name__ == "__main__":
    main()