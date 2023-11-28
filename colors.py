import colorsys
import itertools
import random
from typing import Generator

import numpy as np

ColorType = tuple[float, ...]

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


def colors_fade_rgb(color_0: ColorType, color_1: ColorType, steps: int = 20):
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


def random_rgb() -> ColorType:
    rgb = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(random.random(), 1, 1))
    return rgb


def random_color_fade(steps=20) -> Generator[ColorType, None, None]:
    start = random_rgb()
    end = random_rgb()

    while True:
        yield from colors_fade_rgb(start, end, steps=steps)
        start, end = end, random_rgb()


def radial_out(
    coords: np.ndarray,
    center: tuple[float, float],
    base_color: ColorType,
) -> Generator[list[ColorType], None, None]:
    def func(x, y, t, _center: tuple[float, float]) -> ColorType:
        return np.exp(
            -10 * (np.sqrt((x - _center[0]) ** 2 + (y - _center[1]) ** 2) - t) ** 2
        )

    start = -0.7
    t = start
    dt = 0.025

    while t <= 2:
        color = func(coords[0], coords[1], t, _center=center)
        t += dt

        yield [(base_color[0] * c, base_color[1] * c, base_color[2] * c) for c in color]


def random_radial_out(coords: np.ndarray) -> Generator[list[ColorType], None, None]:
    while True:
        base_color = random_rgb()
        center = (random.uniform(-0.8, -0.3), random.uniform(-0.3, 0.3))
        yield from radial_out(coords, center, base_color)


def tree(coords: np.ndarray) -> Generator[list[ColorType], None, None]:
    while True:
        yield [(0, 127, 14) for _ in range(coords.shape[1])]


def brain_and_tree(brain_coords, tree_coords) -> Generator[list[ColorType], None, None]:
    """Generator for the colors for the brain and the tree."""

    brain_gen = random_radial_out(brain_coords)
    # tree_gen = tree(tree_coords)
    tree_gen = random_color_fade(steps=40)

    for brain_colors, tree_colors in zip(brain_gen, tree_gen):
        yield brain_colors + [tree_colors] * 50  # append both lists
