"""
函數繪圖相關功能
"""
from typing import Callable, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np

from ..algorithm.optimization import gradient_descent


def plot_function(
    f: Callable,
    x_range: Tuple[float, float],
    y_range: Optional[Tuple[float, float]] = None,
    title: str = "Function Plot",
    xlabel: str = "x",
    ylabel: str = "f(x)",
    grid: bool = True,
) -> None:
    """
    繪製函數圖像

    Parameters:
        f (callable): 要繪製的函數
        x_range (tuple): x軸範圍 (x_min, x_max)
        y_range (tuple, optional): y軸範圍 (y_min, y_max)
        title (str): 圖表標題
        xlabel (str): x軸標籤
        ylabel (str): y軸標籤
        grid (bool): 是否顯示網格
    """
    x = np.linspace(x_range[0], x_range[1], 1000)
    y = f(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, "b-", label=f"f(x)")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if y_range:
        plt.ylim(y_range)
    if grid:
        plt.grid(True)

    plt.legend()
    plt.show()


def plot_optimization(
    f: Callable,
    grad_f: Callable,
    x_range: Tuple[float, float],
    y_range: Tuple[float, float],
    x0: np.ndarray,
    method: str = "gradient_descent",
    n_iterations: int = 10,
) -> None:
    """
    視覺化優化過程

    Parameters:
        f (callable): 目標函數
        grad_f (callable): 梯度函數
        x_range (tuple): x軸範圍
        y_range (tuple): y軸範圍
        x0 (np.ndarray): 初始點
        method (str): 優化方法
        n_iterations (int): 迭代次數
    """
    # 創建網格點
    x = np.linspace(x_range[0], x_range[1], 100)
    y = np.linspace(y_range[0], y_range[1], 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    # 計算函數值
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = f(np.array([X[i, j], Y[i, j]]))

    # 繪製等高線圖
    plt.figure(figsize=(10, 8))
    plt.contour(X, Y, Z, levels=20)
    plt.colorbar(label="f(x, y)")

    # 執行優化並記錄路徑
    path = [x0]
    x = x0
    for _ in range(n_iterations):
        grad = grad_f(x)
        x = x - 0.1 * grad  # 簡單的梯度下降
        path.append(x)

    # 繪製優化路徑
    path = np.array(path)
    plt.plot(path[:, 0], path[:, 1], "r.-", label="Optimization path")
    plt.plot(x0[0], x0[1], "go", label="Start")
    plt.plot(path[-1, 0], path[-1, 1], "ro", label="End")

    plt.title("Optimization Process Visualization")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()
