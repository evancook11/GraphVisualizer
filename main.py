import pygame
from components import ui, graph
import config
from engine import Engine




if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))



        # graph_display.fill("white")

        # cur_graph.draw_vertices_fixed(graph_display)

        # screen.blit(graph_display, (20, (config.SCREEN_HEIGHT // 2 - config.GRAPH_DISPLAY_HEIGHT // 2)))

        # for element in ui_elements:
        #     element.update()
        #     screen.blit(element.surface, (element.x, element.y))



        # pygame.display.flip()

    engine = Engine()
    engine.run()

    pygame.quit()
