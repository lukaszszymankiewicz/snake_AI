#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import section
import curses

from apple import Apple
from gameboard import GameBoard
from population import Population

class Game(object):
    ''' Class containing whole snake game.
    '''
    def __init__(self, window_y, window_x, population_size, mutation_rate, crossover_rate):
        
        self.screen_size = (window_y, window_x)       #self-explanatory                
        self.level = 0                                #making gameboard (dummy for now)
        self.morsel = Apple(self.screen_size)         #making apple
        self.population = Population(                 #snake family
                population_size = population_size,
                mutation_rate = mutation_rate, 
                crossover_rate = crossover_rate,
                screen = self.screen_size)
        self.population.first_generation()            #cpus snakes
        self.pressed_key = 0                          #dummy for exiting

    def game(self, stdscr):
        ''' Actual game'''     
   
        self.level = GameBoard(self.screen_size)      #making gameboard

        #game loop
        while self.pressed_key != ord('q'):           #main while loop

            #PLAYER CONTROL SECTION
            self.pressed_key = self.level.board.getch()#getting key from player  

            #CPUs SECTIONS
            for cpu in self.population.cpus:
                self.level.unprint(cpu)               #erasing all snakes
                
                cpu.move(self.morsel)                 #generating moves

                if cpu.collides():                    #collision checking
                    self.population.cpus.remove(cpu)
                    self.level.unprint(cpu)
                                    
                if cpu.eats(self.morsel):             #snake eats an apple
                    pass                              #temporarly disabled
                
                if cpu.starved():                     #if snake dies of
                    self.population.cpus.remove(cpu)  #starvation
                    self.level.unprint(cpu)           #it need to be killed

            #IS FUN OVER?           
            if self.population.empty():               #checking if board has its winner
                self.level.unprint(self.population.cpus[0])
                self.population.new_generation()      #winner is having a child  

            #SCREEN SECTION                           #printing everything out
            for cpu in self.population.cpus:          #printing every snake 
                self.level.inprint(cpu)
            
            self.level.board.border()
            self.level.print_aux(self.morsel,         #print nesseceties
                self.population.generation)

            self.level.board.refresh()                #refreshing the screen

            
    def main(self):
        curses.wrapper(self.game)