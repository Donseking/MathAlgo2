import numpy as np
import pytest

from mathalgo2.algorithm.optimization import adam_optimizer, gradient_descent


def test_gradient_descent():
    # 測試二次函數最小化
    f = lambda x: x[0] ** 2 + x[1] ** 2
    grad_f = lambda x: np.array([2 * x[0], 2 * x[1]])

    x0 = np.array([1.0, 1.0])
    result = gradient_descent(f, grad_f, x0)
    assert np.all(np.abs(result) < 1e-5)


def test_adam_optimizer():
    # 測試 Rosenbrock 函數最小化
    def f(x):
        return (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2

    def grad_f(x):
        dx0 = -2 * (1 - x[0]) - 400 * x[0] * (x[1] - x[0] ** 2)
        dx1 = 200 * (x[1] - x[0] ** 2)
        return np.array([dx0, dx1])

    x0 = np.array([-1.0, 1.0])
    result = adam_optimizer(f, grad_f, x0)
    assert np.allclose(result, np.array([1.0, 1.0]), atol=1e-2)
