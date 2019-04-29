"""
Needleman–Wunsch Algorithm
"""

import numpy as np
from fractions import Fraction
import re


# This function returns to values for cae of match or mismatch


def Diagonal(n1, n2, pt):
    if(n1 == n2):
        return pt['MATCH']
    else:
        return pt['MISMATCH']


def Pointers(di, ho, ve):

    # based on python default maximum(return the first element).
    pointer = max(di, ho, ve)

    if(di == pointer):
        return 'D'
    elif(ho == pointer):
        return 'H'
    else:
        return 'V'


def NW(s1, s2, match=1, mismatch=-1, gap=-1):

    # A dictionary for all the penalty valuse.
    penalty = {'MATCH': match, 'MISMATCH': mismatch, 'GAP': gap}

    n = len(s1) + 1  # The dimension of the matrix columns.
    m = len(s2) + 1  # The dimension of the matrix rows.

    # Initializes the alighment matrix with zeros.
    al_mat = np.zeros((m, n), dtype=int)
    # Initializes the alighment matrix with zeros.
    p_mat = np.zeros((m, n), dtype=str)

    # Scans all the first rows element in the matrix and fill it with "gap penalty"
    for i in range(m):
        al_mat[i][0] = penalty['GAP'] * i
        p_mat[i][0] = 'V'

    # Scans all the first columns element in the matrix and fill it with "gap penalty"
    for j in range(n):
        al_mat[0][j] = penalty['GAP'] * j
        p_mat[0][j] = 'H'

    # Fill the matrix with the correct values.
    # Return the first element of the pointer matrix back to 0.
    p_mat[0][0] = 0
    for i in range(1, m):
        for j in range(1, n):
            # The value for match/mismatch -  diagonal.
            di = al_mat[i-1][j-1] + Diagonal(s1[j-1], s2[i-1], penalty)
            # The value for gap - horizontal.(from the left cell)
            ho = al_mat[i][j-1] + penalty['GAP']
            # The value for gap - vertical.(from the upper cell)
            ve = al_mat[i-1][j] + penalty['GAP']
            # Fill the matrix with the maximal value.(based on the python default maximum)
            al_mat[i][j] = max(di, ho, ve)
            p_mat[i][j] = Pointers(di, ho, ve)

    return np.matrix(al_mat), np.matrix(p_mat)


def traceback(letters, s1, s2):
    res = np.array(letters)
    row_idx = len(res) - 1
    col_idx = len(res[1]) - 1
    return _traceback_helper(res, row_idx, col_idx, s1, s2, "", "")


def _traceback_helper(res, row, col, s1, s2, str1, str2):
    cell = res[row, col]
    if cell == 'D':
        str1 += s1[col-1]
        str2 += s2[row-1]
        return _traceback_helper(res, row-1, col-1, s1, s2, str1, str2)
    elif cell == "H":
        str1 += s1[col-1]
        str2 += "-"
        return _traceback_helper(res, row, col-1, s1, s2, str1, str2)
    elif cell == "V":
        str1 += "-"
        str2 += s2[row-1]
        return _traceback_helper(res, row-1, col, s1, s2, str1, str2)
    elif cell == '0':
        return str1[::-1], str2[::-1]
    else:
        print("error!")


def score(a, b):
    """
    see: https://binf.snipcademy.com/lessons/pairwise-alignment/identity-similarity
    """

    L = len(a)

    # number exact match
    identity = 0

    # similarity
    similarity = 0

    for i in range(L):
        if a[i] == b[i]:
            identity += 1

    s = f"{identity}/{L}"
    frac = Fraction(identity, L)
    f = float(frac)

    return s, f


def nw(s1, s2, verbose=True):

    if verbose:
        print("\nSTRINGS")
        print("~"*50)
        print(s1)
        print("~"*50)
        print(s2)
        print("~"*50)

    print("\n\nALIGNMENT") if verbose else None
    vals, letters = NW(s1, s2)

    a, b = traceback(letters, s1, s2)
    if verbose:
        print(repr(a))
        print(repr(b))

    print("\n\nSCORE") if verbose else None
    s = score(a, b)
    [print(v) for v in s] if verbose else None

    return s
