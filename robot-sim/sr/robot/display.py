from __future__ import division
from math import degrees

import pygame

PIXELS_PER_METER = 100

sprites = {}

def get_surface(name):
    if name not in sprites:
        sprites[name] = pygame.image.load(name).convert_alpha()

    return sprites[name]


def _int_without_remainder(val):
    as_int = int(val)
    assert as_int == val, "Unable to convert {!r} to integer - it has a fractional part".format(val)
    return as_int


class Display(object):
    def __init__(self, arena):
        self.arena = arena
        arena_w, arena_h = self.arena.size
        self.size = (
            _int_without_remainder(arena_w * PIXELS_PER_METER),
            _int_without_remainder(arena_h * PIXELS_PER_METER),
        )

        pygame.display.init()
        self._window = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        pygame.display.set_caption("SR Turtle Robot Simulator")
        self._screen = pygame.display.get_surface()
        self._draw_background()
        self._draw()

    def __del__(self):
        pygame.display.quit()

    def _draw_background(self):
        self._background = pygame.Surface(self.size)
        self.arena.draw_background(self._background, self)

    def _draw(self):
        self._screen.blit(pygame.transform.scale(self._background,self.size), (0, 0))

        for obj in self.arena.objects:
            if obj.surface_name is None:
                continue
            with obj.lock:
                heading = -degrees(obj.heading)
                x, y = self.to_pixel_coord(obj.location)
            surface = get_surface(obj.surface_name)
            surface = pygame.transform.rotate(surface, heading)
            object_width, object_height = surface.get_size()
            surface = pygame.transform.scale(surface, (int(object_width*self.size[0]/1900), int(object_height*self.size[1]/1100)))
            object_width, object_height = surface.get_size()
            screen_location = (int((x - object_width)*self.size[0]/1900), int((y - object_height)*self.size[1]/1100))
            self._screen.blit(surface, screen_location)

        pygame.display.flip()
        
    def resize (self, event):
		self.size = (event.w, event.h)
		self._window = pygame.display.set_mode(self.size, pygame.RESIZABLE)
		pygame.display.set_caption("SR Turtle Robot Simulator")
		self._screen = pygame.display.get_surface()
		self._draw_background()
		self._draw()
		

    ## Public Methods ##

    def tick(self, time_passed):
        self.arena.tick(time_passed)
        # TODO: Allow multiple displays on one arena without them all ticking it
        self._draw()

    def to_pixel_coord(self, world_coord, arena=None):
        if arena is None: arena = self.arena
        offset_x = arena.size[0] / 2
        offset_y = arena.size[1] / 2
        x, y = world_coord
        x, y = ((x + offset_x) * PIXELS_PER_METER, (y + offset_y) * PIXELS_PER_METER)
        return (x, y)

    def to_pixel_dimension(self, world_dimension):
        x,y = world_dimension
        return x * PIXELS_PER_METER, y * PIXELS_PER_METER
