import colorsys
import itertools
import random

low_res_rainbow = itertools.cycle(
    [
        [255, 0, 0],
        [255, 255, 0],
        [0, 255, 0],
        [0, 255, 255],
        [0, 0, 255],
        [255, 0, 255],
    ]
)


def colors_fade_rgb(color_0: list[int], color_1: list[int], steps: int = 20):
    slope = [(color_1[i] - color_0[i]) / steps for i in range(3)]

    new_color = color_0[:]
    for t in range(steps + 1):
        new_color = tuple(int(color_0[i] + t * slope[i]) for i in range(3))
        yield new_color


def rainbow_gen():
    colors = [255, 0, 0]  # initial color
    i = 1  # color index to change
    step = 3
    while True:
        if colors[i - 1] == 255 and colors[i] != 255:
            colors[i] += step

        elif colors[i - 1] != 0 and colors[i] == 255:
            colors[i - 1] -= step

        if colors[i - 1] == 0 and colors[i] == 255:
            i = (i + 1) % 3

        yield colors


def random_rgb() -> list[int]:
    rgb = [int(c * 255) for c in colorsys.hsv_to_rgb(random.random(), 1, 1)]
    return rgb
