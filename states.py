import pygame

from components import ui
from components.graph import Graph


class State:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.ui_elements = []
        self.done = False

    def update(self):
        for element in self.ui_elements:
            element.update()
        self.graph.update()

    def draw(self, screen: pygame.Surface):
        screen.fill("sky blue")

        for element in self.ui_elements:
            element.draw(screen)
        self.graph.draw(screen)

    def get_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for element in self.ui_elements:
                    if element.rect.collidepoint(mouse_pos):
                        element.on_click(mouse_pos)

class DefaultState(State):
    def __init__(self, graph: Graph):
        super().__init__(graph)
        self.vertex_counter = ui.NumberInput(200, 100, 900, 200, graph.num_vertices)
        self.ui_elements.append(self.vertex_counter)
        self.ui_elements.append(ui.InputLabel(200, 50, 900, 150, "Number of vertices"))

    def update(self):
        num_vertices = self.vertex_counter.value
        super().update()
        if self.graph.num_vertices < num_vertices:
            self.graph.add_vertex()
        elif self.graph.num_vertices > num_vertices:
            self.graph.remove_vertex()

    def draw(self, screen: pygame.Surface):
        super().draw(screen)

