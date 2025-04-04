import pygame as pg
from shapes import *

current_color = [255, 255, 255]

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
            return True
        return False

def set_current_shape(new_shape = None):
    global current_shape
    current_shape = new_shape

class shape_button(button):
    def __init__(self, figure, position, transform, key_btn=None):
        global current_color
        super().__init__(figure, position, transform, (255, 255, 255), (50, 50, 50), 1, key_btn, current_color, (lambda:set_current_shape(figure)))

def update_buttons(sc, buttons:list[button]):
    mp = complex(*pg.mouse.get_pos())
    for b in buttons:
        b.draw(sc, mp)

screensize = [1000, 1000]
player_position = complex(*screensize)/2

variations = [shapes.circle(100), shapes.triangle_v, shapes.square, shapes.star, shapes.rhombus, shapes.right_triangle]

button_size = 10
chouse_buttons = [
    shape_button(v, 5 + button_size + 2*button_size*n + screensize[1]*1j - button_size*1.1j, button_size) for n, v in enumerate(variations)
]
    

def negative(color):
    return [255 - c for c in color]

def draw_shape(surf, color, current_shape, pos1, pos2, mode, fill):
    if mode == 0:
        r = normalize(max(current_shape, key=lambda x:abs(x)))
        args = surf, color, current_shape, pos1, (pos2 - pos1) / r
    elif mode == 1:
        f, t = get_box(current_shape)
        size_x, size_y = ctt(t - f)
        to_x, to_y = ctt(pos2 - pos1)
        s = transform_f(current_shape, 1, f)
        s = transform_f(s, 1, 0, lambda x:stretch(x, -complex(to_x/size_x, to_y/size_y)))
        args = surf, color, s, pos1, 1
    if fill:
        draw(*args)
    else:
        draw(*args, w = 1)
current_shape = None

sc = pg.display.set_mode(screensize)
canvas = pg.surface.Surface(screensize)

show_chouse_menu = False
fill_shapes = False
mouse = lambda:complex(*pg.mouse.get_pos())
shape_rotation = 0
positions = []
bg_color = [0, 0, 0]
draw_mode = 1
cursor = mouse()
prev_mouse_position = 0

def set_current_color(r, g, b):
    global current_color
    current_color[0] = r
    current_color[1] = g
    current_color[2] = b
smooth = 0.005
while True:
    sc.fill(bg_color)
    sc.blit(canvas, (0, 0))

    if show_chouse_menu:
        update_buttons(sc, chouse_buttons)

    events = pg.event.get()
    for ev in events:
        match ev.type:
            case pg.QUIT:
                pg.quit()
                quit()
            case pg.MOUSEBUTTONDOWN:
                cursor = mouse()
                if ev.button == 1:
                    if show_chouse_menu:
                        mp = mouse()
                        if any(b.process(sc, mp, True) for b in chouse_buttons):
                            show_chouse_menu = False
                
                    elif not(current_shape is None):
                        positions = []
                        if len(positions) == 0:
                            positions.append(mouse())
                
            case pg.MOUSEBUTTONUP:
                if ev.button == 1:
                    if len(positions) == 1:
                        positions.append(mouse())
                        draw_shape(canvas, current_color, current_shape, positions[0], positions[1], draw_mode, fill_shapes)

            case pg.KEYDOWN:
                if ev.key == pg.K_h or (show_chouse_menu and ev.key == pg.K_ESCAPE):
                    show_chouse_menu = not show_chouse_menu
                if ev.key == pg.K_f:
                    fill_shapes = not fill_shapes
                if ev.key == pg.K_m:
                    draw_mode = 1 - draw_mode
                
                if ev.key == pg.K_r:
                    set_current_color(255, 0, 0)
                elif ev.key == pg.K_g:
                    set_current_color(0, 255, 0)
                elif ev.key == pg.K_b:
                    set_current_color(0, 0, 255)
                if ev.key == pg.K_w:
                    set_current_color(255, 255, 255)

    if pg.mouse.get_pressed()[2]:
        current_shape = None
        for _ in range(5):
            cursor += (mouse() - cursor)*smooth
            pg.draw.circle(canvas, bg_color, ctt(cursor), 10)
    else:
        if current_shape is None:
            if pg.mouse.get_pressed()[0]:
                for _ in range(5):
                    cursor += (mouse() - cursor)*smooth
                    pg.draw.circle(canvas, current_color, ctt(cursor), 10)

        else:
            s = 5
            draw(sc, current_color, current_shape, mouse() + 5*s*get_box(current_shape)[1], s)
            draw(sc, negative(current_color), current_shape, mouse() + 5*s*get_box(current_shape)[1], s, 2)
            if len(positions) == 1:
                draw_shape(sc, current_color, current_shape, positions[0], mouse(), draw_mode, fill_shapes)
            

    pg.display.update()
    prev_mouse_position = mouse()