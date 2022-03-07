"""
The game's colour set plus some general tools for finding the colours you're
looking for. 'Murica spelling.
"""
import settings

big_red = Color(255, 0, 0) 
big_green = Color(0, 255, 0)
big_blue = Color(0, 0, 255)
big_black = Color(0,0,0)
big_white = Color(255,255,255)

def hue(color):
    return color.hsla[0]
def sat(color):
    return color.hsla[1]
def lum(color):
    return color.hsla[2]

def hsla(h, s, l, *a):
    if len(a):
        a = a[0]
    else:
        a = 100
    c = Color()
    c.hsla = (h, s, l, a)
    return c

hue_red = 10
hue_orange = 30
hue_yellow = 50
hue_lemon = 60
hue_green = 120
hue_pea_green = 150
hue_aqua = 180
hue_sky_blue = 210
hue_blue = 240
hue_violet = 260
hue_magenta = 300

lum_black = 0
lum_dark = 10
lum_shade = 20 
lum_dull = 30
lum_soft = 40
lum_neutral = 50
lum_light = 60
lum_pale = 70
lum_highlight = 80
lum_sparkle = 90
lum_white = 100

sat_greyscale = 0
sat_dull = 20
sat_muted = 30
sat_natural = 50
sat_strong = 70
sat_bright = 90
sat_full = 100

#colors
dirt_brown = hsla(hue_orange, sat_dull, lum_dull)
brown_highlight = hsla(hue_orange, sat_muted, lum_soft)
ember_red = hsla(hue_red, sat_bright, lum_light)
ember_orange = hsla(hue_orange, sat_bright, lum_light)
ember_yellow = hsla(hue_yellow, sat_bright, lum_light)
default_bg_dirt = hsla(hue_orange + 10, sat_muted, lum_shade)

#term_matching colors
black = hsla(0, sat_greyscale, lum_black)
bright_black = hsla(0, sat_greyscale, lum_dull)
red = hsla(hue_red, sat_natural, lum_neutral)
bright_red = hsla(hue_red, sat_strong, lum_light)
green = hsla(hue_green, sat_natural, lum_neutral)
bright_green = hsla(hue_green, sat_natural, lum_light)
yellow = hsla(hue_yellow, sat_strong, lum_neutral)
bright_yellow = hsla(hue_yellow, sat_strong, lum_light)
blue = hsla(hue_blue, sat_strong, lum_neutral)
bright_blue = hsla(hue_blue, sat_strong, lum_light)
magenta = hsla(hue_magenta, sat_strong, lum_neutral)
bright_magenta = hsla(hue_magenta, sat_strong, lum_light)
cyan = hsla(hue_aqua, sat_strong, lum_neutral)
bright_cyan = hsla(hue_aqua, sat_strong, lum_light)
white = hsla(0, sat_greyscale, lum_light)
bright_white = hsla(0, sat_greyscale, lum_white)

#tints
tint_purple = hsla(hue_violet, sat_natural, lum_pale)
tint_yellow = hsla(hue_yellow, sat_bright, lum_neutral)
tint_orange = hsla(hue_orange, sat_bright, lum_neutral)
tint_red = hsla(hue_red, sat_bright, lum_neutral)
tint_darkred = hsla(hue_red, sat_dull, lum_dark)


if __name__ == "__main__":
    import time
    import math
    from copy import copy
    bs = settings.TILE_SIZE
    hue_gap = 10
    sat_gap = 10
    lum_gap = 10
    cols = 10
    rows = 5
    pt = 32
    pl = 32
    def length(pos):
        x,y = pos
        return math.sqrt(math.pow(x,2) + math.pow(y,2))
    def ny_length(pos):
        x,y = pos
        return x+y
    grid_positions = [(x*bs, y*bs) 
            for x in range(11) for y in range(11)]
    sorted_positions = list(sorted(grid_positions, key = ny_length))
    current_color = copy(big_red)
    h, s, l, a = current_color.hsla
    new_h = h
    while True:
        gfx.renderer.clear(white)
        h, s, l, a = current_color.hsla
        new_h = (new_h + 50) % 360
        for x, y in sorted_positions:
            new_s = (x/bs)*10
            new_l = (y/bs)*10
            current_color.hsla = (new_h, new_s, new_l, a)
            gfx.renderer.fill((x, y, bs, bs), color = current_color)
            draw_text(gfx, (x, y, bs, bs), str((new_s/10,new_l/10)))
        gfx.renderer.present()
        time.sleep(1)
        
