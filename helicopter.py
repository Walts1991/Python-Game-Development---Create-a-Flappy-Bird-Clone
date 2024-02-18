import  pygame
import  time
from random import randint,randrange

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
grey = (128,139,136)
skyblue = (135,206,235)
sunset = (253,72,47)
greenyellow = (184,255,0)
brightblue = (47,228,253)
orange = (255,113,0)
yellow = (255,236,0)
purple = (252,67,255)

colorChoices = [greenyellow,orange,yellow,purple,black,red,grey]

pygame.init() #import modules from pygame

surfaceWidth = 800
surfaceHeight = 500
imageHeight = 47
imageWidth = 94

surface = pygame.display.set_mode((surfaceWidth,surfaceHeight)) #create the surface that will be used to draw on 800x400 pixels
pygame.display.set_caption("Helicopter") #sets window title
clock = pygame.time.Clock() #used to track time for frames per second (smoothness)

img = pygame.image.load("helicopter-v1.png") #define image outside of helicopter function

def score(count):
    font = pygame.font.Font("freesansbold.ttf",20)
    text = font.render("Score: "+str(count), True, white)
    surface.blit(text, [0,0])

def blocks(x_block,y_block,block_width,block_height,gap,colorChoice):
    pygame.draw.rect(surface,colorChoice,[x_block,y_block,block_width,block_height])
    pygame.draw.rect(surface,colorChoice,[x_block,y_block + block_height + gap,block_width,surfaceHeight - block_height - gap])

def replay_or_quit():
    """Asks the user if they want to play again or quit"""
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            continue

        return event.key

    return None

def makeTextObjs(text,font):
    textSurface = font.render(text,True,white)
    return textSurface, textSurface.get_rect()

def msgSurface(text):
    smallText = pygame.font.Font("freesansbold.ttf",20)
    largeText = pygame.font.Font("freesansbold.ttf",150)

    titleTextSurf, titleTextRect = makeTextObjs(text, largeText)
    titleTextRect.center = surfaceWidth / 2, surfaceHeight / 2
    surface.blit(titleTextSurf,titleTextRect)

    typTextSurf, typTextRect = makeTextObjs("Press any key to play again", smallText)
    typTextRect.center = surfaceWidth / 2, ((surfaceHeight / 2) + 100)
    surface.blit(typTextSurf,typTextRect)

    pygame.display.update()
    time.sleep(2)

    while replay_or_quit() == None:
        clock.tick()

    main()

def gameOver():
    msgSurface("Kaboom!")

def helicopter(x,y,image):
    surface.blit(img,(x,y)) #draws image at x and y coordinates

#creates game loop to run through code x amount of times per second
def main():
    x = 150 #higher x = position is further right
    y = 200 #higher y = position is further down
    y_move = 0

    x_block = surfaceWidth
    y_block = 0

    gap = int(imageHeight * 3)
    block_width = 75
    block_height = randint(0,surfaceHeight-gap)
    block_move = 3

    current_score = 0

    blockColor = colorChoices[randrange(0,len(colorChoices))]

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move = -5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_move = 5

        y += y_move

        surface.fill(skyblue)
        helicopter(x,y,img)

        blocks(x_block,y_block,block_width,block_height,gap,blockColor)
        score(current_score)
        x_block -= block_move

        if y > surfaceHeight-imageHeight or y < 0:
            gameOver()

        if x_block <(-1 * block_width):
            x_block = surfaceWidth
            block_height = randint(0,surfaceHeight-gap)
            blockColor = colorChoices[randrange(0,len(colorChoices))]
            current_score += 1

        if x + imageWidth > x_block:
            if x < x_block + block_width:
                #print("possibly within the boundaries of x")
                if y < block_height:
                    #print("Y crossover UPPER!")
                    if x - imageWidth < block_width + x_block:
                        #print("game over hit upper")
                        gameOver()

        if x + imageWidth > x_block:
            #print("X crossover")
            if y + imageHeight > block_height + gap:
                #print("Y crossover lower")
                if x < block_width + x_block:
                    #print("game over lower")
                    gameOver()

        #if x_block < (x - block_width) < x_block + block_move:
            #current_score += 1

        if 5 <= current_score < 10:
            block_move = 4
            gap = int(imageHeight * 2.9)
        if 10 <= current_score < 15:
            block_move = 5
            gap = int(imageHeight * 2.8)
        if 15 <= current_score < 20:
            block_move = 6
            gap = int(imageHeight * 2.7)
        if 20 <= current_score < 25:
            block_move = 7
            gap = int(imageHeight * 2.6)

        pygame.display.update() #.update without parameter updates whole screen, same as .flip
        #.update with parameters updates specific areas on screen
        clock.tick(60) #specifies how many frames per second (frames per second is roughly equal to ticks per second)

main()
pygame.quit()
quit()
