#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import section
import curses
import random
from copy import deepcopy


from matrices import crossover, mutate
from net import NeuralNetwork
from apple import Apple
from gameboard import GameBoard
from snake import Snake


#parameters section:

MUTATION_RATE = 15                                    #mutation rate in % 

turn_dict = {ord('s'):(1,0), ord('w'):(-1,0),         #keyboard controls
            ord('a'):(0,-1), ord('d'):(0,1)}          #keyboard controls

winy = 28                                             #window heigth
winx = 28                                             #window width

screen = (winy, winx)                                 #screen tuple

class Game(object):
    '''
    Class containing whole snake game.  Actual game loop is put into
    game(self, stdscr) function.
    '''
    def __init__(self):
        
        self.game_is_on = True                        #self-explanatory                
        self.level = GameBoard(screen)                #making gameboard
        self.morsel = 0                               #making apple        
        self.cpus = []                                #cpus snakes
        self.generation = 0                           #no of actual snake generation
        self.snake_family = 10                        #numbers of snake in one generation

    def curses_initialize(self):
        '''
        All nessescary curses parameters set straight.
        Color library creaed below creates 16 color
        '''
        curses.noecho()                               #disabling input confirmation
        curses.cbreak()                               #one char input
        curses.curs_set(0)                            #making cursor non-visible
        curses.start_color()                          #initialising colours
        curses.use_default_colors()                   #initialising default colors
        
        for i in range(1, curses.COLORS):             #generating color librares     
            curses.init_pair(i + 1, i, -1)

    def random_color(self):
        '''Picks random color from color library
        '''
        return curses.color_pair(random.randint(1, 15))

    def eqit_clause(self, key):
        '''Checking if player stopped the game
        '''
        if key == ord('q'):          
            self.game_is_on = False

    def breed_a_children(self, parent):
        '''
        Function for getting the best brain from last generation, mutate it and
        prepere fror snakes children.
        Crossover function crosses two matrices randomly (chance for every value
        is 50%).
        Then the mutation is applied with chance equal to mutate rate
        '''
        child =  NeuralNetwork(
            inp_nodes = parent.inp_nodes, 
            hid_nodes = parent.hid_nodes, 
            out_nodes = parent.out_nodes
            )
        child.weigths_input = crossover(child.weigths_input, parent.weigths_input)
        child.weights_hidden = crossover(child.weights_hidden, parent.weights_hidden)
        child.weigths_output = crossover(child.weigths_output, parent.weigths_output)

        child.weigths_input = mutate(MUTATION_RATE, child.weigths_input)
        child.weights_hidden = mutate(MUTATION_RATE, child.weights_hidden)
        child.weigths_output = mutate(MUTATION_RATE, child.weigths_output)

        return child

    def new_snake(self, new_brain):
        '''
        Function for creating new snakes with random brain
        '''
        return Snake(st_coords = (winy//2, winx//2),
                    direction = random.choice(list(turn_dict.values())),
                    screen = screen,
                    color = self.random_color(),
                    brain = new_brain)

    def is_generation_over(self):
        '''Checks if there is only one (and the best) snake on board
        '''
        return len(self.cpus)==1

    def first_generation(self):
        '''Function creating first generation of snakes
        '''
        for i in range(self.snake_family):            
            self.cpus.append(self.new_snake(NeuralNetwork(8, 8, 4)))

    def new_generation(self):
        '''Function creating next generation of snakes
        '''
        parent = self.cpus.pop()                      #emping cpus list
        new_brain = parent.brain                      #taking its brain out
        
        for i in range(self.snake_family):             
            mutated_new_brain = self.breed_a_children(new_brain)
            self.cpus.append(self.new_snake(mutated_new_brain))

    def new_game(self, stdscr):        
        '''All setups for game
        '''        
        self.curses_initialize()                      #curses nessesceties                                                        
        self.level = GameBoard(screen)                #making gameboard
        self.level.initialize(stdscr)                 #gameboard nesseseties
        self.morsel = Apple(screen, 
                        color = self.random_color())  #creating apple class                
        self.first_generation()                       #making first snake generation
        self.morsel.generate((28,28))                 #placing first apple        

    def game(self, stdscr):
        ''' Actual game
        '''
        
        stdscr = curses.initscr()                     #let the game begin!        
        self.new_game(stdscr)                         #setup for first generation etc       
      
        #game loop
        while self.game_is_on:                        #main while loop
            
            #IS FUN OVER?           
            if self.is_generation_over():             #checking if board has its winner
                self.level.unprint(self.cpus[0])      #erasing the winner
                self.new_generation()                 #winner is having a child
                self.generation += 1                  #couting the generations

            #PLAYER CONTROL SECTION
            pressed_key = self.level.board.getch()    #getting key from player           
            self.eqit_clause(pressed_key)             #just quit if you want            

            #CPUs SECTIONS
            for cpu in self.cpus:
                self.level.unprint(cpu)               #erasing all snakes
                
                cpu.move()                            #generating moves

                if cpu.is_colliding_with_wall():      #collision checking
                    self.cpus.remove(cpu)             #if so - we erase it

                if cpu.is_colliding_with_itself():    #collision checking
                    self.cpus.remove(cpu)             #if so - we erase it                    
                
                if cpu.eats(self.morsel):             #snake eats an apple
                    pass                              #temporarly disabled

            #SCREEN SECTION                           #printing everything out
            for cpu in self.cpus:                     #printing every snake 
                self.level.inprint(cpu)

            self.level.print_apple(self.morsel)       #apple is printed on board            
            self.level.print_gen(self.generation)     #printing score on board            
            self.level.board.refresh()                #refreshing the screen
            
            
    def main(self):
        curses.wrapper(self.game)

game = Game()
game.main()
