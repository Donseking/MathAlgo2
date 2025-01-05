"""
數學算法庫的集合，包含各種常用算法實現
"""

from ..linear_algebra import gauss_elimination, qr_decomposition
from .numerical import bisection_method, newton_method, simpson_integration
from .optimization import adam_optimizer, gradient_descent

__all__ = [
    # 數值方法
    "newton_method",
    "bisection_method",
    "simpson_integration",
    # 最佳化算法
    "gradient_descent",
    "adam_optimizer",
    # 線性代數
    "gauss_elimination",
    "qr_decomposition",
]
