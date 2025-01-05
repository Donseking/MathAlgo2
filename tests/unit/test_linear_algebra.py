import numpy as np
import pytest

from mathalgo2.linear_algebra import gauss_elimination, qr_decomposition


def test_gauss_elimination():
    # 測試簡單的線性方程組
    A = np.array([[2, 1], [1, 3]], dtype=float)
    b = np.array([4, 5], dtype=float)
    x = gauss_elimination(A, b)
    assert np.allclose(np.dot(A, x), b)

    # 測試奇異矩陣
    A_singular = np.array([[1, 1], [1, 1]], dtype=float)
    b_singular = np.array([2, 2], dtype=float)
    with pytest.raises(Exception):  # 應該處理奇異矩陣的情況
        gauss_elimination(A_singular, b_singular)


def test_qr_decomposition():
    # 測試QR分解
    A = np.array([[1, -1], [1, 1], [1, 1]], dtype=float)
    Q, R = qr_decomposition(A)

    # 檢查Q是否正交
    assert np.allclose(np.dot(Q.T, Q), np.eye(2))

    # 檢查R是否上三角
    assert np.allclose(np.tril(R, k=-1), 0)

    # 檢查分解結果
    assert np.allclose(np.dot(Q, R), A)
