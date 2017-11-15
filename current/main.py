
from asteroids import Asteroids
from threading import Thread
from radiocoms import inputScanner

# Create an object for managing the game

game = Asteroids("Asteroids", 600, 400, 3, 0)
# Start the main game loop
game.runGame()







