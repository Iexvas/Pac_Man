# src/main.py
import pygame
import sys
from laberinto import Laberinto
from interfaz import Interfaz
from busqueda_ciega import bfs, dfs, ucs, imprimir_metricas
from busqueda_informada import a_estrella, gbfs

def main():
    print("INICIANDO ENTORNO PAC-MAN")
    mi_laberinto_inicial = Laberinto('mapas/mapa_facil.txt')
    app = Interfaz(mi_laberinto_inicial)

    app.reproducir_inicio()
    
    reloj = pygame.time.Clock()
    escena_actual = "inicio"
    corriendo = True
    mi_laberinto = mi_laberinto_inicial 

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if escena_actual == "inicio":
                    if app.rect_boton_iniciar.collidepoint(mouse_pos):
                        if app.sonido_inicio:
                            app.sonido_inicio.stop()
                        escena_actual = "mapas"
                
                elif escena_actual == "mapas":
                    if app.rect_btn_volver_inicio.collidepoint(mouse_pos):
                        escena_actual = "inicio"
                    else:
                        for btn in app.botones_mapas:
                            if btn["rect"].collidepoint(mouse_pos):
                                print(f"\n--- Cargando {btn['texto']} ---")
                                mi_laberinto = Laberinto(btn["archivo"])
                                app.actualizar_laberinto(mi_laberinto)
                                escena_actual = "juego"
                                app.dibujar() 
                
                elif escena_actual == "juego":
                    if app.rect_btn_volver_mapas.collidepoint(mouse_pos):
                        escena_actual = "mapas"
                    else:
                        for nombre_alg, rect_alg in app.botones_algoritmos.items():
                            if rect_alg.collidepoint(mouse_pos):
                                app.dibujar() 
                                
                                if nombre_alg == "BFS":
                                    ruta, explorados, metrica = bfs(mi_laberinto)
                                elif nombre_alg == "DFS":
                                    ruta, explorados, metrica = dfs(mi_laberinto)
                                elif nombre_alg == "UCS":
                                    ruta, explorados, metrica = ucs(mi_laberinto)
                                elif nombre_alg == "GBFS":
                                    ruta, explorados, metrica = gbfs(mi_laberinto)
                                elif nombre_alg == "A*":
                                    ruta, explorados, metrica = a_estrella(mi_laberinto)
                                
                                imprimir_metricas(nombre_alg, metrica, bool(ruta))
                                if ruta:
                                    app.dibujar_rastro(explorados, ruta)

        if escena_actual == "inicio":
            app.dibujar_menu()
        elif escena_actual == "mapas":
            app.dibujar_menu_mapas()
        elif escena_actual == "juego":
            app.dibujar_panel_algoritmos()
            pygame.display.flip()

        reloj.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()