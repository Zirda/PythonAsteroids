import sys

import random
import pygame
from pygame.locals import *

from game import Game
from objects import Ship
from objects import Asteroid
from objects import Bullet
from objects import Star

class Asteroids( Game ):
    """
    Asteroids extends the base class Game to provide logic for the specifics of the game
    """
    def __init__(self, name, width, height):
        super().__init__( name, width, height )
        # TODO: should create a Ship object here
        self.ship = Ship() # None
        # TODO: should create asteroids
        self.asteroids=[]
        for i in range(8):                  # Change for different amount of Asteroids
            self.asteroids.append(Asteroid())
        self.stars=[]
        for i in range(250):                # Change for different amount of background Stars
            self.stars.append(Star())
        # TODO: should create bullets
        self.bullets = []

    def handle_input(self):
        super().handle_input()
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_LEFT] and self.ship:
            self.ship.rotate(-0.5)
        if keys_pressed[K_RIGHT] and self.ship:
            self.ship.rotate(0.5)
        if keys_pressed[K_UP] and self.ship:
            self.ship.accelerate(0.005)
        if keys_pressed[K_DOWN] and self.ship:
            self.ship.accelerate(0) #TODO: Set to (0) to stop the ship instantly with down-key AKA EASYMODE.
            pass
        if keys_pressed[K_SPACE] and self.ship:
            if len(self.bullets) < 10:
                self.bullets.append(Bullet(self.ship.position,self.ship.rotation))
            elif len(self.bullets) >= 10:
                del self.bullets[0]
                self.bullets.append(Bullet(self.ship.position, self.ship.rotation))
                # TODO: should create a bullet when the user fires



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
        for bullets in self.bullets:
            bullets.update( self.width, self.height)
        # TODO: should probably work out how to remove a bullet when it gets old
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
                    self.running = False
                for bullet in self.bullets:
                    if asteroid.contains(bullet.position):
                        self.bullets.pop(self.bullets.index(bullet))
                        self.asteroids.pop(self.asteroids.index(asteroid))
"""
        handle_collisions() should check:
            - if our ship has crashed into an asteroid (the ship gets destroyed - game over!)
            - if a bullet has hit an asteroid (the asteroid gets destroyed)
        :return:
"""
        # TODO: implement collission detection,
        #       using the collission detection methods in all of the shapes

