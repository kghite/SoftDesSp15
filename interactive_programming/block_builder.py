""" Block Builder
    Authors: Alix McCabe, Kathryn Hite
    Description: This pygame is an interactive block builder where the user can move and place building blocks
                    within the game by moving a blue object in front of the camera to represent the position 
                    of the block they are placing.  This game works best when played in an area where there is
                    limited blue in the backround.
    Classes: BuildModel, DrawableSurface, Background, Block, BuildView, PygameKeyboardController, Build
"""

import pygame
import random
from random import randint
import cv2
import numpy as np
import pygame.locals
import sys
#I don't think pykalman ever got used!
import pykalman as pk

def tracker():
    """ This function uses the camera to track a blue object that the user is holding and 
        tracks the center of the object

        returns: center x and y position of the object
    """
    # Get the raw camera data
    kernel = np.ones((21,21),'uint8')
    #Doesn't look like this kernel variable is used. Was this a smoothing filter at some point? Try to regularly do code cleanup and get rid of stuff like this.
    cv2.destroyAllWindows()
    cap = cv2.VideoCapture(0)

    # Initialize the x and y position lists
    cx_0 = [0]*10
    cy_0 = [0]*10

    #it's not great practice to have your function do more than what your docstring specifies. I'd expect this function to return an x and y coordinate, not to pass it to some previously initialized builder object. It looks like this function grew bigger than it was meant to be. Restructure code when you get the chance! You'll be surprised at how much faster it makes later work.
    while(1):
        # Take each frame
        _, frame = cap.read()
        frame = cv2.blur(frame,(3,3))
        frame = cv2.flip(frame,1)
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define range of blue color in HSV
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])
        thresh = cv2.inRange(hsv,np.array(lower_blue),(upper_blue))
        #shoulda gotten rid of thresh2 if its unused
        thresh2 = thresh.copy()

        # Find contours in the threshold img
        contours,hierarchy= cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        # Find the contour with maximum area and store it as best_cnt
        if len(contours) ==0:
            #what's going on here and why is best_cnt 0.00001? Does cv2.moments complain if you give it zero? Might need some more documentation here.
            best_cnt = 0.00001
        else:
            max_area = 0
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > max_area:
                    max_area = area
                    best_cnt = cnt

        # Find the centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)

        # Get the x and y postion for the block
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        # Smooth the block motion by averaging previous points woth the current one
        cx_0[0] = cx
        cy_0[0] = cy

        i = 1
        while i < 9:
            #use a for loop instead when you know how many times its gonna repeat
            cx_0[i] = cx_0[i-1]
            cy_0[i] = cy_0[i-1]
            i += 1

        x_avg = sum(cx_0)/10
        y_avg = sum(cy_0)/10

        if x_avg < cx < x_avg:
            cx = cx
        else:
            cx = x_avg

        if y_avg < cy < y_avg:
            cy = cy
        else:
            cy = y_avg

        cv2.circle(frame,(cx,cy),5,255,-1)

        cv2.imshow('Original',frame)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Run the game model with the points found by opencv
        # it's best to make this kind of dependency explicit in your code by having the tracker function have a builder object passed to it. Depending on the builder variable having previously been initialized seems less redundant, but really causes a world of pain and makes debugging harder, particularly as things grow more complex.
        builder.run(cx, cy)


class BuildModel():
    """ Represents the game state of the building game """
    def __init__(self, width, height):
        """ Initialize the game model """
        self.blocks = []
        self.width = width
        self.height = height
        self.current_block = Block(300, 200)
        self.background = Background(width, height)
        self.obstacles = []
        self.blocks.append(self.current_block)

    def get_drawables(self):
        """ Return a list of DrawableSurfaces for the model """
        drawables = self.current_block.get_drawables()
        for block in self.blocks:
            drawables += block.get_drawables()
        return drawables

    def get_player(self):
        """ Return the block object """
        return self.block

    def new_block(self, hand_x, hand_y):
        """ Create a new block at the hand position """
        self.current_block = Block(hand_x, hand_y)
        blocks = self.blocks.append(self.current_block)
        return self.blocks

    def update(self, hand_x, hand_y):
        """ Updates the model and its constituent parts """
        self.current_block.update(hand_x, hand_y)

class DrawableSurface():
    """ A class that wraps a pygame.Surface and a pygame.Rect """

    def __init__(self, surface, rect):
        """ Initialize the drawable surface """
        self.surface = surface
        self.rect = rect

    def get_surface(self):
        """ Get the surface """
        return self.surface

    def get_rect(self):
        """ Get the rect """
        return self.rect

class Background():
    """ Represents the contents of the background """
    def __init__(self, screen_width, screen_height):
        """ initialize the game background.  The variables
            screen_width and screen_height are the size of the
            screen in pixels """
        self.screen_width = screen_width
        self.screen_height = screen_height

    def get_drawables(self):
        """ Get the drawables for the background """
        drawables = []

class Block():
    """ Represents the block in the game """
    def __init__(self, hand_x, hand_y):
        """ Initialize a block at the specified position
            pos_x, pos_y """
        self.rect = pygame.Rect(hand_x,hand_y,hand_x+100,hand_y+50)
        self.pos_x = hand_x
        self.pos_y = hand_y
        # Because there are only five images, we are using if statements here, with a  larger number of images to
        # manage we would use a dictionary and lookup the random number as the key for a colored block
        #use python's random.choice function! It's much more elegant, and will randomly choose an element from a list for you.
        i = randint(1, 5)
        if i == 1:
            self.image = pygame.image.load('images/blue_block.fw.png')
        if i == 2:
            self.image = pygame.image.load('images/red_block.fw.png')
        if i == 3:
            self.image = pygame.image.load('images/green_block.fw.png')
        if i == 4:
            self.image = pygame.image.load('images/purple_block.fw.png')
        if i == 5:
            self.image = pygame.image.load('images/yellow_block.fw.png')

        self.image = pygame.transform.scale(self.image, (100, 50))
        self.image.set_colorkey((255,255,255))

    def get_drawables(self):
        """ get the drawables that makeup the block """
        return [DrawableSurface(self.image, self.image.get_rect().move(self.pos_x, self.pos_y))]

    def update(self, hand_x, hand_y):
        """ update the block position """
        self.pos_x = hand_x
        self.pos_y = hand_y

class BuildView():
    def __init__(self, model, width, height):
        """ Initialize the view.  The input model
            is necessary to find the position of relevant objects
            to draw. """
        """ Initialize the game view. We use this to 
        find appropriate drawing positions."""

        pygame.init()
        # Retrieve width and height use screen.get_size()
        self.screen = pygame.display.set_mode((width, height))
        self.screen_boundaries = pygame.Rect(0 ,0, width, height)
        self.model = model

    def draw(self):
        """ Redraw the full game window """
        self.screen.fill((0,51,102))
        # Get the new drawables and use them to update the game screen
        self.drawables = self.model.get_drawables()
        for d in self.drawables:
            rect = d.get_rect()
            surf = d.get_surface()
            self.screen.blit(surf, rect)
        pygame.display.update()

class PygameKeyboardController():
    """ Allows the player to place bloxks by hitting the spacebar """
    def __init__(self, model):
        """ Initialize the keyboard controller.  The specified model
            will be manipulated in response to user key presses """
        self.model = model
        self.space_pressed = False

    def process_events(self, hand_x, hand_y):
        """ Process keyboard events """
        pygame.event.pump()
        if not(pygame.key.get_pressed()[pygame.K_SPACE]):
            self.space_pressed = False
        
        elif not(self.space_pressed):
            self.space_pressed = True
            self.model.new_block(hand_x, hand_y)

class Build():
    """ The main building class """

    def __init__(self):
        """ Initialize the building game.  Use build.run to
            start the game """
        self.model = BuildModel(640, 480)
        self.view = BuildView(self.model, 640, 480)
        self.controller = PygameKeyboardController(self.model)

    def run(self, hand_x, hand_y):
        """ The main runloop, called everytime we process a new hand x and y position """
        #the run function should in fact run a main loop to be more clear, instead of being called by a loop from outside.
        frame_count = 0
        # Update the view, check for the spacebar and collisions, update the block position
        self.view.draw()
        self.controller.process_events(100, 100)
        self.model.update(hand_x, hand_y)

if __name__ == '__main__':
    builder = Build()
    # Run the game while the q key has not been pressed
    while(pygame.key.get_pressed()[pygame.K_q] != True):
        #more conventional way of allowing quit events is the pygame.event.type == pygame.QUIT thing, which let's you x out of windows
        #you've got an endless loop inside another endless loop, when you really only need one event loop. That's if I understand the code correctly.
        #Alos, this pygame key press things hould really be happening inside of process_events!
        tracker()
    # Stop the video capture when the game ends
    cap.release()
    cv2.destroyAllWindows()
