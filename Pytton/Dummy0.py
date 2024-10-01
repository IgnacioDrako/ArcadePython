import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ancho_ventana = 900
alto_ventana = 700
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Space Invaders")

# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
MORADO = (255, 0, 255)
ROSA = (255, 0, 210)

# Contador de oleadas
oleada = 1
# Vidas
vidas = 3

# Clase del jugador
class Jugador:
    def __init__(self):
        self.imagen = pygame.Surface((20, 10))
        self.imagen.fill(VERDE)
        self.rect = self.imagen.get_rect()
        self.rect.center = (ancho_ventana // 2, alto_ventana - 50)

    def mover(self, dx):
        self.rect.x += dx
        # Limitar el movimiento dentro de la ventana
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > ancho_ventana - self.rect.width:
            self.rect.x = ancho_ventana - self.rect.width

    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

# Clase de las balas del jugador
class Bala:
    def __init__(self, x, y):
        self.imagen = pygame.Surface((5, 10))
        self.imagen.fill(AZUL)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.move_speed = 10

    def mover(self):
        self.rect.y -= self.move_speed

    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

# Clase de las balas enemigas
class BalaEnemiga:
    def __init__(self, x, y):
        self.imagen = pygame.Surface((5, 10))
        self.imagen.fill(ROSA)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.move_speed = 5

    def mover(self):
        self.rect.y += self.move_speed

    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

# Clase de los enemigos
class Enemigo:
    def __init__(self):
        self.imagen = pygame.Surface((50, 50))
        self.imagen.fill(ROJO)
        self.rect = self.imagen.get_rect()
        self.rect.x = random.randint(0, ancho_ventana - self.rect.width)
        self.rect.y = random.randint(50, 150)
        self.move_speed = 1  # Velocidad de movimiento hacia abajo
        self.tiempo_ultimo_disparo = 0
        self.cooldown_disparo = 2000  # Tiempo en milisegundos para disparar

    def mover(self, jugador, estado_juego):
        self.rect.y += self.move_speed  # Mover hacia abajo
        # Verificar si el enemigo ha llegado al final de la pantalla
        if self.rect.y > alto_ventana:
            estado_juego['perdido'] = True  # Marcar el juego como perdido
            estado_juego['corriendo'] = False  # Terminar el bucle del juego
            return True  # Retornar verdadero si ha llegado al final
        # Verificar colisión con el jugador
        if self.rect.colliderect(jugador.rect):
            estado_juego['perdido'] = True
            estado_juego['corriendo'] = False
        return False  # Retornar falso si no ha llegado al final ni ha colisionado

    def disparar(self):
        return BalaEnemiga(self.rect.centerx, self.rect.bottom)

    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

# Clase del jefe
class Jefe:
    def __init__(self):
        self.imagen = pygame.Surface((200, 50))
        self.imagen.fill(MORADO)
        self.rect = self.imagen.get_rect()
        self.rect.center = (ancho_ventana // 2, 50)
        self.hp = 500  # Puntos de vida del jefe
        self.tiempo_ultimo_disparo = 0
        self.cooldown_disparo = 1000  # Tiempo en milisegundos para disparar
        self.direccion = 1  # 1 para derecha, -1 para izquierda
        self.velocidad = 2  # Velocidad de movimiento del jefe

    def disparar(self):
        return BalaEnemiga(self.rect.centerx, self.rect.bottom)

    def mover(self):
        # Mover el jefe
        self.rect.x += self.direccion * self.velocidad
        # Cambiar de dirección si llega a los bordes de la ventana
        if self.rect.left < 0 or self.rect.right > ancho_ventana:
            self.direccion *= -1  # Cambiar dirección

    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

# Crear el jugador
jugador = Jugador()

# Función para crear enemigos
def crear_enemigos(cantidad):
    return [Enemigo() for _ in range(cantidad)]

# Crear enemigos
enemigos = crear_enemigos(5)
balas = []
balas_enemigas = []

# Variables para el disparo
tiempo_ultimo_disparo = 0
cooldown_disparo = 150  # Tiempo en milisegundos CHETOS

# Bucle principal del juego
estado_juego = {'corriendo': True, 'perdido': False}

# Configurar la fuente para el texto
fuente = pygame.font.Font(None, 36)  # Fuente predeterminada, tamaño 36

# Inicializar jefe como None
jefe = None

while estado_juego['corriendo']:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            estado_juego['corriendo'] = False

    # Manejo de teclas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        jugador.mover(-10)
    if teclas[pygame.K_RIGHT]:
        jugador.mover(10)
    if teclas[pygame.K_SPACE]:
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultimo_disparo >= cooldown_disparo:
            # Disparar una nueva bala
            balas.append(Bala(jugador.rect.centerx, jugador.rect.top))
            tiempo_ultimo_disparo = tiempo_actual  # Actualizar el tiempo del último disparo

    # Mover balas del jugador
    for bala in balas[:]:
        bala.mover()
        if bala.rect.y < 0:  # Eliminar balas que salen de la pantalla
            balas.remove(bala)

    # Mover balas enemigas
    for bala_enemiga in balas_enemigas[:]:
        bala_enemiga.mover()
        if bala_enemiga.rect.y > alto_ventana:  # Eliminar balas que salen de la pantalla
            balas_enemigas.remove(bala_enemiga)

    # Mover enemigos
    for enemigo in enemigos[:]:
        if enemigo.mover(jugador, estado_juego):  # Pasar el jugador y el estado del juego
            break  # Salir del bucle de enemigos si ha llegado el final

    # Colisión entre balas del jugador y enemigos
    for bala in balas:
        for enemigo in enemigos[:]:
            if bala.rect.colliderect(enemigo.rect):
                balas.remove(bala)
                enemigos.remove(enemigo)
                break  # Salir del bucle de enemigos cuando se colisiona con uno

    # Verificar si no hay enemigos
    if not enemigos:
        oleada += 1  # Incrementar oleada
        if (oleada % 5) == 0:
            vidas += 1  # Aumentar el número de vidas
        if oleada == 5:  # Si es la oleada 5, crear el jefe
            jefe = Jefe()
        else:
            enemigos = crear_enemigos(5 + oleada)  # Crear más enemigos

    # Disparar balas enemigas
    if jefe:
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - jefe.tiempo_ultimo_disparo >= (jefe.cooldown_disparo - (oleada * 50)):  # Aumentar la frecuencia de disparo
            balas_enemigas.append(jefe.disparar())
            jefe.tiempo_ultimo_disparo = tiempo_actual  # Actualizar el tiempo del último disparo

        # Mover el jefe si está en la oleada 15 o mayor
        if oleada >= 15:
            jefe.mover()

    # Disparar enemigos
    for enemigo in enemigos:
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - enemigo.tiempo_ultimo_disparo >= enemigo.cooldown_disparo:
            balas_enemigas.append(enemigo.disparar())
            enemigo.tiempo_ultimo_disparo = tiempo_actual  # Actualizar el tiempo del último disparo

    # Colisión entre balas enemigas y el jugador
    for bala_enemiga in balas_enemigas:
        if bala_enemiga.rect.colliderect(jugador.rect):
            vidas -= 1  # Restar una vida al jugador
            balas_enemigas.remove(bala_enemiga)  # Eliminar la bala enemiga que colisionó
            if vidas <= 0:  # El jugador ha perdido
                estado_juego['perdido'] = True  # El jugador pierde
                estado_juego['corriendo'] = False

    # Eliminar al jefe si su vida llega a 0
    if jefe and jefe.hp <= 0:
        jefe = None  # Eliminar al jefe
    # Dibujar todo
    ventana.fill(NEGRO)
    jugador.dibujar(ventana)
    for enemigo in enemigos:
        enemigo.dibujar(ventana)
    for bala in balas:
        bala.dibujar(ventana)
    for bala_enemiga in balas_enemigas:
        bala_enemiga.dibujar(ventana)

    # Dibujar el jefe si existe
    if jefe:
        jefe.dibujar(ventana)

    # Mostrar el número de oleadas y vidas en la parte superior
    texto_oleada = fuente.render(f'Oleada: {oleada}', True, AMARILLO)
    ventana.blit(texto_oleada, (10, 10))  # Dibujar el texto en la posición (10, 10)
    texto_vidas = fuente.render(f'Vidas: {vidas}', True, AMARILLO)
    ventana.blit(texto_vidas, (10, 40))  # Dibujar el texto en la posición (10, 40)

    # Actualizar la pantalla
    pygame.display.flip()
    # Controlar la velocidad de fotogramas
    pygame.time.Clock().tick(60)

# Mostrar mensaje de pérdida
if estado_juego['perdido']:
    print("¡Has perdido!")
pygame.quit()