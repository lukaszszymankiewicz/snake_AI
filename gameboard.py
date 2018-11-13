#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import section
import curses

#graphics
snake_body = 'x'                                      #ASCI symbol representing snakes body
snake_food = '@'                                      #ASCI symbol representing apple
heads_from = {(1,0):'v', (-1,0):'^',                  #snakes head
            (0,-1):'<', (0,1):'>'}                    #from diffrent angles 

class GameBoard(object):
    '''Class containing gameboard and methods for printing in curses
    '''

    def __init__(self, screen):
        '''Initialising curses window and all paramaters.
        '''
        self.stdscr = curses.initscr()                #starting curses screen
        curses.noecho()                               #disabling input confirmation
        curses.cbreak()                               #one char input
        curses.curs_set(0)                            #making cursor non-visible
        curses.start_color()                          #initialising colours
        curses.use_default_colors()                   #initialising default colors

        for i in range(1, 16):                        #generating color library     
            curses.init_pair(i + 1, i, -1)            #there are 16 of it

        self.maxy, self.maxx = self.stdscr.getmaxyx() #getting max size of window            
        self.board = curses.newwin(                   #creating curses window 
                            screen[0],                #upper-left y coord      
                            screen[1],                #upper-left x coord
                            (self.maxy-screen[0])//2, #down-rigth y coord
                            (self.maxx-screen[1])//2) #down-rigth x coord
        self.board.clear()                            #cleaning the window  
        self.board.border()                           #printing board border
        self.board.timeout(100)                       #applying time 
        self.board.nodelay(1)                         #applying time

    def inprint(self, snake):
        '''Function for printing snake on screen.
        '''        
        
        #head
        self.board.addstr(
                    snake.body[0][0],                 #y coord
                    snake.body[0][1],                 #x coord
                    heads_from[snake.direction],      #snake head ASCII symbol
                    curses.color_pair(snake.color))   #snake color
        
        #rest of the body 
        for part in snake.body[1:]:
            self.board.addstr(
                    part[0],                          #y coord
                    part[1],                          #x coord
                    snake_body,                       #snake body ASCII symbol
                    curses.color_pair(snake.color))   #snake color

    def unprint(self, snake):
        '''Function for erasing snake from screen
        '''
        for part in snake.body:                       #for every part of snake
            self.board.addstr(part[0], part[1], ' ')  #space is printed

    def print_aux(self, apple, generation):
        '''Function is putting apple sign on board.
        '''
        self.board.addstr(apple.coords[0][0],          #y coord 
                        apple.coords[0][1],            #x coord
                        snake_food,                    #apple ASCII symbol
                        curses.color_pair(apple.color))#apple color
        
        #generation        
        self.board.addstr(0, 5, 'Gen:' + str(generation))
