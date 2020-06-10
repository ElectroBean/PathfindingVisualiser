from Classes.GridCell import GridCell
import pygame
import numpy
from threading import Thread
import time


class Grid:
    gridCells = [GridCell]
    grid_as_array = [[]]
    sizeX = int
    sizeY = int
    cellSizeX = float
    cellSizeY = float

    def __init__(self, size_x, size_y, cell_size_x, cell_size_y):
        self.sizeX = size_x
        self.sizeY = size_y
        self.cellSizeX = cell_size_x
        self.cellSizeY = cell_size_y
        self.grid_as_array = [[None for i in range(size_x)] for j in range(size_y)]
        thread = Thread(self.initialize_grid())
        thread.start()

    def hextorgb(self, hex):
        h = hex.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def initialize_grid(self):
        self.gridCells.clear()
        for y in range(0, self.sizeY):
            for x in range(0, self.sizeX):
                newCell = GridCell(x * (self.cellSizeX * 1), 50 + y * (self.cellSizeY * 1), self.cellSizeX * 1,
                                   self.cellSizeY * 1, True, x, y)
                self.gridCells.append(newCell)
                self.grid_as_array[y][x] = newCell
        #for i in range(0, self.sizeY * self.sizeX):
        #    y = int(i / self.sizeY)
        #    x = int(i % self.sizeX)
        #    newCell = GridCell(x * (self.cellSizeX * 1), y * (self.cellSizeY * 1), self.cellSizeX * 1,
        #                       self.cellSizeY * 1, True, x, y)
        #    self.gridCells.append(newCell)
        #    self.grid_as_array[x][y] = newCell

            pass
        self.set_neighbours_of_cells()

    def set_neighbours_of_cells(self):
        for currentCell in self.gridCells:
            searchneighbours = []
            for y in range(currentCell.celly - 1, currentCell.celly + 2):
                for x in range(currentCell.cellx - 1, currentCell.cellx + 2):
                    if x < 0 or x > self.sizeX - 1 or y < 0 or y > self.sizeY - 1 \
                            or self.grid_as_array[y][x] is currentCell:
                        continue
                    searchneighbours.append(self.grid_as_array[y][x])
                    distance = abs(currentCell.cellx - self.grid_as_array[y][x].cellx) \
                               + abs(currentCell.celly - self.grid_as_array[y][x].celly)
                    if distance <=1:
                        currentCell.connect_cell(self.grid_as_array[y][x])
            currentCell.searchneighbours = searchneighbours

    def get_neighbours(self):
        neighbours = []
        for y in range(self.celly - 1, self.celly + 2):
            for x in range(self.cellx - 1, self.cellx + 2):
                if x < 0 or x > self.grid.sizeX - 1 or y < 0 or y > self.grid.sizeY - 1 or self.grid.grid_as_array[y][x] is self:
                    continue
                neighbours.append(self.grid.grid_as_array[y][x])
        return neighbours

    def update(self, window: pygame.Surface):
        for element in self.gridCells:
            element.draw_cell(window)
            if pygame.mouse.get_pressed()[0]:
                element.update()

    def find_grid_cell(self, position):
        for element in self.gridCells:
            my_rect = pygame.Rect((element.x, element.y, element.size_x, element.size_y))
            if my_rect.collidepoint(position):
                return element
        return None
