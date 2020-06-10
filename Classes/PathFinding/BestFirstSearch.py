from Classes.Grid import Grid
from Classes.GridCell import GridCell
import time
from threading import Thread
import sys
import math

class BestFirstSearch:
    open_list = []
    closed_list = []
    path = []

    def __init__(self):
        self.open_list = []
        self.closed_list = []
        self.path = []

    def find_best_cell(self):
        result = self.open_list[0]
        for i in range(0, len(self.open_list)):
            cell = self.open_list[i]
            if cell.F < result.F:
                result = cell
        return result

    @staticmethod
    def euclidean_distance(cellone: GridCell, celltwo: GridCell):
        return abs(abs((cellone.cellx - celltwo.cellx)) + abs((cellone.celly - celltwo.celly)))

    @staticmethod
    def manhattan(cellone, celltwo):
        return abs(cellone.x - celltwo.x) + abs(cellone.y - celltwo.y)

    @staticmethod
    def distance(cellone, celltwo):
        return math.sqrt((cellone.x - celltwo.x) * (cellone.x - celltwo.x) + (cellone.y - celltwo.y) * (cellone.y - celltwo.y))

    def return_path(self, grid: Grid, cell: GridCell):
        self.path.clear()
        current_cell = cell
        self.path.append(current_cell)
        while current_cell.parent is not None:
            current_cell = current_cell.parent
            self.path.append(current_cell)

        self.path.reverse()
        for element in self.path:
            element.color = GridCell.hextorgb(cell.color_dict["path"])
            time.sleep(0.05)
        self.reset_nodes(grid)

    def find_new_path(self, origin: GridCell, destination: GridCell):
        print("Starting search")
        self.open_list.clear()
        self.closed_list.clear()
        self.open_list.insert(0, origin)

        origin.G = 0
        origin.F = origin.G + self.euclidean_distance(origin, destination)
        while len(self.open_list) > 0:
            currentCell = min(self.open_list, key=lambda o: o.G + o.H)

            if currentCell is destination:
                thread = Thread(self.return_path(currentCell))
                thread.start()
                return

            self.open_list.remove(currentCell)
            self.closed_list.append(currentCell)

            currentCell.G = 0
            currentCell.F = self.euclidean_distance(currentCell, destination)

            currentCell.color = (0, 255, 0)

            for gc in currentCell.neighbours:
                if gc.traversable is False:
                    continue
                cost = currentCell.G + self.euclidean_distance(gc, currentCell)
                if gc in self.open_list and cost < gc.G:
                    self.open_list.remove(gc)
                    print("in open and less")
                if gc in self.closed_list and cost < gc.G:
                    self.closed_list.remove(gc)
                    self.open_list.append(gc)
                    gc.G = cost
                    gc.parent = currentCell
                    print("in closed and less")
                if gc not in self.open_list and gc not in self.closed_list:
                    self.open_list.append(gc)
                    gc.G = cost
                    gc.H = self.euclidean_distance(gc, destination)
                    gc.F = gc.G + gc.H
                    gc.parent = currentCell
                    gc.color = (0, 0, 255)
                time.sleep(0.01)
            time.sleep(0.01)

    def find_path(self, grid: Grid, origin: GridCell, destination: GridCell):
        print("Starting search")
        self.open_list.clear()
        self.closed_list.clear()
        self.open_list.append(origin)

        origin.G = 0
        origin.F = self.distance(origin, destination)

        while len(self.open_list) > 0:
            self.open_list.sort(key=lambda o: o.F)
            current_node = self.open_list[0]
            current_node.color = GridCell.hextorgb(current_node.color_dict["searching"])
            self.open_list.remove(current_node)
            self.closed_list.append(current_node)

            if current_node is destination:
                thread = Thread(self.return_path(grid, current_node))
                thread.start()
                print("Found path")
                return None

            for gc in current_node.neighbours:
                if gc is destination:
                    gc.parent = current_node
                    thread = Thread(self.return_path(grid, gc))
                    thread.start()
                    print("found path in child")
                    return None
                if gc not in self.closed_list and gc.traversable is True:
                    if gc not in self.open_list:
                        self.open_list.append(gc)
                        gc.parent = current_node
                        gc.color = GridCell.hextorgb(current_node.color_dict["searchedneighbour"])

                localGoal = current_node.G + self.distance(current_node, gc)

                if localGoal < gc.G:
                    gc.parent = current_node
                    gc.G = localGoal
                    gc.F = gc.G + self.distance(gc, destination)
                time.sleep(0.001)
            time.sleep(0.001)

    def reset_nodes(self, grid):
        for cell in grid.gridCells:
            cell.reset_path_values()
