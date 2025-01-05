# MathAlgo2 數學演算法工具包

## 專案簡介

MathAlgo2 是一個全面的 Python 數學演算法與資料處理工具包，提供多樣化的演算法實現、視覺化功能、檔案處理工具以及數據分析功能。本工具包適合研究人員、數據分析師以及需要進行演算法分析和資料處理的開發者使用。

## 版本資訊

- 當前版本：0.4.1
- 發布日期：2024-03-XX
- 更新日誌：
  - 0.4.1 (2024-03-XX)
    - 新增視覺化模組（函數繪圖、矩陣可視化）
    - 新增線性代數模組（高斯消去法、QR 分解）
    - 改進性能監控功能（系統監控、複雜度分析）
  - 0.4.0 (2024-12-28)
    - 基礎數學運算功能
    - 進階演算法功能
    - 實用工具

## 安裝需求

### 基本依賴

```bash
pip install -r requirements.txt
```

### 開發依賴

```bash
pip install -r requirements-dev.txt
```

## 快速開始

```python
# 基本數學運算
from mathalgo2.BaseMath import Calculus
calc = Calculus("x**2 + 2*x + 1")
result = calc.definite_integral(0, 1)

# 視覺化功能
from mathalgo2.visualization import plot_function
f = lambda x: x**2
plot_function(f, (-2, 2), title="Quadratic Function")

# 線性代數運算
from mathalgo2.linear_algebra import gauss_elimination
import numpy as np
A = np.array([[2, 1], [1, 3]])
b = np.array([4, 5])
x = gauss_elimination(A, b)
```

## 文檔

完整文檔請訪問：[專案文檔](docs/build/html/index.html)

## 貢獻指南

1. Fork 本專案
2. 創建特性分支 (`git checkout -b feature/新功能`)
3. 提交更改 (`git commit -m '新增某功能'`)
4. 推送分支 (`git push origin feature/新功能`)
5. 提交 Pull Request

## 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 作者

- Donseking - [GitHub](https://github.com/Donseking)
- Email: 0717albert@gmail.com
