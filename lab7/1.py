from math import ceil, floor
from random import random
import time
import pygame as pg

pg.init()
clamp = lambda x, max_v, min_v: min(max(x, max_v), min_v)
screensize = (800, 800)
sc = pg.display.set_mode(screensize)

class clock_class:
    def __init__(self, scale = 0.5):
        self.min_hand = pg.image.load("images/min_hand.png")
        self.sec_hand = pg.image.load("images/sec_hand.png")
        self.clock = pg.image.load("images/clock.png")
        self.bias = self.clock.get_size()
        self.scale = scale

        self.bones = pg.mixer.Sound("music/hrust-kostey-perelom-33750.mp3")
        self.ouch = pg.mixer.Sound("music/minecraft-death-sound.mp3")
    
    def draw(self, surf:pg.Surface, mins, secs):
        if abs(floor(secs) - secs) < 0.01 and self.bones.get_num_channels() <= 4:
            self.bones.play()
        if abs(floor(secs) - mins) < 0.05 and self.ouch.get_num_channels() <= 4:
            self.ouch.play()
        secs = ((secs % 1)**0.5 + floor(secs))
        mins = ((mins % 1)**0.1 + floor(mins))
        m = pg.transform.rotozoom(self.min_hand, -(360*mins/60 + 45), self.scale)
        s = pg.transform.rotozoom(self.sec_hand, -(360*secs/60 - 60), self.scale)
        c = pg.transform.scale_by(self.clock, self.scale)
        surf.blit(c, (screensize[0]//2 - self.bias[0]*self.scale/2, screensize[1]//2 - self.bias[1]*self.scale/2))
        surf.blit(m, (screensize[0]//2 - m.get_size()[0]/2, screensize[1]//2 - m.get_size()[1]/2))
        surf.blit(s, (screensize[0]//2 - s.get_size()[0]/2, screensize[1]//2 - s.get_size()[1]/2))
        
clock = clock_class()

while True:
    sc.fill([255] * 3)
    events = pg.event.get()
    #sec, minutes = (t:= time.localtime()).tm_sec, t.tm_min
    t = time.time()
    sec, minutes = t % 60, (t / 60) % 60
    clock.draw(sc, minutes, sec)
    for ev in events:
        match ev.type:
            case pg.QUIT:
                pg.quit()
                quit()
    pg.display.update()
