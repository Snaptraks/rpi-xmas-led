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

EPILEPSY_PURPLE = (93, 63, 211)


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

    while t <= 2.5:
        color = func(coords[0], coords[1], t, _center=center)
        yield [(base_color[0] * c, base_color[1] * c, base_color[2] * c) for c in color]
        t += dt


def seizure(
    n_lights: int, light_start: int, light_end: int
) -> Iterator[list[ColorType]]:
    seizure_color = (255, 255, 255)
    for _ in range(100):
        colors: list[ColorType] = [(0, 0, 0) for _ in range(n_lights)]
        for i in range(light_start, light_end):
            intensity = random.random()
            colors[i] = tuple(intensity * c for c in seizure_color)

        yield colors


def random_radial_out(coords: CoordsType) -> Iterator[list[ColorType]]:
    N = coords.shape[1]
    while True:
        if random.random() < 0.9:
            base_color = random_rgb()
            center = (random.uniform(-0.75, 0.75), random.uniform(-0.75, 0.75))
            yield from radial_out(coords, center, base_color)
        else:
            # seizure!
            yield from seizure(N, 85, 93)


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


def heart(
    coords: CoordsType, center: tuple[float, float] = (0, 0)
) -> Iterator[list[ColorType]]:
    reds = (
        (255, 150, 150),
        (255, 110, 110),
        (255, 70, 70),
        (255, 30, 30),
        (255, 0, 0),
    )
    n_reds = len(reds)
    N = coords.shape[1]
    radius = ((coords[0] - center[0]) ** 2 + (coords[1] - center[1]) ** 2) ** 0.5
    r_max = 0.45
    t = 0
    dt = 0.005
    while True:
        # equation of a semi-circle of radius r_max
        y = (r_max**2 - (t - r_max) ** 2) ** 0.5
        # keep 0 < t < 2 * r_max
        t += dt
        t %= 2 * r_max

        ring_size = y / n_reds
        colors: list[ColorType] = [(0, 0, 0) for _ in range(N)]
        for i, r in enumerate(radius):
            for n in range(n_reds, 0, -1):
                if r <= (n + 1) * ring_size:
                    # if i % n_reds == n - 1:
                    colors[i] = reds[n - 1]
        yield colors


def combine_generators(
    iterator_1: Iterator[list[ColorType]], iterator_2: Iterator[list[ColorType]]
) -> Iterator[list[ColorType]]:
    """Combine two generators that output lists."""
    for colors_1, colors_2 in zip(iterator_1, iterator_2):
        yield colors_1 + colors_2  # append both lists


def brain_and_tree(
    brain_coords: CoordsType, tree_coords: CoordsType
) -> Iterator[list[ColorType]]:
    """Generator for the colors for the brain and the tree."""

    brain_gen = random_radial_out(brain_coords)
    tree_gen = tree(tree_coords)
    # tree_gen = random_color_fade(steps=40)
    # tree_gen = sinus_colors(tree_coords)

    yield from combine_generators(brain_gen, tree_gen)


def brain_and_heart(
    brain_coords: CoordsType, tree_coords: CoordsType
) -> Iterator[list[ColorType]]:
    """Generator for the colors for the brain and the heart."""

    brain_gen = random_radial_out(brain_coords)
    heart_gen = heart(tree_coords, center=(0.732, 0.130))

    yield from combine_generators(brain_gen, heart_gen)
