# src/interfaz.py
# Descripción: Motor visual en Pygame para renderizar el laberinto.

import pygame
import sys


# Definición de Colores (Formato RGB)
NEGRO = (0, 0, 0)         # Camino libre (0)
AZUL = (0, 0, 200)        # Muros (1)
ROJO = (200, 0, 0)        # Zonas de miedo/fantasmas (2)
AMARILLO = (255, 255, 0)  # Pac-Man (P)
VERDE = (0, 200, 0)       # Meta (M)
GRIS = (50, 50, 50)       # Líneas de la cuadrícula

TAMANO_CELDA = 40 # Tamaño en píxeles de cada cuadrado

class Interfaz:
    def __init__(self, laberinto):
        self.laberinto = laberinto
        self.filas = len(laberinto.matriz)
        self.columnas = len(laberinto.matriz[0])
        
        # calculo del tamaño de la ventana según las celdas
        self.ancho = self.columnas * TAMANO_CELDA
        self.alto = self.filas * TAMANO_CELDA
        
        pygame.init()
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Pac-Man IA - Entorno")

    def dibujar(self):
        """Pinta el fondo y luego dibuja cada elemento de la matriz."""
        self.pantalla.fill(NEGRO)
        
        for y in range(self.filas):
            for x in range(self.columnas):
                valor = self.laberinto.matriz[y][x]
                
                rect = pygame.Rect(x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
                
                if valor == '1':
                    pygame.draw.rect(self.pantalla, AZUL, rect)
                elif valor == '2':
                    pygame.draw.rect(self.pantalla, ROJO, rect)
                elif valor == 'P':
                    pygame.draw.rect(self.pantalla, AMARILLO, rect)
                elif valor == 'M':
                    pygame.draw.rect(self.pantalla, VERDE, rect)
                
                pygame.draw.rect(self.pantalla, GRIS, rect, 1)

        pygame.display.flip() # Actualiza la pantalla

    def mantener_abierta(self):
        """Bucle principal para que la ventana no se cierre de inmediato."""
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
            
            self.dibujar()
            
        pygame.quit()
        sys.exit()