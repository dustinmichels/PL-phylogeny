"""
Needleman–Wunsch Algorithm (class-based)
"""

import pandas as pd

from .functional import arr_to_frames, arr_to_table, identity_score, nw_algo, traceback


class NW:
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2
        self.arr = None
        self.aligned_s1 = None
        self.aligned_s2 = None
        self.identity_score = None

    def solve(self, match_score=1, miss_score=-1, gap_score=-1):
        # create matrix
        self.arr = nw_algo(self.s1, self.s2, match_score, miss_score, gap_score)
        # traceback to align strings
        self.aligned_s1, self.aligned_s2 = traceback(self.arr["dir"], self.s1, self.s2)
        # compute score
        self.identity_score = identity_score(self.aligned_s1, self.aligned_s2)

    def __repr__(self):
        return f"S1: {self.s1[:10]}...\nS2: {self.s2[:10]}...\nSTATUS: {self.status}"

    @property
    def status(self):
        if self.arr is not None:
            return "solved"
        else:
            return "unsolved"

    @property
    def matrix(self):
        if self.arr is not None:
            return arr_to_table(self.arr, self.s1, self.s2)
        else:
            return "Not solved yet."

    @property
    def alignment(self):
        if self.status == "solved":
            return f"{self.aligned_s1}\n{self.aligned_s2}"
        else:
            return "Not solved yet."

    @property
    def alignment_table(self):
        if self.aligned_s1 and self.aligned_s2:
            return pd.DataFrame(data=[list(self.aligned_s1), list(self.aligned_s2)])
        else:
            return "Not solved yet."

    @property
    def score_frac(self):
        if self.identity_score:
            return self.identity_score[0]
        else:
            return "Not solved yet."

    @property
    def score_percent(self):
        if self.identity_score:
            return self.identity_score[1] * 100
        else:
            return "Not solved yet."

    def summary(self):
        print(headerify("STRINGS"))
        print("~" * 10)
        print(self.s1)
        print("~" * 10)
        print(self.s2)

        print(headerify("ALIGNMENT"))
        print(self.alignment)

        print()
        print("IDENTITY SCORE".center(30))
        print("=" * 30)
        print(self.score_frac)
        print(f"{self.score_percent} %")


def headerify(text: str):
    header = "\n"
    header += f"{text.upper()}".center(30)
    header += "\n" + "=" * 30
    return header

