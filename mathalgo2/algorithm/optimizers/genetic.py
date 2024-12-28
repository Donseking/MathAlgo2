from mathalgo2.algorithm.OpAlgo import BaseOptimizer
import numpy as np
from typing import Tuple

class GeneticAlgorithm(BaseOptimizer):
    def __init__(self, objective_func, bounds, population_size=50):
        """初始化遺傳算法
        
        Args:
            objective_func: 目標函數
            bounds: 解的範圍限制
            population_size: 種群大小，默認為50
        """
        super().__init__(objective_func, bounds)
        self.population_size = population_size
        self.logger.info(f"初始化GeneticAlgorithm最佳化器，種群大小: {population_size}")

    def _optimize(self, generations=100, mutation_rate=0.1, **kwargs) -> Tuple[np.ndarray, float]:
        # 使用實例變數 self.population_size
        population = np.array([self._initialize_solution() for _ in range(self.population_size)])
        self.logger.info(f"初始種群生成完成，種群大小: {self.population_size}")
        
        for generation in range(generations):
            # 計算適應度
            fitness_values = np.array([self.objective_func(ind) for ind in population])
            self.logger.debug(f"世代 {generation}: 計算適應度值完成")
            
            # 更新最佳解
            best_idx = np.argmin(fitness_values)
            self._update_best_solution(population[best_idx], fitness_values[best_idx], generation)
            self.history.append(self.best_fitness)
            self.logger.info(f"世代 {generation}: 最佳適應度: {self.best_fitness}")
            
            # 更新圖表
            self._update_plot(generation)
            
            # 計算選擇概率（使用適應度的倒數）
            selection_probs = 1 / (fitness_values + 1e-10)
            selection_probs = selection_probs / np.sum(selection_probs)
            
            # 選擇父代
            parents_idx = np.random.choice(
                len(population),  # 修改這裡：使用種群長度而不是 self.population_size
                size=(self.population_size // 2, 2),
                p=selection_probs  # 使用計算好的概率
            )
            
            # 交叉和變異
            new_population = []
            for p1_idx, p2_idx in parents_idx:
                # 交叉
                child = (population[p1_idx] + population[p2_idx]) / 2
                
                # 變異
                if np.random.random() < mutation_rate:
                    child += np.random.normal(0, 0.1, self.dimension)
                
                new_population.append(self._clip_to_bounds(child))
            
            population = np.array(new_population)
            self.logger.debug(f"世代 {generation}: 新種群生成完成")
        
        self.logger.info(f"最佳化完成，最佳解: {self.best_solution}, 最佳適應度: {self.best_fitness}")
        return self.best_solution, self.best_fitness 