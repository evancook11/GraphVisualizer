import pygame
from utils import fonts
from math import sin, cos, radians
import config

class Graph:
    def __init__(self, num_vertices, x, y):
        self.vertices = [Vertex(i) for i in range(1, num_vertices + 1)]
        self.num_vertices = num_vertices
        self.edges = [{self.vertices[0], self.vertices[1]}, {self.vertices[3], self.vertices[5]}]
        self.display = pygame.Surface((config.GRAPH_DISPLAY_WIDTH, config.GRAPH_DISPLAY_HEIGHT))
        self.reset_vertex_positions()
        self.rect = self.display.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
        self.labels = {i for i in range(1, num_vertices + 1)}

    def add_vertex(self, x=0, y=0):
        i = 1
        while i < self.num_vertices + 1:
            if i not in self.labels:
                break
            i += 1

        self.vertices.append(Vertex(i, x, y))
        self.labels.add(i)
        self.num_vertices += 1
        self.reset_vertex_positions()


    def remove_vertex(self, vertex_label=None):
        deleted_vertex = None
        if vertex_label is None:
            deleted_vertex = self.vertices.pop()
        else:
            for vertex in self.vertices:
                if vertex.label == vertex_label:
                    deleted_vertex = vertex
                    self.vertices.remove(vertex)
                    break
        for edge in self.edges:
            if edge[0] == deleted_vertex or edge[1] == deleted_vertex:
                self.edges.remove(edge)
        self.num_vertices -= 1
        self.labels.remove(deleted_vertex.label)
        if vertex_label is None:
            self.reset_vertex_positions()

    def add_edge(self, vertex_1, vertex_2):
        if vertex_1 != vertex_2 and [vertex_1, vertex_2] not in self.edges:
            self.edges.append({vertex_1, vertex_2})

    def remove_edge(self, vertex_1, vertex_2):
        if {vertex_1, vertex_2} in self.edges:
            self.edges.remove({vertex_1, vertex_2})

    def reset_vertex_positions(self):
        if self.num_vertices == 1:
            self.vertices[0].x = config.GRAPH_DISPLAY_WIDTH / 2
            self.vertices[0].y = config.GRAPH_DISPLAY_HEIGHT / 2
        else:
            graph_radius = config.GRAPH_DISPLAY_WIDTH // 3
            for i, vertex in enumerate(self.vertices):
                angle = 360 / len(self.vertices) * i
                angle = radians(angle)
                x = cos(angle) * graph_radius + config.GRAPH_DISPLAY_WIDTH / 2
                y = sin(angle) * graph_radius + config.GRAPH_DISPLAY_HEIGHT / 2
                vertex.x = x
                vertex.y = y


    def update(self):
        self.display.fill("white")

    def draw(self, screen: pygame.Surface):
        for edge in self.edges:
            edge = list(edge)
            pygame.draw.line(self.display, "black", (edge[0].x, edge[0].y), (edge[1].x, edge[1].y))

        for vertex in self.vertices:
            vertex.draw(self.display)

        screen.blit(self.display, (self.x, self.y))

    def check_vertex_collision(self, x, y):
        x -= self.x
        y -= self.y
        for vertex in self.vertices:
            if vertex.x - vertex.radius < x < vertex.x + vertex.radius and vertex.y - vertex.radius < y < vertex.y + vertex.radius:
                return vertex
        return None



class Vertex:
    def __init__(self, label, x=0, y=0, color='gray', radius=20):
        self.x = x
        self.y = y
        self.label = label
        self.radius = radius
        self.color = color

    def draw(self, screen: pygame.Surface):
        x, y = screen.get_rect().center
        font = fonts.arial(20)
        text = font.render(str(self.label), True, "black")
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        screen.blit(text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2))

