快速入門
=======

基本使用
-------

1. 基礎數學運算
~~~~~~~~~~~~~~

.. code-block:: python

    from mathalgo2.BaseMath import Calculus

    # 創建一個微積分計算器
    calc = Calculus("x^2 + 2*x + 1")

    # 計算導數
    derivative = calc.derivative()
    print(f"導數: {derivative}")  # 輸出: 2*x + 2

    # 計算定積分
    integral = calc.definite_integral(0, 1)
    print(f"從0到1的定積分: {integral}")

2. 檔案處理
~~~~~~~~~~

.. code-block:: python

    from mathalgo2.FileUtlies import FileIO, DataAnalyzer

    # 讀取檔案
    file_handler = FileIO()
    content = file_handler.read_file("data.txt")

    # 數據分析
    analyzer = DataAnalyzer()
    df = analyzer.read_csv("data.csv")
    analyzer.create_visualization(df, 'histogram', column='values')

3. 性能監控
~~~~~~~~~~

.. code-block:: python

    from mathalgo2.monitoring import PerformanceMonitor

    monitor = PerformanceMonitor()

    @monitor.track_time
    def my_function():
        # 你的代碼
        pass

    my_function()
    print(f"執行時間: {monitor.metrics['my_function']}秒")
