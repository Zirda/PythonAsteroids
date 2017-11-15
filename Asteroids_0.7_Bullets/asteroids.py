import sys

import random
import pygame
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
        self.ship = Ship()  # Creates a ship
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
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_LEFT] and self.ship:
            self.ship.rotate(-1)
        if keys_pressed[K_RIGHT] and self.ship:
            self.ship.rotate(1)
        if keys_pressed[K_UP] and self.ship:
            self.ship.accelerate(0.05)
        if keys_pressed[K_DOWN] and self.ship:
            self.ship.accelerate(0) #TODO: Set to (0) to stop the ship instantly with down-key AKA EASYMODE.
        if keys_pressed[K_SPACE] and self.ship:
            # makes it possible to only fire one bullet every n=5 frame
            if len(self.bullets) > 0 and self.frame - self.bullets[len(self.bullets) - 1].ttl < 50:
                pass
            else:
                self.bullets.append(Bullet(self.ship.position, self.ship.rotation, self.frame))
            pass

    def update_simulation(self):
        """
        update_simulation() causes all objects in the game to update themselves
        """
        super().update_simulation()

        if self.ship:
            self.ship.update( self.width, self.height )
        for asteroid in self.asteroids:
            asteroid.update( self.width, self.height )
        for star in self.stars:
            star.update( self.width, self.height )
        for bullet in self.bullets:
            bullet.update( self.width, self.height )
            if bullet.ttl < self.frame:
                self.bullets.pop(self.bullets.index(bullet))
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
                if asteroid.collide(self.ship):
                    self.death_screen()
                for bullet in self.bullets:
                    if asteroid.contains(bullet.position):
                        self.score += 10
                        self.bullets.pop(self.bullets.index(bullet))
                        self.asteroids.pop(self.asteroids.index(asteroid))
                        if asteroid.health >= 2:
                            self.asteroids.append(Debris(asteroid.position))
                            self.asteroids.append(Debris(asteroid.position))
                            self.asteroids.append(Debris(asteroid.position))
                            self.asteroids.append(Debris(asteroid.position))


    def death_screen(self):
        game = Asteroids("Asteroids", 640, 480)
        label = self.myfont.render("Bitch Please!", 1, (8, 8, 8))
        label2 = self.myfont.render("You Died!", 1, (255, 255, 255))
        score = self.smallfont.render("Score:" + str(self.score), 1, (255, 255, 255))
        self.screen.blit(label, (self.width * 0.30, self.height * 0.35))
        self.screen.blit(label2, (self.width * 0.35, self.height * 0.40))
        self.screen.blit(score, (self.width * 0.4, self.height * 0.5))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.time.wait(500)
        game.runGame()





