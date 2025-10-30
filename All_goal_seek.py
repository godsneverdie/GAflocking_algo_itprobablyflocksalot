
import pygame
import random
from math import sqrt
WIDTH = 1400 #ur moms box
HEIGHT = 800
BOID_COUNT = 100
PERCEPTION = 30 #FOV of boid
MAX_FORCE = 0.3 #acceleration of boid its turning speed
MAX_SPEED = 8   #top-speed

class Boid:
    def __init__(self):
        self.pos = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))#random position vector during inint
        self.vel = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))#given random direction
        self.vel.scale_to_length(random.uniform(2, MAX_SPEED))#Move it
        self.acc = pygame.Vector2()

    # def edges(self):
    #     if self.pos.x > WIDTH:
    #         self.pos.x = 0            if you don't like walls
    #     elif self.pos.x < 0:
    #         self.pos.x = WIDTH
    #     if self.pos.y > HEIGHT:
    #         self.pos.y = 0
    #     elif self.pos.y < 0:
    #         self.pos.y = HEIGHT
    def edges(self):
        if self.pos.x > WIDTH:      #i like walls
            self.pos.x = WIDTH    
            self.vel.x *= -1   
        elif self.pos.x < 0:
            self.pos.x = 0        
            self.vel.x *= -1    
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT   
            self.vel.y *= -1    
        elif self.pos.y < 0:
            self.pos.y = 0       
            self.vel.y *= -1   

    def apply_force(self, force):   #change acceleration 
        self.acc += force

    def seek(self, target):     #Goal-seeking rule
        desired = target - self.pos #target is the goal
        if desired.length() == 0:
            return pygame.Vector2()
            
        desired.scale_to_length(MAX_SPEED)#go to new desired position
        steer = desired - self.vel  #gives the vector from vel to desired point
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def flock(self, boids):
        #initializing the three forces [star war pun or joke]
        sep = pygame.Vector2()  #seperation
        ali = pygame.Vector2()  #alignment
        coh = pygame.Vector2()  #cohession
        count = 0
        for other in boids:
            d = self.pos.distance_to(other.pos)#compare vectors to find distance between self and every other boid
            if 0 < d < PERCEPTION:          #assign neighbour under the perception levels
                diff = self.pos - other.pos #difference of pos vector
                diff /= d                   
                sep += diff                 #seperate by pointing away from neighbours pos
                ali += other.vel            #align with other neighbour by adding their velocity
                coh += other.pos            #move with the neighbours
                count += 1                  

        if count > 0:
            sep /= count                    #/`````\        \````
            ali /= count                    #\_____/  \   / / __
            coh /= count                    #/     \   \_/  \___\
        
            if sep.length() > 0:                    #if no neighbours, then cause divison by zero
                sep.scale_to_length(MAX_SPEED)      #move at max_speed            
            steer_sep = sep - self.vel              #finds the required  acceleretion
            if steer_sep.length() > MAX_FORCE:
                steer_sep.scale_to_length(MAX_FORCE)#capping required force to max 
            
            if ali.length() > 0:                    #same thing for alignment
                ali.scale_to_length(MAX_SPEED)
            steer_ali = ali - self.vel
            if steer_ali.length() > MAX_FORCE:
                steer_ali.scale_to_length(MAX_FORCE)

            steer_coh = self.seek(coh)              

            self.apply_force(steer_sep * 1.5)       #giving priority to seperation
            self.apply_force(steer_ali * 1.0)
            self.apply_force(steer_coh * 1.0)

    def update(self):                           # running for each frame updating variables
        self.vel += self.acc                    #update velocity with the acceleration
        if self.vel.length() > MAX_SPEED:       
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel                    #pos updated bsed on velocity of boid
        self.acc *= 0                           #changes acc to 0 for next calculation

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.pos.x), int(self.pos.y)), 3)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids Flocking")
clock = pygame.time.Clock()

flock = [Boid() for _ in range(BOID_COUNT)] #initiats constructor

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:           #erase previous frames
            running = False

    screen.fill((30, 30, 30))

    goal = pygame.mouse.get_pos()              #get the goal as the mouse pointer position 

    for boid in flock:                         #for each boid made 
        boid.flock(flock)                      #calculate the forces
        goal_force = boid.seek(goal)           #goal-seeking rule
        boid.apply_force(goal_force * 0.5)     #apply force for goal seek
        boid.edges()                           #detects edge of window 
        boid.update()                          #apply all forces
        boid.draw(screen)                      #fkn draw

    pygame.display.flip()                      #updating frames
    clock.tick(60)                              

pygame.quit()                                  #Never Quit