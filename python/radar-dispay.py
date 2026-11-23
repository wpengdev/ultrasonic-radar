import pygame
import math
import serial
import time

#Connect to arduino serial
arduino = serial.Serial('COM5', 9600)

#Initialise pygame
pygame.init()

#Window dimensions
WIDTH = 1000
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Ultrasonic RADAR")
transparent = pygame.Surface((WIDTH, HEIGHT),pygame.SRCALPHA)

#Colours
Black = (0,0,0)
L_Green = (0,255,70)
D_Green = (0,90,30)
Red = (255,0,0)

#Radar settings
Radius = 100
multi = 4
centrex = WIDTH / 2
centrey = HEIGHT - 200

#Detected list
detected = []

#Angles
rangle = [0,30,60,90,120,150,180]
running = True

#Wait 2 seconds for arduino
time.sleep(2)

#Main loop
while running:

    if arduino.in_waiting > 0:

        #Check for external events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Clear screen
        screen.fill(Black)

        #Read one line of data
        data = arduino.readline()
        #print(data)

        #Convert bytes into normal python string
        message = data.decode('utf-8').strip()

        if message:
            #Display message
            print(message)
            #Split message into angle and distance
            angle, distance = message.split(",")
            #Store as variables
            angle = int(angle)
            distance = float(distance)
            if distance > Radius:
                distance = Radius

        #Draw distance arcs
        for i in range(1,5):
            radius = i*multi*Radius/4
            pygame.draw.arc(
                screen,
                L_Green,
                (centrex - radius, centrey - radius, 2 * radius, 2 * radius),
                0,
                math.pi,
                2
            )

        #Draw angle lines
        for i in rangle:
            endx = multi*Radius*math.cos(math.radians(180-i)) + centrex
            endy = (multi*Radius - (multi*Radius*math.sin(math.radians(180-i)))) + 200
            pygame.draw.line(
                screen,
                L_Green,
                (centrex, centrey),
                (endx, endy),
                1
            )

        #Draw scanner line
        scanx = multi*Radius*math.cos(math.radians(angle)) + centrex
        scany = (multi*Radius - (multi*Radius*math.sin(math.radians(angle)))) + 200
        pygame.draw.line(
            screen,
            (0, 255, 0),
            (centrex, centrey),
            (scanx, scany),
            1
        )

        #Display detected points
        pointx = multi*distance*math.cos(math.radians(angle)) + centrex
        pointy = multi*Radius - (multi*distance*math.sin(math.radians(angle))) + 200
        detected.append([pointx,pointy,255])

        for point in detected:
            x, y, alpha = point
            redness = int(255-0.6375*math.dist((x,y),(centrex,centrey)))
            greenness = int(0.6375*math.dist((x,y),(centrex,centrey)))

            colour = (redness, greenness, 0, alpha)
            pygame.draw.circle(
                        transparent,
                        colour,
                        (x, y),
                        5,
                        0
                    )
            point[2] -= 2

        detected = [point for point in detected if point[2] > 0]

        
        #pygame.draw.circle(
            #screen,
            #Red,
            #(pointx, pointy),
            #5,
            #0
        #)
    screen.blit(transparent)
        #Update display
    pygame.display.flip()

#Close pygame
pygame.quit()
