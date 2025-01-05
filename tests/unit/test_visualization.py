import numpy as np
import pytest

from mathalgo2.visualization import (
    plot_eigenvalues,
    plot_function,
    plot_matrix,
    plot_optimization,
)


def test_plot_function():
    f = lambda x: x**2
    plot_function(f, (-2, 2), title="Test Function")


def test_plot_optimization():
    f = lambda x: x[0] ** 2 + x[1] ** 2
    grad_f = lambda x: np.array([2 * x[0], 2 * x[1]])
    x0 = np.array([1.0, 1.0])

    plot_optimization(f, grad_f, (-2, 2), (-2, 2), x0)


def test_plot_matrix():
    A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    plot_matrix(A, title="Test Matrix")


def test_plot_eigenvalues():
    A = np.array([[1, -2], [2, 1]])
    plot_eigenvalues(A, title="Test Eigenvalues")
