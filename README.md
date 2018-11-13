# snake_AI
Game of snake in which animal is learning by strengthen up neural network and genetic algorithm.

Neural net is creaed from three layers of neurons (only one hidden layer). As input we take snake "vision" - 
a set of things around the snake in distance of two blocks (this will change, because by far animal does not
see apple or antyhing else).

To run program curses library is needes. Instalation process is shown below:
https://stackoverflow.com/a/41224335/9988003

Other library needed id numpy. Everything else is written by hand. 

To run, simply use 'python main.py' in terminal.

Files as follow:
apple - Aplle class and methods. Nothing realy interesting.

gameboard - Class for handling curses. Rather simple usage tho.

game - whole snake game

main - main part of script. The whole brain of program.

matrices - auxilary function for operation on matrices.

population - snake population class (populated with snake class instances)

net - Neural Net Class

snake - Class for Snake. Collision, moving, putting AI to go.
