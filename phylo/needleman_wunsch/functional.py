"""
Needleman–Wunsch Algorithm (pure functions)
"""

from fractions import Fraction
from typing import Tuple

import numpy as np
import pandas as pd


def nw_algo(s1: str, s2: str, match_score=1, miss_score=-1, gap_score=-1) -> np.array:
    """Implementation of needleman–wunsch algorithm"""

    w = len(s1) + 1  # width
    h = len(s2) + 1  # height

    # create single, "structured" np array to hold values (ints) and directions (strings)
    arr = np.empty((h, w), dtype=[("val", "i4"), ("dir", np.unicode_, 1)])
    arr.fill((0, "."))

    # set up matrix: fill in first row & col
    # first row
    arr[0, 1:]["val"] = np.arange(-1, -w, -1)
    arr[0, 1:]["dir"] = "H"
    # first col
    arr[1:, 0]["val"] = np.arange(-1, -h, -1)
    arr[1:, 0]["dir"] = "V"

    # fill in matrix using alogorithm
    for i in range(1, h):
        for j in range(1, w):
            # determine val of horizontal, vertical, and diagnol option
            hor_val = arr[i, j - 1]["val"] + gap_score
            vert_val = arr[i - 1, j]["val"] + gap_score
            diag_val = arr[i - 1, j - 1]["val"] + (
                match_score if s1[j - 1] == s2[i - 1] else miss_score
            )
            # find max value and its corresponding direction
            # (Note: currently ignores ties)
            dirs = {hor_val: "H", vert_val: "V", diag_val: "D"}
            selected_val = max(hor_val, vert_val, diag_val)
            selected_dir = dirs[selected_val]
            # fill in array
            arr[i, j]["val"] = selected_val
            arr[i, j]["dir"] = selected_dir
    return arr


def traceback(dir_matrix, s1: str, s2: str) -> Tuple[str, str]:
    """
    Recursive traceback function,
    Aligns strings by navigating dir_matrix path from bottom right
    """

    def helper(dir_matrix, row, col, aligned_s1, aligned_s2):
        cell = dir_matrix[row, col]
        if cell == "D":
            aligned_s1 += s1[col - 1]
            aligned_s2 += s2[row - 1]
            return helper(dir_matrix, row - 1, col - 1, aligned_s1, aligned_s2)
        elif cell == "H":
            aligned_s1 += s1[col - 1]
            aligned_s2 += "-"
            return helper(dir_matrix, row, col - 1, aligned_s1, aligned_s2)
        elif cell == "V":
            aligned_s1 += "-"
            aligned_s2 += s2[row - 1]
            return helper(dir_matrix, row - 1, col, aligned_s1, aligned_s2)
        elif cell == ".":
            return aligned_s1[::-1], aligned_s2[::-1]
        else:
            return ("Error!", "Bad characters in dir_matrix")

    row_idx = len(dir_matrix) - 1
    col_idx = len(dir_matrix[1]) - 1
    return helper(dir_matrix, row_idx, col_idx, "", "")


def identity_score(aligned_s1: str, aligned_s2: str) -> Tuple[str, float]:
    """
    Get identity score for aligned strings
    """
    assert len(aligned_s1) == len(aligned_s2), "Strings must be the same length"

    identity = 0
    length = len(aligned_s1)

    for i in range(length):
        if aligned_s1[i] == aligned_s2[i]:
            identity += 1

    frac = f"{identity}/{length}"
    percent = identity / length

    return frac, percent


# ---- For visualizing matrix ----


def arr_to_frames(arr: np.array, s1: str, s2: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Covert structured NW matrix into two pretty DataFrames"""
    cols = [" "] + list(s1)
    idx = [" "] + list(s2)
    vals = pd.DataFrame(arr["val"], columns=cols, index=idx)
    dirs = (
        pd.DataFrame(arr["dir"], columns=cols, index=idx)
        .replace(regex="H", value="\u2190")
        .replace(regex="V", value="\u2191")
        .replace(regex="D", value="\u2196")
    )
    return vals, dirs


def arr_to_table(arr: np.array, s1: str, s2: str) -> pd.DataFrame:
    """Convert NW matrix into single pretty DataFrame"""
    vals, dirs = arr_to_frames(arr, s1, s2)
    combined = "[" + dirs + " " + vals.astype(np.unicode_) + "]"  # string concatenation
    return combined
