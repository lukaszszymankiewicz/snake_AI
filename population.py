#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import section
import random

from matrices import crossover, mutate
from net import NeuralNetwork
from snake import Snake

class Population(object):
    '''
    Class containing whole snake game.  Actual game loop is put into
    game(self, stdscr) function.
    '''
    def __init__(self, population_size, mutation_rate, crossover_rate, screen):
        
        self.generation = 0                           
        self.population_size = population_size        
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.screen_size = screen
        self.starting_point = (screen[1]//2, screen[0]//2)
        self.cpus = []
        self.direction = [(1,0), (-1,0), (0,-1), (0,1)] 

    def reproduce(self, parent):
        '''
        Function for getting the best brain from last generation, mutate it and
        prepere for snakes children.
        Crossover function crosses two matrices randomly (chance for every value
        is 50%).
        Then the mutation is applied with chance equal to mutate rate
        '''
        child =  NeuralNetwork(
            inp_nodes = parent.inp_nodes, 
            hid_nodes = parent.hid_nodes, 
            out_nodes = parent.out_nodes
            )
        
        child.weigths_input = crossover(child.weigths_input, parent.weigths_input, self.crossover_rate)
        child.weights_hidden = crossover(child.weights_hidden, parent.weights_hidden, self.crossover_rate)
        child.weigths_output = crossover(child.weigths_output, parent.weigths_output, self.crossover_rate)
        
        #no crossover
        #child.weigths_input = parent.weigths_input[:]
        #child.weights_hidden = parent.weights_hidden[:]
        #child.weigths_output = parent.weigths_output[:]

        child.weigths_input = mutate(self.mutation_rate, child.weigths_input)
        child.weights_hidden = mutate(self.mutation_rate, child.weights_hidden)
        child.weigths_output = mutate(self.mutation_rate, child.weigths_output)

        return child

    def new_snake(self, new_brain):
        '''
        Function for creating new snakes with random brain
        '''
        return Snake(st_coords = (self.starting_point),
                    direction = random.choice(self.direction),
                    screen = self.screen_size,
                    brain = new_brain)

    def empty(self):
        '''Checks if there is only one (and the best) snake on board
        '''
        return len(self.cpus) == 1

    def first_generation(self):
        '''Function creating first generation of snakes
        '''
        self.cpus = []
        for i in range(self.population_size):            
            self.cpus.append((self.new_snake(NeuralNetwork(24, 8, 4))))

    def new_generation(self):
        '''Function creating next generation of snakes
        '''
        self.generation +=1

        parent = self.cpus.pop()                      #emtping cpus list
        #parent.brain.save_to_file(filename = str(self.generation))
        for i in range(self.population_size):             
            new_brain = self.reproduce(parent.brain)
            self.cpus.append(self.new_snake(new_brain))

