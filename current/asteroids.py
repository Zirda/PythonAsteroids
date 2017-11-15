import sys

import random
import pygame
import time
from threading import Thread
from pygame.locals import *
from radiocoms import inputScanner
from game import Game
from objects import Ship
from objects import Asteroid
from objects import Bullet
from objects import Star
from objects import Debris


class Asteroids(Game):

    def __init__(self, name, width, height, lives, score):
        super().__init__( name, width, height )
        self.width = width
        self.height = height
        self.ship = Ship(width, height)  # Creates a ship
        self.asteroids=[]   # A list of all asteroids
        for i in range(5):                  # Change for different amount of Asteroids
            self.asteroids.append(Asteroid(random.randrange(0, width, 5),random.randrange(0, height, 5)))
        self.stars=[]       # A list of all background stars
        for i in range(25):                # Change for different amount of background Stars
            self.stars.append(Star())
        self.bullets = []   # A list of all bullets
        self.score = score # Possible score variable
        self.lives = lives

        self.currentRotation = 0            #Saves current location as RF value to reduce the amount of data sent
        self.rotationRange = (10000, 11000, 12000, 13000, 14000, 15000, 16000)  #All possible rotationvalues, Used to check if input is rotation or not
        self.rotateCheck = False

        self.ship.spawnProtection = True            #Sets up the player for first spawn when the game starts
        self.ship.spawnProtectionTime = time.time()
        self.activeInput = []

    def handle_input(self):
        super().handle_input()
        self.rotateCheck = False        #Resets the counter if the model has updated the rotation this call

        if (self.sniffer.isLocked != True):
            self.sniffer.isLocked = True
            self.activeInput = self.sniffer.inputList
            self.sniffer.isLocked = False

            if (len(self.activeInput) > 0):
                while (len(self.activeInput) > 0):
                    x = 0
                    if self.activeInput[x] in self.rotationRange and self.currentRotation != self.activeInput[x]:   #Checks if it is a rotation input and isn't the current rotation
                        self.ship.adjustedRotation(self.activeInput[x])       #Updates rotation
                        self.currentRotation = self.activeInput[x]            #Saves new rotation as current
                        self.rotateCheck = True                                     #Saves that the ship has rotated with a new value this update
                    if self.activeInput[x] == 1000 and self.ship:
                        self.ship.MovingForward = True                          #Since RF refresh rate is lower we need to save moving forward as a boolian and send start/stop
                    if self.activeInput[x] == 2000 and self.ship:
                        self.ship.MovingForward = False
                    if self.activeInput[x] == 3000 and self.ship:
                        self.ship.MovingForward = False                         #Stop function, Safety catch to set moving forward as false if RF signals are lost
                        self.ship.accelerate(0)
                    if self.activeInput[x] == 4000 and self.ship:
                        if time.time() - self.ship.shot_timer > self.ship.shot_delay:  # Limits the rate of fire. Cannot fire more often than shot_delay value
                            self.ship.shot_timer = time.time()  # if it shoots, saves last fired timestamp
                            self.ship.spawnProtection = False  # removes Spawn protection if bullet is fired
                            if len(self.bullets) >= 15:  # Does not allow more than 15 bullets in total. deletes the oldest if more than 15.
                                del self.bullets[0]
                                self.bullets.append(Bullet(self.ship.position.copy(), self.ship.rotation, self.ship.shot_timer))  # Spawns a bullet with ships location. rotation and timestamp when fired.
                            else:
                                self.bullets.append(Bullet(self.ship.position.copy(), self.ship.rotation, self.ship.shot_timer))

                    if self.activeInput[x] == 5000 and self.ship:
                        if time.time() - self.ship.jump_timer > self.ship.jump_delay:  # Checks if jumpdrive is on cooldown
                            self.ship.jump_timer = time.time()  # Saves timestamp for jump
                            self.ship.jumpDrive()  # Jumps the ship

                    self.activeInput.pop(self.activeInput.index(x))     #Removes current command from the list


        #These two are outside the loop around the command list, so if there is multiple conflicting commands only one will act during one single update.
        if self.rotateCheck == False:                               #If the ship has not received a new rotation command, use the previous one
            self.ship.adjustedRotation(self.currentRotation)
        if self.ship.MovingForward == True:                        #If the ship is commanded to move forward, move it.
            self.ship.accelerate(0.05)

        #if keys_pressed[K_f] and self.ship:
         #   self.asteroids.append(Asteroid(random.randrange(0, self.width, 5), random.randrange(0, self.height, 5)))        #Command for spawning more asteroids
        #if keys_pressed[K_t] and self.ship:


    def update_simulation(self):

        super().update_simulation()
        currentTime = time.time()           #Saves current timestamp for the update

        if self.ship:
            self.ship.update( self.width, self.height, self.dt )
        for asteroid in self.asteroids:
            asteroid.update( self.width, self.height, self.dt )
        for star in self.stars:
            star.update( self.width, self.height, self.dt )
        for bullet in self.bullets:
            bullet.update( self.width, self.height, self.dt )
            if bullet.time + 2 < currentTime:                       #Deletes bullets that is older than 2 seconds
                self.bullets.pop(self.bullets.index(bullet))
        if self.ship.jump_timer + self.ship.jumpProtectionDuration < currentTime:           #Checks if jump protection is still active. if not, remove it
            self.ship.jumpProtection = False
        if self.ship.spawnProtectionTime + self.ship.spawnProtectionDuration < currentTime:
            self.ship.spawnProtection = False                                                   #Checks if spawn protection is still active. if not, remove it
        self.handle_collisions()

    def render_objects(self):

        super().render_objects()
        # Render the ship:
        if self.ship:
            self.ship.draw( self.screen )
        # Render all the stars, if any:
        for star in self.stars:
            star.draw( self.screen )
        # Render all the asteroids, if any:
        for asteroid in self.asteroids:
            asteroid.draw( self.screen )
        # Render all the bullet, if any:
        for bullet in self.bullets:
            bullet.draw( self.screen )
        label = self.smallfont.render("Lives:" + str(self.lives), 1, (255, 255, 255))
        score = self.smallfont.render("Score:" + str(self.score), 1, (255, 255, 255))
        self.screen.blit(label, (1,1))
        self.screen.blit(score, (self.width - 150, 1))

    def handle_collisions(self):
        if self.ship:
            for asteroid in self.asteroids:
                if asteroid.collide(self.ship) and self.ship.spawnProtection == False and self.ship.jumpProtection == False:        #Checks if player is protected when colliding
                    self.lives -= 1
                    if self.lives <= 0:  # If no more lives yet, > player dead
                        self.game_over()
                        break
                    else:
                        self.death_screen()

                for bullet in self.bullets:
                    if asteroid.contains(bullet.position):
                        self.score += 10
                        self.bullets.pop(self.bullets.index(bullet))
                        self.asteroids.pop(self.asteroids.index(asteroid))
                        if asteroid.health >= 2:
                            self.asteroids.append(Debris(asteroid.position.copy()))
                            self.asteroids.append(Debris(asteroid.position.copy()))
                            self.asteroids.append(Debris(asteroid.position.copy()))
                            self.asteroids.append(Debris(asteroid.position.copy()))
               #if asteroid.collide(self.asteroids):


    def death_screen(self):
        game = Asteroids("Asteroids", self.width, self.height, self.lives, self.score)
        label = self.myfont.render("Lives:"+str(self.lives), 1, (255, 255, 255))
        label2 = self.myfont.render("You Died!", 1, (255, 255, 255))
        score = self.smallfont.render("Score:" + str(self.score), 1, (255, 255, 255))
        self.screen.blit(label, (self.width * 0.30, self.height * 0.35))
        self.screen.blit(label2, (self.width * 0.35, self.height * 0.40))
        self.screen.blit(score, (self.width * 0.4, self.height * 0.5))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.time.wait(500)
        for asteroids in self.asteroids:
            self.asteroids.pop(self.asteroids.index(asteroids))
        for bullet in self.bullets:
            self.bullets.pop(self.bullets.index(bullet))
        for x in self.sniffer.inputList:
            self.sniffer.inputList.pop(self.sniffer.inputList.index(x))
        game.runGame()

    def game_over(self):
        game = Asteroids("Asteroids", self.width, self.height, 3, 0)
        label2 = self.myfont.render("GAME OVER!", 1, (255, 255, 255))
        score = self.smallfont.render("Score:" + str(self.score), 1, (255, 255, 255))
        self.screen.blit(label2, (self.width * 0.35, self.height * 0.40))
        self.screen.blit(score, (self.width * 0.4, self.height * 0.5))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.time.wait(500)
        for asteroids in self.asteroids:
            self.asteroids.pop(self.asteroids.index(asteroids))
        for bullet in self.bullets:
            self.bullets.pop(self.bullets.index(bullet))
        for x in self.sniffer.inputList:
            self.sniffer.inputList.pop(self.sniffer.inputList.index(x))
        game.runGame()


