import pygame
import random
import sys
import time

# Configuración general
ANCHO, ALTO = 800, 600
FPS = 60
COLOR_FONDO = (10, 10, 30)

pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Galaga")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Arial", 24)
fuente_grande = pygame.font.SysFont("Arial", 42, bold=True)

def dibujar_fondo_galaxia():
    for y in range(ALTO):
        color = (10 + y // 30, 10 + y // 40, 40 + y // 20)
        pygame.draw.line(ventana, color, (0, y), (ANCHO, y))
    for _ in range(30):
        x, y = random.randint(0, ANCHO), random.randint(0, ALTO)
        pygame.draw.circle(ventana, (200, 200, 255), (x, y), 1)

class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (0, 180, 255), [(30, 0), (0, 50), (60, 50)])
        pygame.draw.circle(self.image, (0, 255, 255), (30, 30), 8)
        pygame.draw.rect(self.image, (0, 100, 255), (25, 45, 10, 10))
        self.rect = self.image.get_rect(center=(ANCHO // 2, ALTO - 60))
        self.velocidad = 5

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        self.rect.x = max(0, min(ANCHO - self.rect.width, self.rect.x))

class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 255, 255), (2, 0, 2, 20))
        pygame.draw.rect(self.image, (0, 150, 255, 120), (0, 0, 6, 20), border_radius=3)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 10

    def update(self):
        self.rect.y -= self.velocidad
        if self.rect.bottom < 0:
            self.kill()

class Meteorito(pygame.sprite.Sprite):
    def __init__(self, velocidad):
        super().__init__()
        self.size = random.randint(30, 50)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        puntos = [(random.randint(5, self.size - 5), random.randint(5, self.size - 5)) for _ in range(6)]
        color = random.choice([(100, 100, 100), (120, 60, 60), (80, 80, 100)])
        pygame.draw.polygon(self.image, color, puntos)
        self.rect = self.image.get_rect(x=random.randint(0, ANCHO - self.size), y=random.randint(-100, -40))
        self.velocidad_x = velocidad * random.uniform(-0.8, 0.8)
        self.velocidad_y = velocidad * random.uniform(1.0, 1.5)

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        if self.rect.left < 0 or self.rect.right > ANCHO:
            self.velocidad_x *= -1
        if self.rect.top > ALTO:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, centro):
        super().__init__()
        self.frames = []
        for i in range(6):
            frame = pygame.Surface((60, 60), pygame.SRCALPHA)
            color = (255, 150 + i*15, 0)
            pygame.draw.circle(frame, color, (30, 30), 10 + i*5)
            self.frames.append(frame)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=centro)
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer % 3 == 0:
            self.index += 1
            if self.index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.index]
                self.rect = self.image.get_rect(center=self.rect.center)

def mostrar_menu():
    dibujar_fondo_galaxia()
    titulo = fuente_grande.render("GALAXIAS", True, (100, 200, 255))
    instrucciones = fuente.render("← → para moverse | ESPACIO para disparar", True, (200, 220, 255))
    iniciar = fuente.render("Presiona cualquier tecla para comenzar", True, (180, 255, 200))
    ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 150))
    ventana.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, 250))
    ventana.blit(iniciar, (ANCHO//2 - iniciar.get_width()//2, 350))
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False

def formatear_tiempo(segundos):
    minutos = int(segundos // 60)
    segundos = int(segundos % 60)
    return f"{minutos:02}:{segundos:02}"

def juego():
    nivel = 1
    puntuacion = 0
    velocidad_enemigos = 1.0
    vidas = 3
    tiempo_inicio = time.time()

    nave = Nave()
    grupo_jugador = pygame.sprite.Group(nave)
    disparos = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    explosiones = pygame.sprite.Group()

    corriendo = True
    while corriendo:
        reloj.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    disparos.add(Disparo(nave.rect.centerx, nave.rect.top))
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False

        grupo_jugador.update()
        disparos.update()
        enemigos.update()
        explosiones.update()

        if random.random() < 0.02 and len(enemigos) < 4 + nivel:
            enemigos.add(Meteorito(velocidad_enemigos))

        if pygame.sprite.spritecollide(nave, enemigos, True):
            vidas -= 1
            if vidas <= 0:
                corriendo = False

        colisiones = pygame.sprite.groupcollide(disparos, enemigos, True, True)
        for lista in colisiones.values():
            for enemigo in lista:
                explosiones.add(Explosion(enemigo.rect.center))
                puntuacion += 10

        if puntuacion >= 100 * nivel:
            nivel += 1
            velocidad_enemigos += 0.5

        dibujar_fondo_galaxia()
        grupo_jugador.draw(ventana)
        disparos.draw(ventana)
        enemigos.draw(ventana)
        explosiones.draw(ventana)

        tiempo_actual = time.time() - tiempo_inicio
        texto_tiempo = fuente.render(f"Tiempo: {formatear_tiempo(tiempo_actual)}", True, (255, 255, 150))

        ventana.blit(fuente.render(f"Puntos: {puntuacion}", True, (255, 255, 255)), (10, 10))
        ventana.blit(fuente.render(f"Vidas: {vidas}", True, (255, 150, 150)), (10, 40))
        ventana.blit(fuente.render(f"Nivel: {nivel}", True, (150, 255, 150)), (10, 70))
        ventana.blit(texto_tiempo, (10, 100))

        pygame.display.flip()

    # Game Over
    ventana.fill(COLOR_FONDO)
    texto_fin = fuente_grande.render("FIN DEL JUEGO", True, (255, 100, 100))
    texto_tiempo_total = fuente.render(f"Duración: {formatear_tiempo(time.time() - tiempo_inicio)}", True, (255, 255, 255))
    ventana.blit(texto_fin, (ANCHO//2 - texto_fin.get_width()//2, 150))
    ventana.blit(fuente.render(f"Puntuación final: {puntuacion}", True, (255, 255, 255)), (ANCHO//2 - 150, 250))
    ventana.blit(texto_tiempo_total, (ANCHO//2 - 100, 280))
    ventana.blit(fuente.render("Presiona R para reiniciar o ESC para salir", True, (200, 200, 255)), (ANCHO//2 - 200, 320))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando = False
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    while True:
        mostrar_menu()
        juego()

if __name__ == "__main__":
    main()
