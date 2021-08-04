import pygame
import sys
import requests
import time

BLACK = (10, 10, 10)
GREY = (80, 80, 80)
WHITE = (250, 250, 250)
RED = (255, 0, 0)
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 450
blockSize = 50
wrongCounts = 0
pygame.font.init()
myfont = pygame.font.SysFont('Lato', 35)

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()['board']

grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

pygame.init()

surface = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT + 50))
pygame.display.set_caption("Sudoku Solver")

surface.fill(WHITE)

clock = pygame.time.Clock()

def backtracking(i , j):
    if i == 9:
        return 1
    if j == 9:
        return backtracking(i + 1, 0)

    if(grid_original[i][j] != 0):
        return backtracking(i, j + 1)

    rect = pygame.Rect(j * blockSize + 5, i * blockSize + 5, blockSize - 10, blockSize - 10)
    pygame.draw.rect(surface, WHITE, rect)

    for c in range(1, 10):
        if(isValid(c, grid, i, j)[0] == -1):

            rect = pygame.Rect(j * blockSize + 5, i * blockSize + 5, blockSize - 10, blockSize - 10)
            pygame.draw.rect(surface, RED, rect)

            pygame.display.update()
            time.sleep(0.2)

            rect = pygame.Rect(j * blockSize + 5, i * blockSize + 5, blockSize - 10, blockSize - 10)
            pygame.draw.rect(surface, WHITE, rect)

            pygame.display.update()

            value = myfont.render(str(c), True, GREY)
            surface.blit(value, (j * blockSize + 15, i * blockSize + 15))
            pygame.display.update()

            draw_rect(j * blockSize , i * blockSize , BLACK)
            pygame.display.update()

            grid[i][j] = c

            if(backtracking(i, j + 1)):
                return 1

    rect = pygame.Rect(j * blockSize + 5, i * blockSize + 5, blockSize - 10, blockSize - 10)
    pygame.draw.rect(surface, RED, rect)

    pygame.display.update()
    time.sleep(0.2)

    rect = pygame.Rect(j * blockSize + 5, i * blockSize + 5, blockSize - 10, blockSize - 10)
    pygame.draw.rect(surface, WHITE, rect)

    draw_rect(j * blockSize , i * blockSize, BLACK)
    pygame.display.update()
    grid[i][j] = 0
    return 0

def isValidBox():
    dict = {}

    for i in range(0 , 9 , 3):
        for j in range (0 , 9 , 3):

            for k in range(3):
                for l in range(3):
                    if(grid[i + k][j + l] == 0):
                        return 0

                    if(dict.get(grid[i + k][j + l]) == None):
                        dict.get(grid[i + k][j + l] , 1)

                    else:
                        return 0

            dict.clear()

    return 1


def isValidRow():
    dict = {}

    for i in range(0 , 9):
        for j in range (0 , 9):


            if(grid[i][j] == 0):
                return 0

            if(dict.get(grid[i][j]) == None):
                dict.get(grid[i][j] , 1)

            else:
                return 0

        dict.clear()

    return 1


def isValidColumn():
    dict = {}

    for i in range(0, 9):
        for j in range(0, 9):

            if (grid[j][i] == 0):
                return 0

            if (dict.get(grid[j][i]) == None):
                dict.get(grid[j][i], 1)

            else:
                return 0

        dict.clear()

    return 1

def hint(i , j):
    for val in range(1,10):

        if(isValid(val, grid, i , j)[0] == -1):
            value = myfont.render(str(val), True, GREY)
            surface.blit(value, (j * blockSize + 15, i * blockSize + 15))
            pygame.display.update()
            time.sleep(0.1)
            draw_rect_solid(j, i , WHITE)
            pygame.display.update()
            return

    draw_rect_solid(j, i, RED)
    time.sleep(0.2)
    draw_rect_solid(j, i, WHITE)
    return



def isValid(num, grid, row, col):
    for i in range(9):

        if(grid[row][i] == num and i != col):
            found_x = row
            found_y = i
            return (0 , found_x , found_y)

        if(grid[i][col] == num and i != row):
            found_x = i
            found_y = col
            return (0 , found_x , found_y)

        x_box = (row // 3) * 3 + (i // 3)
        y_box = (col // 3) * 3 + (i % 3)

        if grid[x_box][y_box] == num and row != x_box and col != y_box :
            found_x = (row // 3) * 3 + (i // 3)
            found_y = (col // 3) * 3 + (i % 3)
            return (0 , found_x , found_y)

    return (-1 , -1 , -1)

def insert(surface, pos):
    myfont = pygame.font.SysFont('Lato', 35)
    i , j = pos[1] , pos[0]
    while 1:
        blit_time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                    if(grid_original[i][j] != 0):
                        return

                    draw_rect_solid(j , i , WHITE)

                    if(event.key == 48):
                        grid[i][j] = event.key - 48
                        pygame.draw.rect(surface , WHITE , (pos[0] * blockSize , pos[1] * blockSize , blockSize , blockSize))

                        pygame.display.update()

                    if event.key == 120:
                        hint(i , j)

                    if event.key == 115:
                        print("S")
                        backtracking(0, 0)
                        time.sleep(10)

                    if(event.key >= 49 and event.key <= 57):
                        # pygame.draw.rect(surface, WHITE, (pos[0] * blockSize, pos[1] * blockSize, blockSize, blockSize))

                        value = myfont.render(str(event.key - 48) , True , GREY)
                        surface.blit(value , (pos[0] * blockSize + 15 , pos[1] * blockSize + 15))
                        pygame.display.update()

                        if(isValid(event.key - 48 , grid , i , j)[0] == 0):
                            found_x = isValid(event.key - 48 , grid , i , j)[1]
                            found_y = isValid(event.key - 48, grid, i, j)[2]

                            blit_time()
                            time.sleep(0.2)
                            draw_rect_solid(found_y , found_x , RED)
                            pygame.display.update()

                            blit_time()
                            time.sleep(0.2)
                            draw_rect_solid(found_y , found_x , WHITE)
                            pygame.display.update()

                            if(grid[found_x][found_y] == grid_original[found_x][found_y]):
                                colour = BLACK

                            else:
                                colour = GREY

                            value = myfont.render(str(grid[found_x][found_y]), True, colour)
                            surface.blit(value, (found_y * blockSize + 15, found_x * blockSize + 15))

                            pygame.draw.rect(surface, WHITE, (pos[0] * blockSize, pos[1] * blockSize, blockSize, blockSize))
                            pygame.display.update()

                        else:
                            grid[i][j] = event.key - 48


                    return


def draw_rect(x, y, color):
    rect = pygame.Rect(x, y, blockSize, blockSize)
    pygame.draw.rect(surface, color, rect, 1)


def draw_rect_solid(x, y, color):
    rect = pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)
    pygame.draw.rect(surface, color, rect)


def time_format(secs):
    sec = secs % 60
    minutes = secs // 60

    mat = " " + str(minutes) + " : " + str(sec)

    return mat


def format():
    time_ = pygame.time.get_ticks() // 1000
    secs = str(time_ % 60)
    if(len(secs) == 1):
        secs = "0" + secs

    mins = str(time_ // 60)

    if(len(mins) == 1):
        mins = "0" + mins

    return  mins + " : " + secs


def blit_time():
    # current_time = time_[0 : min(2 , len(time_))]

    value = myfont.render(format(), True, BLACK)
    surface.blit(value, (SCREEN_WIDTH / 2 - blockSize + 10, SCREEN_HEIGHT + 10))

    pygame.display.update()

    rect = pygame.Rect(SCREEN_WIDTH / 2 - blockSize + 10, SCREEN_HEIGHT + 10, 100, 100)
    pygame.draw.rect(surface, WHITE, rect)


def grids():

    for x in range(0 , SCREEN_WIDTH , blockSize):
        for y in range(0 , SCREEN_HEIGHT , blockSize):
            draw_rect(x , y , BLACK)

            if(x//blockSize % 3 == 0):
                pygame.draw.line(surface , BLACK , (x , 0) , (x , SCREEN_WIDTH) , 4)

            if(y//blockSize % 3 == 0):
                pygame.draw.line(surface , BLACK , (0 , y) , (SCREEN_HEIGHT, y) , 4)


def blit_numbers():
    for i in range(len(grid[0])):
        for j in range(len(grid[0])):
            if (1 <= grid[i][j] <= 9):
                value = myfont.render(str(grid[i][j]), True, BLACK)
                surface.blit(value, (15 + (j) * blockSize, 15 + (i) * blockSize))


def completed():
    return isValidBox() and isValidColumn() and isValidRow()


def display():
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 50))
    pygame.display.set_caption("Sudoku Solver")

    surface.fill(WHITE)
    pygame.display.update()

    img = pygame.image.load("completed2.gif")

    surface.blit(img, (50 , 50))
    pygame.display.update()

    value = myfont.render(format(), True, BLACK)
    surface.blit(value, (SCREEN_WIDTH / 2 - blockSize + 10, SCREEN_HEIGHT))

    pygame.display.update()

    time.sleep(5)




blit_numbers()

running = 1

while running:
    grids()
    blit_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            (x , y) = pos
            x1 = (x // blockSize) * blockSize
            y1 = (y // blockSize) * blockSize

            if x <= SCREEN_WIDTH and y <= SCREEN_HEIGHT:

                if grid_original[y // blockSize][(x // blockSize)] == 0:
                    rect = pygame.Rect(x1 + 1, y1 + 1, blockSize - 2, blockSize - 2)
                    pygame.draw.rect(surface, RED, rect, 3)

                    pygame.display.update()
                # print(x // blockSize , y // blockSize)
                    insert(surface , (x // blockSize , y // blockSize))

                    if completed() == 1:
                        display()
                        running = 0

        # if event.type == pygame.KEYDOWN:
        #     pygame.quit()
        #     sys.exit()


    # pygame.display.update()



