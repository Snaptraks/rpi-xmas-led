from pathlib import Path

import numpy as np


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
