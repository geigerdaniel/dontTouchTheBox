import pygame
from pygame import *
import sys
import time

pygame.init()

canvas = pygame.display.set_mode((1000, 1000))

originalWhiteDot = pygame.image.load("whiteDot.png")

yellowBoxXPosition = 300
yellowBoxYPosition = 300
yellowBoxXLength = 400
yellowBoxYLength = 400
yellowBox = Rect(yellowBoxXPosition, yellowBoxYPosition, yellowBoxXLength, yellowBoxYLength)

redBox = Rect(400, 400, 200, 200)

dotXLength = 20
dotYLength = 20
whiteDot = pygame.transform.scale(originalWhiteDot, (dotXLength, dotYLength))
dotXPosition = 0
dotYPosition = 0
initialXPosition = 0
initialYPosition = 0

clock = pygame.time.Clock()

checkForDirection = pygame.USEREVENT + 1
canCheckForDirection = True
targetTime = None
timerRunning = False

while True:
    clock.tick(60)

    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == checkForDirection and canCheckForDirection:
            if timerRunning:
                timerRunning = False  # stop the timer
                canCheckForDirection = True  # allow direction checking immediately
                targetTime = None  # reset the target time to None
                print("test2")

            else:
                timerRunning = True
                targetTime = time.time() + 0.1  # set the target time for the timer
                canCheckForDirection = False
                initialXPosition = dotXPosition
                initialYPosition = dotYPosition
                print("test3")

    # Check if the target time has passed and print "test" if it has
    if targetTime is not None and time.time() >= targetTime:
        print("test initial X = " + str(initialXPosition) + ", Y = " + str(initialYPosition) + " dot X = " + str(
            dotXPosition) + ", Y = " + str(dotYPosition))
        m = (dotYPosition - initialYPosition) / (dotXPosition - initialXPosition)
        c = dotYPosition - (m * dotXPosition)

        leftCollisionY = m*redBox.left + c
        rightCollisionY = m*redBox.right + c

        if redBox.top <= leftCollisionY <= redBox.bottom or redBox.topright <= rightCollisionY <= redBox.bottomright:
            print("oh no!!!")
        else:
            print("nice")

        timerRunning = False
        canCheckForDirection = False
        targetTime = None

    pygame.draw.rect(canvas, (10, 10, 40), [0, 0, 1000, 1000])
    pygame.draw.rect(canvas, (200, 200, 0), yellowBox)
    pygame.draw.rect(canvas, (255, 0, 0), redBox)
    canvas.blit(whiteDot, (dotXPosition, dotYPosition))

    whiteDotRect = Rect(dotXPosition, dotYPosition, dotXLength, dotYLength)
    dotToYellowCollide = pygame.Rect.colliderect(whiteDotRect, yellowBox)
    if dotToYellowCollide:

        # create an Event object with the user event type and post it to the event queue
        directionEvent = pygame.event.Event(checkForDirection)
        pygame.event.post(directionEvent)
    else:
        canCheckForDirection = True
    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_w] and dotYPosition > 1:
        dotYPosition -= 1
    if keyPressed[pygame.K_s] and dotYPosition < 1000 - dotYLength - 1:
        dotYPosition += 1
    if keyPressed[pygame.K_a] and dotXPosition > 1:
        dotXPosition -= 1
    if keyPressed[pygame.K_d] and dotXPosition < 1000 - dotXLength - 1:
        dotXPosition += 1
    print(initialXPosition)
    print(initialYPosition)

    pygame.display.update()
    pygame.display.flip()
