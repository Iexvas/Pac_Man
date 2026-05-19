# src/interfaz.py
# Descripción: Interfáz para ambientar el entorno Pac-Man.

import pygame
import sys
import os 

# Definición de Colores 
NEGRO = (0, 0, 0)         
GRIS = (40, 40, 40) 
CELESTE = (100, 200, 255) # Nodos visitados
NARANJA = (255, 165, 0)   # Ruta óptima final
BLANCO = (255, 255, 255)
AMARILLO_MENU = (255, 215, 0)
AZUL_BOTON = (70, 130, 180)
ROJO_BOTON = (200, 50, 50)

TAMANO_CELDA = 60

class Interfaz:
    def __init__(self, laberinto):
        self.laberinto = laberinto
        self.filas = len(laberinto.matriz)
        self.columnas = len(laberinto.matriz[0])
        self.ancho = self.columnas * TAMANO_CELDA
        self.alto_mapa = self.filas * TAMANO_CELDA
        self.alto = self.alto_mapa + 80 
        
        pygame.init()
        pygame.mixer.init()
        pygame.font.init() 
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Pac Man")
        
        ruta_base = os.path.join(os.path.dirname(__file__), '..', 'assets')
        
        # Carga de la fuente pixelada
        ruta_fuente = os.path.join(ruta_base, 'font.ttf')
        if os.path.exists(ruta_fuente):
            self.fuente_titulo = pygame.font.Font(ruta_fuente, 40)
            self.fuente_menu = pygame.font.Font(ruta_fuente, 24)
            self.fuente_pequena = pygame.font.Font(ruta_fuente, 16) # Para panel inferior
        else:
            self.fuente_titulo = pygame.font.SysFont(None, 50)
            self.fuente_menu = pygame.font.SysFont(None, 30)
            self.fuente_pequena = pygame.font.SysFont(None, 20)

        # Carga del fondo del menú
        ruta_bg = os.path.join(ruta_base, 'menu_bg.png')
        if os.path.exists(ruta_bg):
            self.fondo_menu = pygame.image.load(ruta_bg).convert()
            self.fondo_menu = pygame.transform.scale(self.fondo_menu, (self.ancho, self.alto))
        else:
            self.fondo_menu = None
            
        # Definición del botón
        ancho_boton, alto_boton = 200, 50
        self.rect_boton_iniciar = pygame.Rect(
            (self.ancho // 2) - (ancho_boton // 2),
            self.alto - 150,
            ancho_boton,
            alto_boton
        )

        #botones
        self.botones_mapas = [
            {"rect": pygame.Rect((self.ancho // 2) - 100, self.alto // 2 - 60, 200, 40), "texto": "Mapa Fácil", "archivo": "mapas/mapa_facil.txt"},
            {"rect": pygame.Rect((self.ancho // 2) - 100, self.alto // 2, 200, 40), "texto": "Mapa Costos", "archivo": "mapas/mapa_costos.txt"},
            {"rect": pygame.Rect((self.ancho // 2) - 100, self.alto // 2 + 60, 200, 40), "texto": "Mapa Trampa", "archivo": "mapas/mapa_trampa.txt"}
        ]

        # Botón volver
        self.rect_btn_volver_inicio = pygame.Rect(10, 10, 80, 30)

        ancho_alg = 60
        espacio = (self.ancho - (ancho_alg * 5)) // 6
        y_panel = self.alto_mapa + 20

        self.rect_btn_volver_mapas = pygame.Rect(5, y_panel, 40, 40)

        self.botones_algoritmos = {
            "BFS": pygame.Rect(espacio, y_panel, ancho_alg, 40),
            "DFS": pygame.Rect(espacio*2 + ancho_alg, y_panel, ancho_alg, 40),
            "UCS": pygame.Rect(espacio*3 + ancho_alg*2, y_panel, ancho_alg, 40),
            "GBFS": pygame.Rect(espacio*4 + ancho_alg*3, y_panel, ancho_alg, 40),
            "A*": pygame.Rect(espacio*5 + ancho_alg*4, y_panel, ancho_alg, 40)
        }
        
        self.imagenes = {}
        archivos = {
            'P': 'pacman.png',
            'M': 'meta.png',
            '2': 'fantasma.png'
        }
        
        for clave, nombre_archivo in archivos.items():
            ruta_completa = os.path.join(ruta_base, nombre_archivo)
            if os.path.exists(ruta_completa):
                img = pygame.image.load(ruta_completa).convert_alpha()
                self.imagenes[clave] = pygame.transform.scale(img, (TAMANO_CELDA, TAMANO_CELDA))
            else:
                print(f"No se encontraron las imagenes.")
                self.imagenes[clave] = None
        
        ruta_sonido = os.path.join(ruta_base, 'inicio.wav')
        if os.path.exists(ruta_sonido):
            self.sonido_inicio = pygame.mixer.Sound(ruta_sonido)
        else:
            print("NO se encontró el sonido.")
            self.sonido_inicio = None

    def actualizar_laberinto(self, nuevo_laberinto):
        """Permite inyectar el mapa seleccionado antes de dibujar el juego."""
        self.laberinto = nuevo_laberinto
        self.filas = len(nuevo_laberinto.matriz)
        self.columnas = len(nuevo_laberinto.matriz[0])

    def dibujar_menu(self):
        """Dibuja la pantalla de inicio estática (Pantalla 1)."""
        if self.fondo_menu:
            self.pantalla.blit(self.fondo_menu, (0, 0))
        else:
            self.pantalla.fill(NEGRO)
        
        texto_titulo = "PAC-MAN IA"
        texto = self.fuente_titulo.render(texto_titulo, True, AMARILLO_MENU)
        rect_texto = texto.get_rect(center=(self.ancho // 2, self.alto // 3))
        self.pantalla.blit(texto, rect_texto)
        
        pygame.draw.rect(self.pantalla, AMARILLO_MENU, self.rect_boton_iniciar, border_radius=10)
        label_iniciar = self.fuente_menu.render("INICIAR", True, NEGRO)
        rect_label = label_iniciar.get_rect(center=self.rect_boton_iniciar.center)
        self.pantalla.blit(label_iniciar, rect_label)
        
        pygame.display.flip()

    def dibujar_menu_mapas(self):
        """Dibuja la pantalla de selección de mapas (Pantalla 2)."""
        self.pantalla.fill(NEGRO)
        
        texto_titulo = "SELECCIONE MAPA"
        texto = self.fuente_titulo.render(texto_titulo, True, BLANCO)
        rect_texto = texto.get_rect(center=(self.ancho // 2, self.alto // 4))
        self.pantalla.blit(texto, rect_texto)
        
        mouse_pos = pygame.mouse.get_pos()

        color_vol_inicio = ROJO_BOTON if self.rect_btn_volver_inicio.collidepoint(mouse_pos) else GRIS
        pygame.draw.rect(self.pantalla, color_vol_inicio, self.rect_btn_volver_inicio, border_radius=5)
        lbl_vol_inicio = self.fuente_pequena.render("Volver", True, BLANCO)
        self.pantalla.blit(lbl_vol_inicio, lbl_vol_inicio.get_rect(center=self.rect_btn_volver_inicio.center))
        
        for btn in self.botones_mapas:
            color = AZUL_BOTON if btn["rect"].collidepoint(mouse_pos) else GRIS
            pygame.draw.rect(self.pantalla, color, btn["rect"], border_radius=8)
            label = self.fuente_menu.render(btn["texto"], True, BLANCO)
            rect_label = label.get_rect(center=btn["rect"].center)
            self.pantalla.blit(label, rect_label)
            
        pygame.display.flip()

    def reproducir_inicio(self):
        if self.sonido_inicio:
            self.sonido_inicio.play()

    def dibujar(self):
        """Dibuja la matriz del laberinto en la pantalla (Pantalla 3)."""
        self.pantalla.fill(NEGRO)
        
        colores_respaldo = {
            '1': (0, 0, 200),  # Muros 
            'P': (255, 255, 0),# Pac-Man Amarillo
            'M': (0, 200, 0),  # Meta Verde
            '2': (200, 0, 0)   # Fantasma Rojo
        }
        
        for y in range(self.filas):
            for x in range(self.columnas):
                valor = self.laberinto.matriz[y][x]
                rect = pygame.Rect(x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
                
                if valor == '1':
                    pygame.draw.rect(self.pantalla, colores_respaldo['1'], rect)
                elif valor in self.imagenes:
                    if self.imagenes[valor] is not None:
                        self.pantalla.blit(self.imagenes[valor], (x * TAMANO_CELDA, y * TAMANO_CELDA))
                    elif valor in colores_respaldo:
                        pygame.draw.rect(self.pantalla, colores_respaldo[valor], rect)
                
                pygame.draw.rect(self.pantalla, GRIS, rect, 1)

        self.dibujar_panel_algoritmos()
        pygame.display.flip() 

    def dibujar_panel_algoritmos(self):
        """Redibuja dinámicamente los botones en la parte inferior para mostrar efecto Hover."""
        pygame.draw.rect(self.pantalla, GRIS, (0, self.alto_mapa, self.ancho, 80))
        mouse_pos = pygame.mouse.get_pos()

        color_vol_mapas = ROJO_BOTON if self.rect_btn_volver_mapas.collidepoint(mouse_pos) else NEGRO
        pygame.draw.rect(self.pantalla, color_vol_mapas, self.rect_btn_volver_mapas, border_radius=5)
        lbl_vol_mapas = self.fuente_pequena.render("<", True, BLANCO)
        self.pantalla.blit(lbl_vol_mapas, lbl_vol_mapas.get_rect(center=self.rect_btn_volver_mapas.center))
        
        for nombre, rect in self.botones_algoritmos.items():
            color = AMARILLO_MENU if rect.collidepoint(mouse_pos) else NEGRO
            color_texto = NEGRO if color == AMARILLO_MENU else BLANCO
            
            pygame.draw.rect(self.pantalla, color, rect, border_radius=5)
            label = self.fuente_pequena.render(nombre, True, color_texto)
            rect_label = label.get_rect(center=rect.center)
            self.pantalla.blit(label, rect_label)

    def dibujar_rastro(self, nodos_explorados, ruta_final):
        """Pinta de celeste los nodos visitados y de naranja la ruta final."""
        for x, y in nodos_explorados:
            valor = self.laberinto.matriz[y][x]
            if valor not in ['P', 'M']:
                rect = pygame.Rect(x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
                pygame.draw.rect(self.pantalla, CELESTE, rect)
                pygame.draw.rect(self.pantalla, GRIS, rect, 1)

        for x, y in ruta_final:
            valor = self.laberinto.matriz[y][x]
            if valor not in ['P', 'M']:
                rect = pygame.Rect(x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
                pygame.draw.rect(self.pantalla, NARANJA, rect)
                pygame.draw.rect(self.pantalla, GRIS, rect, 1)

        pygame.display.flip() 

    def mantener_abierta(self):
        pass