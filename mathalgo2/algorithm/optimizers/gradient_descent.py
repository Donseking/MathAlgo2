from mathalgo2.algorithm.OpAlgo import BaseOptimizer
import numpy as np
from typing import Tuple

class GradientDescent(BaseOptimizer):
    def __init__(self, objective_func, bounds, learning_rate=0.01):
        """初始化梯度下降算法
        
        Args:
            objective_func: 目標函數
            bounds: 解的範圍限制
            learning_rate: 學習率，控制每次更新的步長
        """
        super().__init__(objective_func, bounds)
        self.learning_rate = learning_rate
        self.logger.info(f"初始化GradientDescent最佳化器，學習率: {self.learning_rate}")

    def optimize(self, max_iter=1000, epsilon=1e-6) -> Tuple[np.ndarray, float]:
        """執行梯度下降最佳化
        
        Args:
            max_iter: 最大迭代次數
            epsilon: 用於計算數值梯度的微小變量
        
        Returns:
            Tuple[np.ndarray, float]: (最佳解, 最佳適應度值)
        """
        # 初始化解
        current_solution = self._initialize_solution()
        self.logger.info(f"初始解: {current_solution}")

        for i in range(max_iter):
            # 計算數值梯度
            gradient = np.zeros(self.dimension)
            for j in range(self.dimension):
                h = np.zeros(self.dimension)
                h[j] = epsilon
                gradient[j] = (self.objective_func(current_solution + h) - 
                               self.objective_func(current_solution - h)) / (2 * epsilon)
            self.logger.debug(f"迭代 {i}: 計算梯度: {gradient}")

            # 更新解
            current_solution = self._clip_to_bounds(
                current_solution - self.learning_rate * gradient
            )
            current_fitness = self.objective_func(current_solution)
            self.logger.info(f"迭代 {i}: 更新解: {current_solution}, 適應度: {current_fitness}")

            # 更新最佳解
            self._update_best_solution(current_solution, current_fitness, i)
            self.history.append(self.best_fitness)
            self._update_plot(i)

        self.logger.info(f"最佳化完成，最佳解: {self.best_solution}, 最佳適應度: {self.best_fitness}")
        return self.best_solution, self.best_fitness 