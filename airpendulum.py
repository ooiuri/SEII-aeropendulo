import math
import pygame, random, pygame_widgets
from pygame.locals import *
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.init()

# Display dimensions
Width, Height = (1000, 600)

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Aeropendulo')

slider = Slider(screen, Width/2 - 100, Height - 100, 200, 10, min=0, max=90, step=1)
output = TextBox(screen, Width/2 - 25, Height - 75, 50, 50, fontSize=30)

aero_len = 200
aeropendulum = (Width/2, 200)
angle = 0


def draw_line_round_corners(screen, color, origin, end, width):
    pygame.draw.line(screen, color, origin, end, width)
    pygame.draw.circle(screen, color, origin, width/2)
    pygame.draw.circle(screen, color, end, width/2)

clock = pygame.time.Clock()

angle_propeller = 0

while True:
    clock.tick(30)
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()

    output.setText(slider.getValue())
    angle = slider.getValue()

    screen.fill((255,255,255))
    endX = aeropendulum[0] + math.sin(math.radians(angle)) * aero_len
    endY = aeropendulum[1] + math.cos(math.radians(angle)) * aero_len


    draw_line_round_corners(screen, Color("black"), aeropendulum, (endX,endY), 5)
    
    motorX = 30*math.sin(math.radians(90 + angle)) + endX 
    motorY = 30*math.cos(math.radians(90 + angle)) + endY 

    draw_line_round_corners(screen, Color("silver"), (endX,endY), (motorX,motorY), 15)

    alfa = math.radians(90 - angle)
    angle_propeller += 20
    propeller_len = 30 * math.sin(math.radians(angle_propeller))
    propellerX1 = 30*math.sin(math.radians(90 + angle)) + endX - propeller_len*math.cos(alfa)
    propellerY1 = 30*math.cos(math.radians(90 + angle)) + endY - propeller_len*math.sin(alfa)
    propellerX2 = 30*math.sin(math.radians(90 + angle)) + endX + propeller_len*math.cos(alfa)
    propellerY2 = 30*math.cos(math.radians(90 + angle)) + endY + propeller_len*math.sin(alfa)

    draw_line_round_corners(screen, Color("blue"), (propellerX1,propellerY1), (propellerX2,propellerY2), 5)

    pygame_widgets.update(events)
    pygame.display.update()