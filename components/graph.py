import pygame
from utils import fonts
from math import sin, cos, radians
import config

class Graph:
    def __init__(self, num_vertices):
        self.vertices = [Vertex(i) for i in range(1, num_vertices + 1)]
        self.num_vertices = num_vertices
        self.edges = []
        self.display = pygame.Surface((config.GRAPH_DISPLAY_WIDTH, config.GRAPH_DISPLAY_HEIGHT))
        self.reset_vertex_positions()


    def add_vertex(self, x=0, y=0):
        self.vertices.append(Vertex(len(self.vertices) + 1, x, y))
        self.num_vertices += 1
        self.reset_vertex_positions()


    def remove_vertex(self, vertex_label=None):
        if vertex_label is None:
            self.vertices.pop()
            self.num_vertices -= 1
        else:
            self.vertices = list(filter(lambda v: v.label != vertex_label, self.vertices))
            self.num_vertices = len(self.vertices)
        self.reset_vertex_positions()


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
        for vertex in self.vertices:
            vertex.draw(self.display)
        screen.blit(self.display, (20, (config.SCREEN_HEIGHT // 2 - config.GRAPH_DISPLAY_HEIGHT // 2)))

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