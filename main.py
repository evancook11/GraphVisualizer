import pygame
from components import ui, graph
import config
from engine import Engine
import states





if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    state_dict = {"DEFAULT": states.DefaultState(), "VERTEX_SELECTED": states.VertexSelected(), "MANAGE_EDGES": states.ManageEdges()}

    engine = Engine(state_dict, "DEFAULT")
    engine.run()

    pygame.quit()
