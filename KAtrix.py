__author__ = 'Kliment Andreev'
__version__ = '20151108 15:48'

# Imports
import random
import time
import pygame
import sys
from pygame.locals import *

# Frames per second
FPS = 25
# The top left column where the falling shape is positioned initially
START_COL = 4
# Window dimensions
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
# Matrix dimensions, including 4 borders (left, right, top, bottom)
MATRIX_WIDTH = 12
MATRIX_HEIGHT = 22
# Fill the matrix with zeros
ARENA = [[0 for x in range(MATRIX_WIDTH)] for x in range(MATRIX_HEIGHT)]
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
#SHAPES = (SHAPE_I, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_S, SHAPE_T, SHAPE_Z)

# Shape Colors - Dictionary
SHAPE_COLOR = {SHAPE_I: BLUE,
               SHAPE_J: PURPLE,
               SHAPE_L: RED,
               SHAPE_O: GREEN,
               SHAPE_S: WHITE,
               SHAPE_T: FUCHSIA,
               SHAPE_Z: AQUA}
#Colors, web colors - dictionary
COLOR_COLOR = {BLACK: 0,
               YELLOW: 1,
               BLUE: 2,
               PURPLE: 3,
               RED: 4,
               GREEN: 5,
               WHITE: 6,
               FUCHSIA: 7,
               AQUA: 8}

find_color = dict([[value, key] for key, value in COLOR_COLOR.items()])

# All possible combinations of rotations
ROTATE_0_DEGREES = 0
ROTATE_90_DEGREES = 1
ROTATE_180_DEGREES = 2
ROTATE_270_DEGREES = 3

# This is the size of one shape, 4 x 4
SHAPE_SIZE = 4

# Shapes
class Shape(object):
    """A class for shapes"""
    def __init__(self, name, rotation, pos_y, pos_x):
        self.name = name
        self.rotation = rotation
        self.pos_x = pos_x
        self.pos_y = pos_y

    def drawBox(self):
        piece = self.name[self.rotation]
        for x in range(SHAPE_SIZE):
            for y in range(SHAPE_SIZE):
                if piece[y][x] != '-':
                    # This line draws all the squares
                    pygame.draw.rect(DISPLAY_SURFACE, SHAPE_COLOR[self.name],
                                     (x * BOX_SIZE + TOP_X + BOX_SIZE * self.pos_x,
                                      y * BOX_SIZE + TOP_Y + BOX_SIZE * self.pos_y,
                                      BOX_SIZE,
                                      BOX_SIZE))
                    # This line outlines each square with 1 pixel black line
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

    def eraseBox(self):
        piece = self.name[self.rotation]
        for x in range(SHAPE_SIZE):
            for y in range(SHAPE_SIZE):
                if piece[y][x] != '-':
                    # This line erases all the squares
                    pygame.draw.rect(DISPLAY_SURFACE, BLACK,
                                     (x * BOX_SIZE + TOP_X + BOX_SIZE * self.pos_x,
                                      y * BOX_SIZE + TOP_Y + BOX_SIZE * self.pos_y,
                                      BOX_SIZE, BOX_SIZE))


    def deleteArenaBox(self):
        piece = self.name[self.rotation]
        for x in range(SHAPE_SIZE):
            for y in range(SHAPE_SIZE):
                if x + self.pos_x < 11 and y + self.pos_y < 21 and piece[y][x] == 'X':
                    ARENA[y + self.pos_y][x + self.pos_x] = COLOR_COLOR[BLACK]
        resetArena()

    def returnMaxWidth(self):
        '''find max widht of a shape'''
        max_x = 0
        piece = self.name[self.rotation]
        for x in range(SHAPE_SIZE):
            for y in range(SHAPE_SIZE):
                if piece[x][y] == 'X' and y > max_x :
                    max_x = y
        return max_x

    def returnMinWidth(self):
        '''find min widht of a shape'''
        min_x = SHAPE_SIZE
        piece = self.name[self.rotation]
        for x in range(SHAPE_SIZE):
            for y in range(SHAPE_SIZE):
                if piece[x][y] == 'X' and y < min_x :
                    min_x = y
        return min_x

    def returnMaxHeight(self):
        '''find max height of a shape'''
        max_y = 0
        piece = self.name[self.rotation]
        for x in range(SHAPE_SIZE):
            for y in range(SHAPE_SIZE):
                if piece[x][y] == 'X' and x > max_y :
                    max_y = x
        return max_y

    def returnMaxHeightPerColumn(self, column):
        max_y = 0
        piece = self.name[self.rotation]
        for y in range(SHAPE_SIZE):
            #print piece[y][column]
            if piece[y][column] == 'X' and y > max_y:
                max_y = y
        return max_y

    def moveLeft(self):
        if isAvailableLeft(self):
            self.deleteArenaBox()
            self.eraseBox()
            self.pos_x -= 1
            updateArena(self)
            self.drawBox()

    def moveRight(self):
         if isAvailableRight(self):
            self.deleteArenaBox()
            self.eraseBox()
            self.pos_x += 1
            updateArena(self)
            self.drawBox()

    def moveDown(self):
        if isAvailableDown(self):
            self.deleteArenaBox()
            self.eraseBox()
            self.pos_y += 1
            updateArena(self)
            self.drawBox()

    def moveRotate(self):
        if isAvailableRotate(self):
            self.deleteArenaBox()
            self.eraseBox()
            self.rotation += 1
            if self.rotation == 4:
                self.rotation = 0
            updateArena(self)
            self.drawBox()

def resetArena():
    for x in range(0, MATRIX_HEIGHT):
        ARENA[x][0] = COLOR_COLOR[YELLOW]
        ARENA[x][MATRIX_WIDTH - 1] = COLOR_COLOR[YELLOW]
    for y in range(0, MATRIX_WIDTH):
        ARENA[0][y] = COLOR_COLOR[YELLOW]
        ARENA[MATRIX_HEIGHT - 1][y] = COLOR_COLOR[YELLOW]

def isAvailable(Shape):
    Allowed = True
    piece = Shape.name[Shape.rotation]
    for x in range(SHAPE_SIZE):
        for y in range(SHAPE_SIZE):
            #print piece[y][x]
            if piece[y][x] == 'X' and ARENA[y + Shape.pos_y][x + Shape.pos_x] >= COLOR_COLOR[YELLOW]:
                Allowed = False
                break
    #print "isAvailable: ", Allowed
    return Allowed

def isAvailableLeft(Shape):
    Allowed = True
    piece = Shape.name[Shape.rotation]
    for y in range(SHAPE_SIZE):
        if piece[y][Shape.returnMinWidth()] == 'X' \
                and ARENA[y + Shape.pos_y][Shape.pos_x +Shape.returnMinWidth() - 1] >= COLOR_COLOR[YELLOW] :
            Allowed = False
            break
    #print "isAvailable: ", Allowed
    return Allowed

def isAvailableRight(Shape):
    Allowed = True
    piece = Shape.name[Shape.rotation]
    for y in range(SHAPE_SIZE):
        if piece[y][Shape.returnMaxWidth()] == 'X' \
                and ARENA[y + Shape.pos_y][Shape.pos_x + Shape.returnMaxWidth() + 1 ] >= COLOR_COLOR[YELLOW]:
            Allowed = False
            break
    #print "isAvailableRight: ", Allowed
    return Allowed


def isAvailableRotate(Shape):
    Allowed = True
    maxx1= Shape.returnMaxWidth()
    minn1 = Shape. returnMinWidth()
    maxx3 = Shape.returnMaxHeight()
    old_rotation = Shape.rotation
    Shape.rotation += 1
    if Shape.rotation == 4:
        Shape.rotation = 0
    maxx2 = Shape.returnMaxWidth()
    minn2 = Shape.returnMinWidth()
    maxx4 = Shape.returnMaxHeight()
    if (minn2 - minn1) + Shape.pos_x < 0 or (maxx2 - maxx1) + Shape.pos_x >= 9:
        #print minn2 -minn1, Shape.pos_x
        #print "ovde false"
        Allowed = False
    if (maxx4 - maxx3) + Shape.pos_y >=20:
        #print "ovde ovde false"
        Allowed = False
    #if minn2 < minn1 and Shape.pos_x < 1:
    #    Allowed = False
    Shape.rotation = old_rotation
    #print "isAvailableRotate: ", Allowed
    return Allowed

def isAvailableDown(Shape):
    Allowed = True
    piece = Shape.name[Shape.rotation]
    for x in range(SHAPE_SIZE):
        if piece[Shape.returnMaxHeightPerColumn(x)][x] == 'X' and \
                        ARENA[Shape.pos_y + Shape.returnMaxHeightPerColumn(x) + 1][x + Shape.pos_x] >= COLOR_COLOR[YELLOW] :
            Allowed = False
            break
    #print "isAvailableDown: ", Allowed
    return Allowed

def updateArena(Shape):
    piece = Shape.name[Shape.rotation]
    for x in range(SHAPE_SIZE):
        for y in range(SHAPE_SIZE):
            k = piece[y][x]
            poz_y = y + Shape.pos_y
            poz_x = x + Shape.pos_x
            #print COLOR_COLOR[SHAPE_COLOR[Shape.name]]
            if piece[y][x] == "X" and poz_y in range (1,21) and poz_x in range(1,11) and ARENA[poz_y][poz_x] == COLOR_COLOR[BLACK]:
                ARENA[poz_y][poz_x] = COLOR_COLOR[SHAPE_COLOR[Shape.name]]
            #if piece[y][x] == "-" and poz_y in range (1,21) and poz_x in range(1,11) and ARENA[poz_y][poz_x] == 0:
            #    print "true"
            #    ARENA[poz_y][poz_x] = 0
    resetArena()
    #ARENA[2][1] = 1
    #ARENA[10][1] = 1
    #ARENA[20][1] = 1
    #ARENA[10][10] = 1
    #print ARENA[0]
    print ARENA[1]
    print ARENA[2]
    print ARENA[3]
    print ARENA[4]
    print ARENA[5]
    print ARENA[6]
    print ARENA[7]
    print ARENA[8]
    print ARENA[9]
    print ARENA[10]
    print ARENA[11]
    print ARENA[12]
    print ARENA[13]
    print ARENA[14]
    print ARENA[15]
    print ARENA[16]
    print ARENA[17]
    print ARENA[18]
    print ARENA[19]
    print ARENA[20]
    #print ARENA[21]
    print "---------------"
def drawArena():
    '''
    Draws four bars where the game occurs
    '''
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
    for x in range(MATRIX_HEIGHT - 2, 0, - 1):
        if 0 not in ARENA[x]:
            return x

def writeText(msg, FONT, x_cor, y_cor, b_color, f_color):
    text = FONT.render(msg, True, b_color, f_color)
    textRect = text.get_rect()
    textRect.centerx = x_cor
    textRect.centery = y_cor
    DISPLAY_SURFACE.blit(text, textRect)

def drawRectangle(x_cor, y_cor, width, height, color):
    pygame.draw.rect(DISPLAY_SURFACE, color, (x_cor, y_cor, width, height))

def drawScore(score):
    writeText('SCORE:', FONT_SMALL, 490, 240, WHITE, BLACK)
    writeText(str(score), FONT_SMALL, 580, 240, WHITE, BLACK)

def shiftShapes(row):
    for col in range(1, MATRIX_WIDTH -1):
        pygame.draw.rect(DISPLAY_SURFACE,
                         find_color[ARENA[row][col]],
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

def shiftArena(row):
    while row > 1:
        for xx in range(1, MATRIX_WIDTH):
            ARENA[row][xx] = ARENA[row - 1][xx]
        shiftShapes(row)
        row -= 1

def main():
    global FPS_CLOCK, DISPLAY_SURFACE, FONT_BIG, FONT_SMALL, FONT_SUPER_SMALL, SCORE
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Tetrominox')
    FONT_BIG = pygame.font.SysFont(None, 48)
    FONT_SMALL = pygame.font.SysFont(None, 24)
    FONT_SUPER_SMALL = pygame.font.SysFont(None, 12)
    DISPLAY_SURFACE.fill(BLACK)
    resetArena()
    drawArena()
    SCORE = 0
    drawScore(SCORE)
    writeText('Program by: Kliment ANDREEV, 2015', FONT_SUPER_SMALL, 320, 470, SILVER, BLACK)
    # MAIN GAME LOOP
    while True:
        new_shape = Shape(SHAPES[random.randint(0, len(SHAPES) - 1)], ROTATE_0_DEGREES, 1, START_COL)
        #new_shape = Shape(SHAPE_I, ROTATE_0_DEGREES, 1, 3)
        NewPiece = True
        if isAvailable(new_shape):
            Shape.drawBox(new_shape)
            #print "new shape"
            updateArena(new_shape)
        else:
            NewPiece=False
            Shape.drawBox(new_shape)
            print "no new piece...G A M E    O V E R"
            pygame.display.update()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()

        while NewPiece:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if (event.key == K_LEFT):
                        Shape.moveLeft(new_shape)
                    elif (event.key == K_RIGHT):
                        Shape.moveRight(new_shape)
                    elif (event.key == K_UP):
                        Shape.moveRotate(new_shape)
                    elif (event.key == K_DOWN):
                        Shape.moveDown(new_shape)
                    elif (event.key == K_SPACE):
                        #Shape.moveDown(new_shape)
                        while isAvailableDown(new_shape):
                            Shape.moveDown(new_shape)
                            #updateArena(new_shape)
                        NewPiece = False
                        while checkFullLine() > 0:
                        #if checkFullLine() > 0:
                            SCORE += 10
                            drawScore(SCORE)
                            shiftArena(checkFullLine())

                        #print x
                        #print "OK. NEW PIECE COMING"
            pygame.display.update()
            FPS_CLOCK.tick(FPS)

if __name__ == '__main__':
    main()
