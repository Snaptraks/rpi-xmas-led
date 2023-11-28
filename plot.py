import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PathCollection

from colors import ColorType, brain_and_tree


def norm_color(color: ColorType) -> ColorType:
    """Return a value between 0 and 1 for color, as required by matplotlib."""
    return tuple(c / 255 for c in color)  # type: ignore


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


def plot(coords: np.ndarray):
    fig, ax = plt.subplots()
    colors = np.zeros((coords.shape[1], 3))
    # colors[coords[1] > 0.4, :] = [1, 0, 0]
    # colors[coords[1] < 0.4, :] = [0, 1, 0]
    sc: PathCollection = ax.scatter(*coords)
    sc.set_facecolor(colors)  # type: ignore
    ax.plot(*coords, c="g")
    ax.set_aspect("equal", "box")
    plt.show()
    fig.savefig("led.png")


def update_plot(
    colors: list[tuple[float, float, float]], sc: PathCollection
) -> tuple[PathCollection]:
    sc.set_facecolor([norm_color(c) for c in colors])  # type:ignore
    return (sc,)


def animate(coords: np.ndarray):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal", "box")
    ax.set_axis_off()
    ax.set_facecolor((0, 0, 0))
    fig.set_facecolor((0, 0, 0))
    sc = ax.scatter(*coords, facecolor="k", edgecolor="0.1")

    # color_gen = random_color_fade()
    # color_gen = random_radial_out(coords)
    color_gen = brain_and_tree(coords[:, :50], coords[:, 50:])

    anim = animation.FuncAnimation(  # noqa
        fig,
        update_plot,
        color_gen,  # type: ignore
        fargs=(sc,),
        interval=50,
        cache_frame_data=False,
    )
    plt.show()


def main() -> None:
    coords_file = "coords.csv"
    coords = np.loadtxt(coords_file, delimiter=",", unpack=True)
    coords = norm_coords(coords)

    # plot(coords)
    animate(coords)

    # brain_and_tree(coords[:, :50], coords[:, 50:])


if __name__ == "__main__":
    main()
