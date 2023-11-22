import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import PathCollection
import numpy as np

from colors import low_res_rainbow


def plot(coords: np.ndarray):
    fig, ax = plt.subplots()
    colors = np.zeros((coords.shape[0], 3))
    colors[coords[:, 1] > 0.4, :] = [1, 0, 0]
    colors[coords[:, 1] < 0.4, :] = [0, 1, 0]
    sc: PathCollection = ax.scatter(*coords.T)
    sc.set_facecolor(colors)  # type: ignore
    ax.set_aspect("equal", "box")
    fig.savefig("led.png")


def update_plot(i: int, sc: PathCollection) -> tuple[PathCollection]:
    color = [c / 255 for c in next(low_res_rainbow)]
    sc.set_facecolor([color for _ in range(100)])
    print(i)
    return (sc,)


def animate(coords: np.ndarray):
    fig, ax = plt.subplots()
    sc = ax.scatter(*coords.T)
    anim = animation.FuncAnimation(
        fig, update_plot, frames=60, fargs=(sc,), interval=500
    )
    plt.show()


def main() -> None:
    coords = np.loadtxt("coords.txt", delimiter=",")
    # plot(coords)
    animate(coords)


if __name__ == "__main__":
    main()
