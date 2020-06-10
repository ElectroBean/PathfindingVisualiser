import pygame

class Button:

    rect = ()
    function = None
    text = ""
    text_size = 15
    text_color = ()
    color = ()
    hover_color = ()
    font = None

    def __init__(self, rect, function, text, text_size, text_color, color, hover_color):
        self.rect = rect
        self.function = function
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont(None, self.text_size)
        pass

    def on_click(self):
        print("blah", ": you touched a butt(on)")
        self.function()
        pass

    def on_mouse_over(self):
        pass

    def draw(self, window: pygame.Surface):
        pygame.draw.rect(window, self.color, self.rect)
        text = self.font.render(self.text, 1, self.text_color)
        window.blit(text, self.rect)

        pass

    def update(self, window: pygame.Surface):
        self.draw(window)
        #for event in pygame.event.get():
        #    if event.type == pygame.MOUSEBUTTONUP:
        #        print("clicked button")
        #        if pygame.Rect(self.rect).collidepoint(pygame.mouse.get_pos()):
        #            self.on_click()

    def check_button_click(self, position):
        if pygame.Rect(self.rect).collidepoint(position):
            self.on_click()

    pass