import pygame
from utils import fonts
from math import sin, cos, radians

class Graph:
    def __init__(self, num_vertices):
        self.vertices = [Vertex(i) for i in range(1, num_vertices + 1)]
        self.edges = []

    def add_vertex(self, x=0, y=0):
        self.vertices.append(Vertex(len(self.vertices) + 1,x, y))

    def remove_vertex(self):
        self.vertices.pop()

    def draw_vertices_fixed(self, screen: pygame.Surface):
        font = fonts.arial(20)
        if len(self.vertices) == 1:
            x, y = screen.get_rect().center
            pygame.draw.circle(screen, self.vertices[0].color, (x, y), self.vertices[0].radius)
            text = font.render(str(self.vertices[0].label), True, "black")
            screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
        else:
            graph_radius = screen.get_rect().width // 3
            for i, vertex in enumerate(self.vertices):
                angle = 360 / len(self.vertices) * i
                angle = radians(angle)
                x = cos(angle) * graph_radius + screen.get_rect().centerx
                y = sin(angle) * graph_radius + screen.get_rect().centery
                pygame.draw.circle(screen, vertex.color, (x, y), vertex.radius)
                text = font.render(str(vertex.label), True, "black")
                screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))


class Vertex:
    def __init__(self, label, x=0, y=0, color='gray', radius=20):
        self.x = x
        self.y = y
        self.label = label
        self.radius = radius
        self.color = color

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)