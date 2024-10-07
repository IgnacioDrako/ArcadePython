import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ancho_ventana = 1900
alto_ventana = 1020
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
BLANCO = (255, 255, 255)
naranga = (255, 134, 51)

# Contador de oleadas
oleada = 1
# Vidas
vidas = 100

# Clase del jugador
class Jugador:
    def __init__(self):
        self.imagen = pygame.Surface((20, 10))
        self.imagen.fill(VERDE)
        self.rect = self.imagen.get_rect()
        self.rect.center = (ancho_ventana // 2, alto_ventana - 50)
        self.cooldown_disparo = 250  # Cooldown del disparo del jugador
        self.tiempo_ultimo_disparo = 0  # Inicializar tiempo del último disparo
        self.tiempo_invulnerable = 0  # Inicializar tiempo de invulnerabilidad

    def mover(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(self.rect.x, ancho_ventana - self.rect.width))

    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

# Clase de las balas del jugador
class Bala:
    def __init__(self, x, y):
        self.imagen = pygame.Surface((5, 10))
        self.imagen.fill(AZUL)
        self.rect = self.imagen.get_rect(center=(x, y))

    def mover(self):
        self.rect.y -= 10

    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

# Clase de las balas enemigas
class BalaEnemiga:
    def __init__(self, x, y):
        self.imagen = pygame.Surface((5, 10))
        self.imagen.fill(ROSA)
        self.rect = self.imagen.get_rect(center=(x, y))

    def mover(self):
        self.rect.y += 5

    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

# Clase de los enemigos
class Enemigo:
    def __init__(self):
        self.hp = self.establecer_hp()
        self.color_original = ROJO if oleada < 5 else AMARILLO
        self.imagen = pygame.Surface((50, 50))
        self.imagen.fill(self.color_original)
        self.rect = self.imagen.get_rect()
        self.rect.x = random.randint(0, ancho_ventana - self.rect.width)
        self.rect.y = random.randint(50, 150)
        self.cooldown_disparo = 2000
        self.tiempo_ultimo_disparo = 0
        self.tiempo_dano = 0  # Para almacenar el tiempo en que se recibió daño

    def establecer_hp(self):
        return 2 

    def perder_vida(self):
        self.hp -= 1
        self.tiempo_dano = pygame.time.get_ticks()  # Guardar el tiempo de daño
        if self.hp == 0:
            return True  # Indica que el enemigo debe ser eliminado
        return False

    def mover(self, jugador, estado_juego):
        self.rect.y += 0.5
        if self.rect.y > alto_ventana:
            estado_juego['perdido'] = True
            estado_juego['corriendo'] = False
            return True
        if self.rect.colliderect(jugador.rect):
            estado_juego['perdido'] = True
            estado_juego['corriendo'] = False
            return True
        return False

    def disparar(self):
        return BalaEnemiga(self.rect.centerx, self.rect.bottom)

    def dibujar(self, superficie):
        # Verificar si el enemigo ha recibido daño y cambiar su color temporalmente
        if self.tiempo_dano > 0 and pygame.time.get_ticks() - self.tiempo_dano < 500:
            self.imagen.fill(BLANCO)  # Colorear de blanco
        else:
            self.imagen.fill(self.color_original)  # Restaurar color original
        superficie.blit(self.imagen, self.rect)

class Bust:
    def __init__(self):
        self.imagen = pygame.Surface((20, 20))
        self.imagen.fill(naranga)
        self.rect = self.imagen.get_rect()
        self.rect.x = random.randint(0, ancho_ventana - self.rect.width)
        self.rect.y = 0  # Comienza desde la parte superior
        self.velocidad = 3  # Velocidad de descenso

    def mover(self):
        self.rect.y += self.velocidad

    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

# Agregar la lista de Busts
busts = []

# Clase del jefe
class Jefe:
    def __init__(self):
        self.imagen = pygame.Surface((200, 50))
        self.imagen.fill(MORADO)
        self.rect = self.imagen.get_rect(center=(ancho_ventana // 2, 50))
        self.hp = 1500
        self.cooldown_disparo = 75
        self.tiempo_ultimo_disparo = 0
        self.direccion = 1
        self.velocidad = 10

    def disparar(self):
        return BalaEnemiga(self.rect.centerx, self.rect.bottom)

    def mover(self):
        self.rect.x += self.direccion * self.velocidad
        if self.rect.left < 0 or self.rect.right > ancho_ventana:
            self.direccion *= -1

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

# Bucle principal del juego
estado_juego = {'corriendo': True, 'perdido': False}
fuente = pygame.font.Font(None, 36)
jefe = None

while estado_juego['corriendo']:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            estado_juego['corriendo'] = False

    # Manejo de teclas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        jugador.mover(-5)
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jugador.mover(5)
    
    # Disparo del jugador
    if teclas[pygame.K_UP] or teclas[pygame.K_SPACE] or teclas[pygame.K_w]:
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - jugador.tiempo_ultimo_disparo >= jugador.cooldown_disparo:
            balas.append(Bala(jugador.rect.centerx, jugador.rect.top))
            jugador.tiempo_ultimo_disparo = tiempo_actual

    # Mover balas del jugador
    balas = [bala for bala in balas if bala.rect.y >= 0]
    for bala in balas:
        bala.mover()

    # Mover balas enemigas
    balas_enemigas = [bala for bala in balas_enemigas if bala.rect.y <= alto_ventana]
    for bala_enemiga in balas_enemigas:
        bala_enemiga.mover()

    # Mover Busts
    for bust in busts[:]:
        bust.mover()
        if bust.rect.y > alto_ventana:  # Eliminar si sale de la pantalla
            busts.remove(bust)

    # Generar Busts de manera ocasional
    if random.randint(1, 450) == 1:  # Ajusta la frecuencia de aparición
        busts.append(Bust())

    # Colisión entre Busts y el jugador
    for bust in busts[:]:
        if bust.rect.colliderect(jugador.rect):
            vidas += 5  # Aumentar vida
            jugador.cooldown_disparo = max(50, jugador.cooldown_disparo - 25)  # Reducir cooldown 
            jugador.tiempo_invulnerable = pygame.time.get_ticks() + 5000  # los enemigos se quedan quietos por 5 segundos
            busts.remove(bust)  # Eliminar el Bust al ser recogido

    # Mover enemigos
    for enemigo in enemigos[:]:
        if pygame.time.get_ticks() > jugador.tiempo_invulnerable:  # Solo si el jugador no está invulnerable
            if enemigo.mover(jugador, estado_juego):
                break
            if pygame.time.get_ticks() - enemigo.tiempo_ultimo_disparo >= enemigo.cooldown_disparo:
                balas_enemigas.append(enemigo.disparar())
                enemigo.tiempo_ultimo_disparo = pygame.time.get_ticks()

    # Colisión entre balas del jugador y enemigos
    for bala in balas[:]:
        for enemigo in enemigos[:]:
            if bala.rect.colliderect(enemigo.rect):
                if enemigo.perder_vida():  # Verificar si el enemigo pierde vida
                    enemigos.remove(enemigo)
                balas.remove(bala)
                break

    # Colisión entre balas jugador y Jefe
    for bala in balas[:]:
        if jefe and bala.rect.colliderect(jefe.rect):
            jefe.hp -= 1
            balas.remove(bala)
            # Eliminar al jefe si su vida llega a 0
            if jefe.hp <= 0:
                jefe = None

    # Verificar si no hay enemigos
    if not enemigos:
        oleada += 1
        jugador.cooldown_disparo = max(50, jugador.cooldown_disparo + 20)
        if (oleada % 5) == 0:
            jefe = Jefe()
        else:
            enemigos = crear_enemigos(5 + oleada)

    # Disparar balas del jefe
    if jefe and pygame.time.get_ticks() - jefe.tiempo_ultimo_disparo >= jefe.cooldown_disparo:
        balas_enemigas.append(jefe.disparar())
        jefe.tiempo_ultimo_disparo = pygame.time.get_ticks()
        jefe.mover()

    # Colisión entre balas enemigas y el jugador
    for bala_enemiga in balas_enemigas[:]:
        if bala_enemiga.rect.colliderect(jugador.rect):
            if pygame.time.get_ticks() > jugador.tiempo_invulnerable:  # Solo si no está invulnerable
                vidas -= 1
                balas_enemigas.remove(bala_enemiga)
                if vidas <= 0:
                    estado_juego['perdido'] = True
                    estado_juego['corriendo'] = False

    # Dibujar todo
    ventana.fill(NEGRO)
    jugador.dibujar(ventana)
    for enemigo in enemigos:
        enemigo.dibujar(ventana)
    for bala in balas:
        bala.dibujar(ventana)
    for bala_enemiga in balas_enemigas:
        bala_enemiga.dibujar(ventana)
    if jefe:
        jefe.dibujar(ventana)
    for bust in busts:
        bust.dibujar(ventana)

    # Mostrar el número de oleadas y vidas en la parte superior
    texto_oleada = fuente.render(f'Oleada: {oleada}', True, AMARILLO)
    ventana.blit(texto_oleada, (10, 10))
    texto_vidas = fuente.render(f'Vidas: {vidas}', True, AMARILLO)
    ventana.blit(texto_vidas, (10, 40))
    texto_velocidadAtaque = fuente.render(f'Velocidad de ataque: {jugador.cooldown_disparo}', True, AMARILLO)
    ventana.blit(texto_velocidadAtaque, (10, 70))

    # Mostrar HP del jefe si existe
    if jefe:
        textoHPJefe = fuente.render(f'HP Jefe: {jefe.hp}', True, MORADO)  
        ventana.blit(textoHPJefe, (10, 100))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    pygame.time.Clock().tick(85)

# Mostrar mensaje de pérdida
if estado_juego['perdido']:
    print("¡Has perdido!")
pygame.quit()
