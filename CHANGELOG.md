# Changelog

所有重要的版本更新都會記錄在這個文件中。

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，
並且本專案遵循 [Semantic Versioning](https://semver.org/lang/zh-TW/)。

## [0.4.1] - 2024-03-XX

### 新增 (Added)

- 視覺化模組 (visualization/)
  - 函數繪圖功能
    - plot_function: 繪製一般函數圖像
    - plot_optimization: 視覺化優化過程和等高線圖
  - 矩陣可視化功能
    - plot_matrix: 使用熱力圖展示矩陣
    - plot_eigenvalues: 視覺化矩陣特徵值分布
- 線性代數模組 (linear_algebra.py)
  - 高斯消去法 (gauss_elimination)
  - QR 分解 (qr_decomposition)
  - 矩陣運算和分析功能
- 新增相應的單元測試
  - test_visualization.py
  - test_linear_algebra.py

### 改進 (Enhanced)

- 性能監控模組 (monitoring.py)
  - 新增系統資訊監控功能
    - CPU 使用率和頻率
    - 記憶體使用情況
    - 網路介面統計
  - 改進時間複雜度分析
    - 支援自定義輸入生成器
    - 提供更詳細的分析結果
  - 完善文檔和類型提示

### 修改 (Changed)

- 重構算法目錄結構
  - 優化數值計算模組
  - 改進最佳化算法
  - 更新線性代數功能

### 依賴 (Dependencies)

- 添加 matplotlib 和 seaborn 作為繪圖依賴
- 添加 psutil 用於系統監控
- 添加 numpy 用於線性代數計算

## [0.4.0] - 2024-12-28

### 新增 (Added)

- 基礎數學運算功能
  - 微積分計算
  - 矩陣運算
  - 向量空間運算
  - 數學函數視覺化
- 資料結構實現
  - 二元樹
  - 堆疊和佇列
  - 鏈結串列
  - 圖結構
- 搜尋與圖論演算法
  - 二分搜尋和線性搜尋
  - DFS 和 BFS
  - Dijkstra 最短路徑
- 加密與編碼功能
  - 基礎編碼
  - 古典密碼
  - 現代加密
- 檔案處理工具
  - 多格式檔案讀寫
  - 檔案加密解密
- 日誌系統
  - 多級別日誌
  - 日誌輪轉
  - 性能監控

### 安全性 (Security)

- 實現基本的加密功能
- 添加檔案安全處理機制
