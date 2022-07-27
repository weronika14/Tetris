import pygame
import random
import math


'''pretty much everything is done the rotion is all done and the scoring system works
the game ends if the most recent shape that fell touches or goes over the red line
there is an end screen
well not really it just says you lost but the game stops
the timing is a bit off i think but i cant be bothered to change it
'''


pygame.init()
playScreenWidth, playScreenHeight = 400, 800
screenWidth, screenHeight = 400, 800
screen = pygame.display.set_mode((screenWidth,screenHeight))
screen.fill(0)
white = (255,255,255)
count = 1
sideKeyDown = False
downwardsKey = False
spaceDown = False
width = 40
currentRect = []
screenRect = []
score = 0
level = 0
lines_removed = 0
clock = pygame.time.Clock()
for i in range(0,playScreenWidth, width):
    for j in range(0,playScreenHeight,width):
        screenRect.append(pygame.Rect([i+0.01,j+0.01], [width-0.1, width-0.1]))


def writingText(text, x, y, width, height, txt_colour, rect_colour, size): #function for writing text
    textFont = pygame.font.Font('freesansbold.ttf', size)
    #pygame.draw.rect(screen, rect_colour, (x,y, width, height))
    textDisplay = textFont.render(str(text), True, txt_colour)
    textRect = textDisplay.get_rect()
    textRect.center = ((x + width/2), (y + height/2))
    screen.blit(textDisplay, textRect)


class Block:

    def __init__(self):

        number = random.randint(0,6)#picks a random block

        if number == 0:
            self.shape = YellowSquare()
        elif number == 1:
            self.shape = BlueL()
        elif number == 2:
            self.shape = OrangeL()
        elif number == 3:
            self.shape = PurpleT()
        elif number == 4:
            self.shape = GreenShape()
        elif number == 5:
            self.shape = RedShape()
        elif number == 6:
            self.shape = BlueLine()

        self.colour = self.shape.colour

    def falling(self,direction): #every square in the shape will have its y value decreased by the width of a square.
        for i in range(0,4):
            self.shape.currentSquares[i].fall(direction, i)

    def drawing(self): #draws every square in the shape.
        for i in range(0,4):
            pygame.draw.rect(screen, self.colour, currentRect[i])
            pygame.draw.rect(screen, white, currentRect[i],1)
        #pygame.draw.circle(screen, (255,255,255), self.shape.centre, 5)

    def rotate(self): #rotates anticlockwise.
        for i in range(0,4):
            xDistance = currentBlock.shape.currentSquares[i].x - (currentBlock.shape.xCoordinate)
            yDistance = currentBlock.shape.currentSquares[i].y - (currentBlock.shape.yCoordinate)
            currentBlock.shape.currentSquares[i].x = yDistance * -1 + currentBlock.shape.xCoordinate - width
            currentBlock.shape.currentSquares[i].y = xDistance + currentBlock.shape.yCoordinate

        for i in range(0,4):
            currentBlock.shape.currentSquares[i].updating(i)

        allShapes.collision()
        if allShapes.collided:
            allShapes.collided = False
            return 'collided'

        self.translating_at_edge()
        self.translating_at_edge()

    def rotateClockwise(self):
        for i in range(0,4):
            xDistance = currentBlock.shape.currentSquares[i].x - (currentBlock.shape.xCoordinate)
            yDistance = currentBlock.shape.currentSquares[i].y - (currentBlock.shape.yCoordinate)
            currentBlock.shape.currentSquares[i].x = yDistance + currentBlock.shape.xCoordinate
            currentBlock.shape.currentSquares[i].y = xDistance * -1 + currentBlock.shape.yCoordinate - width

        for j in range(0,4):
            currentBlock.shape.currentSquares[j].updating(j)

        allShapes.collision()
        if allShapes.collided:
            allShapes.collided = False
            return 'collided'

        self.translating_at_edge()
        self.translating_at_edge()

    def translating_at_edge(self): #if the shape is being rotated by is at the edge it can't be rotated out of the screen so instead it is moved.
        move_to_side = 0
        for i in range(0,4):
            if currentRect[i].x < 0:
                move_to_side = 1
            elif currentRect[i].x >= playScreenWidth:
                move_to_side = -1


        for j in range(0,4):
            currentBlock.shape.currentSquares[i].move(1, move_to_side, j)
            currentBlock.shape.currentSquares[i].updating(j)


class Square:

    def __init__(self, x, y):
        self.y = y
        self.x = x
        currentRect.append(pygame.Rect([self.x, self.y], [width, width]))

    def fall(self, direction, i):
        currentBlock.shape.currentSquares[i].y += (width * direction)
        currentRect[i] = pygame.Rect([currentBlock.shape.currentSquares[i].x, currentBlock.shape.currentSquares[i].y], [width, width])

    def updating(self,i):
        currentRect[i].x = currentBlock.shape.currentSquares[i].x
        currentRect[i].y = currentBlock.shape.currentSquares[i].y
        currentBlock.shape.assignCentre()

    def checkIfEdge(self):
        for j in range(0,4):
            if side == 1:
                if (currentBlock.shape.currentSquares[j].x + width) == (playScreenWidth):
                    return True
            elif side == -1:
                if (currentBlock.shape.currentSquares[j].x) == 0:
                    return True
        return False

    def move(self, side, multiplier, i):
        self.side = side
        currentBlock.shape.currentSquares[i].x += width * side * multiplier


class ExistingShapes:

    def __init__(self):
        self.squareList = []
        self.colours = []
        self.collision1 = False
        self.collided = False

    def appending(self):
        for i in range(0,4):
            self.squareList.append(currentRect[i])
        for i in range(0,4):
            self.colours.append(currentBlock.colour)

    def drawAllShapes(self):
        for i in range(0, len(self.squareList)):
            pygame.draw.rect(screen, self.colours[i], self.squareList[i])
            pygame.draw.rect(screen, 0, self.squareList[i], 1)

    def collision(self):

        for i in range(len(self.squareList)):
            for j in range(0,4):
                self.collision1 = (currentRect[j]).colliderect(self.squareList[i])
                if self.collision1:
                    self.collided = True
                    return

    def deletingLines(self):
        remove = []
        num_removed = 0
        for i in range(0, playScreenHeight, width):
            count1 = 0
            for j in range(len(self.squareList)):
                if self.squareList[j].y == i:
                    count1 += 1
            if count1 == 10:
                num_removed += 1
                remove.append(i)
                #remove = list(set(remove))

        remove2 = []
        for i in remove:
            for pos,square in enumerate(self.squareList):
                if square.y == i:
                    remove2.append(pos)
                elif square.y < i:
                    square.y += width
        remove2 = list(set(remove2))
        remove2.sort()
        for i in remove2[::-1]:
            self.squareList.pop(i)
            self.colours.pop(i)

        return num_removed


class PurpleT:
    def __init__(self):
        self.currentSquares = [0,1,2,3]
        self.currentRect = [0,1,2,3]
        self.colour = (148,0,211)
        self.x = 120
        self.y = 0

        self.currentSquares[0] = Square(self.x, (self.y+width))
        self.currentSquares[1] = Square((self.x+width), self.y)
        self.currentSquares[2] = Square((self.x+width), (self.y+width))
        self.currentSquares[3] = Square((self.x+(2*width)), (self.y+width))
        self.angle = 0

        self.assignCentre()

    def assignCentre(self):
        self.xCoordinate = (self.currentSquares[0].x + self.currentSquares[3].x + width)/2
        self.yCoordinate = (self.currentSquares[0].y + self.currentSquares[3].y + width)/2
        self.centre = (self.xCoordinate), (self.yCoordinate)


class BlueLine:
    def __init__(self):
        self.currentSquares = [0,1,2,3]
        self.currentRect = [0,1,2,3]
        self.colour = (0,255,255)
        self.x = 120
        self.y = 0

        self.currentSquares[0] = Square(self.x, (self.y))
        self.currentSquares[1] = Square((self.x+width), self.y)
        self.currentSquares[2] = Square((self.x+(2*width)), (self.y))
        self.currentSquares[3] = Square((self.x+3*width), (self.y))
        self.angle = 0

        self.assignCentre()

    def assignCentre(self):
        y_diff = self.currentSquares[0].y - self.currentSquares[1].y
        if y_diff == 0:
            self.xCoordinate = (self.currentSquares[0].x - self.currentSquares[2].x + 2*width)/4
            self.xCoordinate += self.currentSquares[2].x
        else:
            self.xCoordinate = self.currentSquares[0].x + (y_diff+width)/2


        x_diff = self.currentSquares[1].x - self.currentSquares[0].x
        if x_diff == 0:
            self.yCoordinate = (self.currentSquares[0].y - self.currentSquares[2].y + 2*width)/4
            self.yCoordinate += self.currentSquares[2].y
        else:
            self.yCoordinate = self.currentSquares[0].y + (x_diff+width)/2

        self.centre = (self.xCoordinate), (self.yCoordinate)


class YellowSquare:

    def __init__(self):
        self.currentSquares = [0,1,2,3]
        self.currentRect = [0,1,2,3]
        self.colour = (255,255,0)
        self.x = 160
        self.y = 0

        self.currentSquares[0] = Square(self.x, (self.y))
        self.currentSquares[1] = Square((self.x+width), self.y)
        self.currentSquares[2] = Square((self.x), (self.y+width))
        self.currentSquares[3] = Square((self.x+width), (self.y+width))
        self.angle = 0

        self.assignCentre()

    def assignCentre(self):
        self.xCoordinate = (self.currentSquares[0].x + self.currentSquares[3].x + width)/2
        self.yCoordinate = (self.currentSquares[0].y + self.currentSquares[3].y + width)/2
        self.centre = (self.xCoordinate), (self.yCoordinate)


class BlueL:
    def __init__(self):
        self.currentSquares = [0,1,2,3]
        self.currentRect = [0,1,2,3]
        self.colour = (0,0,205)
        self.x = 120
        self.y = 0

        self.currentSquares[0] = Square(self.x, (self.y))
        self.currentSquares[1] = Square((self.x), self.y+width)
        self.currentSquares[2] = Square((self.x+width), (self.y+width))
        self.currentSquares[3] = Square((self.x+(2*width)), (self.y+width))
        self.angle = 0

        self.assignCentre()

    def assignCentre(self):
        self.xCoordinate = (self.currentSquares[1].x + self.currentSquares[3].x + width)/2
        self.yCoordinate = (self.currentSquares[1].y + self.currentSquares[3].y + width)/2
        self.centre = (self.xCoordinate), (self.yCoordinate)


class OrangeL:
    def __init__(self):
        self.currentSquares = [0,1,2,3]
        self.currentRect = [0,1,2,3]
        self.colour = (255,165,0)
        self.x = 120
        self.y = 0

        self.currentSquares[0] = Square(self.x+(2*width), (self.y))
        self.currentSquares[1] = Square((self.x), self.y+width)
        self.currentSquares[2] = Square((self.x+width), (self.y+width))
        self.currentSquares[3] = Square((self.x+(2*width)), (self.y+width))
        self.angle = 0

        self.assignCentre()

    def assignCentre(self):
        self.xCoordinate = (self.currentSquares[1].x + self.currentSquares[3].x + width)/2
        self.yCoordinate = (self.currentSquares[1].y + self.currentSquares[3].y + width)/2
        self.centre = (self.xCoordinate), (self.yCoordinate)


class GreenShape:
    def __init__(self):
        self.currentSquares = [0,1,2,3]
        self.currentRect = [0,1,2,3]
        self.colour = (0,255,0)
        self.x = 120
        self.y = 0

        self.currentSquares[0] = Square(self.x, (self.y+width))
        self.currentSquares[1] = Square((self.x+width), self.y+width)
        self.currentSquares[2] = Square((self.x+width), (self.y))
        self.currentSquares[3] = Square((self.x+(2*width)), (self.y))
        self.angle = 0

        self.assignCentre()

    def assignCentre(self):
        self.xCoordinate = (self.currentSquares[1].x + 20)
        self.yCoordinate = (self.currentSquares[1].y + 20)
        self.centre = (self.xCoordinate), (self.yCoordinate)


class RedShape:
    def __init__(self):
        self.currentSquares = [0,1,2,3]
        self.currentRect = [0,1,2,3]
        self.colour = (255,0,0)
        self.x = 120
        self.y = 0

        self.currentSquares[0] = Square(self.x, (self.y))
        self.currentSquares[1] = Square((self.x+width), self.y)
        self.currentSquares[2] = Square((self.x+width), (self.y+width))
        self.currentSquares[3] = Square((self.x+(2*width)), (self.y+width))
        self.angle = 0

        self.assignCentre()

    def assignCentre(self):
        self.xCoordinate = self.currentSquares[2].x + 20
        self.yCoordinate = self.currentSquares[2].y + 20
        self.centre = (self.xCoordinate), (self.yCoordinate)


def increasing_score(num_removed, score, level):
    if num_removed == 1:
        score += (level+1) * 40
    elif num_removed == 2:
        score += (level+1) * 100
    elif num_removed == 3:
        score += (level+1) * 300
    elif num_removed == 4:
        score += (level+1) * 1200
    return score


currentBlock = Block()
allShapes = ExistingShapes()

playing = True
finishing_y = 50 #its the y coordinate of the red line at the top of the screen

def playing():
    global currentBlock, count, spaceDown, downwardsKey, sideKeyDown, allShapes, currentRect, side, lines_removed, score, level, playing

    for i in range(0,4):
        currentBlock.shape.currentSquares[i].updating(i)
    screen.fill(0)
    allShapes.drawAllShapes()
    currentBlock.drawing()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                side = 1
                sideKeyDown = True

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                side = -1
                sideKeyDown = True

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                downwardsKey = True

            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                rotate = currentBlock.rotate()
                if rotate == 'collided':
                    currentBlock.rotateClockwise()

            elif event.key == pygame.K_SPACE:
                spaceDown = True

            elif event.key == pygame.K_z:
                rotate = currentBlock.rotateClockwise()
                if rotate == 'collided':
                    currentBlock.rotate()


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                downwardsKey = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_d:
                sideKeyDown = False

    if sideKeyDown:
        if int(count%40) == 0:
            if currentBlock.shape.currentSquares[1].checkIfEdge() == False:
                for i in range(0,4):
                    currentBlock.shape.currentSquares[i].move(side, 1, i) #side is declared higher up whe the key is pressed so that whe the right key is pressed it moves right so the side is positive as then the x value should increase.
            for i in range(0,4):
                currentBlock.shape.currentSquares[i].updating(i)
            allShapes.collision()
            if allShapes.collided:
                for i in range(0,4):
                    currentBlock.shape.currentSquares[i].move(side, -1, i) #the -1 is because it wants it to move in the oppposite dire3ctio to before. all the plusers and minuses somehow make sense.
            allShapes.collided = False

    if downwardsKey: #soft drop
        if int(count%30) == 0: #the biggeer the number the slower itll fall because maths.
            score += 1
            currentBlock.falling(1) #one means itll fall downswards (positive so y will increase)
            #currentBlock.shape.draw()
            allShapes.collision()
            if allShapes.collided:
                count -= 1
                currentBlock.falling(-1) #- means itll move upwards (negative means y will decrease)

    if int(count%400) == 0 and not(allShapes.collided):
        currentBlock.falling(1)
        allShapes.collision()
        if allShapes.collided:
            currentBlock.falling(-1)

    if spaceDown: #falling all the way down. This will keep evaluating to true until the block collides with all the shapes at the bottom only then itll be false.
        currentBlock.falling(1)
        allShapes.collision()
        score += 2 #two points are added for every cell is falls
        if allShapes.collided:
            score -= 2 #because the points where added but it moves back up so they have to be taken away again.
            currentBlock.falling(-1)
            spaceDown = False

    for i in range(0,4):
        if (currentBlock.shape.currentSquares[i].y + width) == playScreenHeight:
            allShapes.collided = True

    if allShapes.collided:
        spaceDown = False
        allShapes.appending()

        allShapes.collided = False
        num_removed = allShapes.deletingLines() #tnis will return the number of lines that have been removed.
        score = increasing_score(num_removed, score, level)
        for i in range(0,num_removed): #so that it adds one by one so if the level is to go up it does like if more than one line is being deleted.
            lines_removed += 1
            if lines_removed % 10 == 0: #the level increases every 10 lines.
                level += 1

        for i in currentRect: #checks if any of the squares are touching or over the red line. if yes then the payer loses and the game is ended.
            if i.y <= finishing_y:
                playing = False

        currentRect = []
        currentBlock = Block() #picks a new random block.

    writingText(score, (screenWidth-100)/2, 0, 100, 50, (255,255,255), 0, 50)
    pygame.draw.line(screen, (255,0,0), (0,finishing_y), (screenWidth,50)) #red line at the top of the screen.

    count+=1
    clock.tick(1000)
    pygame.display.flip()


def main():
    while playing:
        playing()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        writingText('You lost', (screenWidth-100)/2, (screenHeight-50)/2, 100, 50, (255,255,255), 0, 80)
        pygame.display.flip()


while True:
    main()
