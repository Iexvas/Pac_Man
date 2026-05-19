# src/busqueda_ciega.py
# Implementación de BFS, DFS y UCS para Pac-Man

from collections import deque
import heapq


def bfs(laberinto):
    """
    Búsqueda en Anchura (Breadth-First Search).
    Explora nivel por nivel. Garantiza el camino con MENOS PASOS,
    pero no necesariamente el de menor costo (ignora costos de fantasmas).

    Retorna:
        ruta        : lista de (x, y) desde inicio hasta meta
        explorados  : lista de (x, y) en orden de visita (para visualizar)
        metricas    : dict con nodos_generados, nodos_expandidos, costo_total
    """
    inicio = laberinto.inicio
    meta   = laberinto.meta

    # Frontera: cola FIFO. Cada elemento es (nodo_actual, camino_hasta_aqui)
    frontera  = deque()
    frontera.append((inicio, [inicio]))

    visitados = set()
    visitados.add(inicio)

    nodos_generados  = 1   # el nodo inicial ya se genera
    nodos_expandidos = 0

    while frontera:
        nodo_actual, camino = frontera.popleft()
        nodos_expandidos += 1

        if nodo_actual == meta:
            # Calcular costo real del camino (respetando costos de fantasmas)
            costo_total = _calcular_costo(laberinto, camino)
            metricas = {
                "nodos_generados":  nodos_generados,
                "nodos_expandidos": nodos_expandidos,
                "costo_total":      costo_total,
            }
            return camino, list(visitados), metricas

        # Expandir sucesores
        for (nx, ny), _ in laberinto.get_sucesores(*nodo_actual):
            if (nx, ny) not in visitados:
                visitados.add((nx, ny))
                nodos_generados += 1
                frontera.append(((nx, ny), camino + [(nx, ny)]))

    # Sin solución
    return [], list(visitados), {"nodos_generados": nodos_generados,
                                  "nodos_expandidos": nodos_expandidos,
                                  "costo_total": float('inf')}


def dfs(laberinto):
    """
    Búsqueda en Profundidad (Depth-First Search).
    Explora un camino hasta el fondo antes de retroceder.
    NO garantiza la ruta óptima ni en pasos ni en costo.

    Retorna:
        ruta        : lista de (x, y) desde inicio hasta meta
        explorados  : lista de (x, y) en orden de visita
        metricas    : dict con nodos_generados, nodos_expandidos, costo_total
    """
    inicio = laberinto.inicio
    meta   = laberinto.meta

    # Frontera: pila LIFO. Cada elemento es (nodo_actual, camino_hasta_aqui)
    frontera = []
    frontera.append((inicio, [inicio]))

    visitados = set()
    visitados.add(inicio)

    nodos_generados  = 1
    nodos_expandidos = 0
    orden_exploracion = []

    while frontera:
        nodo_actual, camino = frontera.pop()   # POP del final = LIFO
        nodos_expandidos += 1
        orden_exploracion.append(nodo_actual)

        if nodo_actual == meta:
            costo_total = _calcular_costo(laberinto, camino)
            metricas = {
                "nodos_generados":  nodos_generados,
                "nodos_expandidos": nodos_expandidos,
                "costo_total":      costo_total,
            }
            return camino, orden_exploracion, metricas

        for (nx, ny), _ in laberinto.get_sucesores(*nodo_actual):
            if (nx, ny) not in visitados:
                visitados.add((nx, ny))
                nodos_generados += 1
                frontera.append(((nx, ny), camino + [(nx, ny)]))

    return [], orden_exploracion, {"nodos_generados": nodos_generados,
                                    "nodos_expandidos": nodos_expandidos,
                                    "costo_total": float('inf')}


def ucs(laberinto):
    """
    Búsqueda de Costo Uniforme (Uniform Cost Search).
    Expande siempre el nodo de MENOR COSTO ACUMULADO.
    Garantiza la ruta ÓPTIMA considerando que los fantasmas ('2') cuestan 10
    y las celdas normales cuestan 1.

    Frontera: min-heap de (costo_acumulado, contador_desempate, nodo, camino)

    Retorna:
        ruta        : lista de (x, y) desde inicio hasta meta
        explorados  : lista de (x, y) en orden de expansión
        metricas    : dict con nodos_generados, nodos_expandidos, costo_total
    """
    inicio = laberinto.inicio
    meta   = laberinto.meta

    # (costo_g, contador, nodo, camino)
    contador = 0  # desempate cuando dos nodos tienen igual costo
    frontera = [(0, contador, inicio, [inicio])]
    heapq.heapify(frontera)

    # Diccionario: nodo -> menor costo conocido para llegar a él
    costo_minimo = {inicio: 0}

    nodos_generados  = 1
    nodos_expandidos = 0
    orden_exploracion = []

    while frontera:
        costo_g, _, nodo_actual, camino = heapq.heappop(frontera)
        nodos_expandidos += 1
        orden_exploracion.append(nodo_actual)

        if nodo_actual == meta:
            metricas = {
                "nodos_generados":  nodos_generados,
                "nodos_expandidos": nodos_expandidos,
                "costo_total":      costo_g,
            }
            return camino, orden_exploracion, metricas

        # Descartar si ya encontramos un camino más barato a este nodo
        if costo_g > costo_minimo.get(nodo_actual, float('inf')):
            continue

        for (nx, ny), costo_paso in laberinto.get_sucesores(*nodo_actual):
            nuevo_costo = costo_g + costo_paso

            if nuevo_costo < costo_minimo.get((nx, ny), float('inf')):
                costo_minimo[(nx, ny)] = nuevo_costo
                nodos_generados += 1
                contador += 1
                heapq.heappush(frontera, (nuevo_costo, contador, (nx, ny),
                                          camino + [(nx, ny)]))

    return [], orden_exploracion, {"nodos_generados": nodos_generados,
                                    "nodos_expandidos": nodos_expandidos,
                                    "costo_total": float('inf')}


# Función auxiliar


def _calcular_costo(laberinto, camino):
    """Suma el costo real de recorrer el camino dado."""
    costo = 0
    for x, y in camino[1:]:   # el nodo inicio no tiene costo de entrada
        valor = laberinto.matriz[y][x]
        costo += 10 if valor == '2' else 1
    return costo


def imprimir_metricas(nombre_algoritmo, metricas, tiene_solucion):
    """Imprime en consola una tabla sencilla con los resultados."""
    print(f"\n{'='*45}")
    print(f"  Algoritmo : {nombre_algoritmo}")
    print(f"  Solución  : {'SÍ' if tiene_solucion else 'NO'}")
    print(f"  Nodos generados  : {metricas['nodos_generados']}")
    print(f"  Nodos expandidos : {metricas['nodos_expandidos']}")
    print(f"  Costo total      : {metricas['costo_total']}")
    print(f"{'='*45}")