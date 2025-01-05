"""
性能監控模組

此模組提供了一個名為 PerformanceMonitor 的類，用於監控和分析系統性能。
主要功能包括：
- 獲取系統資訊，如 CPU 和記憶體使用情況
- 追蹤函數的執行時間
- 分析函數的時間複雜度

Classes:
    PerformanceMonitor: 提供性能監控和分析功能的類

Examples:
    >>> from mathalgo2.monitoring import PerformanceMonitor
    >>> monitor = PerformanceMonitor()
    >>> system_info = monitor.get_system_info()
    >>> print(system_info['cpu_percent'])
    >>> @monitor.track_time
    ... def slow_function():
    ...     time.sleep(1)
    >>> slow_function()
    >>> complexity = monitor.analyze_complexity(slow_function, [10, 100, 1000])
    >>> print(complexity['estimated_complexity'])
"""

import platform
import time
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import psutil


class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        self.complexity_data = {}

    def get_system_info(self) -> Dict[str, Any]:
        """
        獲取系統資訊

        Returns:
            Dict[str, Any]: 包含系統資訊的字典

        Examples:
            >>> monitor = PerformanceMonitor()
            >>> system_info = monitor.get_system_info()
            >>> print(system_info['cpu_percent'])
        """
        info = {
            # CPU 資訊
            "cpu_percent": psutil.cpu_percent(interval=1),
            "cpu_count": psutil.cpu_count(),
            "cpu_freq": psutil.cpu_freq().current
            if hasattr(psutil.cpu_freq(), "current")
            else None,
            # 記憶體資訊
            "memory": {
                "total": psutil.virtual_memory().total / (1024**3),  # GB
                "available": psutil.virtual_memory().available / (1024**3),  # GB
                "percent": psutil.virtual_memory().percent,
            },
            # 網路資訊
            "network": {},
            # 系統資訊
            "system": {
                "system": platform.system(),
                "version": platform.version(),
                "machine": platform.machine(),
            },
        }

        # 獲取網路介面資訊
        net_io = psutil.net_io_counters(pernic=True)
        for interface, stats in net_io.items():
            info["network"][interface] = {
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv,
                "packets_sent": stats.packets_sent,
                "packets_recv": stats.packets_recv,
            }

        return info

    def track_time(self, func: Callable) -> Callable:
        """
        追蹤函數執行時間的裝飾器

        Args:
            func (Callable): 要監控的函數

        Returns:
            Callable: 包裝後的函數
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            self.metrics[func.__name__] = end - start
            return result

        return wrapper

    def analyze_complexity(
        self,
        func: Callable,
        input_sizes: List[int],
        input_generator: Optional[Callable[[int], Tuple]] = None,
    ) -> dict:
        """
        分析函數的時間複雜度

        Args:
            func (Callable): 要分析的函數
            input_sizes (List[int]): 不同的輸入大小
            input_generator (Callable): 生成測試輸入的函數，預設為None

        Returns:
            dict: 包含複雜度分析結果的字典
        """
        execution_times = []

        if input_generator is None:
            input_generator = lambda n: (n,)

        for size in input_sizes:
            start = time.time()
            func(*input_generator(size))
            end = time.time()
            execution_times.append(end - start)

        x = np.log(input_sizes)
        y = np.log(execution_times)
        coefficient = np.polyfit(x, y, 1)[0]

        complexities = {
            0: "O(1)",
            0.5: "O(√n)",
            1: "O(n)",
            2: "O(n²)",
            3: "O(n³)",
            float("inf"): "O(2ⁿ)",
        }

        closest_complexity = min(
            complexities.keys(), key=lambda k: abs(k - coefficient)
        )

        result = {
            "input_sizes": input_sizes,
            "execution_times": execution_times,
            "coefficient": coefficient,
            "estimated_complexity": complexities[closest_complexity],
        }

        self.complexity_data[func.__name__] = result
        return result
