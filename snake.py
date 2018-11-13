#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from random import randint

turning_dict = [(-1,0), (0,1), (1,0), (0,-1)]

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
        self.body = [( randint(5,23), randint(5,23))] * 3 
        self.head = self.body[0]
        self.direction = direction                    
        self.color = randint(1,15)                           
        self.brain = brain                           
        self.lifespan = 200                          
        self.goodnes = 0                             

    def give_me_head(self):
        '''Calculates where snake head is heading (pun intented)
        '''
        self.head = self.body[0]

    def move_head(self):
        '''Calculated head moved to new direction
        '''
        self.head = (self.body[0][0] + self.direction[0], 
            self.body[0][1] + self.direction[1])

    def move(self, apple):
        '''Function for moving the snake.
        '''        
        
        #snake`s head moving
        self.move_head()

        #snakes`s tail moving
        self.body = [self.head] + self.body[:-1] 

        self.give_me_head()

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
            self.lifespan += 15

    def look_for_body(self):
        '''Looking for snakes body in eigth directions
        TODO: For goddamn sake. look_for_for body and look_for_food 
        can be concat easyli!
        '''
        dirs = [(-1,0), (0, 1), (1, 0), (0,-1),       #horizontal/vertical 
                (-1,1), (1,1), (1,-1),(-1,-1)]        #cross direction
        
        body_vectors = [0]*8
            
        for number, dir in enumerate(dirs, 0):
            
            searched_distance = 0
            searched_coord = self.head[:]            

            while searched_coord[0]>0 and searched_coord[1]>0 \
            and searched_coord[0]<self.screeny and searched_coord[1]<self.screenx:

                searched_coord = (searched_coord[0]+dir[0], searched_coord[1]+dir[1])    

                if searched_coord in self.body:
                    body_vectors[number] = searched_distance + 1
                    break
                    
                searched_distance += 1

        return body_vectors

    def look_for_food(self, apple):
        '''Looking for food body in eigth directions
        '''
        dirs = [(-1,0), (0, 1), (1, 0), (0,-1),       #horizontal/vertical 
                (-1,1), (1,1), (1,-1),(-1,-1)]        #cross direction

        apple_vectors = [0]*8               
            
        for number, dir in enumerate(dirs, 0):
            
            searched_distance = 0
            searched_coord = self.head[:]            

            while searched_coord[0]>0 and searched_coord[1]>0 \
            and searched_coord[0]<self.screeny and searched_coord[1]<self.screenx:

                searched_coord = (searched_coord[0]+dir[0], searched_coord[1]+dir[1])    

                if searched_coord == apple:
                    apple_vectors[number] = searched_distance + 1
                    return apple_vectors
                    
                searched_distance += 1

        return apple_vectors

    def look_around(self, apple):
        '''
        Function calculating obstacles in four direction from snakes head
        Visions consists from 24 numbers. First eight are distances from walls,
        next eight is distance from apple (0 if there isn`t apple in such direction),
        ant the last eight are distances from snakes body (0 if there isn`t no
        snake body in duch direction).

        visions[0-7] - distance from snakes head to walls.
            0-upper    4-upper,right
            1-right    5-down,right
            2-down     6-down,left
            3-left     7-upper,left
        First four is easy to catch - they are coded in heads coords.

        visions[8-15] - distance beetwen snakes head and appple.
            8-upper    12-upper,right
            9-right    13-down,right
            10-down    14-down,left
            11-left    15-upper,left
        First four is easy to catch - they are coded in heads coords.

        visions[16-23] - distance beetwen snakes head its body.
            16-upper    20-upper,right
            17-right    21-down,right
            18-down     22-down,left
            19-left     23-upper,left
        First four is easy to catch - they are coded in heads coords.

        '''
        visions = [0]*8
        apples = [0]*8
        bodys = [0]*8                             
        
        #walls
        
        visions[0] = self.head[0]                     #distance from upper wall
        visions[1] = self.screenx - self.head[1]      #distance from right wall
        visions[2] = self.screeny - self.head[0]      #distance from down wall
        visions[3] = self.head[1]                     #distance from left wall
        
        visions[4] = min(visions[0], visions[1])      #distance from upper-right wall
        visions[5] = min(visions[2], visions[1])      #distance from down-right wall
        visions[6] = min(visions[2], visions[3])      #distance from down-left wall
        visions[7] = min(visions[0], visions[3])      #distance from upper-left wall        

        apples = self.look_for_food(apple)
        bodys = self.look_for_body()

        return visions + apples + bodys

    def think_about_your_life(self, apple):
        '''Function making snake thinks about his life and
        his future
        '''
        output = self.brain.output(self.look_around(apple))#neural net getting output
        
        #first best option
        max_value = np.argmax(output)
        
        self.direction = turning_dict[max_value]

    def starved(self):
        '''Check if snake is starved to death
        '''
        return self.lifespan == 0 

    def rate(self):
        '''
        Function rating the particular snake.
        By now, unused yet.
        '''
        self.goodnes = self.lifespan + len(self.body)*15

