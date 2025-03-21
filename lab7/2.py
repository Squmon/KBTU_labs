import pygame as pg
from pytools import shift

def ctt(z:complex): # complex to tuple
    return (z.real, z.imag)

def dot(a, b):
    return a.real*b.real + a.imag*b.imag

def normalize(z):
    return z/abs(z) if abs(z) > 0 else 0j

def transform_f(figure, transform, position = 0j, fnc = lambda x:x):
    return [fnc(transform*f + position) for f in figure]

def inside(figure:list[complex], point:complex):
    center = sum(figure)/len(figure)
    return all(map(lambda c: dot(d := 1j*normalize(c[0] - c[1]), point - center) < dot(d, c[0] - center), zip(figure, shift(figure, -1))))

triangle_v = tuple(normalize(1j**(i+1) + 0.5) for i in range(0, 3))
square = tuple(1j**0.5*normalize(1j**i) for i in range(0, 4))

def draw(surf, color, figure:tuple[complex], position, transform:complex = 1, w = 0):
    pg.draw.polygon(surf, color, transform_f(figure, transform, position, ctt), w)

class button:
    def __init__(self, figure, position, transform, color_outside, color_inside, frame_w = 0, key_btn = None, color_active = None, action = None):
        self.transoform = transform
        self.figure = figure
        self.pos = position
        self.color_outside = color_outside
        self.color_inside = color_inside
        self.frame_w = frame_w
        self.kb = key_btn
        self.ca = color_inside if color_active is None else color_active
        self.action = (lambda:print(self, "-> на меня нажали")) if action is None else action

    def draw(self, sc, mouse_position:complex):
        color = self.color_inside
        if inside(transform_f(self.figure, self.transoform), mouse_position - self.pos):
            color = self.ca
        draw(sc, color, self.figure, self.pos, self.transoform)
        if self.frame_w > 0:
            draw(sc, self.color_outside, self.figure, self.pos, self.transoform, self.frame_w)
    
    def process(self, sc, mouse_position:complex, pressed = False):
        if pressed and inside(transform_f(self.figure, self.transoform), mouse_position - self.pos):
            self.action()


def update_buttons(sc, buttons:list[button]):
    mp = complex(*pg.mouse.get_pos())
    for b in buttons:
        b.draw(sc, mp)

music = [
    "music/hrust-kostey-perelom-33750.mp3",
    "music/minecraft-death-sound.mp3",
    "music/Star Palace.mp3",
    "music/Tubling army.mp3"
]
pg.init()
current = 0
isPlay = 1
def play_pause_sound():
    global isPlay, pause_button
    if isPlay > 0:
        pg.mixer_music.pause()
        pause_button.figure = square
    else:
        pg.mixer_music.unpause()
        pause_button.figure = triangle_v
    isPlay *= -1

def next_music():
    global current, isPlay
    current = (current + 1) % len(music)
    pg.mixer_music.load(music[current])
    pg.mixer_music.play()
    isPlay = 1
    
def prev_music():
    global current, isPlay
    current = (current - 1) % len(music)
    pg.mixer_music.load(music[current])
    pg.mixer_music.play()
    isPlay = 1

screensize = [800, 400]
player_position = complex(*screensize)/2
buttons = [
    next_button := button(triangle_v, player_position + 200, -100, [0, 0, 0], [255, 255, 255], 10, color_active = [255, 255, 0], action=next_music),
    prev_button := button(triangle_v, player_position - 200, +100, [0, 0, 0], [255, 255, 255], 10, color_active = [255, 255, 0], action = prev_music),
    pause_button := button(square, player_position, 100, [0, 0, 0], [255, 255, 255], 10, color_active = [255, 255, 0], action= play_pause_sound),
]


sc = pg.display.set_mode(screensize)

while True:
    sc.fill([100] * 3)

    if isPlay > 0:
        pause_button.figure = square
    else:
        pause_button.figure = tuple(-v*0.5 for v in triangle_v)

    update_buttons(sc, buttons)

    events = pg.event.get()
    for ev in events:
        match ev.type:
            case pg.QUIT:
                pg.quit()
                quit()
            case pg.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    mp = complex(*pg.mouse.get_pos())
                    for b in buttons: b.process(sc, mp, True)
            case pg.KEYDOWN:
                if ev.key == pg.K_RIGHT:
                    next_music()
                if ev.key == pg.K_LEFT:
                    prev_music()
                if ev.key == pg.K_SPACE:
                    play_pause_sound()
    
    pg.display.update()