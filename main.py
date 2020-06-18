from threading import Thread
from Classes.Grid import Grid
import pygame, time
from Classes.Grid import Grid
from Classes.PathFinding.BestFirstSearch import BestFirstSearch
from Classes.MazeGeneration.RecursiveDivision import RecursiveDivision
from Classes.GridCell import GridCell
from Classes.GUI.Button import Button

pygame.init()
myWindow = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Pygame window")
myWindow.fill((138, 132, 117))
mouse_position = None
previous_mouse_position = None

# myGrid = Grid(15, 15, 22.8, 22.8)
# 500x450
myGrid = Grid(100, 90, 5, 5)
recursive = RecursiveDivision()

start = None
end = None

buttons = []


def update_game(window: pygame.Surface):
    myGrid.update(window)


def create_maze():
    thread2 = Thread(target=recursive.make_new_maze, args=(myGrid,))
    thread2.start()


def find_path():
    new_thread = Thread(target=pathfinding.find_path, args=(myGrid, start, end))
    new_thread.start()


def reset_grid():
    for cell in myGrid.gridCells:
        cell.reset()

    global start
    global end
    start = myGrid.gridCells[0]
    start.color = start.hextorgb(start.color_dict["origin/destination"])
    end = myGrid.gridCells[899]
    end.color = end.hextorgb(end.color_dict["origin/destination"])
    pass


buttons.append(Button(((500 / 2) - 50, 0, 100, 50), find_path, "Find Path", 30, (255, 255, 255), (204, 153, 255), (255, 0, 0)))
buttons.append(Button(((500 - 100), 0, 100, 50), create_maze, "Create Maze", 20, (255, 255, 255), (204, 153, 255), (255, 0, 0)))
buttons.append(Button((0, 0, 100, 50), reset_grid, "Reset Grid", 20, (255, 255, 255), (204, 153, 255), (255, 0, 0)))


def handle_button_click(position):
    for button in buttons:
        button.check_button_click(position)
        pass


def handle_mouse_move(position):

    pass


def update():
    running = True
    global start
    global end
    start = myGrid.gridCells[0]
    start.color = start.hextorgb(start.color_dict["origin/destination"])
    end = myGrid.gridCells[899]
    end.color = end.hextorgb(end.color_dict["origin/destination"])
    isTrue = True
    while running:

        pygame.time.delay(100)

        global mouse_position
        global previous_mouse_position
        mouse_position = pygame.mouse.get_pos()

        if mouse_position != previous_mouse_position:
            # add on mouse move event
            pass

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                handle_button_click(pygame.mouse.get_pos())
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    cell = myGrid.find_grid_cell(pygame.mouse.get_pos())
                    if cell is not None:
                        if start.traversable is True:
                            start.color = GridCell.hextorgb(start.color_dict["walkable"])
                        start = cell
                        start.color = GridCell.hextorgb(start.color_dict["origin/destination"])
                if event.key == pygame.K_2:
                    cell = myGrid.find_grid_cell(pygame.mouse.get_pos())
                    if cell is not None:
                        if end.traversable is True:
                            end.color = GridCell.hextorgb(start.color_dict["walkable"])
                        end = cell
                        end.color = GridCell.hextorgb(start.color_dict["origin/destination"])
                    pass

        update_game(myWindow)
        # mybutton.update(myWindow)
        for button in buttons:
            button.update(myWindow)
        pygame.display.update()
        previous_mouse_position = mouse_position


pathfinding = BestFirstSearch()

update_thread = Thread(target=update())
update_thread.start()
update_thread.join()

pygame.quit()
