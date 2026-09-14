import os
import sys
import time

# Intentar dirigir la salida al Framebuffer de Linux si se ejecuta en la placa
if os.path.exists("/dev/fb0"):
    os.environ["SDL_FBDEV"] = "/dev/fb0"
    os.environ["SDL_VIDEODRIVER"] = "fbcon"

import pygame

# Inicialización de Pygame
pygame.init()
pygame.font.init()

# Dimensiones exactas de la pantalla TFT 4.3"
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 272

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if os.path.exists("/dev/fb0") else 0)
pygame.display.set_caption("Kiosco de Turnos IPS")
clock = pygame.time.Clock()

# Paleta de Colores (Diseño Industrial Slate/Cyan)
COLOR_BG          = (15, 23, 42)     # Slate 900
COLOR_CARD        = (30, 41, 59)     # Slate 800
COLOR_ACCENT      = (6, 182, 212)    # Cyan 500
COLOR_TEXT_MAIN   = (241, 245, 249)  # Slate 100
COLOR_TEXT_MUTED  = (148, 163, 184)  # Slate 400
COLOR_ALERT       = (234, 179, 8)    # Amber 500

# Fuentes del Sistema
try:
    font_large  = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 28)
    font_small  = pygame.font.Font(None, 20)
except Exception:
    font_large  = pygame.font.SysFont("sans", 48)
    font_medium = pygame.font.SysFont("sans", 28)
    font_small  = pygame.font.SysFont("sans", 20)

# Estado del Sistema de Turnos
turno_actual = 14
modulo_actual = 2
mensajes_educativos = [
    "Recuerde presentar su documento de identidad original.",
    "Lave sus manos frecuentemente y use tapabocas si presenta síntomas.",
    "IPS Territorial: Garantizando salud con dignidad y tecnología.",
    "Citas prioritarias para adultos mayores y mujeres embarazadas."
]
msg_index = 0
last_msg_time = time.time()

running = True
while running:
    # Manejo de Eventos (Teclado/Táctil/Cierre)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT:
                # Avanzar turno (Simulación de botón físico o táctil)
                turno_actual += 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click táctil en pantalla para avanzar turno
            turno_actual += 1

    # Rotación de mensajes educativos cada 6 segundos
    if time.time() - last_msg_time > 6.0:
        msg_index = (msg_index + 1) % len(mensajes_educativos)
        last_msg_time = time.time()

    # Renderizado - Fondo
    screen.fill(COLOR_BG)

    # 1. Encabezado Superior (Barra de Estado IPS)
    pygame.draw.rect(screen, COLOR_CARD, (0, 0, SCREEN_WIDTH, 40))
    lbl_title = font_small.render("IPS TERRITORIAL - GESTIÓN DE TURNOS", True, COLOR_ACCENT)
    screen.blit(lbl_title, (12, 12))
    
    lbl_time = font_small.render(time.strftime("%H:%M:%S"), True, COLOR_TEXT_MUTED)
    screen.blit(lbl_time, (SCREEN_WIDTH - 80, 12))

    # 2. Tarjeta Principal: Turno Actual
    pygame.draw.rect(screen, COLOR_CARD, (12, 50, 280, 160), border_radius=12)
    lbl_turno_txt = font_small.render("TURNO ACTUAL", True, COLOR_TEXT_MUTED)
    screen.blit(lbl_turno_txt, (24, 62))

    num_str = f"A-{turno_actual:03d}"
    lbl_num = font_large.render(num_str, True, COLOR_ACCENT)
    screen.blit(lbl_num, (24, 95))

    lbl_mod = font_medium.render(f"Módulo: {modulo_actual:02d}", True, COLOR_TEXT_MAIN)
    screen.blit(lbl_mod, (24, 165))

    # 3. Tarjeta Secundaria: Siguientes Turnos
    pygame.draw.rect(screen, COLOR_CARD, (302, 50, 166, 160), border_radius=12)
    lbl_sig = font_small.render("SIGUIENTES", True, COLOR_TEXT_MUTED)
    screen.blit(lbl_sig, (314, 62))

    for i in range(1, 4):
        next_str = f"A-{(turno_actual + i):03d}"
        lbl_next = font_medium.render(next_str, True, COLOR_TEXT_MAIN)
        screen.blit(lbl_next, (314, 85 + (i * 30)))

    # 4. Barra Inferior: Contenido Educativo de Salud (Ticker)
    pygame.draw.rect(screen, COLOR_CARD, (0, 222, SCREEN_WIDTH, 50))
    lbl_tip = font_small.render(mensajes_educativos[msg_index], True, COLOR_TEXT_MAIN)
    screen.blit(lbl_tip, (12, 238))

    pygame.display.flip()
    clock.tick(30) # 30 FPS suficiente y óptimo para ahorro de energía

pygame.quit()
sys.exit()
