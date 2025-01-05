"""
矩陣可視化相關功能
"""
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_matrix(
    A: np.ndarray,
    title: str = "Matrix Visualization",
    cmap: str = "viridis",
    annot: bool = True,
) -> None:
    """
    視覺化矩陣

    Parameters:
        A (np.ndarray): 要視覺化的矩陣
        title (str): 圖表標題
        cmap (str): 顏色映射
        annot (bool): 是否顯示數值標註
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(A, cmap=cmap, annot=annot, fmt=".2f")
    plt.title(title)
    plt.show()


def plot_eigenvalues(
    A: np.ndarray, title: str = "Eigenvalue Distribution", size: int = 100
) -> None:
    """
    視覺化矩陣的特徵值分布

    Parameters:
        A (np.ndarray): 方陣
        title (str): 圖表標題
        size (int): 點的大小
    """
    eigenvals = np.linalg.eigvals(A)

    plt.figure(figsize=(8, 8))
    plt.scatter(eigenvals.real, eigenvals.imag, s=size)
    plt.axhline(y=0, color="k", linestyle="-", alpha=0.3)
    plt.axvline(x=0, color="k", linestyle="-", alpha=0.3)
    plt.grid(True)
    plt.title(title)
    plt.xlabel("Real Part")
    plt.ylabel("Imaginary Part")

    # 設置相等的軸比例
    plt.axis("equal")
    plt.show()
