import math
import pygame, random, pygame_widgets
from pygame.locals import *
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import os

initial_angle = 0
from sysairpendulum import AirPendulum
pendulo = AirPendulum(theta_b = initial_angle)

pygame.init()

# Display dimensions
Width, Height = (1000, 600)

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Aeropendulo')

slider = Slider(screen, Width/2 - 100, Height - 100, 200, 10, min=0, max=90, step=1, initial = initial_angle)
output = TextBox(screen, Width/2 - 90, Height - 75, 50, 50, fontSize=30)

aero_len = 225
aeropendulum = (Width/2, 125)
angle = 0

image_path = os.path.abspath("assets/assembly.jpg")
pendulum_background = pygame.image.load(image_path).convert()
background_pos = (Width/2 - 206, 100)

button = Button(
    screen, Width/2 - 25, Height - 75, 100, 50,

    # Optional Parameters
    text='Enviar',  # Text to display
    fontSize=25,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=lambda: pendulo.update_reference(slider.getValue())  # Function to call when clicked on
)

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

    

    angle, _anglep = pendulo.dynamic(pendulo.calc_pid())
    # angle = slider.getValue()
    angle = math.degrees(angle)
    screen.fill((255,255,255))
    screen.blit(pendulum_background, background_pos)
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