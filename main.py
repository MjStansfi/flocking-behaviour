# -*- coding: utf-8 -*-
"""
Flocking behaviour
 - Seperation
 - Cohesion
 - Alignment
@author: Mjs
"""

import pygame, os, random, glob
from PIL import Image

size = width, height = 800,700
speed = [2,2]
black = 0,0,0
white = 255,255,255
red = 255,0,0

#Define a bird with the key properties
class bird(pygame.sprite.Sprite):
    
    def __init__(self, startpos, startdir, speed):
        self.pos = pygame.math.Vector2(startpos)
        self.dir = pygame.math.Vector2(startdir).normalize()     
        self.speed = speed  
        self.maxspeed = 3
        self.vel = self.dir * random.randint(2,4)
        self.accl = pygame.math.Vector2()

        
    def flock(self,boids):
        
        self.accl+=self.align(boids)
        self.accl+=self.separate(boids)
        self.accl+=self.cohesion(boids)
        
    def update(self):
        self.pos+=self.vel
        self.vel+= self.accl
        
        if(self.vel!=(0,0)):
            self.vel = self.vel.normalize() * self.maxspeed
            
        self.accl = self.accl*0
            
    def align(self, boid):
        vision = 100
        self.near = 0
        self.avg = pygame.math.Vector2()
        for i in boid:
            d = self.pos.distance_to(i.pos)
            if(self != i and d < vision):
                self.avg+=i.vel
                self.near+=1
        if(self.near>0):            
            self.avg = self.avg/self.near
            
            if(self.avg!=(0,0)):
                self.avg = self.avg.normalize() * self.maxspeed

        return self.avg
    
    def cohesion(self,boid):
        vision = 100
        self.near = 0
        self.coh = pygame.math.Vector2()
        for i in boid:
            d = self.pos.distance_to(i.pos)
            if(self != i and d < vision):
                self.coh+=i.pos
                self.near+=1
                
        if(self.near>0):           
            self.coh = self.coh/self.near
            self.coh-=self.pos
            if(self.coh!=(0,0)):
                self.coh = self.coh.normalize() * self.maxspeed
                #self.coh-=self.vel

        return self.coh   
    
    def separate(self,boid):
        vision = 80
        self.near = 0
        self.sep = pygame.math.Vector2()
        for i in boid:
            d = self.pos.distance_to(i.pos)
            if(self != i and d < vision):
                self.dist = self.pos - i.pos
                self.sep += self.dist / (d*d)
                self.near+=1
                
        if(self.near>0):           
            self.sep = self.sep/self.near
           # self.avg = self.avg - self.pos
            if(self.sep!=(0,0)):
                self.sep = self.sep.normalize() * self.maxspeed 
                #self.sep-=self.vel

        return self.sep  
    
    def stats(self):
        #print("Vel:",self.vel)
        #print("Pos:",self.pos,"\n")
        #print("Mag:", self.vel.magnitude(),'\n')
        print("Near:", self.near,'\n')
        print("avg:", self.avg,'\n')
        
    def bounds(self):
        if(self.pos.x>width):
            self.pos.x =0
            
        if(self.pos.x<0):
            self.pos.x =width
            
        if(self.pos.y<0):
            self.pos.y =height
            
        if(self.pos.y>height):
            self.pos.y =0

#Generate flock of birds
flock = []
for i in range(0,100):
    flock.append(bird(startpos = (random.randint(0,width),
                                       random.randint(0,height)),
                           startdir = (random.uniform(-1, 1),random.uniform(-1, 1)),
                           speed = 0.2))

    
    

    
pygame.init()
screen = pygame.display.set_mode(size)

active = True
steps=0
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
    screen.fill(black)  
    
    for bird in flock:
        
        bird.bounds()
        bird.flock(flock)
        bird.update()
        
        if bird == flock[0]:
            pygame.draw.circle(screen,red,(bird.pos.x,bird.pos.y),4)
            #bird.stats()
        else:
            pygame.draw.circle(screen,white,(bird.pos.x,bird.pos.y),4)
        
      
    
    pygame.display.update()
    #steps+=1
    #pygame.image.save(screen, "pngs/pic" + str(steps).zfill(5) + ".png")