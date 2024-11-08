import pygame
import random

# Inicializar Pygame
pygame.init()

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (213, 50, 80)
verde = (0, 255, 0)
azul = (50, 153, 213)
amarillo = (255, 255, 0)

# Dimensiones de la pantalla
anchoPantalla = 1000
largoPantalla = 1000

# Dimensiones de la cuadrícula
tamanoCuadro = 35
anchoCuadricula = 10  # 10 cuadros de ancho
largoCuadricula = 20  # 20 cuadros de largo

# Calcular el desplazamiento para centrar la cuadrícula
offsetX = (anchoPantalla - (anchoCuadricula * tamanoCuadro)) // 2
offsetY = (largoPantalla - (largoCuadricula * tamanoCuadro)) // 2

# Configuración de la pantalla
pantalla = pygame.display.set_mode((anchoPantalla, largoPantalla))
pygame.display.set_caption('Tetris')

# Reloj para controlar la velocidad del juego
reloj = pygame.time.Clock()

# Definir las formas del Tetris
formas = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]]  # J
]

# Crear la cuadrícula
cuadricula = [[negro for _ in range(anchoCuadricula)] for _ in range(largoCuadricula)]

# Clase para manejar los bloques
class Bloque:
    def __init__(self):
        self.forma = random.choice(formas)
        self.color = random.choice([rojo, verde, azul, amarillo])
        self.pos_x = anchoCuadricula // 2 - len(self.forma[0]) // 2
        self.pos_y = 0

    def dibujar(self):
        for y, fila in enumerate(self.forma):
            for x, valor in enumerate(fila):
                if valor:
                    pygame.draw.rect(pantalla, self.color, (offsetX + (self.pos_x + x) * tamanoCuadro, offsetY + (self.pos_y + y) * tamanoCuadro, tamanoCuadro, tamanoCuadro), 0)
                    pygame.draw.rect(pantalla, blanco, (offsetX + (self.pos_x + x) * tamanoCuadro, offsetY + (self.pos_y + y) * tamanoCuadro, tamanoCuadro, tamanoCuadro), 1)

    def mover(self, dx, dy):
        nueva_pos_x = self.pos_x + dx
        nueva_pos_y = self.pos_y + dy

        # Verificar límites horizontales
        if nueva_pos_x < 0 or nueva_pos_x + len(self.forma[0]) > anchoCuadricula:
            return

        # Verificar límites verticales y colisiones con bloques anteriores
        if nueva_pos_y + len(self.forma) > largoCuadricula or self.colision(nueva_pos_x, nueva_pos_y):
            if dy > 0:  # Si el movimiento es hacia abajo y hay colisión, fijar el bloque
                self.fijar()
                return False
            return

        self.pos_x = nueva_pos_x
        self.pos_y = nueva_pos_y
        return True

    def rotar(self):
        nueva_forma = [list(row) for row in zip(*self.forma[::-1])]
        # Verificar que la rotación no salga de los límites y no colisione
        if self.pos_x + len(nueva_forma[0]) <= anchoCuadricula and self.pos_y + len(nueva_forma) <= largoCuadricula and not self.colision(self.pos_x, self.pos_y, nueva_forma):
            self.forma = nueva_forma

    def colision(self, pos_x, pos_y, forma=None):
        if forma is None:
            forma = self.forma
        for y, fila in enumerate(forma):
            for x, valor in enumerate(fila):
                if valor and (pos_y + y >= largoCuadricula or cuadricula[pos_y + y][pos_x + x] != negro):
                    return True
        return False

    def fijar(self):
        for y, fila in enumerate(self.forma):
            for x, valor in enumerate(fila):
                if valor:
                    cuadricula[self.pos_y + y][self.pos_x + x] = self.color
        eliminar_lineas_completas()

# Función para dibujar la cuadrícula
def dibujar_cuadricula():
    for y in range(largoCuadricula):
        for x in range(anchoCuadricula):
            pygame.draw.rect(pantalla, cuadricula[y][x], (offsetX + x * tamanoCuadro, offsetY + y * tamanoCuadro, tamanoCuadro, tamanoCuadro), 0)
            pygame.draw.rect(pantalla, blanco, (offsetX + x * tamanoCuadro, offsetY + y * tamanoCuadro, tamanoCuadro, tamanoCuadro), 1)

# Función para eliminar líneas completas
def eliminar_lineas_completas():
    global puntos
    lineas_completas = 0
    for y in range(largoCuadricula):
        if all(cuadricula[y][x] != negro for x in range(anchoCuadricula)):
            del cuadricula[y]
            cuadricula.insert(0, [negro for _ in range(anchoCuadricula)])
            lineas_completas += 1
    puntos += lineas_completas * 100

# Función principal del juego
def juego():
    global puntos
    puntos = 0
    game_over = False
    bloque = Bloque()  # Generar el primer bloque

    def nuevo_bloque():
        nonlocal bloque
        bloque = Bloque()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            bloque.mover(-1, 0)
        if keys[pygame.K_RIGHT]:
            bloque.mover(1, 0)
        if keys[pygame.K_DOWN]:
            if not bloque.mover(0, 1):
                nuevo_bloque()
        if keys[pygame.K_UP]:
            bloque.rotar()

        pantalla.fill(negro)
        dibujar_cuadricula()
        bloque.dibujar()
        pygame.display.update()
        reloj.tick(30)

    pygame.quit()

# Iniciar el juego
juego()