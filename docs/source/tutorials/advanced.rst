進階使用指南
==========

最佳化演算法
----------

1. 遺傳演算法
~~~~~~~~~~~

.. code-block:: python

    from mathalgo2.algorithm.optimizers import GeneticAlgorithm

    def objective_func(x):
        return x[0]**2 + x[1]**2

    ga = GeneticAlgorithm(
        objective_func=objective_func,
        bounds=[(-5, 5), (-5, 5)],
        population_size=50
    )

    solution, fitness = ga._optimize(max_iter=100)

2. 圖論演算法
~~~~~~~~~~~

.. code-block:: python

    from mathalgo2.algorithm.GraphAlgo import GraphAlgo

    # 創建圖結構
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'D'],
        'D': ['B', 'C']
    }

    graph_algo = GraphAlgo(graph)
    path = graph_algo.shortest_path('A', 'D')
