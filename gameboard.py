#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import section
import curses

#graphics
snake_body = 'x'                                      #ASCI symbol representing snakes body
snake_food = '@'                                      #ASCI symbol representing apple
heads_from = {(1,0):'v', (-1,0):'^',                  #snakes head
            (0,-1):'<', (0,1):'>'}                    #snaked head

class GameBoard(object):
    '''
    Class containing actual gameboard and all methods which prints anything
    on curses-based window.
    '''

    def __init__(self, screen):
        '''
        self.board will contain curses stdscr (window object). But it must be
        a dummy at a start, before the curses is initialised.
        '''
        self.board = 0
        self.screenx = screen[1]
        self.screeny = screen[0]

    def initialize(self, stdscr):
        '''
        Setting up params for game board in curses window
        '''
        maxy, maxx = stdscr.getmaxyx()                #screen max_x and max_y
        maxwiny = (maxy-self.screeny)//2              #window max_y
        maxwinx = (maxx-self.screenx)//2              #window max_x

        self.board = curses.newwin(self.screeny,      #out actual window
                                    self.screenx, 
                                    maxwiny, 
                                    maxwinx)  

        self.board.clear()                            #cleaning the window
        self.board.border()                           #printing board border
        self.board.timeout(100)                       #applying time 
        self.board.nodelay(1)                         #applying time
        self.print_gen(0)                             #setting starting score                               
    
    def inprint(self, snake):
        '''
        Function for printing snake on screen.
        Visuals of snake is parametriased
        '''        
        #head
        self.board.addstr(snake.body[0][0],            #y coord
                        snake.body[0][1],              #x coord
                        heads_from[snake.direction],   #snake head ASCII symbol
                        snake.color)                   #snake color
        
        #rest of the body 
        for part in snake.body[1:]:
            self.board.addstr(part[0],                 #y coord
                            part[1],                   #x coord
                            snake_body,                #snake body ASCII symbol
                            snake.color)               #snake color

    def unprint(self, snake):
        '''
        Function for erasing snake from screen
        '''
        for part in snake.body:
            self.board.addstr(part[0], part[1], ' ')

    def print_apple(self, apple):
        '''
        Function is putting apple sign on board. Coordinates is taken Apple
        object
        '''
        self.board.addstr(apple.coords[0][0],          #y coord 
                        apple.coords[0][1],            #x coord
                        snake_food,                    #apple ASCII symbol
                        apple.color)                   #red

    def print_gen(self, generation):
        '''
        Function for printing score on game board. Coords are fixed to
        avoid problems.
        '''
        self.board.addstr(0, 5, 'Generation:' + str(generation))