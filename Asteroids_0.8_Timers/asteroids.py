import sys

import random
import pygame
import time
from pygame.locals import *

from game import Game
from objects import Ship
from objects import Asteroid
from objects import Bullet
from objects import Star
from objects import Debris


class Asteroids(Game):

    def __init__(self, name, width, height):
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
        self.score = 0 # Possible score variable


    def handle_input(self):
        super().handle_input()
        pygame.key.set_repeat(0, 100)
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_LEFT] and self.ship:
            self.ship.rotate(-3)
        if keys_pressed[K_RIGHT] and self.ship:
            self.ship.rotate(3)
        if keys_pressed[K_UP] and self.ship:
            self.ship.accelerate(0.05)
        if keys_pressed[K_DOWN] and self.ship:
            self.ship.accelerate(0) #TODO: Set to (0) to stop the ship instantly with down-key AKA EASYMODE.
        if keys_pressed[K_SPACE] and self.ship:
            if time.time() - self.ship.shot_timer > self.ship.shot_delay:      #Limits the rate of fire. Cannot fire more often than shot_delay value
                self.ship.shot_timer = time.time()                        #if it shoots, saves last fired timestamp
                self.ship.spawnProtection = False                   #removes Spawn protection if bullet is fired
                if len(self.bullets) >= 15:                         #Does not allow more than 15 bullets in total. deletes the oldest if more than 15.
                    del self.bullets[0]
                    self.bullets.append(Bullet(self.ship.position.copy(), self.ship.rotation, self.ship.shot_timer))      #Spawns a bullet with ships location. rotation and timestamp when fired.
                else:
                    self.bullets.append(Bullet(self.ship.position.copy(), self.ship.rotation, self.ship.shot_timer))
        if keys_pressed[K_f] and self.ship:
            self.asteroids.append(Asteroid(random.randrange(0, self.width, 5), random.randrange(0, self.height, 5)))        #Command for spawning more asteroids
        if keys_pressed[K_t] and self.ship:
            if time.time() - self.ship.jump_timer > self.ship.jump_delay:           #Checks if jumpdrive is on cooldown
                self.ship.jump_timer = time.time()        #Saves timestamp for jump
                self.ship.jumpDrive()                        #Jumps the ship




    def update_simulation(self):
        """
        update_simulation() causes all objects in the game to update themselves
        """
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
        """
        render_objects() causes all objects in the game to draw themselves onto the screen
        """
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


    def handle_collisions(self):
        if self.ship:
            for asteroid in self.asteroids:
                if asteroid.collide(self.ship) and self.ship.spawnProtection == False and self.ship.jumpProtection == False:        #Checks if player is protected when colliding
                    self.ship.lives =- 1                #NOT WORKING YET, Player has 3 lives. Plan is to do remove a life and gain 2-3 seconds immunity when losing a life.
                    if self.ship.lives < 0:             #If no more lives yet, > player dead
                        self.death_screen()
                    elif self.ship.lives > 1:
                        self.ship.spawnProtection = True
                        self.ship.spawnProtectionTime = time.time()

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
        game = Asteroids("Asteroids", self.width, self.height)
        label = self.myfont.render("Lives:"+str(self.ship.lives), 1, (255, 255, 255))
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
        game.runGame()





