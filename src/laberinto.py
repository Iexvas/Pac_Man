# src/laberinto.py
# Descripción: Clase base para cargar y gestionar la matriz del mapa de Pac-Man.

class Laberinto:
    def __init__(self, ruta_archivo):
        self.matriz = []
        self.inicio = None
        self.meta = None
        self.cargar_mapa(ruta_archivo)

    def cargar_mapa(self, ruta_archivo):
        """Lee el archivo .txt y construye la matriz 2D."""
        with open(ruta_archivo, 'r') as archivo:
            for y, linea in enumerate(archivo):
                fila = linea.strip().split(' ')
                if not fila or fila == ['']:
                    continue
                
                self.matriz.append(fila)
                
                # Identificamos dónde está Pac-Man (P) y la Meta (M)
                for x, valor in enumerate(fila):
                    if valor == 'P':
                        self.inicio = (x, y) # (Columna, Fila)
                    elif valor == 'M':
                        self.meta = (x, y)

    def mostrar_consola(self):
        """Imprime la matriz en la terminal"""
        for fila in self.matriz:
            print(" ".join(fila))
        print(f"\nCoordenada de Inicio (P): {self.inicio}")
        print(f"Coordenada de Meta (M): {self.meta}")

    def get_sucesores(self, x, y):
        """
        Recibe una coordenada (x, y).
        Devuelve una lista de tuplas con los vecinos válidos y su costo:
        [((nuevo_x, nuevo_y), costo), ...]
        """
        sucesores = []
        
        # Movimientos posibles: Arriba, Abajo, Izquierda, Derecha
        movimientos = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            
            # Validar que no nos salgamos de los bordes de la matriz
            if 0 <= nx < len(self.matriz[0]) and 0 <= ny < len(self.matriz):
                valor_celda = self.matriz[ny][nx]
                
                # Validar que no sea un muro ('1')
                if valor_celda != '1':
                    # 3. Calcular el costo
                    # Si es fantasma ('2'), cuesta 10. Si es camino ('0', 'P', 'M'), cuesta 1.
                    costo = 10 if valor_celda == '2' else 1
                    
                    sucesores.append(((nx, ny), costo))
                    
        return sucesores