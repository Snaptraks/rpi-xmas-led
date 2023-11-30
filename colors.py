import colorsys
import random
from collections.abc import Iterator
from itertools import cycle, repeat

import numpy as np

from coords import CoordsType

ColorType = tuple[float, ...]

low_res_rainbow = cycle(
    [
        [255, 0, 0],
        [255, 255, 0],
        [0, 255, 0],
        [0, 255, 255],
        [0, 0, 255],
        [255, 0, 255],
    ]
)


def colors_fade_rgb(
    color_0: ColorType, color_1: ColorType, steps: int = 50
) -> Iterator[ColorType]:
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


def random_color_fade(steps=20) -> Iterator[ColorType]:
    start = random_rgb()
    end = random_rgb()

    while True:
        yield from colors_fade_rgb(start, end, steps=steps)
        start, end = end, random_rgb()


def radial_out(
    coords: CoordsType,
    center: tuple[float, float],
    base_color: ColorType,
) -> Iterator[list[ColorType]]:
    def func(x, y, t, _center: tuple[float, float]) -> ColorType:
        return np.exp(
            -10 * (np.sqrt((x - _center[0]) ** 2 + (y - _center[1]) ** 2) - t) ** 2
        )

    t = -0.7
    dt = 0.025

    while t <= 2:
        color = func(coords[0], coords[1], t, _center=center)
        yield [(base_color[0] * c, base_color[1] * c, base_color[2] * c) for c in color]
        t += dt


def random_radial_out(coords: CoordsType) -> Iterator[list[ColorType]]:
    while True:
        base_color = random_rgb()
        center = (random.uniform(-0.8, -0.3), random.uniform(-0.3, 0.3))
        yield from radial_out(coords, center, base_color)


def sinus_colors(coords: CoordsType) -> Iterator[list[ColorType]]:
    def sinus(pixel: int, rgb: int, t: float) -> float:
        """
        pixel: index of the pixel
        rgb: 0: r, 1: g, 2:b
        """
        v = np.sin(3 * np.pi * (pixel - t) + 2 * np.pi * rgb / 3) + 1
        return v / 2 * 255

    t = 0
    while True:
        c = [tuple(sinus(p, rgb, t) for rgb in (0, 1, 2)) for p in coords[1]]
        yield c
        t += 0.01


def tree(coords: CoordsType) -> Iterator[list[ColorType]]:
    tree_green = (0, 127, 14)
    star_yellow = (255, 80, 0)
    N = coords.shape[1]  # total number of lights
    k = 20  # number of lights with random color

    while True:
        random_lights = random.sample(range(N), k=k)
        random_colors = [random_rgb() for _ in range(k)]
        colors: list[Iterator[ColorType]] = [repeat(tree_green) for _ in range(N)]

        def lights_generator(ascend: bool = True) -> Iterator[list[ColorType]]:
            for i, light in enumerate(random_lights):
                if ascend:
                    # start with green, fade to light color
                    start, end = tree_green, random_colors[i]
                else:
                    # start with light color, fade back to green
                    start, end = random_colors[i], tree_green
                colors[light] = colors_fade_rgb(start, end)

            # set top of tree to a star (yellow)
            colors[-1] = repeat(star_yellow)

            for c in zip(*colors):
                yield list(c)

        # light up the random lights
        yield from lights_generator(ascend=True)
        # fade out the random lights
        yield from lights_generator(ascend=False)


def brain_and_tree(
    brain_coords: CoordsType, tree_coords: CoordsType
) -> Iterator[list[ColorType]]:
    """Generator for the colors for the brain and the tree."""

    brain_gen = random_radial_out(brain_coords)
    tree_gen = tree(tree_coords)
    # tree_gen = random_color_fade(steps=40)
    # tree_gen = sinus_colors(tree_coords)

    for brain_colors, tree_colors in zip(brain_gen, tree_gen):
        yield brain_colors + tree_colors  # append both lists
