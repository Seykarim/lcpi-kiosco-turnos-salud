import os
import sys
import time
import math

# Directo al Framebuffer de Linux si se ejecuta en la placa
if os.path.exists("/dev/fb0"):
    os.environ["SDL_FBDEV"] = "/dev/fb0"
    os.environ["SDL_VIDEODRIVER"] = "fbcon"

import pygame

# Inicialización de Pygame y Mezclador de Audio
pygame.init()
pygame.font.init()
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
    AUDIO_AVAILABLE = True
except Exception:
    AUDIO_AVAILABLE = False

# Dimensiones TFT 4.3" (480x272 px)
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 272

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if os.path.exists("/dev/fb0") else 0)
pygame.display.set_caption("Kiosco de Turnos IPS - Linux Embebido")
clock = pygame.time.Clock()

# Paleta de Colores
COLOR_BG          = (15, 23, 42)     # Slate 900
COLOR_CARD        = (30, 41, 59)     # Slate 800
COLOR_ACCENT      = (6, 182, 212)    # Cyan 500
COLOR_PRIORITY    = (239, 68, 68)    # Red 500
COLOR_TEXT_MAIN   = (241, 245, 249)  # Slate 100
COLOR_TEXT_MUTED  = (148, 163, 184)  # Slate 400

# Fuentes
try:
    font_large  = pygame.font.Font(None, 46)
    font_medium = pygame.font.Font(None, 26)
    font_small  = pygame.font.Font(None, 18)
except Exception:
    font_large  = pygame.font.SysFont("sans", 46)
    font_medium = pygame.font.SysFont("sans", 26)
    font_small  = pygame.font.SysFont("sans", 18)

# Función para Generar Tono de Alerta Auditiva
def play_chime():
    if not AUDIO_AVAILABLE:
        return
    try:
        sample_rate = 22050
        duration = 0.3
        n_samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(n_samples):
            # Tono dual armónico 880Hz (A5)
            t = float(i) / sample_rate
            val = int(16000 * math.sin(2.0 * math.pi * 880.0 * t) * math.exp(-i / (sample_rate * 0.1)))
            buf += val.to_bytes(2, byteorder='little', signed=True)
        sound = pygame.mixer.Sound(buffer=bytes(buf))
        sound.set_volume(0.8)
        sound.play()
    except Exception:
        pass

# Estado del Sistema de Turnos IPS
turno_preferencial = 1
turno_general = 12
es_prioritario = True
modulo_actual = 1

mensajes_educativos = [
    "Atención Prioritaria: Adultos mayores, embarazadas y personas con discapacidad.",
    "Recuerde presentar su documento de identidad original en la taquilla.",
    "Lave sus manos frecuentemente con agua y jabón.",
    "IPS Territorial: Garantizando atención digna y eficiente."
]
msg_index = 0
last_msg_time = time.time()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_p or event.key == pygame.K_1:
                # Avanzar Turno Preferencial
                turno_preferencial += 1
                es_prioritario = True
                play_chime()
            elif event.key == pygame.K_g or event.key == pygame.K_2:
                # Avanzar Turno General
                turno_general += 1
                es_prioritario = False
                play_chime()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click Táctil: Alternar turno según zona de toque
            x, y = event.pos
            if x < SCREEN_WIDTH // 2:
                turno_preferencial += 1
                es_prioritario = True
            else:
                turno_general += 1
                es_prioritario = False
            play_chime()

    # Rotación de mensajes
    if time.time() - last_msg_time > 6.0:
        msg_index = (msg_index + 1) % len(mensajes_educativos)
        last_msg_time = time.time()

    # Renderizado - Fondo
    screen.fill(COLOR_BG)

    # 1. Barra Superior de Estado
    pygame.draw.rect(screen, COLOR_CARD, (0, 0, SCREEN_WIDTH, 36))
    lbl_title = font_small.render("IPS TERRITORIAL - ATENCIÓN AL PACIENTE", True, COLOR_ACCENT)
    screen.blit(lbl_title, (12, 10))
    lbl_time = font_small.render(time.strftime("%H:%M:%S"), True, COLOR_TEXT_MUTED)
    screen.blit(lbl_time, (SCREEN_WIDTH - 75, 10))

    # 2. Tarjeta Principal: Turno Llamado
    pygame.draw.rect(screen, COLOR_CARD, (12, 46, 276, 168), border_radius=10)
    
    tipo_str = "PREFERENCIAL" if es_prioritario else "GENERAL"
    color_tipo = COLOR_PRIORITY if es_prioritario else COLOR_ACCENT
    lbl_tipo = font_small.render(f"TURNO ACTUAL [{tipo_str}]", True, color_tipo)
    screen.blit(lbl_tipo, (22, 56))

    num_str = f"P-{turno_preferencial:03d}" if es_prioritario else f"G-{turno_general:03d}"
    lbl_num = font_large.render(num_str, True, COLOR_TEXT_MAIN)
    screen.blit(lbl_num, (22, 85))

    lbl_mod = font_medium.render(f"Módulo: {modulo_actual:02d}", True, COLOR_ACCENT)
    screen.blit(lbl_mod, (22, 170))

    # 3. Tarjeta Secundaria: Próximos Turnos
    pygame.draw.rect(screen, COLOR_CARD, (298, 46, 170, 168), border_radius=10)
    lbl_sig = font_small.render("SIGUIENTES", True, COLOR_TEXT_MUTED)
    screen.blit(lbl_sig, (308, 56))

    lbl_p = font_medium.render(f"P-{(turno_preferencial + 1):03d}", True, COLOR_PRIORITY)
    screen.blit(lbl_p, (308, 90))
    lbl_p_tag = font_small.render("Preferencial", True, COLOR_TEXT_MUTED)
    screen.blit(lbl_p_tag, (308, 115))

    lbl_g = font_medium.render(f"G-{(turno_general + 1):03d}", True, COLOR_ACCENT)
    screen.blit(lbl_g, (308, 140))
    lbl_g_tag = font_small.render("General", True, COLOR_TEXT_MUTED)
    screen.blit(lbl_g_tag, (308, 165))

    # 4. Barra Inferior Ticker
    pygame.draw.rect(screen, COLOR_CARD, (0, 222, SCREEN_WIDTH, 50))
    lbl_tip = font_small.render(mensajes_educativos[msg_index], True, COLOR_TEXT_MAIN)
    screen.blit(lbl_tip, (12, 238))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
