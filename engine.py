import pygame
from components import ui, graph
import config
from states import State
class Engine:
    def __init__(self, states: dict[str, State], start_state: str):
        self.cur_graph = graph.Graph(config.DEFAULT_NUM_VERTICES, 20, config.SCREEN_HEIGHT // 2 - config.GRAPH_DISPLAY_HEIGHT // 2)
        self.running = True
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]
        self.state.startup({"graph": self.cur_graph})
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

    def change_state(self):
        if self.state.done:
            if self.state.next_state:
                prev_state = self.state_name
                persistent = self.state.persist
                print(persistent)
                self.state_name = self.state.next_state
                self.state = self.states[self.state_name]
                self.state.startup(persistent)
                self.state.prev_state = prev_state
            else:
                persistent = self.state.persist
                self.state_name = self.state.prev_state
                self.state = self.states[self.state_name]
                self.state.startup(persistent)


    def run(self):
        while self.running:
            self.event_loop()
            self.change_state()
            self.update()
            self.draw()
            pygame.display.flip()
