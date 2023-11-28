import argparse
import time
from pathlib import Path

import board
import neopixel
import numpy as np

import colors

N_PIXELS: int = 100
pixels = neopixel.NeoPixel(
    board.D21,  # type: ignore
    n=N_PIXELS,
    brightness=0.3,
    pixel_order=neopixel.RGB,
    auto_write=False,
)


def clear_pixels():
    pixels.deinit()


def run_pixels(coords: np.ndarray) -> None:
    color_gen = colors.brain_and_tree(coords[:, :50], coords[:, 50:])
    for color in color_gen:
        for p, c in enumerate(color):
            pixels[p] = c

        pixels.show()
        time.sleep(0.1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coords", type=Path, default=Path("./coords.csv"))
    parser.add_argument("--clear", action="store_true")

    args = parser.parse_args()

    if args.clear:
        clear_pixels()
    else:
        try:
            coords = np.loadtxt(args.coords, delimiter=",", unpack=True)
            run_pixels(coords)
        except KeyboardInterrupt:
            print()
            clear_pixels()


if __name__ == "__main__":
    main()
