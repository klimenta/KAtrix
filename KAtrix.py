__author__ = 'Kliment Andreev'
__version__ = '20201227 15:48'

# Imports
import random
import time
import pygame
import sys
from pygame.locals import *

# Constants and dictionaries
# Frames per second
FPS = 25
# Delay ms for a shape to go down
DELAY = 1000
# The top left column where the falling shape is positioned initially
START_COL = 4
# Represent a box or empty space for a shape
EMPTY_BOX = '-'
FULL_BOX = 'X'
# Window dimensions
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
# Matrix dimensions, including 4 borders (left, right, top, bottom)
MATRIX_WIDTH = 12
MATRIX_HEIGHT = 22
# Fill the matrix with zeros
MATRIX = [[0 for x in range(MATRIX_WIDTH)] for x in range(MATRIX_HEIGHT)]
#Box width in pixels. Each shape is composed of boxes.
BOX_SIZE = 20
# Define 16 web colors
BLACK = (0x00, 0x00, 0x00)
YELLOW = (0xff, 0xff, 0x00)
WHITE = (0xff, 0xff, 0xff)
SILVER = (0xc0, 0xc0, 0xc0)
GRAY = (0x80, 0x80, 0x80)
RED = (0xff, 0x00, 0x00)
MAROON = (0x80, 0x00, 0x00)
OLIVE = (0x80, 0x80, 0x00)
LIME = (0x00, 0xff, 0x00)
GREEN = (0x00, 0x80, 0x00)
AQUA = (0x00, 0xff, 0xff)
TEAL = (0x00, 0x80, 0x80)
BLUE = (0x00, 0x00, 0xff)
NAVY = (0x00, 0x00, 0x80)
FUCHSIA = (0xff, 0x00, 0xff)
PURPLE = (0x80, 0x00, 0x80)
# Top left coordinates of the matrix
TOP_X = 199
TOP_Y = 19
# Top left coordinates of the the box at (0,0)
# This is the top left coordinate of the top-left shape can be
TOP_BOX_X = TOP_X + BOX_SIZE
TOP_BOX_Y = TOP_Y + BOX_SIZE
# These are the shapes
# Each line represent an original position
# and three possible rotations
SHAPE_I = (("----"), ("XXXX"), ("----"), ("----")), \
          (("-X--"), ("-X--"), ("-X--"), ("-X--")), \
          (("----"), ("XXXX"), ("----"), ("----")), \
          (("-X--"), ("-X--"), ("-X--"), ("-X--"))
SHAPE_J = (("--X-"), ("--X-"), ("-XX-"), ("----")), \
          (("-X--"), ("-XXX"), ("----"), ("----")), \
          (("-XX-"), ("-X--"), ("-X--"), ("----")), \
          (("-XXX"), ("---X"), ("----"), ("----"))
SHAPE_L = (("-X--"), ("-X--"), ("-XX-"), ("----")), \
          (("XXX-"), ("X---"), ("----"), ("----")), \
          (("-XX-"), ("--X-"), ("--X-"), ("----")), \
          (("--X-"), ("XXX-"), ("----"), ("----"))
SHAPE_O = (("-XX-"), ("-XX-"), ("----"), ("----")), \
          (("-XX-"), ("-XX-"), ("----"), ("----")), \
          (("-XX-"), ("-XX-"), ("----"), ("----")), \
          (("-XX-"), ("-XX-"), ("----"), ("----"))
SHAPE_S = (("----"), ("-XX-"), ("XX--"), ("----")), \
          (("-X--"), ("-XX-"), ("--X-"), ("----")), \
          (("----"), ("-XX-"), ("XX--"), ("----")), \
          (("-X--"), ("-XX-"), ("--X-"), ("----"))
SHAPE_T = (("XXX-"), ("-X--"), ("----"), ("----")), \
          (("--X-"), ("-XX-"), ("--X-"), ("----")), \
          (("-X--"), ("XXX-"), ("----"), ("----")), \
          (("X---"), ("XX--"), ("X---"), ("----"))
SHAPE_Z = (("----"), ("-XX-"), ("--XX"), ("----")), \
          (("--X-"), ("-XX-"), ("-X--"), ("----")), \
          (("----"), ("-XX-"), ("--XX"), ("----")), \
          (("--X-"), ("-XX-"), ("-X--"), ("----"))
# List of shapes
SHAPES = (SHAPE_I, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_S, SHAPE_T, SHAPE_Z)
# Shape Colors - Dictionary
SHAPE_COLOR = {SHAPE_I: BLUE,
               SHAPE_J: PURPLE,
               SHAPE_L: RED,
               SHAPE_O: GREEN,
               SHAPE_S: WHITE,
               SHAPE_T: FUCHSIA,
               SHAPE_Z: AQUA}
# Colors, web colors - dictionary
COLOR_COLOR = {BLACK: 0,
               YELLOW: 1,
               BLUE: 2,
               PURPLE: 3,
               RED: 4,
               GREEN: 5,
               WHITE: 6,
               FUCHSIA: 7,
               AQUA: 8}
# This is a reverse dictionary finder
find_color = dict([[value, key] for key, value in COLOR_COLOR.items()])
# All possible combinations of rotations
ROTATE_0_DEGREES = 0
ROTATE_90_DEGREES = 1
ROTATE_180_DEGREES = 2
ROTATE_270_DEGREES = 3
# This is the size of one shape, 4 x 4
SHAPE_SIZE = 4

class Shape(object):
    """A class for shapes"""
    def __init__(self, name, rotation, pos_y, pos_x):
        self.name = name            # Name of the shape, e.g. SHAPE_T
        self.rotation = rotation    # Rotation index of the shape
        self.pos_x = pos_x          # X position of the shape, it can be from 1 to 10
        self.pos_y = pos_y          # Y position of the shape, it can be from 1 to 20

    def drawShapeOnScreen(self):
        """
        This method draws all boxes that form a shape on the screen
        and outline each box with a black edge line
        """
        piece = self.name[self.rotation]
        for x in range(SHAPE_SIZE):
            for y in range(SHAPE_SIZE):
                if piece[y][x] != EMPTY_BOX:
                    # This line draws all the squares on the screen
                    pygame.draw.rect(DISPLAY_SURFACE, SHAPE_COLOR[self.name],
                                     (x * BOX_SIZE + TOP_X + BOX_SIZE * self.pos_x,
                                      y * BOX_SIZE + TOP_Y + BOX_SIZE * self.pos_y,
                                      BOX_SIZE,
                                      BOX_SIZE))
                    # The following lines outline each square with 1 pixel black line
                    # Top vertical
                    pygame.draw.line(DISPLAY_SURFACE, BLACK,
                                     (x * BOX_SIZE + TOP_X + BOX_SIZE * self.pos_x,
                                      y * BOX_SIZE + TOP_Y + BOX_SIZE * self.pos_y),
                                     (x * BOX_SIZE + TOP_X + BOX_SIZE * self.pos_x + BOX_SIZE,
                                      y * BOX_SIZE + TOP_Y + BOX_SIZE * self.pos_y), 1)
                    # Right horizontal
                    pygame.draw.line(DISPLAY_SURFACE, BLACK,
                                     (x * BOX_SIZE + TOP_X + BOX_SIZE * self.pos_x + BOX_SIZE,
                                      y * BOX_SIZE + TOP_Y + BOX_SIZE * self.pos_y),
                                     (x * BOX_SIZE + TOP_X + BOX_SIZE * self.pos_x + BOX_SIZE,
                                      y * BOX_SIZE + TOP_Y + BOX_SIZE * self.pos_y + BOX_SIZE),
                                     1)
                    # Left horizontal
                    pygame.draw.line(DISPLAY_SURFACE, BLACK,
                                     (x * BOX_SIZE + TOP_X + BOX_SIZE * self.pos_x,
                                      y * BOX_SIZE + TOP_Y + BOX_SIZE * self.pos_y),
                                     (x * BOX_SIZE + TOP_X + BOX_SIZE * self.pos_x,
                                      y * BOX_SIZE + TOP_Y + BOX_SIZE * self.pos_y + BOX_SIZE),
                                     1)
                    # Bottom vertical
                    pygame.draw.line(DISPLAY_SURFACE, BLACK,
                                     (x * BOX_SIZE + TOP_X + BOX_SIZE * self.pos_x,
                                      y * BOX_SIZE + TOP_Y + BOX_SIZE * self.pos_y + BOX_SIZE),
                                     (x * BOX_SIZE + TOP_X + BOX_SIZE * self.pos_x + BOX_SIZE,
                                      y * BOX_SIZE + TOP_Y + BOX_SIZE * self.pos_y + BOX_SIZE),
                                     1)

    def deleteShapeFromScreen(self):
        """
        This method deletes the shape from the screen
        """
        piece = self.name[self.rotation]
        for x in range(SHAPE_SIZE):
            for y in range(SHAPE_SIZE):
                if piece[y][x] != EMPTY_BOX:
                    # This line erases all the squares
                    pygame.draw.rect(DISPLAY_SURFACE, BLACK,
                                     (x * BOX_SIZE + TOP_X + BOX_SIZE * self.pos_x,
                                      y * BOX_SIZE + TOP_Y + BOX_SIZE * self.pos_y,
                                      BOX_SIZE, BOX_SIZE))


    def deleteShapeFromMatrix(self):
        """
        This method deletes the shape from the matrix
        """
        piece = self.name[self.rotation]
        for x in range(SHAPE_SIZE):
            for y in range(SHAPE_SIZE):
                if x + self.pos_x < (MATRIX_WIDTH - 1) \
                        and y + self.pos_y < (MATRIX_HEIGHT -1) \
                        and piece[y][x] == FULL_BOX:
                    MATRIX[y + self.pos_y][x + self.pos_x] = COLOR_COLOR[BLACK]
        resetMatrix()

    def returnMaxWidth(self):
        """
        Each shape is 4 x 4, but the actual width is different
        for each shape, e.g. horizontal "I" shape is 4 boxes in width
        but the same vertical shape is 2 boxes in width
        This method returns the width from the left. See the shape definition above
        """
        max_x = 0
        piece = self.name[self.rotation]
        for x in range(SHAPE_SIZE):
            for y in range(SHAPE_SIZE):
                if piece[x][y] == FULL_BOX and y > max_x :
                    max_x = y
        return max_x

    def returnMinWidth(self):
        """
        Each shape is 4 x 4, but the actual width is different
        for each shape, e.g. horizontal "I" shape is 4 boxes in width
        but the same vertical shape is 2 boxes in width
        This method returns the width from right. See the shape definition above
        """
        min_x = SHAPE_SIZE
        piece = self.name[self.rotation]
        for x in range(SHAPE_SIZE):
            for y in range(SHAPE_SIZE):
                if piece[x][y] == FULL_BOX and y < min_x :
                    min_x = y
        return min_x

    def returnMaxHeight(self):
        """
        Each shape is 4 x 4, but the actual height is different
        for each shape, e.g. horizontal "I" shape is 2 boxes in width
        but the same vertical shape is 4 boxes in height
        This method returns the height. See the shape definition above
        """
        max_y = 0
        piece = self.name[self.rotation]
        for x in range(SHAPE_SIZE):
            for y in range(SHAPE_SIZE):
                if piece[x][y] == FULL_BOX and x > max_y :
                    max_y = x
        return max_y

    def returnMaxHeightPerColumn(self, column):
        """
        Each shape is 4 x 4, but the actual height is different per column
        for each shape, e.g. horizontal "T" shape can be 1 boxes or 3 boxes in height
        This method return the max height and that's the box that's the lowest in a shape
        """
        max_y = 0
        piece = self.name[self.rotation]
        for y in range(SHAPE_SIZE):
            if piece[y][column] == FULL_BOX and y > max_y:
                max_y = y
        return max_y

    def moveLeft(self):
        """
        Move the shape left if possible
        """
        if isAvailableLeft(self):
            self.deleteShapeFromMatrix()
            self.deleteShapeFromScreen()
            self.pos_x -= 1
            updateShapeInMatrix(self)
            self.drawShapeOnScreen()

    def moveRight(self):
        """
        Move the shape right if possible
        """
        if isAvailableRight(self):
            self.deleteShapeFromMatrix()
            self.deleteShapeFromScreen()
            self.pos_x += 1
            updateShapeInMatrix(self)
            self.drawShapeOnScreen()

    def moveDown(self):
        """
        Move the shape down if possible
        """
        if isAvailableDown(self):
            self.deleteShapeFromMatrix()
            self.deleteShapeFromScreen()
            self.pos_y += 1
            updateShapeInMatrix(self)
            self.drawShapeOnScreen()

    def moveRotate(self):
        """
        Rotate the shape if possible
        """
        if isAvailableRotate(self):
            self.deleteShapeFromMatrix()
            self.deleteShapeFromScreen()
            self.rotation += 1
            if self.rotation == 4:
                self.rotation = 0
            updateShapeInMatrix(self)
            self.drawShapeOnScreen()

def resetMatrix():
    """
    Updates the edges of the matrix in memory, that's the YELLOW borders
    """
    for x in range(0, MATRIX_HEIGHT):
        MATRIX[x][0] = COLOR_COLOR[YELLOW]
        MATRIX[x][MATRIX_WIDTH - 1] = COLOR_COLOR[YELLOW]
    for y in range(0, MATRIX_WIDTH):
        MATRIX[0][y] = COLOR_COLOR[YELLOW]
        MATRIX[MATRIX_HEIGHT - 1][y] = COLOR_COLOR[YELLOW]

def isAvailable(Shape):
    """
    Is the shape available to be moved in the matrix
    Checks the new position initially when dropping it for the first time
    """
    allowed = True
    piece = Shape.name[Shape.rotation]
    for x in range(SHAPE_SIZE):
        for y in range(SHAPE_SIZE):
            if piece[y][x] == FULL_BOX and \
                            MATRIX[y + Shape.pos_y][x + Shape.pos_x] >= COLOR_COLOR[YELLOW]:
                allowed = False
                break
    return allowed

def isAvailableLeft(Shape):
    """
    Is the shape available to be moved left in the matrix
    """
    allowed = True
    piece = Shape.name[Shape.rotation]
    for y in range(SHAPE_SIZE):
        if piece[y][Shape.returnMinWidth()] == FULL_BOX \
                and MATRIX[y + Shape.pos_y][Shape.pos_x +Shape.returnMinWidth() - 1] >= COLOR_COLOR[YELLOW] :
            allowed = False
            break
    return allowed

def isAvailableRight(Shape):
    """
    Is the shape available to be moved right in the matrix
    """
    allowed = True
    piece = Shape.name[Shape.rotation]
    for y in range(SHAPE_SIZE):
        if piece[y][Shape.returnMaxWidth()] == FULL_BOX \
                and MATRIX[y + Shape.pos_y][Shape.pos_x + Shape.returnMaxWidth() + 1] >= COLOR_COLOR[YELLOW]:
            allowed = False
            break
    return allowed

def isAvailableRotate(Shape):
    """
    Is the shape available to be rotated in the matrix
    """
    allowed = True
    oldMaxWidth= Shape.returnMaxWidth()
    oldMinWidth = Shape. returnMinWidth()
    oldMaxHeight = Shape.returnMaxHeight()
    oldRotation = Shape.rotation
    Shape.rotation += 1
    if Shape.rotation == 4:
        Shape.rotation = 0
    newMaxWidth = Shape.returnMaxWidth()
    newMinWidth = Shape.returnMinWidth()
    newMaxHeight = Shape.returnMaxHeight()
    if (newMinWidth - oldMinWidth) + Shape.pos_x < 0 \
            or (newMaxWidth - oldMaxWidth) + Shape.pos_x >= (MATRIX_WIDTH - 2):
        allowed = False
    if (newMaxHeight - oldMaxHeight) + Shape.pos_y >= (MATRIX_HEIGHT -2):
        allowed = False
    Shape.rotation = oldRotation
    return allowed

def isAvailableDown(Shape):
    """
    Is the shape available to be moved down in the matrix
    """
    allowed = True
    piece = Shape.name[Shape.rotation]
    for x in range(SHAPE_SIZE):
        if piece[Shape.returnMaxHeightPerColumn(x)][x] == FULL_BOX and \
                        MATRIX[Shape.pos_y + Shape.returnMaxHeightPerColumn(x) + 1][x + Shape.pos_x] >= COLOR_COLOR[YELLOW] :
            allowed = False
            break
    return allowed

def updateShapeInMatrix(Shape):
    """
    Updates the matrix with the moved shape
    """
    piece = Shape.name[Shape.rotation]
    for x in range(SHAPE_SIZE):
        for y in range(SHAPE_SIZE):
            if piece[y][x] == "X" and (y + Shape.pos_y) in range (1, MATRIX_HEIGHT - 1) \
                    and (x + Shape.pos_x) in range(1, MATRIX_WIDTH - 1) \
                    and MATRIX[y + Shape.pos_y][x + Shape.pos_x] == COLOR_COLOR[BLACK]:
                MATRIX[y + Shape.pos_y][x + Shape.pos_x] = COLOR_COLOR[SHAPE_COLOR[Shape.name]]
    resetMatrix()

def drawMatrixOnScreen():
    """
    Draws four bars where the game occurs
    """
    # Left bar
    pygame.draw.rect(DISPLAY_SURFACE, YELLOW, (TOP_X,
                                               TOP_Y,
                                               BOX_SIZE,
                                               MATRIX_HEIGHT * BOX_SIZE + 1))
    # Right bar
    pygame.draw.rect(DISPLAY_SURFACE, YELLOW, (TOP_X + (MATRIX_WIDTH - 1) * BOX_SIZE + 1,
                                               TOP_Y,
                                               BOX_SIZE,
                                               MATRIX_HEIGHT * BOX_SIZE + 1))
    # Bottom bar
    pygame.draw.rect(DISPLAY_SURFACE, YELLOW, (TOP_X + BOX_SIZE,
                                               TOP_Y + (MATRIX_HEIGHT - 1) * BOX_SIZE + 1,
                                               (MATRIX_WIDTH - 2) * BOX_SIZE + 1,
                                               BOX_SIZE))
    # Top bar
    pygame.draw.rect(DISPLAY_SURFACE, YELLOW, (TOP_X + BOX_SIZE,
                                               TOP_Y,
                                               (MATRIX_WIDTH - 2) * BOX_SIZE + 1,
                                               BOX_SIZE))

def checkFullLine():
    """
    Check if there is a full horizontal line in the matrix.
    """
    for x in range(MATRIX_HEIGHT - 2, 0, - 1):
        if 0 not in MATRIX[x]:
            return x      
    return 0

def printText(msg, FONT, x_cor, y_cor, b_color, f_color):
    """
    Writes Text on the screen
    """
    text = FONT.render(msg, True, b_color, f_color)
    textRect = text.get_rect()
    textRect.centerx = x_cor
    textRect.centery = y_cor
    DISPLAY_SURFACE.blit(text, textRect)

def drawRectangle(x_cor, y_cor, width, height, color):
    """
    Draws rectangle on the screen
    """
    pygame.draw.rect(DISPLAY_SURFACE, color, (x_cor, y_cor, width, height))

def printScore(score):
    """
    Prints score on the screen
    """
    printText('SCORE:', FONT_SMALL, 490, 240, WHITE, BLACK)
    printText(str(score), FONT_SMALL, 580, 240, WHITE, BLACK)

def shiftShapesOnScreen(row):
    """
    Shift shapes down on the screen when one line is full and collapses
    """
    for col in range(1, MATRIX_WIDTH -1):
        pygame.draw.rect(DISPLAY_SURFACE,
                         find_color[MATRIX[row][col]],
                         (TOP_X + BOX_SIZE * col,
                          TOP_Y + BOX_SIZE * row,
                          BOX_SIZE,
                          BOX_SIZE))

        # This line outlines each square with 1 pixel black line
        # Top vertical
        pygame.draw.line(DISPLAY_SURFACE, BLACK,
            (TOP_X + BOX_SIZE * col,
            TOP_Y + BOX_SIZE * row),
            (TOP_X + BOX_SIZE * col + BOX_SIZE,
            TOP_Y + BOX_SIZE * row), 1)
        # Right horizontal
        pygame.draw.line(DISPLAY_SURFACE, BLACK,
            (TOP_X + BOX_SIZE * col + BOX_SIZE,
            TOP_Y + BOX_SIZE * row),
            (TOP_X + BOX_SIZE * col + BOX_SIZE,
            TOP_Y + BOX_SIZE * row + BOX_SIZE),
            1)
        # Left horizontal
        pygame.draw.line(DISPLAY_SURFACE, BLACK,
            (TOP_X + BOX_SIZE * col,
            TOP_Y + BOX_SIZE * row),
            (TOP_X + BOX_SIZE * col,
            TOP_Y + BOX_SIZE * row + BOX_SIZE),
            1)
        # Bottom vertical
        pygame.draw.line(DISPLAY_SURFACE, BLACK,
            (TOP_X + BOX_SIZE * col,
            TOP_Y + BOX_SIZE * row + BOX_SIZE),
            (TOP_X + BOX_SIZE * col + BOX_SIZE,
            TOP_Y + BOX_SIZE * row + BOX_SIZE),
            1)

def shiftShapesInMatrix(row):
    """
    Shift shapes down in the matrix when one line is full and collapses
    """
    while row > 1:
        for xx in range(1, MATRIX_WIDTH):
            MATRIX[row][xx] = MATRIX[row - 1][xx]
        shiftShapesOnScreen(row)
        row -= 1

def main():
    global FPS_CLOCK, DISPLAY_SURFACE, FONT_BIG, FONT_SMALL, FONT_SUPER_SMALL, SCORE
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    count_ms = 0
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('KAtrix')
    FONT_BIG = pygame.font.SysFont(None, 44)
    FONT_SMALL = pygame.font.SysFont(None, 24)
    FONT_SUPER_SMALL = pygame.font.SysFont(None, 12)
    DISPLAY_SURFACE.fill(BLACK)
    resetMatrix()
    drawMatrixOnScreen()
    SCORE = 0
    printScore(SCORE)
    printText('Program by: Kliment ANDREEV, 2015 - 2020', FONT_SMALL, 320, 470, SILVER, BLACK)
    # MAIN GAME LOOP
    while True:
        new_shape = Shape(SHAPES[random.randint(0, len(SHAPES) - 1)], ROTATE_0_DEGREES, 1, START_COL)
        NewPiece = True
        if isAvailable(new_shape):
            Shape.drawShapeOnScreen(new_shape)
            updateShapeInMatrix(new_shape)
        else:
            NewPiece=False
            Shape.drawShapeOnScreen(new_shape)
            drawRectangle(TOP_X, WINDOW_HEIGHT / 2 - 50, 241, 160, BLUE)
            printText("G A M E  O V E R", FONT_BIG, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 30, YELLOW, BLUE)
            pygame.display.update()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()
        while NewPiece:
            passed_ms = FPS_CLOCK.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if (event.key == K_LEFT):
                        Shape.moveLeft(new_shape)
                    elif (event.key == K_ESCAPE):
                        sys.exit()
                    elif (event.key == K_RIGHT):
                        Shape.moveRight(new_shape)
                    elif (event.key == K_UP):
                        Shape.moveRotate(new_shape)
                    elif (event.key == K_DOWN):
                        Shape.moveDown(new_shape)
                    elif (event.key == K_SPACE):
                        while isAvailableDown(new_shape):
                            Shape.moveDown(new_shape)
                        NewPiece = False
                        while checkFullLine() > 0:
                            SCORE += 10
                            printScore(SCORE)
                            shiftShapesInMatrix(checkFullLine())
            count_ms += passed_ms
            if count_ms >= DELAY:
                count_ms = count_ms % DELAY
                if (isAvailableDown(new_shape)):
                    Shape.moveDown(new_shape)
                else: NewPiece = False          
            pygame.display.update()
if __name__ == '__main__':
    main()
