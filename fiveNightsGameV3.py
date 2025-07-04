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

class GameState:
    def __init__(self):
        self.freddy_timer=0
        self.freddy_x = window_size[0]/2
        self.freddy_dir = -1 #neg means left, pos right
        self.game_hour = 0
        self.hour_timer = 0
        self.game_over = False
        self.freddy_wins = False
        self.power_level = 500

game = GameState()
        
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

    if game.freddy_wins == False:
        msg= myfont.render('Five Nights at Freddy\'s', False, (255,0,0))
        win.blit(msg, (250,10))

        win.blit(freddy, (game.freddy_x, 100))
        win.blit(office, (150, 100))
                 
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

        if game.game_hour == 0:
            display_hour = 12
        else:
            display_hour = game.game_hour
        time = myfont.render(f'{display_hour} AM', False, (0,255,0))
        win.blit(time, (250, 35))

        power = myfont.render(f'{int(100*(game.power_level/500))} %', False, (0,255,0))
        win.blit(power, (250,60))

        if game.game_hour >= 6:
            msg2 = myfont.render("You Survived!", False, (255, 0,0))
            win.blit(msg2, (250, 95))
        
    else:
        if game.freddy_x < 700 and game.freddy_x >200:
            game.game_over = True
            win.blit(fred_head, (0,0))
            msg2 = myfont.render("Game Over", False, (255, 0,0))
            win.blit(msg2, (250, 95))
        else:
            win.blit(freddy, (game.freddy_x, 100))
    
    pygame.display.update() #update the display


def main():  
    run=True
    len_hour = 6000
    clock = pygame.time.Clock()
    game.freddy_timer = pygame.time.get_ticks() + 100
    game.hour_timer = pygame.time.get_ticks() + len_hour
    
    while run:
        current_time = pygame.time.get_ticks()
        clock.tick(60) #limit to 60 FPS
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
                    
        #if random.randint(0,120) == 0 and (game.freddy_wins == False):
        #    game.freddy_dir *= -1
                    
        if current_time > game.freddy_timer and (game.game_over == False):
            if game.power_level > 0 and (game.game_hour < 6):
                if door1.door_open == False:
                    game.power_level -= 2
                if door2.door_open == False:
                    game.power_level -= 2
                if door1.light_on :
                    game.power_level -= 2
                if door2.light_on:
                    game.power_level -= 2
            else:
                #everything shut off
                if door1.door_open == False:
                    door1.doorSwitch()
                if door2.door_open == False:
                    door2.doorSwitch()
                if door1.light_on:
                    door1.lightSwitch()
                if door2.light_on:
                    door2.lightSwitch()
                game.power_level = 0


            #see if freddy in an open doorway
            if door1.door_open and game.freddy_x <= -60:
                print("freddy enters door1")
                game.freddy_wins = True
            elif door2.door_open and game.freddy_x >= 750:
                print("freddy enters door2")
                game.freddy_wins = True

            if game.game_hour <=6:
                game.freddy_x += 10*game.freddy_dir
                
            if game.freddy_x < -60 or game.freddy_x > 750:
                game.freddy_dir *= -1
            game.freddy_timer = pygame.time.get_ticks() + 100
        if current_time > game.hour_timer and game.game_hour < 6 and (game.game_over==False):
            game.game_hour += 1
            game.hour_timer = pygame.time.get_ticks() + len_hour

        if game.game_hour >= 6:
            game.game_over = True
        draw_window()        
    pygame.quit()
main()
    






