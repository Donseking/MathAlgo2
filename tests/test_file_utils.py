import json
import os
import shutil
import sys
import time
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from PIL import Image

from mathalgo2.FileUtlies import DataAnalyzer, FileIO, FileProcessor
from mathalgo2.loading import ProgressBar


# ====== Fixtures ======
@pytest.fixture
def test_dir(tmp_path):
    """創建臨時測試目錄"""
    return tmp_path


@pytest.fixture
def test_files(test_dir):
    """創建測試用的檔案"""
    # 創建文本文件
    text_file = test_dir / "test.txt"
    text_file.write_text("Hello, World!")

    # 創建 JSON 文件
    json_file = test_dir / "test.json"
    json_file.write_text('{"key": "value"}')

    # 創建 CSV 文件
    csv_file = test_dir / "test.csv"
    pd.DataFrame({"A": [1, 2], "B": ["x", "y"]}).to_csv(csv_file, index=False)

    return {"text": text_file, "json": json_file, "csv": csv_file}


@pytest.fixture
def sample_df():
    """創建測試用的 DataFrame"""
    np.random.seed(42)
    return pd.DataFrame(
        {
            "numeric": np.random.normal(0, 1, 100),
            "category": np.random.choice(["A", "B", "C"], 100),
            "missing": np.random.choice([1, np.nan], 100),
        }
    )


@pytest.fixture
def large_test_file(test_dir):
    """創建大型測試文件"""
    file_path = test_dir / "large_test.txt"
    with open(file_path, "wb") as f:
        f.write(b"0" * (1024 * 100))  # 100KB
    return file_path


@pytest.fixture
def capture_output(capsys):
    """使用 pytest 的 capsys 來捕獲輸出"""
    return capsys


# ====== ProgressBar Tests ======
class TestProgressBar:
    def test_progress_bar_basic(self, capture_output):
        """測試基本進度條功能"""
        with ProgressBar(total=100, desc="Test") as bar:
            bar.update(50)
            captured = capture_output.readouterr()
            assert "50.0%" in captured.out

    def test_progress_bar_with_filename(self, capture_output):
        """測試帶檔案名的進度條"""
        with ProgressBar(total=100, desc="Test") as bar:
            bar.update(50, "test.txt")
            captured = capture_output.readouterr()
            assert "test.txt" in captured.out


# ====== FileIO Tests ======
class TestFileIO:
    def setup_method(self, method):
        self.file_io = FileIO()

    def test_read_file_success(self, test_files):
        """測試成功讀取文本文件"""
        content = self.file_io.read_file(path=str(test_files["text"]))
        assert content == "Hello, World!"

    def test_read_file_with_encoding(self, test_dir):
        """測試使用不同編碼讀取文件"""
        file_path = test_dir / "encoded.txt"
        content = "測試中文"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        assert self.file_io.read_file(path=str(file_path), encoding="utf-8") == content

    def test_read_nonexistent_file(self):
        """測試讀取不存在的文件"""
        with pytest.raises(FileNotFoundError):
            self.file_io.read_file(path="nonexistent.txt")

    def test_write_file_success(self, test_dir):
        """測試成功寫入文件"""
        file_path = test_dir / "output.txt"
        content = "Test content"
        self.file_io.write_file(str(file_path), content)

        assert file_path.read_text() == content

    def test_json_operations(self, test_dir):
        """測試 JSON 操作"""
        file_path = test_dir / "test.json"
        test_data = {"name": "test", "values": [1, 2, 3]}
        self.file_io.write_json(str(file_path), test_data)
        loaded_data = self.file_io.read_json(str(file_path))
        assert loaded_data == test_data

    def test_csv_operations(self, test_dir):
        """測試 CSV 操作"""
        file_path = test_dir / "test.csv"
        df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})

        # 測試寫入
        self.file_io.write_csv(str(file_path), df)

        # 測試讀取，使用 cast 確保類型
        loaded_df = pd.DataFrame(self.file_io.read_csv(str(file_path)))
        pd.testing.assert_frame_equal(loaded_df, df)

    def test_list_files(self, test_files):
        """測試列出目錄文件"""
        files = self.file_io.list_files(str(test_files["text"].parent))
        assert len(files) == 3  # text, json, csv
        assert any("test.txt" in f for f in files)


# ====== FileIO Tests with ProgressBar ======
class TestFileIOWithProgress:
    def setup_method(self, method):
        self.file_io = FileIO()

    def test_read_file_with_progress(self, large_test_file, capture_output):
        """測試檔案讀取時的進度條"""
        self.file_io.read_file(path=str(large_test_file))
        captured = capture_output.readouterr()

        # 檢查進度條顯示
        assert "Reading" in captured.out
        assert os.path.basename(str(large_test_file)) in captured.out
        assert "100.0%" in captured.out

    def test_write_file_with_progress(self, test_dir, capture_output):
        """測試檔案寫入時的進度條"""
        file_path = test_dir / "output.txt"
        content = "0" * (1024 * 100)  # 100KB
        self.file_io.write_file(str(file_path), content)
        captured = capture_output.readouterr()

        # 檢查進度條顯示
        assert "Writing" in captured.out
        assert os.path.basename(str(file_path)) in captured.out
        assert "100.0%" in captured.out

    def test_progress_bar_speed_format(self):
        """測試進度條速度格式化"""
        bar = ProgressBar(total=100)
        assert "B/s" in bar._format_speed(500)
        assert "KB/s" in bar._format_speed(1500)
        assert "MB/s" in bar._format_speed(1500000)

    def test_progress_bar_time_format(self):
        """測試進度條時間格式化"""
        bar = ProgressBar(total=100)
        assert "s" in bar._format_time(30)
        assert "m" in bar._format_time(90)
        assert "h" in bar._format_time(3600)


# ====== FileProcessor Tests ======
class TestFileProcessor:
    def test_compression_operations(self, test_files, test_dir):
        """測試壓縮和解壓縮操作"""
        processor = FileProcessor()
        zip_path = test_dir / "archive.zip"
        extract_path = test_dir / "extracted"

        # 測試壓縮
        processor.compress_files([str(f) for f in test_files.values()], str(zip_path))
        assert zip_path.exists()

        # 測試解壓縮
        processor.extract_files(str(zip_path), str(extract_path))
        assert (extract_path / "test.txt").exists()

    def test_encryption_operations(self, test_files):
        """測試加密和解密操作"""
        processor = FileProcessor()
        encrypted_path = test_files["text"].parent / "encrypted.bin"
        decrypted_path = test_files["text"].parent / "decrypted.txt"

        # 測試加密
        processor.encrypt_file(str(test_files["text"]), str(encrypted_path))
        assert encrypted_path.exists()

        # 測試解密
        processor.decrypt_file(str(encrypted_path), str(decrypted_path))
        assert decrypted_path.read_text() == test_files["text"].read_text()

    def test_backup_operations(self, test_files):
        """測試文件備份"""
        processor = FileProcessor()
        backup_path = processor.backup_file(str(test_files["text"]))
        assert Path(backup_path).exists()


# ====== DataAnalyzer Tests ======
class TestDataAnalyzer:
    def test_analyze_data(self, sample_df):
        """測試數據分析"""
        results = DataAnalyzer.analyze_data(sample_df)

        assert "summary" in results
        assert "missing" in results
        assert "shape" in results
        assert results["shape"] == (100, 3)

    def test_visualization(self, test_dir, sample_df):
        """測試數據視覺化"""
        plot_path = test_dir / "plot.png"

        # 測試直方圖
        DataAnalyzer.create_visualization(
            sample_df,
            "histogram",
            column="numeric",
            save_path=str(plot_path),
            show=False,
        )
        assert plot_path.exists()

        # 測試散點圖
        plot_path = test_dir / "scatter.png"
        DataAnalyzer.create_visualization(
            sample_df,
            "scatter",
            x="numeric",
            y="numeric",
            save_path=str(plot_path),
            show=False,
        )
        assert plot_path.exists()

    def test_data_processing(self, sample_df):
        """測試數據處理"""
        # 測試填充缺失值
        filled_df = DataAnalyzer.process_data(sample_df, "fillna", value=0)
        assert not filled_df["missing"].isnull().any()

        # 測試標準化
        normalized_df = DataAnalyzer.process_data(sample_df[["numeric"]], "normalize")
        assert abs(normalized_df["numeric"].mean()) < 0.01
        assert abs(normalized_df["numeric"].std() - 1) < 0.01

        # 測試排序
        sorted_df = DataAnalyzer.process_data(sample_df, "sort", column="numeric")
        assert sorted_df["numeric"].is_monotonic_increasing
