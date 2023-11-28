import argparse
import math
import random
import time

import board
import neopixel

from colors import colors_fade_rgb, low_res_rainbow, rainbow_gen, random_rgb

N_PIXELS: int = 100
pixels = neopixel.NeoPixel(
    board.D21,  # type: ignore
    n=N_PIXELS,
    brightness=0.3,
    pixel_order=neopixel.RGB,
    auto_write=False,
)


def rainbow_wave():
    colors = rainbow_gen()
    # colors = low_res_rainbow
    while True:
        color = next(colors)
        pixels.fill(color)
        pixels.show()
        time.sleep(0.1)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)


def rainbow_cycle(wait):
    while True:
        for j in range(255):
            for i in range(N_PIXELS):
                pixel_index = (i * 256 // N_PIXELS) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)


def pong():
    p = 0  # pixel ID
    direction = 1  # +/- 1
    colors = low_res_rainbow
    color = None
    while True:
        if p == 0 and direction == 1:
            color = next(colors)
        pixels.fill((0, 0, 0))  # turn off
        pixels[p] = color
        pixels.show()
        time.sleep(0.1)

        p += direction
        if p == N_PIXELS - 1 or p == 0:
            direction *= -1


def tree():
    while True:
        pixels.fill((3, 7, 0))
        pixels.show()
        time.sleep(1)
        for p in range(N_PIXELS):
            if random.random() < 0.2:
                colors: list[tuple[int, ...]] = [
                    (255, 255, 0),
                    (255, 0, 0),
                    (0, 0, 255),
                ]
                c = random.choice(colors)
                pixels[p] = c
        pixels.show()
        time.sleep(5)


def sinus_colors():
    def sinus(pixel: int, rgb: int, t: float) -> float:
        """
        pixel: index of the pixel
        rgb: 0: r, 1: g, 2:b
        """
        v = math.sin(2 * math.pi * (pixel + t) / N_PIXELS + 2 * math.pi * rgb / 3) + 1
        return int(v / 2 * 255)

    t = 0
    while True:
        for p in range(N_PIXELS):
            pixels[p] = [sinus(p, rgb, t) for rgb in (0, 1, 2)]

        t += 1
        time.sleep(0.02)
        pixels.show()


def random_color_fade():
    start = random_rgb()
    end = random_rgb()

    while True:
        print(f"{start} -> {end}")
        for color in colors_fade_rgb(start, end, steps=20):
            pixels.fill(color)
            pixels.show()
            time.sleep(0.1)
        start, end = end, random_rgb()


def clear_pixels():
    pixels.deinit()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clear", action="store_true")

    args = parser.parse_args()
    if args.clear:
        clear_pixels()
    else:
        try:
            # rainbow_wave()
            # rainbow_cycle(0.01)
            # pong()
            # tree()
            # sinus_colors()
            # colors_fade_rgb([255, 0, 0], [0, 0, 255], steps=50)
            random_color_fade()
        except KeyboardInterrupt:
            print()
            clear_pixels()


if __name__ == "__main__":
    main()
