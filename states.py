import pygame

from components import ui
from components.graph import Graph, Vertex


class State:
    def __init__(self):
        self.graph = None
        self.ui_elements = []
        self.done = False
        self.next_state = None
        self.prev_state = None
        self.persist = {}

    def startup(self, persistent: dict[str]):
        self.done = False
        self.next_state = None
        self.persist = persistent
        self.graph = persistent['graph']

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

    def change_state(self, next_state: str):
        self.next_state = next_state
        self.done = True


class DefaultState(State):
    def __init__(self):
        super().__init__()

    def startup(self, persistent: dict[str]):
        super().startup(persistent)
        self.ui_elements = []
        self.vertex_counter = ui.NumberInput(200, 100, 900, 200, self.graph.num_vertices)
        self.ui_elements.append(self.vertex_counter)
        self.ui_elements.append(ui.InputLabel(200, 50, 900, 150, "Number of vertices"))

    def update(self):
        num_vertices = self.vertex_counter.value
        super().update()
        if self.graph.num_vertices < num_vertices:
            self.graph.add_vertex()
        elif self.graph.num_vertices > num_vertices:
            self.graph.remove_vertex()

    def get_event(self, event: pygame.event.Event):
        super().get_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                x, y = mouse_pos
                vertex = self.graph.check_vertex_collision(x, y)
                if vertex:
                    self.vertex_selected(vertex)

    def vertex_selected(self, vertex: Vertex):
        self.persist['selected_vertex'] = vertex
        self.change_state("VERTEX_SELECTED")


class VertexSelected(State):
    def __init__(self):
        super().__init__()
        self.selected_vertex = None
        self.selected_vertex_label = None

    def startup(self, persistent: dict[str]):
        super().startup(persistent)
        self.selected_vertex = persistent['selected_vertex']
        self.ui_elements = []
        self.selected_vertex_label = ui.InputLabel(200, 50, 900, 150, "Selected vertex: " + str(self.selected_vertex.label))
        self.ui_elements.append(self.selected_vertex_label)
        self.ui_elements.append(ui.Button(200, 50, 900, 200, self.add_edge, "Add Edge"))
        self.ui_elements.append(ui.Button(200, 50, 900, 300, self.delete_edge, "Remove Edge"))
        self.ui_elements.append(ui.Button(200, 50, 900, 400, self.delete_vertex, "Remove Vertex"))

    def add_edge(self):
        self.persist['manage_edges_mode'] = "add"
        self.persist['selected_vertex'] = self.selected_vertex
        self.change_state("MANAGE_EDGES")

    def delete_edge(self):
        self.persist['manage_edges_mode'] = "remove"
        self.persist['selected_vertex'] = self.selected_vertex
        self.change_state("MANAGE_EDGES")

    def delete_vertex(self):
        self.graph.remove_vertex(self.selected_vertex.label)
        self.done = True

    def get_event(self, event: pygame.event.Event):
        super().get_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                x, y = mouse_pos
                vertex = self.graph.check_vertex_collision(x, y)
                if vertex:
                    self.selected_vertex = vertex
                    self.selected_vertex_label.value = "Selected vertex: " +  str(self.selected_vertex.label)
                elif self.graph.rect.collidepoint(mouse_pos):
                    self.done = True



class ManageEdges(State):
    def __init__(self):
        super().__init__()
        self.selected_vertex = None
        self.mode = None

    def startup(self, persistent: dict[str]):
        super().startup(persistent)
        self.mode = persistent['manage_edges_mode']
        self.selected_vertex = persistent['selected_vertex']
        self.ui_elements = []
        self.ui_elements.append(ui.InputLabel(200, 50, 900, 150, "Select a vertex"))
        self.ui_elements.append(ui.Button(50, 50, 975, 250, self.cancel, "X", color="red", text_color="white"))

    def cancel(self):
        self.done = True

    def get_event(self, event: pygame.event.Event):
        super().get_event(event)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                x, y = mouse_pos
                vertex = self.graph.check_vertex_collision(x, y)
                if vertex:
                    if self.mode == "add":
                        self.graph.add_edge(self.selected_vertex, vertex)
                    else:
                        self.graph.remove_edge(self.selected_vertex, vertex)
                    self.done = True

