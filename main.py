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


def make_color_int(color: colors.ColorType) -> colors.ColorType:
    return tuple(int(c) for c in color)


def norm_coords(coords: np.ndarray) -> np.ndarray:
    """Return coordinates normalized between -1 and 1, keeping the aspect ratio."""

    _coords = coords.copy()
    _coords[0] -= _coords[0].min()
    _coords[1] -= _coords[1].min()

    coords_max = _coords[0].max() / 2
    _coords /= coords_max
    _coords[0] -= 1

    _coords[1] -= _coords[1].max() / 2

    return _coords


def load_coords(coords_file: Path | str) -> np.ndarray:
    coords = np.loadtxt(coords_file, delimiter=",", unpack=True)
    coords = norm_coords(coords)
    return coords


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
