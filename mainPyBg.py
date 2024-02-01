from datetime import datetime
import pygame as pg
import random
import math

vec2, vec3 = pg.math.Vector2, pg.math.Vector3

RES = WIDTH, HEIGHT = 1200, 800
NUM_STARS = 1500
CENTER = vec2(WIDTH // 2, HEIGHT // 2)
COLORS = 'red green blue orange purple cyan'.split()
Z_DISTANCE = 40
ALPHA = 120

H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2
RADIUS = H_HEIGHT - 50
radius_list = {'sec': RADIUS - 10, 'min': RADIUS - 55, 'hour': RADIUS - 100, 'digit': RADIUS - 30}
RADIUS_ARK = RADIUS + 8
pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()

clock60 = dict(zip(range(60), range(0, 360, 6)))  # for hours, minutes and seconds

font = pg.font.SysFont('Verdana', 60)
img = pg.image.load('img/2.png').convert_alpha()
# bg = pg.image.load('img/bg4.jpg').convert()
# bg_rect = bg.get_rect()
# bg_rect.center = WIDTH, HEIGHT


class Star:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3d = self.get_pos3d()
        self.vel = random.uniform(0.05, 0.25)
        self.color = random.choice(COLORS)
        self.screen_pos = vec2(0, 0)
        self.size = 10

    def get_pos3d(self, scale_pos=35):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // scale_pos, HEIGHT) * scale_pos
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        return vec3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z)
        # rotate xy
        self.pos3d.xy = self.pos3d.xy.rotate(0.2)
        # mouse
        # mouse_pos = CENTER - vec2(pg.mouse.get_pos())
        # self.screen_pos += mouse_pos

    def draw(self):
        s = self.size
        if (-s < self.screen_pos.x < WIDTH + s) and (-s < self.screen_pos.y < HEIGHT + s):
            pg.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))


class Starfield:
    def __init__(self, app):
        self.stars = [Star(app) for i in range(NUM_STARS)]

    def run(self):
        [star.update() for star in self.stars]
        self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)
        [star.draw() for star in self.stars]


def get_clock_pos(clock_dict, clock_hand, key):
    x = H_WIDTH + radius_list[key] * math.cos(math.radians(clock_dict[clock_hand]) - math.pi / 2)
    y = H_HEIGHT + radius_list[key] * math.sin(math.radians(clock_dict[clock_hand]) - math.pi / 2)
    return x, y

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES)
        self.alpha_surface = pg.Surface(RES)
        self.alpha_surface.set_alpha(ALPHA)
        self.clock = pg.time.Clock()
        self.starfield = Starfield(self)
        self.dx, self.dy = 1, 1
        
    
    def run(self):
        while True:
            # self.screen.fill('black')
            self.screen.blit(self.alpha_surface, (0, 0))
            self.starfield.run()


            # self.dx *= -1 if bg_rect.left > 0 or bg_rect.right < WIDTH else 1
            # self.dy *= -1 if bg_rect.top > 0 or bg_rect.bottom < HEIGHT else 1
            # bg_rect.centerx += self.dx
            # bg_rect.centery += self.dy
            # self.screen.blit(bg, bg_rect)
            # surface.blit(img, (0, 0))
            # get time now
            t = datetime.now()
            hour, minute, second = ((t.hour % 12) * 5 + t.minute // 12) % 60, t.minute, t.second
            # draw base
            pg.draw.circle(surface, pg.Color('black'), (H_WIDTH, H_HEIGHT), RADIUS)
            # draw face
            for digit, pos in clock60.items():
                radius = 20 if not digit % 3 and not digit % 5 else 8 if not digit % 5 else 2
                pg.draw.circle(surface, pg.Color('gainsboro'), get_clock_pos(clock60, digit, 'digit'), radius, 7)
            # draw clock
            pg.draw.line(surface, pg.Color('orange'), (H_WIDTH, H_HEIGHT), get_clock_pos(clock60, hour, 'hour'), 15)
            pg.draw.line(surface, pg.Color('green'), (H_WIDTH, H_HEIGHT), get_clock_pos(clock60, minute, 'min'), 7)
            pg.draw.line(surface, pg.Color('magenta'), (H_WIDTH, H_HEIGHT), get_clock_pos(clock60, second, 'sec'), 4)
            pg.draw.circle(surface, pg.Color('white'), (H_WIDTH, H_HEIGHT), 8)
            # digital clock
            time_render = font.render(f'{t:%H:%M:%S}', True, pg.Color('forestgreen'), pg.Color('orange'))
            surface.blit(time_render, (0, 0))
            # draw arc
            sec_angle = -math.radians(clock60[t.second]) + math.pi / 2
            colorLeft = "green"
            if t.second > 41 : 
                colorLeft = "red"
            elif t.second > 22 :
                colorLeft = "orange"
            elif t.second > 3 :
                colorLeft = "yellow"
            else :
                colorLeft = "green"        
            pg.draw.arc(surface, pg.Color(colorLeft),
                            (H_WIDTH - RADIUS_ARK, H_HEIGHT - RADIUS_ARK, 2 * RADIUS_ARK, 2 * RADIUS_ARK),
                            math.pi / 2, sec_angle, 8)
            pg.draw.arc(surface, pg.Color('green'),
                            (H_WIDTH - RADIUS_ARK, H_HEIGHT - RADIUS_ARK, 2 * RADIUS_ARK, 2 * RADIUS_ARK),
                            sec_angle, math.pi / 2,  8)

            pg.display.flip()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()