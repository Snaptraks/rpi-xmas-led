import argparse
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

CoordsType = NDArray[np.floating]


def norm_coords(coords: CoordsType) -> CoordsType:
    """Return coordinates normalized between -1 and 1, keeping the aspect ratio."""

    _coords = coords.copy()
    _coords[0] -= _coords[0].min()
    _coords[1] -= _coords[1].min()

    _coords /= _coords[0].max() / 2
    _coords[0] -= 1

    _coords[1] -= _coords[1].max() / 2

    return _coords


def load_coords(coords_file: Path | str) -> CoordsType:
    coords = np.loadtxt(coords_file, delimiter=",", unpack=True)
    coords = norm_coords(coords)
    return coords


def get_lights_coords_interactive(args: argparse.Namespace) -> None:
    import tkinter as tk

    from PIL import Image, ImageTk

    coords = []

    def get_coordinates(event: tk.Event):
        coords.append((event.x, event.y))

    root = tk.Tk()
    root.bind("<Button 1>", get_coordinates)
    scale = 0.9
    width, height = int(1920 * scale), int(1080 * scale)
    image = Image.open(args.image)
    image.thumbnail((width, height))
    image_tk = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(root, width=image.width, height=image.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)

    root.mainloop()

    if coords:
        with open(args.coords, "w") as f:
            for x, y in coords:
                f.write(f"{x},{image_tk.height()-y}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--coords", type=Path, required=False)

    args = parser.parse_args()
    if args.coords is None:
        args.coords = args.image.with_stem(f"{args.image.stem}_coords").with_suffix(
            ".csv"
        )

    get_lights_coords_interactive(args)


if __name__ == "__main__":
    main()
