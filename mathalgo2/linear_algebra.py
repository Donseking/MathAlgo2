"""
線性代數算法模組
"""
from typing import List, Optional, Tuple, Union

import numpy as np


def gauss_elimination(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    高斯消去法求解線性方程組 Ax = b

    Parameters:
        A (np.ndarray): 係數矩陣
        b (np.ndarray): 常數向量

    Returns:
        np.ndarray: 解向量
    """
    n = len(A)
    # 建立增廣矩陣
    Ab = np.concatenate((A, b.reshape(n, 1)), axis=1)

    # 前向消去
    for i in range(n):
        # 選主元
        pivot = abs(Ab[i:, i]).argmax() + i
        if pivot != i:
            Ab[i], Ab[pivot] = Ab[pivot].copy(), Ab[i].copy()

        for j in range(i + 1, n):
            factor = Ab[j, i] / Ab[i, i]
            Ab[j, i:] -= factor * Ab[i, i:]

    # 回代求解
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i + 1 : n], x[i + 1 :])) / Ab[i, i]

    return x


def qr_decomposition(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    QR分解，使用Gram-Schmidt正交化

    Parameters:
        A (np.ndarray): 待分解矩陣

    Returns:
        Tuple[np.ndarray, np.ndarray]: (Q, R)，其中Q為正交矩陣，R為上三角矩陣
    """
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))

    for j in range(n):
        v = A[:, j].copy()
        for i in range(j):
            R[i, j] = np.dot(Q[:, i], A[:, j])
            v -= R[i, j] * Q[:, i]
        R[j, j] = np.linalg.norm(v)
        Q[:, j] = v / R[j, j]

    return Q, R
