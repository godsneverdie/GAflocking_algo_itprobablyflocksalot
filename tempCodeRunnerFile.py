import pygame
import random
from math import sqrt
wb=1400
hb=800
boid_count=100
perception = 50
max_force=0.3
max_speed= 50 

class boid():
    def __init__(self,is_leader):
        self.pos=pygame.Vector2(random.uniform(0,wb), random.uniform(0,hb))
        self.vel=pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1))
        self.vel.scale_to_length(random.uniform(2,max_speed))
        self.acc=pygame.Vector2()
        self.is_leader=is_leader
        if is_leader:
            self.color=(225,0,0)
        else:
            self.color=(0,0,0)
    def edge(self):
        if self.pos.x>wb:
            self.pos.x = wb    
            self.vel.x *= -1
        elif self.pos.x<0:
            self.pos.x=0
            self.vel.x*=-1
        if self.pos.y>hb:
            self.pos.y = hb   
            self.vel.y *= -1    
        elif self.pos.y < 0:
            self.pos.y = 0       
            self.vel.y *= -1
    def apply_force(self,force):
        self.acc+=force
    def seek(self,target):
        des=target-self.pos
        if des.length()==0:
            return pygame.Vector2()
        des.scale_to_length(max_speed)
        steer=des-self.vel
        if steer.length()>max_force:
            steer.scale_to_length(max_force)
        return steer
    def flock(self, boid):
        sep=pygame.Vector2()
        ali=pygame.Vector2()
        coh=pygame.Vector2()
        cnt=0
        for o in boid:
            d=self.pos.distance_to(o.pos)# returns int
            if 0<d<perception:
                dif=self.pos-o.pos
                dif/=d
                sep+=dif
                ali+=o.vel
                coh+=o.pos
                cnt+=1
        if cnt>0:
            sep/=cnt
            ali/=cnt
            coh/=cnt
            steer_coh=self.seek(coh)

        if sep.length()>0:
            sep.scale_to_length(max_speed)
        steer_sep=sep-self.vel
        if steer_sep.length()>max_force:
            steer_sep.scale_to_length(max_force)
        
        if ali.length()>0:
            ali.scale_to_length(max_speed)
        steer_ali=ali-self.vel
        if steer_ali.length()>max_force:
            steer_ali.scale_to_length(max_force)

        self.apply_force(steer_sep*1.0)
        self.apply_force(steer_ali*1.0)
        self.apply_force(steer_coh*1.0)
    def update(self):
        self.vel+=self.acc  #this acc is made of all the forces look at apply_force()
        if self.vel.length()>max_speed:
            self.vel.scale_to_length(max_speed)
        self.pos+=self.vel
        self.acc*=0
    def draw(self,screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.pos.x), int(self.pos.y)), 3)
pygame.init()
screen=pygame.display.set_mode((wb,hb))
pygame.display.set_caption("CHASE")
clock=pygame.time.Clock()
lead=boid(is_leader=True)
follower=[boid(is_leader=False) for _ in range(boid_count-1)]
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running =False
    screen.fill((30,30,30))
    goal=pygame.mouse.get_pos()
    goal_force=lead.seek(goal)
    lead.apply_force(goal_force * 0.5)
    lead.edge()
    lead.update()
    lead.draw(screen)
    lead_pos=lead.pos
    for b in follower:
        b.flock(follower)
        lead_force=b.seek(lead_pos)
        b.apply_force(lead_force*1.0)
        b.edge()
        b.update()
        b.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
