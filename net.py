#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from copy import deepcopy
from matrices import randomize, sigmoid, add_bias

class NeuralNetwork:
    def __init__(self, inp_nodes, hid_nodes, out_nodes):
       '''
       self.inp_nodes - number of input nodes. Right now - 24
       self.hid_nodes - number of hidden layer nodes. Right now - 12
       self.out_nodes - number of output nodes. Right now - 4. It symbolize
       the direction in where snake can go.
       
       self.weigths_input - matrix with input layer weigths
       self.weights_hidden - matrix with hidden layer weigths
       self.weigths_output - matrix with output layer weigths

       Three matrices above is randomized at first. Values ranges
       from -1 to 1.
       '''

       self.inp_nodes = inp_nodes              
       self.hid_nodes = hid_nodes              
       self.out_nodes = out_nodes              
       self.weigths_input = randomize(hid_nodes, inp_nodes)
       self.weights_hidden = randomize(hid_nodes, hid_nodes)
       self.weigths_output = randomize(out_nodes, hid_nodes)

    def output(self, input):
        '''Generating neural net output
        TO DO: OPTIMIZE!
        '''
        #level one
        #add bias
        input_biased = add_bias(np.array(input))

        #apply weights
        hidden_inputs = np.dot(self.weigths_input, input_biased)
        
        #pass through sigmoid
        hidden_output = sigmoid(hidden_inputs)
        

        #level two
        #add bias
        hidden_output_biased = add_bias(hidden_output)

        #apply weights
        hidden_input2 = np.dot(self.weights_hidden, hidden_output_biased)
        
        #pass through sigmoid
        hidden_output2 = sigmoid(hidden_input2)
        
        
        #level three
        #add bias
        hidden_output2_biased = add_bias(hidden_output2)

        #apply weights
        output_inputs = np.dot(self.weigths_output, hidden_output2_biased)

        #pass through sigmoid
        outputs = sigmoid(output_inputs)

        return list(outputs)

    def save_to_file(self, filename):
        '''Unused
        '''
        name = 'weigths_input.txt'
        file = open(name ,'a')        
        file.write(str(self.weigths_input))
        file.close

        name = 'weights_hidden.txt'
        file = open(name,'a')        
        file.write(str(self.weights_hidden))
        file.close
        
        name = 'weigths_output.txt'
        file = open(name,'a')        
        file.write(str(self.weigths_output))
        file.close

    def read_from_file(self):
        '''As name suggests. TO DO.
        '''
        pass
