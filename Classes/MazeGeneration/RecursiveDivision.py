from Classes.Grid import Grid
from Classes.GridCell import GridCell
import random
import math
import time


class RecursiveDivision:
    stack = []
    current_cell = None

    def __init__(self):
        pass

    def test_cell(self, grid_cell: GridCell):
        for cell in grid_cell.neighbours:
            cell.looked_at = False
        goodcell = False

        while goodcell is False:
            current_cell = random.choice(grid_cell.neighbours)
            canuse = True
            canContinue = False
            if current_cell.looked_at is True:
                for cell in grid_cell.neighbours:
                    if cell.looked_at is False:
                        canContinue = True


                if canContinue is False:
                    print("should remove from stack: ", len(self.stack))
                    # remove from end of stack
                    # set current to new end
                    if len(self.stack) > 0:
                        self.stack.pop(len(self.stack) - 1)
                    if len(self.stack) > 0:
                        self.current_cell = self.stack[len(self.stack) - 1]
                    return

                continue
            else:
                current_cell.looked_at = True

            # check cells around the current cell and see if any of them are already removed
            for cell in current_cell.neighbours:
                # make sure the neighbour isnt the testing cell
                if cell is grid_cell:
                    continue
                # is the neighbour is not traversable set canuse to false
                if cell.traversable is False:
                    canuse = False
                pass

            # if the current cells neighbours are all traversable set it to non-traversable
            if canuse is True:
                current_cell.traversable = False
                current_cell.color = (255, 0, 0)

                self.stack.append(grid_cell)
                self.current_cell = current_cell
                goodcell = True
            else:

                pass
        pass

    def create_maze(self, grid: Grid):
        # initialize stack and insert a random grid cell
        self.test_cell(random.choice(grid.gridCells))
        counter = 0
        while len(self.stack) > 0:
            counter += 1
            if counter > 500:
                return
            self.test_cell(self.current_cell)

            pass

        pass

    def test_new_cell(self, grid: Grid, grid_cell: GridCell):
        while True:
            # count the neighbours ive looked at
            neighbourslookedat = 0
            for cell in grid_cell.neighbours:
                if cell.looked_at is True:
                    neighbourslookedat += 1

            # if i've gone through all available neighbours
            if neighbourslookedat == len(grid_cell.neighbours):
                # check the stack isn't empty
                if len(self.stack) > 0:
                    # drop the current cell and set it to popped stack cell
                    # also reset values of popped
                    self.current_cell = self.stack.pop()
                    self.current_cell.traversable = False
                    self.current_cell.color = (255, 0, 0)
                    print("popped, len is: ", len(self.stack))
                    return
                else:
                    # if stack is empty, return
                    return

            # set current to random neighbour of current
            currentCell = random.choice(grid_cell.neighbours)
            # make sure we haven't looked at it already, redundancy check
            while currentCell.looked_at is True:
                currentCell = random.choice(grid_cell.neighbours)
            # if i cant place it at the current neighbour
            if self.check_neighbours(grid, currentCell) is False:
                # rerun this function with updated neighbour variables
                self.test_new_cell(grid, self.current_cell)
            else:
                # if i can place it, it has been placed
                return
        pass

    def check_neighbours(self, grid: Grid, grid_cell: GridCell):
        currentIndex = (self.current_cell.cellx, self.current_cell.celly)

        grid_cell.looked_at = True

        direction = (grid_cell.cellx - self.current_cell.cellx, grid_cell.celly - self.current_cell.celly)

        thing = 0

        for y in range(grid_cell.celly - 1, grid_cell.celly + 1):
            for x in range(grid_cell.cellx - 1, grid_cell.cellx + 1):
                if direction == (-1, 0) or direction == (1, 0):
                    if x < 0 or x > grid.sizeX - 1 or y < 0 or y > grid.sizeY - 1 or y is currentIndex[1]:
                        continue
                elif direction == (0, -1) or direction == (0, 1):
                    if x < 0 or x > grid.sizeX - 1 or y < 0 or y > grid.sizeY - 1 or x is currentIndex[0]:
                        continue

                if grid.grid_as_array[x][y].traversable is True:
                    return False

        if grid_cell.traversable is True:
            return False

        self.stack.append(self.current_cell)
        self.current_cell = grid_cell
        grid_cell.traversable = True
        grid_cell.color = (128, 0, 128)
        return True

        pass

    def make_maze(self, grid: Grid):
        for cell in grid.gridCells:
            cell.traversable = False
            cell.color = (255, 0, 0)
        self.current_cell = random.choice(grid.gridCells)
        self.current_cell.traversable = True
        self.current_cell.color = (128, 0, 128)
        self.test_new_cell(grid, self.current_cell)
        counter = 0
        while len(self.stack) > 0:
            if counter > 10000:
                print("break counter")
                return
            counter += 1
            for cell in self.current_cell.neighbours:
                cell.looked_at = False
            self.test_new_cell(grid, self.current_cell)
            pass

        print("Completed Maze")
        pass

    # working maze generation using prim's algorithm
    # https://stackoverflow.com/questions/23843197/maze-generating-algorithm-in-grid
    def make_new_maze(self, grid: Grid):
        # start with filled grid
        for cell in grid.gridCells:
            cell.traversable = False
            cell.color = GridCell.hextorgb(cell.color_dict["obstacle"])
            cell.looked_at = False
        # pick a cell, mark it as part of maze
        self.current_cell = random.choice(grid.gridCells)
        self.current_cell.traversable = True
        self.current_cell.color = GridCell.hextorgb(self.current_cell.color_dict["walkable"])
        # add surrounding cells to stack
        neigh = self.current_cell.searchneighbours
        self.stack.extend(neigh)
        # while stack is not empty
        while len(self.stack) > 0:
            # pick random cell from stack
            current = random.choice(self.stack)
            # if cell doesn't have 2 explored neighbours
            count = 0

            for cell in current.searchneighbours:

                direction = (cell.cellx - current.cellx, cell.celly - current.celly)

                if direction == (-1, 0) or direction == (1, 0):
                    if current.celly is cell.celly or current.celly == 0 or current.celly == grid.sizeY - 1:
                        # print("continued")
                        continue
                elif direction == (0, -1) or direction == (0, 1):
                    if current.cellx is cell.cellx or current.cellx == 0 or current.cellx == grid.sizeX - 1:
                        # print("continued")
                        continue

                if cell.traversable is True:
                    count += 1

            if count < 2:
                # make cell walkable
                current.traversable = True
                current.color = GridCell.hextorgb(cell.color_dict["walkable"])
                # add neighbours to stack
                for cell in current.searchneighbours:
                    if cell.looked_at is False and cell not in self.stack:
                        self.stack.append(cell)
                # self.stack.extend(current_neighbours)

            # remove cell from stack
            self.stack.remove(current)
            current.looked_at = True
            print("removed from stack at length: ", len(self.stack))
            pass
        print("Completed Maze")
        pass

    # static method to get nearby cells
    @staticmethod
    def get_neighbours(grid: Grid, grid_cell: GridCell):
        neighbours = []
        for y in range(grid_cell.celly - 1, grid_cell.celly + 2):
            for x in range(grid_cell.cellx - 1, grid_cell.cellx + 2):
                if x < 0 or x > grid.sizeX - 1 or y < 0 or y > grid.sizeY - 1 or grid.grid_as_array[x][y] is grid_cell:
                    continue
                neighbours.append(grid.grid_as_array[x][y])
        return neighbours
