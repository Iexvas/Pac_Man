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

TAMANO_CELDA = 40

class Interfaz:
    def __init__(self, laberinto):
        self.laberinto = laberinto
        self.filas = len(laberinto.matriz)
        self.columnas = len(laberinto.matriz[0])
        self.ancho = self.columnas * TAMANO_CELDA
        self.alto = self.filas * TAMANO_CELDA
        
        pygame.init()
        pygame.mixer.init()
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Pac Man")
        
        self.imagenes = {}
        ruta_base = os.path.join(os.path.dirname(__file__), '..', 'assets')
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

    def reproducir_inicio(self):
        if self.sonido_inicio:
            self.sonido_inicio.play()

    def dibujar(self):
        """Colores de respaldo si es que las imágenes no cargan."""
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
                
                # Detecta si es un muro
                if valor == '1':
                    pygame.draw.rect(self.pantalla, colores_respaldo['1'], rect)
                
                # Para P, M, o 2 usamos la imágen
                elif valor in self.imagenes:
                    if self.imagenes[valor] is not None:
                        self.pantalla.blit(self.imagenes[valor], (x * TAMANO_CELDA, y * TAMANO_CELDA))
                    # Si no hay imagen, usamos el color de respaldo
                    elif valor in colores_respaldo:
                        pygame.draw.rect(self.pantalla, colores_respaldo[valor], rect)
                
                # Bordes
                pygame.draw.rect(self.pantalla, GRIS, rect, 1)

        pygame.display.flip() 

    def dibujar_rastro(self, nodos_explorados, ruta_final):
        """
        Recibe dos listas de tuplas (x, y).
        Pinta de celeste los nodos visitados y de naranja la ruta final.
        """
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
        """Bucle principal para que la ventana no se cierre de inmediato."""
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                    
        pygame.quit()
        sys.exit()