import random, pygame, sys
from pygame.locals import *


FPS = 12
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20

# makes sure that only a whole integer number of cells fits in the window
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

WHITE = (255, 255, 255)
PINK = (247, 219, 222)
GREEN = (49, 124, 66)
RED = (215, 16, 16)
BROWN = (206, 170, 133)
DARKBROWN = (165, 127, 88)
LIGHTGREEN = (85, 159, 101)
BGCOLOR = GREEN

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # inderx of the snake's heading

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')
    
    showStartScreen()
    while True:  # will loop forever until the program terminates
        
        runGame()
        showGameOverScreen()
        
def runGame():
    # set a random start point, not to close to the edge
    
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    snakeCoords = [{'x': startx,    'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}] 
    
    direction = RIGHT
    
    # start the apple in a random place
    apple = getRandomLocation()
    
    while True:  # mail loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN: 
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP: 
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
                    
        # check if the snake hit the edge
        if snakeCoords[HEAD]['x'] == -1 or snakeCoords[HEAD]['x'] == CELLWIDTH or snakeCoords[HEAD]['y'] == -1 or snakeCoords[HEAD]['y'] == CELLHEIGHT:
            return  # game over
        for snakeBody in snakeCoords[1:]: # check if the snake hit itself
            if snakeBody['x'] == snakeCoords[HEAD]['x'] and snakeBody['y'] == snakeCoords[HEAD]['y']:
                return # game over
        
        #check if the snake has eaten the apple
        if snakeCoords[HEAD]['x'] == apple['x'] and snakeCoords[HEAD]['y'] == apple['y']:
            # don't remove snake's tail segment
             apple = getRandomLocation() # set a new apple
        else:
            del snakeCoords[-1] # remove snake's tale segment
       
        # move the worm by adding a segment of the direction it is moving
        if direction == UP:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': snakeCoords[HEAD]['x'] - 1, 'y': snakeCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': snakeCoords[HEAD]['x'] + 1, 'y': snakeCoords[HEAD]['y']}
        snakeCoords.insert(0, newHead)# .insert(index, itemValue) adds item anywehre in a list
        
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawSnake(snakeCoords)
        drawApple(apple)
        drawScore(len(snakeCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to play.', True, LIGHTGREEN)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
        
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key 
    
    
def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100) # Font() constructor function creates a Font object that is 100 points in size
    titleSurf1 = titleFont.render('Snake!', True, WHITE, DARKBROWN) # white text, darkgreen background
    titleSurf2 = titleFont.render('Snake!', True, BROWN)
    
    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)
        
        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)
        
        drawPressKeyMsg()
        
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame

     
def terminate():
    pygame.quit()
    sys.exit()

def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2 , gameRect.height + 10 + 25)
    
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(600)
    checkForKeyPress() # clear out any key presses in the event queue
    
    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    
    
def drawSnake(snakeCoords):
    for coord in snakeCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKBROWN, snakeSegmentRect)
        snakeInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, BROWN, snakeInnerSegmentRect)
        
def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)
    appleInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 16, CELLSIZE - 16)
    pygame.draw.rect(DISPLAYSURF, PINK, appleInnerSegmentRect)
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines up to WINDOWWIDTH increasind by CELLSIZE each time
        pygame.draw.line(DISPLAYSURF, LIGHTGREEN, (x, 0), (x, WINDOWHEIGHT))
    for y in range (0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines up to WINDOWHEIGHT increasind by CELLSIZE each time
        pygame.draw.line(DISPLAYSURF, LIGHTGREEN, (0, y), (WINDOWWIDTH, y))

if __name__ == '__main__':
    main()
  