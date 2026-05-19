# src/busqueda_informada.py
# Implementación de A* y Greedy Best-First Search (GBFS)

import heapq

def heuristica_manhattan(a, b):
    """
    Calcula la distancia de Manhattan entre el punto a y el b.
    h(n) = |x1 - x2| + |y1 - y2|
    """
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_estrella(laberinto):
    """
    Algoritmo A*: f(n) = g(n) + h(n).
    Combina el costo real acumulado y la heurística hacia la meta.
    """
    inicio = laberinto.inicio
    meta = laberinto.meta
    
    # (prioridad f, costo_g, contador, nodo_actual, camino)
    contador = 0
    frontera = [(0 + heuristica_manhattan(inicio, meta), 0, contador, inicio, [inicio])]
    heapq.heapify(frontera)
    
    costo_minimo = {inicio: 0}
    nodos_generados = 1
    nodos_expandidos = 0
    orden_exploracion = []

    while frontera:
        f, g, _, nodo_actual, camino = heapq.heappop(frontera)
        nodos_expandidos += 1
        orden_exploracion.append(nodo_actual)

        if nodo_actual == meta:
            return camino, orden_exploracion, {
                "nodos_generados": nodos_generados,
                "nodos_expandidos": nodos_expandidos,
                "costo_total": g
            }

        if g > costo_minimo.get(nodo_actual, float('inf')):
            continue

        for (nx, ny), costo_paso in laberinto.get_sucesores(*nodo_actual):
            nuevo_costo_g = g + costo_paso
            if nuevo_costo_g < costo_minimo.get((nx, ny), float('inf')):
                costo_minimo[(nx, ny)] = nuevo_costo_g
                h = heuristica_manhattan((nx, ny), meta)
                f_n = nuevo_costo_g + h
                nodos_generados += 1
                contador += 1
                heapq.heappush(frontera, (f_n, nuevo_costo_g, contador, (nx, ny), camino + [(nx, ny)]))

    return [], orden_exploracion, {"nodos_generados": nodos_generados, "nodos_expandidos": nodos_expandidos, "costo_total": float('inf')}

def gbfs(laberinto):
    """
    Greedy Best-First Search: f(n) = h(n).
    Ignora el costo g(n) y solo se guía por la heurística.
    Es "ambicioso" y puede caer en rutas de alto costo si parecen más directas.
    """
    inicio = laberinto.inicio
    meta = laberinto.meta
    
    # (prioridad h, contador, nodo_actual, camino)
    contador = 0
    frontera = [(heuristica_manhattan(inicio, meta), contador, inicio, [inicio])]
    heapq.heapify(frontera)
    
    visitados = {inicio}
    nodos_generados = 1
    nodos_expandidos = 0
    orden_exploracion = []

    while frontera:
        h, _, nodo_actual, camino = heapq.heappop(frontera)
        nodos_expandidos += 1
        orden_exploracion.append(nodo_actual)

        if nodo_actual == meta:
            # Calculamos el costo real al final
            from busqueda_ciega import _calcular_costo
            return camino, orden_exploracion, {
                "nodos_generados": nodos_generados,
                "nodos_expandidos": nodos_expandidos,
                "costo_total": _calcular_costo(laberinto, camino)
            }

        for (nx, ny), _ in laberinto.get_sucesores(*nodo_actual):
            if (nx, ny) not in visitados:
                visitados.add((nx, ny))
                nodos_generados += 1
                contador += 1
                h_n = heuristica_manhattan((nx, ny), meta)
                heapq.heappush(frontera, (h_n, contador, (nx, ny), camino + [(nx, ny)]))

    return [], orden_exploracion, {"nodos_generados": nodos_generados, "nodos_expandidos": nodos_expandidos, "costo_total": float('inf')}