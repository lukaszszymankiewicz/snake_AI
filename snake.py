#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np
from matrices import crossover, mutate
from net import NeuralNetwork

directions_dict = {0:(-1,0), 1:(1,0), 2:(1,0), 3:(0,-1)}

class Snake(object):
    '''Class for representing snake in a game.
    '''
    def __init__(self, st_coords, direction, screen, color, brain):
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
        self.body = [(st_coords[0], st_coords[1])]*3 
        self.head = (st_coords[0], st_coords[1])
        self.direction = direction                    
        self.color = color                           
        self.brain = brain                           
        self.lifespan = 200                          
        self.goodnes = 0                             

    def give_me_head(self):
        '''
        Calculates where snake head is heading (pun intented)
        '''
        self.head = (self.body[0][0] + self.direction[0], 
            self.body[0][1] + self.direction[1])

    def move(self):
        '''Function for moving the snake.
        '''
        
        #snake`s head moving
        self.give_me_head()

        #snake thinks
        self.think_about_your_life() 

        #snakes`s tail moving
        self.body = [self.head] + self.body[:-1]

        #shortening lifespan
        self.lifespan -= 1    

    def is_colliding_with_itself(self):
        '''Colision detection function
        '''
        return self.head in self.body[1:]

    def is_colliding_with_wall(self):
        '''Colision detection function
        '''
        if self.head[1] == self.screenx-1 or self.head[0] == self.screeny-1:
            return True

        if self.head[1] == 0 or self.head[0] == 0:
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

    def look_around(self):
        '''
        Function calculating obstacles in four direction from snakes head
        TO DO: optimisation
        '''
        visions = [0]*8
        
        head = self.body[0]                          
        
        #searching for obstacle rigth to snakes head
        if head[1]+1 >= self.screenx-1 or (head[0], head[1]+1) in self.body:
            visions[0] = 1
        if head[1]+2 >= self.screenx-1 or (head[0], head[1]+2) in self.body:
            visions[1] = 1
        
        #searching for obstacle left to snakes head
        if head[1]-1 <= 0 or (head[0], head[1]-1) in self.body:
            visions[2] = 1
        if head[1]-2 <= 0 or (head[0], head[1]-2) in self.body:
            visions[3] = 1
        
        #searching for obstacle up to snakes head
        if head[0]+1 >= self.screeny-1  or (head[0]+1, head[1]) in self.body:
            visions[4] = 1
        if head[0]+2 >= self.screeny-1  or (head[0]+2, head[1]) in self.body:
            visions[5] = 1
        
        #searching for obstacle down to snakes head
        if head[0]-1 <= 0  or (head[0]-1, head[1]) in self.body:
            visions[6] = 1
        if head[0]-2 <= 0  or (head[0]-2, head[1]) in self.body:
            visions[7] = 1
        
        return visions

    def think_about_your_life(self):
        '''Function making snake thinks about his life and
        his future
        '''
        output = self.brain.output(self.look_around())#neural net getting output
        index_max = np.argmax(output)                 #taking best option
        self.direction = directions_dict[index_max]   #turning snake to best option

    def rate(self):
        '''
        Function rating the particular snake.
        By now, unused yet.
        '''
        self.goodnes = self.lifespan + len(self.body)*15

