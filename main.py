import pygame
from components import ui, graph

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRAPH_DISPLAY_WIDTH = SCREEN_WIDTH / 2
GRAPH_DISPLAY_HEIGHT = SCREEN_HEIGHT * 0.8


if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    graph_display = pygame.Surface((GRAPH_DISPLAY_WIDTH, GRAPH_DISPLAY_HEIGHT))

    num_vertices = 10

    cur_graph = graph.Graph(num_vertices)
    vertex_counter = ui.NumberInput(200, 100, 900, 200, num_vertices)

    ui_elements = [vertex_counter,
                   ui.InputLabel(200, 50, 900, 150, "Number of vertices")]

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for element in ui_elements:
                        if element.check_collide(mouse_pos):
                            element.on_click(mouse_pos)

        screen.fill("sky blue")

        graph_display.fill("white")

        if num_vertices < vertex_counter.value:
            num_vertices = vertex_counter.value
            cur_graph.add_vertex()
        elif num_vertices > vertex_counter.value:
            num_vertices = vertex_counter.value
            cur_graph.remove_vertex()

        cur_graph.draw_vertices_fixed(graph_display)

        screen.blit(graph_display, (20, (SCREEN_HEIGHT // 2 - GRAPH_DISPLAY_HEIGHT // 2)))

        for element in ui_elements:
            element.update()
            screen.blit(element.surface, (element.x, element.y))



        pygame.display.flip()

    pygame.quit()
