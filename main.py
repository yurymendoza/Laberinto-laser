import pygame
import random
import sys
import time

# Inicializar pygame
pygame.init()

# Constantes generales
ANCHO = 800
ALTO = 600
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 128, 255)
VERDE = (0, 255, 0)

# Ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Fuga del Laberinto Láser")
clock = pygame.time.Clock()

# Imágenes / objetos básicos
jugador_img = pygame.Surface((50, 50))
jugador_img.fill(AZUL)

laser_img = pygame.Surface((10, 60))
laser_img.fill(ROJO)

# Variables globales
jugador = pygame.Rect(ANCHO//2 - 25, ALTO - 60, 50, 50)
lasers = []
puntaje = 0
record = 0
inicio_tiempo = 0
velocidad_laser = 5
frecuencia_laser = 20

# Funciones
def mover_jugador(teclas, jugador):
    if teclas[pygame.K_LEFT] and jugador.left > 0:
        jugador.x -= 6
    if teclas[pygame.K_RIGHT] and jugador.right < ANCHO:
        jugador.x += 6
    if teclas[pygame.K_UP] and jugador.top > 0:
        jugador.y -= 6
    if teclas[pygame.K_DOWN] and jugador.bottom < ALTO:
        jugador.y += 6

def generar_laser():
    if random.randint(1, frecuencia_laser) == 1:
        x = random.randint(0, ANCHO - 10)
        laser = pygame.Rect(x, -60, 10, 60)
        lasers.append(laser)

def mover_lasers():
    for laser in lasers[:]:
        laser.y += velocidad_laser
        if laser.top > ALTO:
            lasers.remove(laser)

def detectar_colision():
    for laser in lasers:
        if jugador.colliderect(laser):
            return True
    return False

def mostrar_texto(texto, size, x, y, color=BLANCO):
    fuente = pygame.font.SysFont(None, size)
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))

def menu_inicio():
    pantalla.fill(NEGRO)
    mostrar_texto("FUGA DEL LABERINTO LÁSER", 64, ANCHO//6, ALTO//4)
    mostrar_texto("Presiona ESPACIO para comenzar", 32, ANCHO//4 + 50, ALTO//2)
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                esperando = False

def game_over(puntaje_actual):
    global record
    pantalla.fill(NEGRO)
    if puntaje_actual > record:
        record = puntaje_actual
    mostrar_texto("¡GAME OVER!", 64, ANCHO//3, ALTO//3)
    mostrar_texto(f"Tiempo sobrevivido: {int(puntaje_actual)} seg", 32, ANCHO//4 + 30, ALTO//2 - 30)
    mostrar_texto(f"Récord: {int(record)} seg", 32, ANCHO//4 + 30, ALTO//2)
    mostrar_texto("Presiona R para reiniciar o ESC para salir", 28, ANCHO//5, ALTO//2 + 60)
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    main()
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    global lasers, jugador, puntaje, inicio_tiempo
    jugador.x = ANCHO//2 - 25
    jugador.y = ALTO - 60
    lasers = []
    puntaje = 0
    inicio_tiempo = time.time()

    ejecutando = True
    while ejecutando:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        mover_jugador(teclas, jugador)
        generar_laser()
        mover_lasers()

        puntaje = time.time() - inicio_tiempo

        if detectar_colision():
            game_over(puntaje)

        pantalla.fill(NEGRO)
        pantalla.blit(jugador_img, jugador)
        for laser in lasers:
            pantalla.blit(laser_img, laser)

        mostrar_texto(f"Tiempo: {int(puntaje)}", 28, 10, 10)
        mostrar_texto(f"Récord: {int(record)}", 28, 10, 40)

        pygame.display.flip()

# Iniciar juego
menu_inicio()
main()
