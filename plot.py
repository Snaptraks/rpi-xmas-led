import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import PathCollection
import numpy as np
from typing import Generator, Iterable, Sequence

from colors import low_res_rainbow, colors_fade_rgb, random_rgb

ColorType = tuple[float, ...]


def norm_color(color: ColorType) -> ColorType:
    """Return a value between 0 and 1 for color, as required by matplotlib."""
    return tuple(c / 255 for c in color)  # type: ignore


def plot(coords: np.ndarray):
    fig, ax = plt.subplots()
    colors = np.zeros((coords.shape[0], 3))
    colors[coords[:, 1] > 0.4, :] = [1, 0, 0]
    colors[coords[:, 1] < 0.4, :] = [0, 1, 0]
    sc: PathCollection = ax.scatter(*coords.T)
    sc.set_facecolor(colors)  # type: ignore
    ax.set_aspect("equal", "box")
    fig.savefig("led.png")


def random_color_fade() -> Generator[ColorType, None, None]:
    start = random_rgb()
    end = random_rgb()

    while True:
        for c in colors_fade_rgb(start, end, steps=20):
            yield norm_color(c)
        start, end = end, random_rgb()


def update_plot(
    c: tuple[float, float, float], sc: PathCollection
) -> tuple[PathCollection]:
    sc.set_facecolor(c)
    return (sc,)


def animate(coords: np.ndarray):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_aspect("equal", "box")
    ax.set_axis_off()
    ax.set_facecolor((0, 0, 0))
    fig.set_facecolor((0, 0, 0))
    sc = ax.scatter(*coords.T)

    color_gen = random_color_fade()

    anim = animation.FuncAnimation(
        fig,
        update_plot,
        color_gen,  # type: ignore
        fargs=(sc,),
        interval=100,
        cache_frame_data=False,
    )
    plt.show()


def main() -> None:
    coords = np.loadtxt("coords.txt", delimiter=",")
    # plot(coords)
    animate(coords)


if __name__ == "__main__":
    main()
