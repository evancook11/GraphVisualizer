import pygame
from components import ui, graph
import config
import states

class Engine:
    def __init__(self):
        self.cur_graph = graph.Graph(config.DEFAULT_NUM_VERTICES)
        self.running = True
        self.state = states.DefaultState(self.cur_graph)
        self.screen = pygame.display.get_surface()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.state.get_event(event)

    def update(self):
        self.state.update()

    def draw(self):
        self.state.draw(self.screen)

    def run(self):
        while self.running:
            self.event_loop()
            self.update()
            self.draw()
            pygame.display.flip()
