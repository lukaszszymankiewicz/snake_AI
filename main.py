#!/usr/bin/env python
# -*- coding: utf-8 -*-

from game import Game

#parameters
window_heigth = 28 
window_width = 28
population_rate = 20
mutation_rate = 15                                     
crossover_rate = 10 

game = Game(window_heigth, window_width, population_rate, mutation_rate, crossover_rate)
game.main()
