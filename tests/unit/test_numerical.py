import numpy as np
import pytest

from mathalgo2.algorithm.numerical import (
    bisection_method,
    newton_method,
    simpson_integration,
)


def test_newton_method():
    # 測試函數 f(x) = x^2 - 4
    f = lambda x: x**2 - 4
    df = lambda x: 2 * x

    result = newton_method(f, df, x0=3.0)
    assert abs(result - 2.0) < 1e-6


def test_newton_method_error():
    # 測試錯誤情況
    with pytest.raises(ValueError):
        newton_method(lambda x: x, lambda x: 0, x0=1.0)


def test_bisection_method():
    f = lambda x: x**2 - 4
    result = bisection_method(f, 0, 3)
    assert abs(result - 2.0) < 1e-6

    with pytest.raises(ValueError):
        bisection_method(f, 1, 3)  # 測試區間端點函數值同號的情況


def test_simpson_integration():
    # 測試 sin(x) 在 [0, pi] 上的積分，結果應該為 2
    f = lambda x: np.sin(x)
    result = simpson_integration(f, 0, np.pi)
    assert abs(result - 2.0) < 1e-6
