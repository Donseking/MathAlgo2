"""
最佳化算法
"""
from typing import Callable, Optional, Tuple

import numpy as np


def gradient_descent(
    f: Callable,
    grad_f: Callable,
    x0: np.ndarray,
    learning_rate: float = 0.1,
    tol: float = 1e-6,
    max_iter: int = 1000,
) -> np.ndarray:
    """
    梯度下降法

    Parameters:
        f (callable): 目標函數
        grad_f (callable): 梯度函數
        x0 (array-like): 初始點
        learning_rate (float): 學習率
        tol (float): 收斂容差
        max_iter (int): 最大迭代次數

    Returns:
        array-like: 最優解
    """
    x = x0
    for i in range(max_iter):
        grad = grad_f(x)
        if np.linalg.norm(grad) < tol:
            return x
        x = x - learning_rate * grad
    return x


def adam_optimizer(
    f: Callable,
    grad_f: Callable,
    x0: np.ndarray,
    learning_rate: float = 0.001,
    beta1: float = 0.9,
    beta2: float = 0.999,
    epsilon: float = 1e-8,
    max_iter: int = 1000,
) -> np.ndarray:
    """
    Adam優化算法

    Parameters:
        f (callable): 目標函數
        grad_f (callable): 梯度函數
        x0 (array-like): 初始點
        learning_rate (float): 學習率
        beta1 (float): 一階矩估計的指數衰減率
        beta2 (float): 二階矩估計的指數衰減率
        epsilon (float): 數值穩定性係數
        max_iter (int): 最大迭代次數

    Returns:
        array-like: 最優解
    """
    x = x0
    m = np.zeros_like(x)
    v = np.zeros_like(x)

    for t in range(1, max_iter + 1):
        g = grad_f(x)
        m = beta1 * m + (1 - beta1) * g
        v = beta2 * v + (1 - beta2) * g**2

        m_hat = m / (1 - beta1**t)
        v_hat = v / (1 - beta2**t)

        x = x - learning_rate * m_hat / (np.sqrt(v_hat) + epsilon)

    return x


def conjugate_gradient(
    A: np.ndarray,
    b: np.ndarray,
    x0: np.ndarray,
    tol: float = 1e-6,
    max_iter: int = 1000,
) -> np.ndarray:
    """
    共軛梯度法求解線性方程組 Ax = b

    Parameters:
        A (np.ndarray): 對稱正定矩陣
        b (np.ndarray): 常數向量
        x0 (np.ndarray): 初始猜測
        tol (float): 收斂容差
        max_iter (int): 最大迭代次數

    Returns:
        np.ndarray: 解向量
    """
    x = x0
    r = b - np.dot(A, x)
    p = r.copy()

    for i in range(max_iter):
        Ap = np.dot(A, p)
        alpha = np.dot(r, r) / np.dot(p, Ap)
        x += alpha * p
        r_new = r - alpha * Ap

        if np.linalg.norm(r_new) < tol:
            return x

        beta = np.dot(r_new, r_new) / np.dot(r, r)
        p = r_new + beta * p
        r = r_new

    return x
