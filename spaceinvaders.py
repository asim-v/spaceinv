# Invasores Espaciales  
# Concursos interpreparatorianos 3ra modalidad - Computacion Grafica
# Iniciado el 25 de Enero de 2019
# By SydFx & Emiliobot
import pygame_textinput
import sys 
from pygame import *
from random import *
from os.path import *

# Colores ROJO, VERDE y AZUL (R, G, B).
BLANCO = (255, 255, 255)
NARANJA = (255, 153, 0)
VERDE = (0, 255, 0)
AMARILLO = (241, 255, 0)
PURPLE = (80, 0, 255)
RED = (237, 28, 36)
CAFE = (61, 36, 20)
CAFEOSCURO = (40, 10, 0)

# El tamaño de la ventana en pixeles
VENTANA = display.set_mode((1100, 618))

# Carpetas de recursos del juego
RAIZ = abspath(dirname(__file__))
CARPETA_FUENTE = RAIZ + '/fuente/'
CARPETA_IMAGENES = RAIZ + '/imagenes/'
CARPETA_SONIDOS = RAIZ + '/sonidos/'
NOMBRES_IMAGENES = ['nave','enemigo1_1', 'enemigo1_2', 'enemigo2_1', 'enemigo2_2', 'enemigo3_1', 'enemigo3_2',
             'explosionblue', 'explosiongreen', 'explosionpurple', 'laser', 'enemigolaser']
IMAGENES = {name: image.load(CARPETA_IMAGENES + '{}.png'.format(name)).convert_alpha()
for name in NOMBRES_IMAGENES}
FUENTE = CARPETA_FUENTE + '8_bit_party.ttf'
POSICION_BLOQUEADORES = 450 # Valor de los bloqueadores en Y
POSICION_ENEMIGOS = 65  # Valor inicial por cada nuevo juego
enemigo_BAJAR = 35



class Nave(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.imagen = IMAGENES['nave']
        self.rect = self.imagen.get_rect(topleft=(520, 535))
        self.velocidad = 5

    def update(self, keys, *args):
        if keys[K_LEFT] and self.rect.x > 200:
            self.rect.x -= self.velocidad
        if keys[K_RIGHT] and self.rect.x < 850:
            self.rect.x += self.velocidad
        game.pantalla.blit(self.imagen, self.rect)

class Bala(sprite.Sprite):
    def __init__(self, xpos, ypos, direccion, velocidad, nombre_archivo, lado):
        sprite.Sprite.__init__(self)
        self.imagen = IMAGENES[nombre_archivo]
        self.rect = self.imagen.get_rect(topleft=(xpos, ypos))
        self.velocidad = velocidad*1.3
        self.direccion = direccion
        self.lado = lado
        self.nombre_archivo = nombre_archivo

    def update(self, keys, *args):
        game.pantalla.blit(self.imagen, self.rect)
        self.rect.y += self.velocidad * self.direccion
        if self.rect.y < 15 or self.rect.y > 600:
            self.kill()

class Invasores(sprite.Sprite):
    def __init__(self, fila, columna):
        sprite.Sprite.__init__(self)
        self.fila = fila
        self.columna = columna
        self.imagens = []
        self.cargar_imagenes()
        self.indice = 0
        self.imagen = self.imagens[self.indice]
        self.rect = self.imagen.get_rect()

    def alternar_imagen(self):
        self.indice += 1
        if self.indice >= len(self.imagens):
            self.indice = 0
        self.imagen = self.imagens[self.indice]

    def update(self, *args):
        game.pantalla.blit(self.imagen, self.rect)

    def cargar_imagenes(self):
        images = {0: ['1_2', '1_1'],
                  1: ['2_2', '2_1'],
                  2: ['2_2', '2_1'],
                  3: ['3_1', '3_2'],
                  4: ['3_1', '3_2'],
                  }
        img1, img2 = (IMAGENES['enemigo{}'.format(img_num)] for img_num in
                      images[self.fila])
        self.imagens.append(transform.scale(img1, (40, 35)))
        self.imagens.append(transform.scale(img2, (40, 35)))

class Grupo(sprite.Group):
    def __init__(self, columnas, filas):
        sprite.Group.__init__(self)
        self.enemigos = [[None] * columnas for _ in range(filas)]
        self.columnas = columnas
        self.filas = filas
        self.AgregarMovimientoIzquierda = 0
        self.AgregarMovimientoIzquierda = 0
        self.tiempoMovimiento = 400  # Velocidad de los invasores
        self.direccion = 1
        self.movimientosDerecha = 25  # Movimientos a la derecha
        self.movimientosIzquierda = 25
        self.MoverNumero = 15
        self.temporizador = time.get_ticks()
        self.fondo = game.PosicionEnemigo + ((filas - 1) * 45) + 35
        self._ColumnasVivas = list(range(columnas))
        self._ColumnaVivaIzquierda = 0
        self._ColumnaVivaDerecha = columnas - 1

    def update(self, tiempo_actual):
        if tiempo_actual - self.temporizador > self.tiempoMovimiento:
            if self.direccion == 1:
                max_mov = self.movimientosDerecha + self.AgregarMovimientoIzquierda
            else:
                max_mov = self.movimientosIzquierda + self.AgregarMovimientoIzquierda

            if self.MoverNumero >= max_mov:
                self.movimientosIzquierda = 25 + self.AgregarMovimientoIzquierda # Movimientos a la izquierda
                self.movimientosDerecha = 25 + self.AgregarMovimientoIzquierda
                self.direccion *= -1
                self.MoverNumero = 0
                self.fondo = 0
                for enemigo in self:
                    enemigo.rect.y += enemigo_BAJAR
                    enemigo.alternar_imagen()
                    if self.fondo < enemigo.rect.y + 35:
                        self.fondo = enemigo.rect.y + 35
            else:
                velocidad = 10 if self.direccion == 1 else -10
                for enemigo in self:
                    enemigo.rect.x += velocidad
                    enemigo.alternar_imagen()
                self.MoverNumero += 1

            self.temporizador += self.tiempoMovimiento

    def add_internal(self, *sprites):
        super(Grupo, self).add_internal(*sprites)
        for s in sprites:
            self.enemigos[s.fila][s.columna] = s

    def remove_internal(self, *sprites):
        super(Grupo, self).remove_internal(*sprites)
        for s in sprites:
            self.kill(s)
        self.actualizar_velocidad()

    def columna_muerta(self, columna):
        return not any(self.enemigos[fila][columna]
                       for fila in range(self.filas))

    def random_disparador(self):
        col = choice(self._ColumnasVivas)
        col_enemigos = (self.enemigos[fila - 1][col]
                       for fila in range(self.filas, 0, -1))
        return next((en for en in col_enemigos if en is not None), None)

    def actualizar_velocidad(self):
        if len(self) == 1:
            self.tiempoMovimiento = 200
        elif len(self) <= 10:
            self.tiempoMovimiento = 400

    def kill(self, enemigo):
        self.enemigos[enemigo.fila][enemigo.columna] = None
        columna_muerta = self.columna_muerta(enemigo.columna)
        if columna_muerta:
            self._ColumnasVivas.remove(enemigo.columna)

        if enemigo.columna == self._ColumnaVivaDerecha:
            while self._ColumnaVivaDerecha > 0 and columna_muerta:
                self._ColumnaVivaDerecha -= 1
                self.AgregarMovimientoIzquierda += 5
                columna_muerta = self.columna_muerta(self._ColumnaVivaDerecha)

        elif enemigo.columna == self._ColumnaVivaIzquierda:
            while self._ColumnaVivaIzquierda < self.columnas and columna_muerta:
                self._ColumnaVivaIzquierda += 1
                self.AgregarMovimientoIzquierda += 5
                columna_muerta = self.columna_muerta(self._ColumnaVivaIzquierda)

class Blocker(sprite.Sprite):
    def __init__(self, size, color, fila, columna):
        sprite.Sprite.__init__(self)
        self.height = size
        self.width = size
        self.color = color
        self.imagen = Surface((self.width, self.height))
        self.imagen.fill(self.color)
        self.rect = self.imagen.get_rect()
        self.fila = fila
        self.columna = columna

    def update(self, keys, *args):
        game.pantalla.blit(self.imagen, self.rect)

class Explosion_enemigos(sprite.Sprite):
    def __init__(self, enemigo, *groups):
        super(Explosion_enemigos, self).__init__(*groups)
        self.imagen = transform.scale(self.get_image(enemigo.fila), (40, 35))
        self.imagen2 = transform.scale(self.get_image(enemigo.fila), (50, 45))
        self.rect = self.imagen.get_rect(topleft=(enemigo.rect.x, enemigo.rect.y))
        self.temporizador = time.get_ticks()

    @staticmethod
    def get_image(fila):
        img_colores = ['purple', 'blue', 'blue', 'green', 'green']
        return IMAGENES['explosion{}'.format(img_colores[fila])]

    def update(self, tiempo_actual, *args):
        pasado = tiempo_actual - self.temporizador
        if pasado <= 100:
            game.pantalla.blit(self.imagen, self.rect)
        elif pasado <= 200:
            game.pantalla.blit(self.imagen2, (self.rect.x - 6, self.rect.y - 6))
        elif 400 < pasado:
            self.kill()

class NaveExplosion(sprite.Sprite):
    def __init__(self, nave, *groups):
        super(NaveExplosion, self).__init__(*groups)
        self.imagen = IMAGENES['nave']
        self.rect = self.imagen.get_rect(topleft=(nave.rect.x, nave.rect.y))
        self.temporizador = time.get_ticks()

    def update(self, tiempo_actual, *args):
        pasado = tiempo_actual - self.temporizador
        if 300 < pasado <= 600:
            game.pantalla.blit(self.imagen, self.rect)
        elif 900 < pasado:
            self.kill()

class Vidas(sprite.Sprite):
    def __init__(self, xpos, ypos):
        sprite.Sprite.__init__(self)
        self.imagen = IMAGENES['nave']
        self.imagen = transform.scale(self.imagen, (30, 23))
        self.rect = self.imagen.get_rect(topleft=(xpos, ypos))

    def update(self, *args):
        game.pantalla.blit(self.imagen, self.rect)

class Texto(object):
    def __init__(self, textoFont, size, mensaje, color, xpos, ypos):
        self.font = font.Font(textoFont, size)
        self.superficie = self.font.render(mensaje, True, color)
        self.rect = self.superficie.get_rect(topleft=(xpos, ypos))

    def draw(self, surface):
        surface.blit(self.superficie, self.rect)

class Invasores_Espaciales(object):
    def __init__(self):
        def Mejor_Puntuacion():
            puntuacionData = open('Puntajes.txt','r')
            best = '0'
            for x in puntuacionData:
                if int(x) > int(best): best = int(x)
            return str(best)

        mixer.pre_init(44100, -16, 1, 4096)
        init()
        self.MejorPuntaje = Mejor_Puntuacion()
        self.reloj = time.Clock()
        self.caption = display.set_caption('Invasores Espaciales UNAM')
        self.pantalla = VENTANA
        self.fondo = image.load(CARPETA_IMAGENES + 'fondo.jpg').convert()
        self.MejorPuntajeTexto = Texto(FUENTE, 25,'Mejor Puntuacion ' + self.MejorPuntaje , BLANCO, 410, 80)
        self.IniciarJuego = False
        self.PantallaPrincipal = True
        self.Derrota = False
        # Contador para la posicion inicial del enemigo incrementado cada nuevo round
        self.PosicionEnemigo = POSICION_ENEMIGOS
        self.TextoTitulo = Texto(FUENTE, 55, 'Invasores Espaciales', BLANCO, 255, 130)
        self.TextoTitulo2 = Texto(FUENTE, 25, 'Presiona tu nombre y enter', BLANCO, 380, 270)
        self.DerrotaTexto = Texto(FUENTE, 50, 'Has perdido', BLANCO, 380, 270)
        self.SiguienteRondaTexto = Texto(FUENTE, 50, 'Siguiente Ronda', BLANCO, 240, 270)
        self.MejorPuntajeTexto3 = Texto(FUENTE, 20,'Mejor Puntaje'  , BLANCO, 930, 115)
        self.TextoPuntuacion = Texto(FUENTE, 20, 'Puntuacion', BLANCO, 20, 45)
        self.TextoVidas = Texto(FUENTE, 20, 'Vidas ', BLANCO, 985, 40)
        self.vida1 = Vidas(965, 70)
        self.vida2 = Vidas(995, 70)
        self.vida3 = Vidas(1025, 70)
        self.ConjuntoVidas = sprite.Group(self.vida1, self.vida2, self.vida3)
        self.CancionPrincipal = mixer.Sound(CARPETA_SONIDOS + 'Soundtrack1.wav')
        self.CancionPrincipal.set_volume(0.5)
        self.CancionBatalla = mixer.Sound(CARPETA_SONIDOS + 'Soundtrack2.wav')
        self.CancionBatalla.set_volume(0.5)
        self.textinput = pygame_textinput.TextInput()

    def reset(self, puntuacion):
        self.jugador = Nave()
        self.jugadorConjunto = sprite.Group(self.jugador)
        self.ConjuntoExplosiones = sprite.Group()
        self.balas = sprite.Group()
        self.BalasInvasores = sprite.Group()
        self.crear_invasores()
        self.SpritesTodos = sprite.Group(self.jugador, self.enemigos,
                                       self.ConjuntoVidas)
        self.keys = key.get_pressed()

        self.temporizador = time.get_ticks()
        self.temporizador
        self.temporizadorNotas = time.get_ticks()
        self.temporizadorNave = time.get_ticks()
        self.puntuacion = puntuacion
        self.crear_sonido()
        self.CrearNuevaNave = False
        self.naveAlive = True
        self.t = 1
        self.t2 = 1
        self.t3 = 1

    def hacer_bloqueadores(self, number):
        colors = [CAFE,CAFEOSCURO,PURPLE,CAFEOSCURO]
        blockerGroup = sprite.Group()
        for fila in range(4):
            for columna in range(9):
                blocker = Blocker(10, choice(colors), fila, columna)
                blocker.rect.x = 200 + (200 * number) + (columna * blocker.width)
                blocker.rect.y = POSICION_BLOQUEADORES + (fila * blocker.height)
                blockerGroup.add(blocker)
        return blockerGroup

    def crear_sonido(self):
        self.sonidos = {}
        for sound_name in ['shoot', 'shoot2', 'invaderkilled',
                           'naveexplosion']:
            self.sonidos[sound_name] = mixer.Sound(
                CARPETA_SONIDOS + '{}.wav'.format(sound_name))
            self.sonidos[sound_name].set_volume(0.3)
 
        self.musicNotes = [mixer.Sound(CARPETA_SONIDOS + '{}.wav'.format(i)) for i
                           in range(4)]
        for sound in self.musicNotes:
            sound.set_volume(0.3)

        self.noteIndex = 0

    @staticmethod
    def deberia_salir(evt):
        #Metodo estatico, permite salir del juego, a traves un booleano
        return evt.type == QUIT or (evt.type == KEYUP and evt.key == K_ESCAPE)

    def checar_entrada(self):
        self.keys = key.get_pressed()
        for e in event.get():
            if self.deberia_salir(e):
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if len(self.balas) == 0 and self.naveAlive:
                        if self.puntuacion < 1000:
                            bala = Bala(self.jugador.rect.x + 23,
                                            self.jugador.rect.y + 5, -1,
                                            15, 'laser', 'center')
                            self.balas.add(bala)
                            self.SpritesTodos.add(self.balas)
                            self.sonidos['shoot'].play()
                        else:
                            balaizquierda = Bala(self.jugador.rect.x + 8,
                                                self.jugador.rect.y + 5, -1,
                                                15, 'laser', 'left')
                            baladerecha = Bala(self.jugador.rect.x + 38,
                                                 self.jugador.rect.y + 5, -1,
                                                 15, 'laser', 'right')
                            self.balas.add(balaizquierda)
                            self.balas.add(baladerecha)
                            self.SpritesTodos.add(self.balas)
                            self.sonidos['shoot2'].play()

    def crear_invasores(self):
        enemigos = Grupo(10, 5)
        for fila in range(5):
            for columna in range(10):
                enemigo = Invasores(fila, columna)
                enemigo.rect.x = 320 + (columna * 50)   # La posicion en X de los invasores
                enemigo.rect.y = self.PosicionEnemigo + (fila * 45)
                enemigos.add(enemigo)

        self.enemigos = enemigos

    def hacer_invasores_disparar(self):
        if (time.get_ticks() - self.temporizador) > 700 and self.enemigos:
            enemigo = self.enemigos.random_disparador()
            self.BalasInvasores.add(
                Bala(enemigo.rect.x + 14, enemigo.rect.y + 20, 1, 5,
                       'enemigolaser', 'center'))
            self.SpritesTodos.add(self.BalasInvasores)
            self.temporizador = time.get_ticks()

    def calcular_puntuacion(self, fila):
        puntuacions = {0: 30,
                  1: 20,
                  2: 20,
                  3: 10,
                  4: 10,
                  5: choice([50, 100, 150, 300])
                  }

        puntuacion = puntuacions[fila]
        self.puntuacion += puntuacion
        return puntuacion

    def create_main_menu(self):
        def crear_texto_menu():
            self.pantalla.blit(self.fondo, (0, 0))
            self.TextoTitulo.draw(self.pantalla)
            self.TextoTitulo2.draw(self.pantalla)
            self.MejorPuntajeTexto.draw(self.pantalla)

        while True:
            breaker = False
            events = event.get()
            crear_texto_menu()
            for e in events:
                if self.deberia_salir(e): exit()
                if e.type == KEYDOWN:
                    if e.key == K_RETURN: 
                        breaker = True         
                        break
            self.textinput.update(events)
            self.pantalla.blit(self.textinput.get_surface(),(490, 220))
            display.update()
            self.reloj.tick(60)
            if breaker : break

    def checar_colisiones(self):
        sprite.groupcollide(self.balas, self.BalasInvasores, True, True)

        for enemigo in sprite.groupcollide(self.enemigos, self.balas,
                                         True, True).keys():
            self.sonidos['invaderkilled'].play()
            self.calcular_puntuacion(enemigo.fila)
            Explosion_enemigos(enemigo, self.ConjuntoExplosiones)
            self.gameTimer = time.get_ticks()

        for jugador in sprite.groupcollide(self.jugadorConjunto, self.BalasInvasores,
                                          True, True).keys():
            if self.vida3.alive():
                self.vida3.kill()
            elif self.vida2.alive():
                self.vida2.kill()
            elif self.vida1.alive():
                self.vida1.kill()
            else:
                self.Derrota = True
                self.IniciarJuego = False
            self.sonidos['naveexplosion'].play()
            NaveExplosion(jugador, self.ConjuntoExplosiones)
            self.CrearNuevaNave = True
            self.temporizadorNave = time.get_ticks()
            self.naveAlive = False

        if self.enemigos.fondo >= 540:
            sprite.groupcollide(self.enemigos, self.jugadorConjunto, True, True)
            if not self.jugador.alive() or self.enemigos.fondo >= 600:
                self.Derrota = True
                self.IniciarJuego = False

        sprite.groupcollide(self.balas, self.allBlockers, True, True)
        sprite.groupcollide(self.BalasInvasores, self.allBlockers, True, True)
        if self.enemigos.fondo >= POSICION_BLOQUEADORES:
            sprite.groupcollide(self.enemigos, self.allBlockers, False, True)

    def crear_nueva_nave(self, createNave, tiempoActual):
        if createNave and (tiempoActual - self.temporizadorNave > 900):
            self.jugador = Nave()
            self.SpritesTodos.add(self.jugador)
            self.jugadorConjunto.add(self.jugador)
            self.CrearNuevaNave = False 
            self.naveAlive = True

    def crear_fin_del_juego(self, tiempoActual):

        def Mejor_Puntuacion():
            puntuacionData = open('puntuacions.txt','r')
            best = '0'
            for x in puntuacionData:
                if int(x) > int(best): best = int(x)
            return str(best)

        self.pantalla.blit(self.fondo, (0, 0))
        pasado = tiempoActual - self.temporizador
        if pasado < 750:
            self.DerrotaTexto.draw(self.pantalla)
        elif 750 < pasado < 1500:
            self.pantalla.blit(self.fondo, (0, 0))
        elif 1500 < pasado < 2250:
            self.DerrotaTexto.draw(self.pantalla)
        elif 2250 < pasado < 2750:
            self.pantalla.blit(self.fondo, (0, 0))
        elif pasado > 3000:
            self.PantallaPrincipal = True
        #Actualiza la mejor puntuacion
        self.MejorPuntajeTexto = Texto(FUENTE, 17,'Mejor Puntuacion ' + Mejor_Puntuacion() , BLANCO, 100, 100)
        self.MejorPuntaje = Mejor_Puntuacion()
        self.t = 1
        self.t2 = 1
        self.t3 = 1

        for e in event.get():
            if self.deberia_salir(e):
                sys.exit()
   
    def main(self):
        self.t = 1
        self.t2 = 1
        self.t3 = 1
        while True: #Ciclo del juego
            if self.PantallaPrincipal:
                self.pantalla.blit(self.fondo, (0, 0))
                self.TextoTitulo.draw(self.pantalla)
                self.TextoTitulo2.draw(self.pantalla)
                self.MejorPuntajeTexto.draw(self.pantalla)
                

                if self.t == 1: self.CancionPrincipal.play()
                self.t -= 1

                for e in event.get():
                    if self.deberia_salir(e):
                        sys.exit()
                    self.create_main_menu()
                        # Crea bloquadores en un nuevo juego, no en un nuevo round
                    self.allBlockers = sprite.Group(self.hacer_bloqueadores(0),
                                                    self.hacer_bloqueadores(1),
                                                    self.hacer_bloqueadores(2),
                                                    self.hacer_bloqueadores(3))
                    self.ConjuntoVidas.add(self.vida1, self.vida2, self.vida3)
                    self.reset(0)
                    self.IniciarJuego = True
                    self.PantallaPrincipal = False
            elif self.IniciarJuego:
                self.CancionPrincipal.stop()
                if not self.enemigos and not self.ConjuntoExplosiones:
                    tiempoActual = time.get_ticks()

                    if tiempoActual - self.gameTimer < 3000:
                        self.pantalla.blit(self.fondo, (0, 0))
                        self.TextoPuntuacion2 = Texto(FUENTE, 20, str(self.puntuacion),
                                               VERDE, 300, 5)
                        self.SiguienteRondaTexto.draw(self.pantalla)
                        self.TextoVidas.draw(self.pantalla)
                        self.ConjuntoVidas.update()
                        self.checar_entrada()
                    if tiempoActual - self.gameTimer > 3000:
                        # Baja a los enemigos por bloque
                        self.PosicionEnemigo += enemigo_BAJAR*2
                        self.reset(self.puntuacion)
                        self.gameTimer += 3000
                else:
                    tiempoActual = time.get_ticks()
                    self.pantalla.blit(self.fondo, (0, 0))
                    self.allBlockers.update(self.pantalla) 
                                        #Escudo anti loop -------------------\\\\
                    if self.t2 == 1:
                        self.CancionBatalla.play()     
                    self.t2 = 0
                                        #Escudo anti loop --------------------////
                    
                    self.TextoPuntuacion2 = Texto(FUENTE, 40, str(self.puntuacion), VERDE,40, 75)
                    self.MejorPuntajeTexto2 = Texto(FUENTE, 40, str(self.MejorPuntaje), RED,975, 145)
                    self.TextoPuntuacion.draw(self.pantalla)
                    self.TextoPuntuacion2.draw(self.pantalla)
                    self.MejorPuntajeTexto3.draw(self.pantalla)
                    self.MejorPuntajeTexto2.draw(self.pantalla)
                    self.TextoVidas.draw(self.pantalla)
                    self.checar_entrada()
                    self.enemigos.update(tiempoActual)
                    self.SpritesTodos.update(self.keys, tiempoActual)
                    self.ConjuntoExplosiones.update(tiempoActual)
                    self.checar_colisiones()
                    self.crear_nueva_nave(self.CrearNuevaNave, tiempoActual)
                    self.hacer_invasores_disparar()
            elif self.Derrota:
                self.CancionBatalla.stop()
                tiempoActual = time.get_ticks()
                # Reestablece la posicion inicial de los enemigos
                self.PosicionEnemigo = POSICION_ENEMIGOS
                
                #Escudo anti loop ---
                if self.t3 == 1: 
                    puntuacionData = open('puntuacions.txt','a')
                    puntuacionData.write(str(self.puntuacion)+'\n')
                    puntuacionData.close()
                self.t3 = 0 
                #Escudo anti loop ---

                self.crear_fin_del_juego(tiempoActual)

            display.update()
            self.reloj.tick(60)

if __name__ == '__main__':
    game = Invasores_Espaciales()
    game.main()