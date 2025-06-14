class node:
    def __init__(self, pygame, screen, w, h, rows, cols, x, y):
        self.pygame = pygame
        self.screen = screen
        self.w = w
        self.h = h
        self.rows = rows
        self.cols = cols
        self.x = x  
        self.y = y  
        self.pixel_x = x * w  
        self.pixel_y = y * h 
        self.is_obsetecle = False
        self.weight = 1 
    def show(self, color, thickness):
        self.pygame.draw.rect(self.screen, color, (self.pixel_x, self.pixel_y, self.w, self.h), thickness)
        self.pygame.display.update() 