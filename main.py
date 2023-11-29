import argparse
import time
from pathlib import Path

import board
import neopixel
import numpy as np

import colors
from coords import load_coords

N_PIXELS: int = 100
pixels = neopixel.NeoPixel(
    board.D21,  # type: ignore
    n=N_PIXELS,
    brightness=1,
    pixel_order=neopixel.RGB,
    auto_write=False,
)


def clear_pixels():
    pixels.deinit()


def make_color_int(color: colors.ColorType) -> colors.ColorType:
    return tuple(int(c) for c in color)


def run_pixels(coords: np.ndarray) -> None:
    color_gen = colors.brain_and_tree(coords[:, :50], coords[:, 50:])
    for color in color_gen:
        for p, c in enumerate(color):
            pixels[p] = make_color_int(c)

        pixels.show()
        time.sleep(1 / 60)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coords", type=Path, default=Path("./coords.csv"))
    parser.add_argument("--clear", action="store_true")

    args = parser.parse_args()

    if args.clear:
        clear_pixels()
    else:
        try:
            coords = load_coords(args.coords)
            run_pixels(coords)
        except KeyboardInterrupt:
            print()
            clear_pixels()


if __name__ == "__main__":
    main()
