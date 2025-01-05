使用範例
===============================

基礎數學運算
--------------------------------

.. code-block:: python

    from mathalgo2.BaseMath import Calculus
    calc = Calculus("x**2 + 2*x + 1")
    result = calc.definite_integral(0, 1)

視覺化功能
--------------------------------

.. code-block:: python

    from mathalgo2.visualization import plot_function
    f = lambda x: x**2
    plot_function(f, (-2, 2), title="Quadratic Function")
