"""
Needleman–Wunsch Algorithm (class wrapper around pure functions)
"""

import pandas as pd
from IPython.display import Latex, Markdown, display

from .functional import (
    arr_to_frames,
    arr_to_table,
    identity_score,
    gap_score,
    nw_algo,
    traceback,
)


class NW:
    """
    Align strings using Needleman–Wunsch Algorithm
    """

    # define constants for string replacement
    newline_char = "\u21B5"
    space_char = "\u00B7"
    gap_char = "\u25ac"

    # values to be filled once matrix is solved
    arr = None
    aligned_s1 = None
    aligned_s2 = None
    identity_score = None

    def __init__(
        self,
        s1,
        s2,
        s1_name="s1",
        s2_name="s2",
        match_penalty=1,
        miss_penalty=-1,
        gap_penalty=-1,
    ):
        self.s1 = s1
        self.s2 = s2
        self.s1_name = s1_name
        self.s2_name = s2_name
        self.match_penalty = match_penalty
        self.miss_penalty = miss_penalty
        self.gap_penalty = gap_penalty

    def __repr__(self):
        return f"S1: {self.s1[:10]}...\nS2: {self.s2[:10]}...\nSOLVED: {self.solved}"

    def solve(self):
        """Create & solve matrix using NW. Traceback path to align strings. Compute score"""
        self.arr = nw_algo(**self.__dict__)
        self.aligned_s1, self.aligned_s2 = traceback(self.arr["dir"], self.s1, self.s2)
        self.identity_score = identity_score(self.aligned_s1, self.aligned_s2)
        self.gap_score = gap_score(self.aligned_s1, self.aligned_s2)

    # ----- properties & summary methods -----

    def _check_solved(func):
        """Use as a wrapper for the repeated task of checking if matrix is solved"""
        # pylint: disable=no-self-argument,not-callable
        def wrapper(self, *args, **kwargs):
            if self.solved:
                return func(self, *args, **kwargs)
            else:
                return "Not solved yet."

        return wrapper

    @property
    def solved(self):
        """True if matrix has been solved, False otherwise"""
        return self.arr is not None

    @property  # type: ignore
    @_check_solved
    def matrix(self):
        return arr_to_table(self.arr, self.s1, self.s2)

    @property  # type: ignore
    @_check_solved
    def aligned_strings(self):
        """Display aligned strings cleanly, with connector string"""

        def clean(s):
            return (
                s.replace("\n", self.newline_char)
                .replace(" ", self.space_char)
                .replace("-", self.gap_char)
            )

        return clean(self.aligned_s1), clean(self.aligned_s2)

    @_check_solved
    def get_aligned_strings_with_connector(self):
        a, b = self.aligned_strings
        conn = ""
        for i in range(len(a)):
            conn += "|" if a[i] == b[i] else " "
        return a, conn, b

    @_check_solved
    def summarize(self):
        align1, conn, align2 = self.get_aligned_strings_with_connector()
        data = dict(
            L=len(align1),
            iden_score_frac=self.identity_score[0],
            iden_score_percent=self.identity_score[1] * 100,
            gap_score_frac=self.gap_score[0],
            gap_score_percent=self.gap_score[1] * 100,
            s1_name=self.s1_name,
            align1=align1,
            blank="",
            conn=conn,
            s2_name=self.s2_name,
            align2=align2,
            name_len=max(len(self.s1_name), len(self.s2_name)),
        )
        return summary_template.format(**data)


# Based off: http://emboss.sourceforge.net/docs/themes/AlignFormats.html
summary_template = """
#=======================================
#
# Aligned_sequences: 2
# Length: {L}
# Identity:     {iden_score_frac:6s} ({iden_score_percent:.4g} %)
# Gaps:         {gap_score_frac:6s} ({gap_score_percent:.4g} %)
#
#=======================================

{s1_name:{name_len}s}\t{align1}
{blank:{name_len}s}\t{conn}
{s2_name:{name_len}s}\t{align2}
"""
