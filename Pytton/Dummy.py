import pygame
import time
import random

pygame.init()
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (213, 50, 80)
verde = (0, 255, 0)
azul = (50, 153, 213)
ancho_pantalla = 800
alto_pantalla = 800
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Serpiente Game")
reloj = pygame.time.Clock()
tamaño_snake = 10
velocidad_snake = 20
fuente = pygame.font.SysFont("bahnschrift", 25)

def mostrar_puntaje(puntaje):
    valor = fuente.render("Puntaje: " + str(puntaje), True, azul)
    pantalla.blit(valor, [0, 0])

def dibujar_snake(tamaño_snake, lista_snake):
    for x in lista_snake:
        pygame.draw.rect(pantalla, verde, [x[0], x[1], tamaño_snake, tamaño_snake])

def juego():
    game_over = False
    game_cerrado = False
    x_snake = ancho_pantalla / 2
    y_snake = alto_pantalla / 2
    x_cambio = 0
    y_cambio = 0
    lista_snake = []
    largo_snake = 1
    x_comida = round(random.randrange(0, ancho_pantalla - tamaño_snake) / 10.0) * 10.0
    y_comida = round(random.randrange(0, alto_pantalla - tamaño_snake) / 10.0) * 10.0
    
    while not game_over:
        while game_cerrado:
            pantalla.fill(negro)
            mensaje = fuente.render(" C para jugar de nuevo  Q para salir", True, rojo)
            pantalla.blit(mensaje, [ancho_pantalla / 6, alto_pantalla / 3])
            mostrar_puntaje(largo_snake - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_cerrado = False
                    if event.key == pygame.K_c:
                        juego()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_cambio = -tamaño_snake
                    y_cambio = 0
                elif event.key == pygame.K_RIGHT:
                    x_cambio = tamaño_snake
                    y_cambio = 0
                elif event.key == pygame.K_UP:
                    y_cambio = -tamaño_snake
                    x_cambio = 0
                elif event.key == pygame.K_DOWN:
                    y_cambio = tamaño_snake
                    x_cambio = 0
        
        if x_snake >= ancho_pantalla or x_snake < 0 or y_snake >= alto_pantalla or y_snake < 0:
            game_cerrado = True
        
        x_snake += x_cambio
        y_snake += y_cambio
        pantalla.fill(negro)
        pygame.draw.rect(pantalla, rojo, [x_comida, y_comida, tamaño_snake, tamaño_snake])
        cabeza_snake = []
        cabeza_snake.append(x_snake)
        cabeza_snake.append(y_snake)
        lista_snake.append(cabeza_snake)
        
        if len(lista_snake) > largo_snake:
            del lista_snake[0]
        
        for segmento in lista_snake[:-1]:
            if segmento == cabeza_snake:
                game_cerrado = True
        
        dibujar_snake(tamaño_snake, lista_snake)
        mostrar_puntaje(largo_snake - 1)
        pygame.display.update()
        
        if x_snake == x_comida and y_snake == y_comida:
            x_comida = round(random.randrange(0, ancho_pantalla - tamaño_snake) / 10.0) * 10.0
            y_comida = round(random.randrange(0, alto_pantalla - tamaño_snake) / 10.0) * 10.0
            largo_snake += 1
            #velocidad_snake += 1 
        reloj.tick(velocidad_snake +1)
    
    pygame.quit()
    quit()
juego()