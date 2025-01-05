"""
數值計算相關算法
"""
from typing import Callable, Tuple, Union

import numpy as np


def newton_method(
    f: Callable, df: Callable, x0: float, tol: float = 1e-6, max_iter: int = 100
) -> float:
    """
    牛頓法求根

    Parameters:
        f (callable): 目標函數
        df (callable): 目標函數的導數
        x0 (float): 初始猜測值
        tol (float): 收斂容差
        max_iter (int): 最大迭代次數

    Returns:
        float: 函數的根
    """
    x = x0
    for i in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        dfx = df(x)
        if dfx == 0:
            raise ValueError("導數為零，無法繼續迭代")
        x = x - fx / dfx
    raise RuntimeError(f"在{max_iter}次迭代後未收斂")


def bisection_method(
    f: Callable, a: float, b: float, tol: float = 1e-6, max_iter: int = 100
) -> float:
    """
    二分法求根

    Parameters:
        f (callable): 目標函數
        a (float): 區間左端點
        b (float): 區間右端點
        tol (float): 收斂容差
        max_iter (int): 最大迭代次數

    Returns:
        float: 函數的根
    """
    if f(a) * f(b) > 0:
        raise ValueError("區間端點函數值必須異號")

    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        if abs(fc) < tol:
            return c

        if f(a) * fc < 0:
            b = c
        else:
            a = c

    return (a + b) / 2


def simpson_integration(f: Callable, a: float, b: float, n: int = 1000) -> float:
    """
    辛普森積分法

    Parameters:
        f (callable): 被積函數
        a (float): 積分下限
        b (float): 積分上限
        n (int): 區間分割數（必須為偶數）

    Returns:
        float: 定積分值
    """
    if n % 2 != 0:
        n += 1

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)

    return h / 3 * (y[0] + y[-1] + 4 * sum(y[1:-1:2]) + 2 * sum(y[2:-1:2]))
