#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class Apple(object):
    '''
    Class for apple (object which, when eaten grow up the snake).
    Method inside handles generating new apple on the boards
    '''

    def __init__(self, screen, color):
        '''
        self.coords - list on single tuple containing x and y coordinate.
        Because of using curses module, the coordinates is placed in a form:
        self.coords = [(y-coord, x-coord)]
        So, in diffrent way as we used normally.        '''
        
        self.screenx = screen[1]
        self.screeny = screen[0]
        self.color = color
        self.coords = [(self.screenx//2, self.screeny//2)]

    def generate(self, obstacles):
        '''
        Function is generating apple on new random place on game board. 
        This process will generating apples till it will find place 
        where there isnt any part of snake.
        The first apple is placed directly on snakes head,
        just to put this functions condition working.
        '''
        while self.coords[0] in obstacles:
            self.coords.pop()                                #empting apple tuple list
            self.coords = [(random.randint(1, self.screeny-2), #generation is paramater-based in
                        random.randint(1, self.screenx-2))]    #case of changing screen dimension    