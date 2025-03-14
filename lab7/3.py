import pygame as pg

clamp = lambda x, max_v, min_v: min(max(x, max_v), min_v)
screensize = (800, 800)
sc = pg.display.set_mode(screensize)


class ball:
    def __init__(self, pos=0j):
        self.pos = pos
        self.speed = 0j
        self.r = 25

    def draw(self):
        new_pos = self.pos + self.speed
        self.pos = (
            clamp(new_pos.real, self.r, screensize[0] - self.r)
            + clamp(new_pos.imag, self.r, screensize[1] - self.r) * 1j
        )
        pg.draw.circle(sc, (255, 0, 0), (self.pos.real, self.pos.imag), self.r)


b = ball(screensize[0] / 2 + 1j * screensize[1] / 2)
speed = 1
while True:
    sc.fill([255] * 3)
    events = pg.event.get()
    for ev in events:
        match ev.type:
            case pg.QUIT:
                pg.quit()
                quit()
            case pg.KEYDOWN:
                match ev.key:
                    case pg.K_LEFT:
                        b.speed -= speed
                    case pg.K_RIGHT:
                        b.speed += speed
                    case pg.K_DOWN:
                        b.speed += speed * 1j
                    case pg.K_UP:
                        b.speed -= speed * 1j
    b.draw()
    b.speed *= 0
    pg.display.update()
