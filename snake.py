#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np

RANDOM_RATE = 10

directions_dict = {0:(-1,0), 1:(1,0), 2:(1,0), 3:(0,-1)}

class Snake(object):
    '''Class for representing snake in a game.
    '''
    def __init__(self, st_coords, direction, screen, brain):
        '''
        self.screenx, self.screeny - screen size for colision detection

        self.body - list of tuples, containing coords of snake parts. 
        Because we can create many snakes on level, we can can create 
        parametrisied instance. By now, every snake starts at this same spot.
        A little trick is hidden in last expression (multiplying by 3).


        self.head - first element of body moved in snakes self.direction. For
        colision detection purposes.

        self.direction - starting direction of a snake. As you can see, methods blocks
        vertical movments as starting directions.

        self.color - color of the snake. It is handling by curses library. Colors
        library are created in main.py. Check curses_initialize funtions for more
        details

        self.brain - neural network of snake

        self.lifespan - snake can only took that much steps before dying

        self.goodnes - calculated goodness of a snake
        '''
        self.screenx = screen[1]                     
        self.screeny = screen[0]                     
        self.body = [(st_coords[0], st_coords[1])] * 3 
        self.head = (st_coords[0], st_coords[1])
        self.direction = direction                    
        self.color = random.randint(1,15)                           
        self.brain = brain                           
        self.lifespan = 200                          
        self.goodnes = 0                             

    def give_me_head(self):
        '''Calculates where snake head is heading (pun intented)
        '''
        self.head = (self.body[0][0] + self.direction[0], 
            self.body[0][1] + self.direction[1])

    def move(self, apple):
        '''Function for moving the snake.
        '''
        
        #snake`s head moving
        self.give_me_head()

        #snakes`s tail moving
        self.body = [self.head] + self.body[:-1]

        #snake thinks
        self.think_about_your_life(apple)         

        #shortening lifespan
        self.lifespan -= 1    

    def collides(self):
        '''Colision detection function
        '''
        if self.head[1] == self.screenx-1 or self.head[0] == self.screeny-1:
            return True

        if self.head[1] == 0 or self.head[0] == 0:
            return True
        
        if self.head in self.body[1:]:
            return True  

    def eats(self, apple):
        '''
        Function checks if new calculated head collides with apple.
        If so, new apple is generated and lat element of snakes body is 
        doubled making it longer.
        Function returns True for adding score reason.
        '''
        if self.body[0] in apple.coords:       
            apple.generate(self.body)
            self.body.append(self.body[-1])

    def look_around(self, apple):
        '''
        Function calculating obstacles in four direction from snakes head
        TO DO: optimisation
        '''
        #apple.coords[0][0]  = y 
        #apple.coords[0][1] = x
        visions = [0]*6                               #clearing the visions

        visions[0] = self.head[1]                     #upper
        visions[1] = self.screenx - self.head[1]      #right
        visions[2] = self.screeny - self.head[0]      #down
        visions[3] = self.head[0]                     #left
        visions[4] = self.head[1] - apple.coords[0][1]
        visions[5] = self.head[0] - apple.coords[0][0]

        return visions

    def negative_direction(self):
        '''Generating negative direction of snake
        '''
        return (self.direction[0] * -1, self.direction[1] * -1)

    def think_about_your_life(self, apple):
        '''Function making snake thinks about his life and
        his future
        '''
        old_direction = tuple(self.direction)         #coping direction
        output = self.brain.output(self.look_around(apple))#neural net getting output
        
        #first best option
        max_value = max(output)
        max_value_index = output.index(max_value)
        best_dir = directions_dict[max_value_index]
        output.remove(max_value)  
        
        #second best option
        sec_max_value = max(output)
        sec_max_value_index = output.index(sec_max_value)
        sec_best_dir = directions_dict[sec_max_value_index]

        #cheking options (snake cannot turn 180 degrees!)
        if best_dir == self.negative_direction():
            self.direction = sec_best_dir
        else:
            self.direction = best_dir  

    def rate(self):
        '''
        Function rating the particular snake.
        By now, unused yet.
        '''
        self.goodnes = self.lifespan + len(self.body)*15

