import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PathCollection

from colors import ColorType, brain_and_tree, heart
from coords import CoordsType, load_coords


def norm_color(color: ColorType) -> ColorType:
    """Return a value between 0 and 1 for color, as required by matplotlib."""
    return tuple(c / 255 for c in color)  # type: ignore


def plot(coords: CoordsType):
    fig, ax = plt.subplots()
    colors = np.zeros((coords.shape[1], 3))
    sc: PathCollection = ax.scatter(*coords)
    sc.set_facecolor(colors)  # type: ignore
    ax.plot(*coords, c="g")
    ax.set_aspect("equal", "box")
    plt.show()
    fig.savefig("led.png")


def update_plot(colors: list[ColorType], sc: PathCollection) -> tuple[PathCollection]:
    sc.set_facecolor([norm_color(c) for c in colors])  # type:ignore
    return (sc,)


def animate(coords: CoordsType):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal", "box")
    ax.set_axis_off()
    ax.set_facecolor((0, 0, 0))
    fig.set_facecolor("k")
    sc = ax.scatter(*coords, facecolor="k", edgecolor="0.1")

    # color_gen = random_color_fade()
    # color_gen = random_radial_out(coords)
    # color_gen = brain_and_tree(coords[:, :50], coords[:, 50:])
    color_gen = heart(coords[:, :50], center=(0.7, 0))

    anim = animation.FuncAnimation(  # noqa
        fig,
        update_plot,
        color_gen,  # type: ignore
        fargs=(sc,),
        interval=2000 / 60,
        cache_frame_data=False,
    )
    plt.show()


def main() -> None:
    coords = load_coords("coords.csv")
    # plot(coords)
    animate(coords[:, 50:])


if __name__ == "__main__":
    main()
