import pygame
from utils import fonts

DEFAULT_FONT = fonts.arial(20)

class UIElement:
    def __init__(self, width, height, x, y):
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect(topleft=(x, y))
        self.active = False
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def check_collide(self, pos):
        return self.rect.collidepoint(pos)

    def update(self):
        pass

    def on_click(self, pos):
        pass

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))

class NumberInput(UIElement):
    def __init__(self, width, height, x, y, value=0):
        super().__init__(width, height, x, y)
        self.value = value
        button_size = (width // 5, height)
        self.dec_rect = pygame.Rect((0, 0), button_size)
        self.inc_rect = pygame.Rect((width - button_size[0], 0), button_size)
        self.font = fonts.arial(40)


    def update(self):
        self.surface.fill("white")
        text = self.font.render(str(self.value), True, "black")
        pygame.draw.rect(self.surface, "green", self.inc_rect)
        pygame.draw.rect(self.surface, "red", self.dec_rect)

        self.surface.blit(text, (self.width // 2 - text.width // 2, self.height // 2 - text.height // 2))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, (self.x, self.y))


    def on_click(self, pos):
        x, y = pos
        x -= self.rect.x
        y -= self.rect.y
        if self.inc_rect.collidepoint((x, y)):
            self.value += 1
        elif self.dec_rect.collidepoint((x, y)) and self.value > 0:
            self.value -= 1


class InputLabel(UIElement):
    def __init__(self, width, height, x, y, value="", font=DEFAULT_FONT):
        super().__init__(width, height, x, y)
        self.value = value
        self.font = font
        self.text = self.font.render(self.value, True, "black")

    def update(self):
        self.surface.fill("skyblue")
        self.text = self.font.render(self.value, True, "black")
        self.surface.blit(self.text, (self.width // 2 - self.text.width // 2, self.height // 2 - self.text.height // 2))

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))

class Button(UIElement):
    def __init__(self, width, height, x, y, callback=None, text="", font=DEFAULT_FONT, color="white", text_color="black"):
        super().__init__(width, height, x, y)
        self.callback = callback
        self.text_color = text_color
        self.text = font.render(text, True, text_color)
        self.color = color

    def update(self):
        self.surface.fill(self.color)
        self.surface.blit(self.text, (self.width // 2 - self.text.width // 2, self.height // 2 - self.text.height // 2))

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def on_click(self, pos):
        if self.callback:
            self.callback()

