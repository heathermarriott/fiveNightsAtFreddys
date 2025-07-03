#   game 900x500
#
#   door      office   door
#    150x45   600x455   150x45
import pygame
import random

#define size of window
window_size=(900,500)
win=pygame.display.set_mode(window_size)

#set title on window
pygame.display.set_caption("Five Nights At Freddy's") 
    
#load images
freddy=pygame.image.load('freddy.png')
fred_head=pygame.image.load('freddyHead.png')
office=pygame.image.load('office.png')

window=pygame.image.load('window.png')
window_dark=pygame.image.load('windowDark.png')

light_button=pygame.image.load('lightButton.png')
light_button_on=pygame.image.load('lightButtonOn.png')

door_button=pygame.image.load('doorButton.png')
door_button_on=pygame.image.load('doorButtonOn.png')

door_closed=pygame.image.load('doorClosed.png')
door_dark=pygame.image.load('doorDark.png')
door_light=pygame.image.load('door.png')

class Door:
    def __init__(self):
        self.door_open = True
        self.light_on = False
        self.door_graphic = door_dark
        self.door_button_graphic = door_button
        self.light_button_graphic = light_button
        self.light_timer = 0
        self.window_graphic = window_dark
        
    def lightSwitch(self):
        print("light button")
        if self.light_on: #if light was on, turn off
            self.light_button_graphic = light_button
            self.window_graphic = window_dark
            self.door_graphic = door_dark
            self.light_on = False
        else: # if light was off, turn on
            print("light was off, turn on", self.door_open)
            self.light_button_graphic = light_button_on
            self.window_graphic = window
            if self.door_open:
                self.door_graphic = door_light
            else:
                self.door_graphic = door_closed
            
            self.light_on = True
            self.light_timer = 0
            
    def doorSwitch(self):
        if self.door_open: #door was open, close it
            print("door was open, close it")
            self.door_button_graphic = door_button_on
            if self.light_on:
                self.door_graphic = door_closed
            self.door_open = False
             
        else: #door was closed, open it
            self.door_button_graphic = door_button
            if self.light_on:
                self.door_graphic = door_light
            self.door_open = True
        
door1 = Door()
door2 = Door()

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 40)

# Button rect for click detection
light_button1_rect = pygame.Rect(130, 200, light_button.get_width(), light_button.get_height())
light_button2_rect = pygame.Rect(730, 200, light_button.get_width(), light_button.get_height())
door_button1_rect = pygame.Rect(130, 150, door_button.get_width(), door_button.get_height())
door_button2_rect = pygame.Rect(730, 150, door_button.get_width(), door_button.get_height())

def draw_window():
    background=(34, 30, 27) # red, green, blue tuple
    win.fill(background)

    msg= myfont.render('Five Nights at Freddy\'s', False, (255,0,0))
    win.blit(msg, (250,10))
    
    #Left Door
    win.blit(door1.door_graphic, (0, 55))
    win.blit(door1.light_button_graphic, (130, 200))
    win.blit(door1.door_button_graphic, (130, 150))
    win.blit(door1.window_graphic, (180, 130))
        
    #Right Door
    win.blit(door2.door_graphic, (750, 55))
    win.blit(door2.light_button_graphic, (730, 200))
    win.blit(door2.door_button_graphic, (730, 150))
    win.blit(door2.window_graphic, (570, 130))
    
    pygame.display.update() #update the display


def main():  
    run=True
    while run:
        for event in pygame.event.get():
            #user clicked X in upper left corner to quit
            if event.type == pygame.QUIT:
                print('User quit game')
                run=False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if light_button1_rect.collidepoint(mouse_pos):
                    door1.lightSwitch()
                elif light_button2_rect.collidepoint(mouse_pos):
                    door2.lightSwitch()
                elif door_button1_rect.collidepoint(mouse_pos):
                    door1.doorSwitch()
                elif door_button2_rect.collidepoint(mouse_pos):
                    door2.doorSwitch()
            
        draw_window()        
    pygame.quit()
main()
    






