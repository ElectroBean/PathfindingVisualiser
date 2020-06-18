import pygame
import math
import sys

class GridCell:
    cellx = 0
    celly = 0
    x = 0
    y = 0
    size_x = 0
    size_y = 0
    neighbours = []
    color = (128, 0, 128)
    G = 0
    H = 0
    F = 0
    visited = False
    on_path = False
    traversable = True
    parent = None
    meant_to_be_here = False
    looked_at = False
    i_x = 0
    i_y = 0
    color_dict = {"":""}
    searchneighbours = []

    def __init__(self, x, y, size_x, size_y, yes, cellx, celly):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.meant_to_be_here = yes
        self.neighbours = []
        self.visited = False
        self.on_path = False
        self.traversable = True
        self.parent = None
        self.cellx = cellx
        self.celly = celly
        self.G = sys.maxsize
        self.F = sys.maxsize
        self.looked_at = False
        self.color = GridCell.hextorgb("EAB0D9")
        self.color_dict = {"walkable": "EAB0D9",
                           "obstacle": "5D5B6A",
                           "origin/destination": "F67280",
                           "searching": "A4D4AE",
                           "searchedneighbour": "87A8D0",
                           "path": "DFE38E"}
        self.searchneighbours = []

    def reset_path_values(self):
        self.parent = None
        self.G = sys.maxsize
        self.F = sys.maxsize
        self.looked_at = False

    def reset(self):
        self.parent = None
        self.G = sys.maxsize
        self.F = sys.maxsize
        self.looked_at = False
        self.traversable = True
        self.color = self.hextorgb(self.color_dict["walkable"])
        pass

    def distance_to_cell(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def draw_cell(self, window: pygame.Surface):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size_x, self.size_y))
        #if len(self.neighbours) > 0:
            #for element in self.neighbours:
                #pygame.draw.line(window, (128, 0, 128), (self.x + self.size_x / 2, self.y + self.size_y / 2), (element.x + element.size_x / 2, element.y + element.size_y / 2), 1)

    def on_click(self):
        if self.traversable is True:
            self.traversable = False
            self.color = self.hextorgb(self.color_dict["obstacle"])
        else:
            self.traversable = True
            self.color = self.hextorgb(self.color_dict["walkable"])

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            if pygame.Rect((self.x, self.y, self.size_x, self.size_y)).collidepoint(pygame.mouse.get_pos()):
                self.on_click()

    def connect_cell(self, other):
        if other in self.neighbours or self in other.neighbours:
            return None
        self.neighbours.insert(0, other)
        other.neighbours.insert(0, self)

    @staticmethod
    def hextorgb(hex):
        h = hex.lstrip('#')
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
