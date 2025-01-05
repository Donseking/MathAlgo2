"""
檔案處理工具模組

提供檔案操作、處理和分析的功能：
- 基礎檔案讀寫
- 檔案格式轉換
- 檔案加密解密
- 數據分析和視覺化

Classes:
    FileIO: 基礎檔案操作
    FileProcessor: 進階檔案處理
    DataAnalyzer: 數據分析工具

Examples:
    >>> from mathalgo2.FileUtlies import FileIO
    >>> file_handler = FileIO()
    >>> content = file_handler.read_file("example.txt")
"""

import csv
import hashlib
import json
import os
import shutil
import time
import zipfile
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import cv2
import imageio.v2 as imageio
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from cryptography.fernet import Fernet
from PIL import Image

from mathalgo2.Logger import Logger, logging

from .loading import ProgressBar

ROOT_DIR = Path(__file__).parent.parent
log_file = ROOT_DIR / "__log__" / "file_utiles.log"

logger_manager = Logger(name="file_utiles", log_file=str(log_file), level=logging.INFO)

__all__ = ["FileIO", "FileProcessor", "DataAnalyzer"]


class FileIO:
    """檔案輸入輸出處理類

    此類負責處理所有基本的檔案讀寫操作，支援多種檔案格式。

    主要功能：
        - 一般文字檔案的讀寫
        - JSON 格式檔案的處理
        - CSV 格式檔案的處理
        - 目錄檔案列表獲取

    使用範例：
        file_io = FileIO()
        content = file_io.read_file("example.txt")
        json_data = file_io.read_json("config.json")
        csv_data = file_io.read_csv("data.csv")
    """

    def read_file(self, path: str, encoding: str = "utf-8") -> str:
        """
        讀取文件內容

        Args:
            path (str): 檔案路徑
            encoding (str, optional): 檔案編碼. 默認為 'utf-8'

        Returns:
            str: 檔案內容

        Raises:
            FileNotFoundError: 檔案不存在時拋出
            IOError: 讀取錯誤時拋出
        """
        logger_manager.info(f"開始讀取檔案: {path}")

        try:
            # 獲取檔案大小
            file_size = os.path.getsize(path)
            current_size = 0
            chunks = []
            filename = os.path.basename(path)  # 獲取檔案名

            # 直接使用進度條
            print(f"\n讀取檔案: {filename}")
            with ProgressBar(total=file_size, desc="Reading") as bar:
                with open(path, "rb") as file:
                    while True:
                        chunk = file.read(1024)  # 1KB chunks
                        if not chunk:
                            break
                        chunks.append(chunk)
                        current_size += len(chunk)
                        bar.update(current_size, filename)  # 傳遞檔案名
                        time.sleep(0.2)  # 200ms 延遲

            # 合併並解碼
            content = b"".join(chunks).decode(encoding)
            logger_manager.info(f"成功讀取檔案: {path}")
            return content

        except FileNotFoundError:
            logger_manager.error(f"檔案不存在: {path}")
            raise
        except Exception as e:
            logger_manager.error(f"讀取檔案時發生錯誤: {str(e)}")
            raise

    def write_file(self, file_path: str, content: str, encoding: str = "utf-8") -> None:
        """寫入一般檔案"""
        try:
            # 編碼內容
            content_bytes = content.encode(encoding)
            total_size = len(content_bytes)
            current_size = 0
            filename = os.path.basename(file_path)  # 獲取檔案名

            # 直接使用進度條
            print(f"\n寫入檔案: {filename}")
            with ProgressBar(total=total_size, desc="Writing") as bar:
                with open(file_path, "wb") as file:
                    for i in range(0, total_size, 1024):  # 1KB chunks
                        chunk = content_bytes[i : i + 1024]
                        file.write(chunk)
                        current_size += len(chunk)
                        bar.update(current_size, filename)  # 傳遞檔案名
                        time.sleep(0.2)  # 200ms 延遲

        except Exception as e:
            logger_manager.error(f"寫入錯誤: {str(e)}")
            raise

    def read_json(self, file_path: str) -> Dict:
        """讀取 JSON 檔案"""
        try:
            # 使用 read_file 來獲得進度條效果
            content = self.read_file(file_path, encoding="utf-8")
            return json.loads(content)
        except Exception as e:
            logger_manager.error(f"JSON 讀取錯誤: {str(e)}")
            raise

    def write_json(self, file_path: str, data: Dict, indent: int = 4) -> None:
        """寫入 JSON 檔案"""
        try:
            # 先轉換為字串
            content = json.dumps(data, indent=indent, ensure_ascii=False)
            # 使用 write_file 來獲得進度條效果
            self.write_file(file_path, content, encoding="utf-8")
        except Exception as e:
            logger_manager.error(f"JSON 寫入錯誤: {str(e)}")
            raise

    def read_csv(self, file_path: str, has_header: bool = True) -> pd.DataFrame:
        """讀取 CSV 檔案"""
        try:
            content = self.read_file(file_path, encoding="utf-8")
            return pd.read_csv(StringIO(content))
        except Exception as e:
            logger_manager.error(f"CSV 讀取錯誤: {str(e)}")
            raise

    def write_csv(
        self,
        file_path: str,
        data: Union[pd.DataFrame, List],
        header: Optional[List[str]] = None,
    ) -> None:
        """寫入 CSV 檔案"""
        try:
            if isinstance(data, pd.DataFrame):
                content = data.to_csv(index=False)
            else:
                df = pd.DataFrame(data, columns=header)
                content = df.to_csv(index=False)
            # 使用 write_file 來獲得進度條效果
            self.write_file(file_path, content, encoding="utf-8")
        except Exception as e:
            logger_manager.error(f"CSV 寫入錯誤: {str(e)}")
            raise

    def list_files(self, dir_path: str, pattern: str = "*") -> List[str]:
        """列出目錄中的檔案"""
        return [str(f) for f in Path(dir_path).glob(pattern) if f.is_file()]


class FileProcessor:
    """檔案處理類

    此類提供進階的檔案處理功能，包括檔案的壓縮、加密和圖片處理等操作。

    主要功能：
        - 檔案壓縮與解壓縮
        - 檔案加密與解密
        - 圖片處理（調整大小、旋轉、濾鏡等）
        - 檔案備份

    屬性：
        key (bytes): 加密金鑰
        cipher_suite (Fernet): 加密工具實例

    使用範例：
        processor = FileProcessor()
        processor.compress_files(['file1.txt', 'file2.txt'], 'archive.zip')
        processor.encrypt_file('sensitive.txt', 'encrypted.bin')
    """

    def __init__(self):
        """初始化 FileProcessor 實例並生成加密金鑰"""
        logger_manager.info("初始化 FileProcessor")
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        logger_manager.debug("加密金鑰已生成")

    def compress_files(self, file_paths: List[str], output_path: str) -> None:
        """將多個檔案壓縮為一個 ZIP 檔案

        Args:
            file_paths (List[str]): 要壓縮的檔案路徑列表
            output_path (str): 輸出的 ZIP 檔案路徑

        Raises:
            FileNotFoundError: 當來源檔案不存在時
            PermissionError: 當沒有寫入權限時
        """
        logger_manager.info(f"開始壓縮檔案到: {output_path}")
        logger_manager.debug(f"要壓縮的檔案: {file_paths}")

        try:
            with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file in file_paths:
                    logger_manager.debug(f"正在壓縮: {file}")
                    zipf.write(file, os.path.basename(file))

            logger_manager.info(f"檔案壓縮完成: {output_path}")
        except Exception as e:
            logger_manager.error(f"壓縮過程發生錯誤: {str(e)}")
            raise

    def extract_files(self, zip_path: str, extract_path: str) -> None:
        """解壓縮檔案"""
        try:
            with zipfile.ZipFile(zip_path, "r") as zipf:
                zipf.extractall(extract_path)
        except Exception as e:
            logger_manager.error(f"解壓縮錯誤: {str(e)}")
            raise

    def encrypt_file(self, file_path: str, output_path: str) -> None:
        """加密檔案"""
        try:
            with open(file_path, "rb") as file:
                encrypted_data = self.cipher_suite.encrypt(file.read())
            with open(output_path, "wb") as file:
                file.write(encrypted_data)
        except Exception as e:
            logger_manager.error(f"加密錯誤: {str(e)}")
            raise

    def decrypt_file(self, file_path: str, output_path: str) -> None:
        """解密檔案"""
        try:
            with open(file_path, "rb") as file:
                decrypted_data = self.cipher_suite.decrypt(file.read())
            with open(output_path, "wb") as file:
                file.write(decrypted_data)
        except Exception as e:
            logger_manager.error(f"解密錯誤: {str(e)}")
            raise

    def process_image(self, image_path: str, operation: str, **kwargs) -> Image.Image:
        """圖片處理"""
        try:
            img = Image.open(image_path)
            if operation == "resize":
                return img.resize(kwargs.get("size", (800, 600)))
            elif operation == "rotate":
                return img.rotate(kwargs.get("angle", 90))
            elif operation == "filter":
                img_cv = cv2.imread(image_path)
                if kwargs.get("filter_type") == "blur":
                    return Image.fromarray(cv2.GaussianBlur(img_cv, (5, 5), 0))
                elif kwargs.get("filter_type") == "edge":
                    return Image.fromarray(cv2.Canny(img_cv, 100, 200))
            return img
        except Exception as e:
            logger_manager.error(f"圖片處理錯誤: {str(e)}")
            raise

    def backup_file(self, file_path: str, backup_dir: Optional[str] = None) -> str:
        """備份檔案"""
        try:
            if not backup_dir:
                backup_dir = os.path.dirname(file_path)
            os.makedirs(backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{os.path.splitext(file_path)[0]}_{timestamp}{os.path.splitext(file_path)[1]}"
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            logger_manager.error(f"備份錯誤: {str(e)}")
            raise


class DataAnalyzer:
    """數據分析類

    此類提供數據分析和視覺化功能，用於處理和展示數據。

    主要功能：
        - 基本統計分析
        - 數據視覺化（圖表生成）
        - 數據處理和轉換

    使用範例：
        analyzer = DataAnalyzer()
        stats = analyzer.analyze_data(df)
        analyzer.create_visualization(df, 'histogram', column='values')
    """

    @staticmethod
    def analyze_data(data: pd.DataFrame) -> Dict[str, Any]:
        """執行基本的數據分析

        Args:
            data (pd.DataFrame): 要分析的數據框架

        Returns:
            Dict[str, Any]: 包含分析結果的字典，包括：
                - summary: 基本統計摘要
                - missing: 缺失值統計
                - dtypes: 數據類型資訊
                - shape: 數據框架的形狀
        """
        logger_manager.info("開始數據分析")
        logger_manager.debug(f"數據框架大小: {data.shape}")

        try:
            results = {
                "summary": data.describe().to_dict(),
                "missing": data.isnull().sum().to_dict(),
                "dtypes": data.dtypes.to_dict(),
                "shape": data.shape,
            }

            logger_manager.info("數據分析完成")
            logger_manager.debug(f"分析結果摘要: {results['shape']}")
            return results
        except Exception as e:
            logger_manager.error(f"數據分析過程發生錯誤: {str(e)}")
            raise

    @staticmethod
    def create_visualization(data: pd.DataFrame, plot_type: str, **kwargs) -> None:
        """創建視覺化圖表"""
        try:
            plt.figure(figsize=kwargs.get("figsize", (10, 6)))

            if plot_type == "line":
                plt.plot(data[kwargs["x"]], data[kwargs["y"]])
            elif plot_type == "scatter":
                plt.scatter(data[kwargs["x"]], data[kwargs["y"]])
            elif plot_type == "histogram":
                plt.hist(data[kwargs["column"]], bins=kwargs.get("bins", 30))
            elif plot_type == "heatmap":
                sns.heatmap(data.corr(), annot=True)

            plt.title(kwargs.get("title", ""))
            plt.xlabel(kwargs.get("xlabel", ""))
            plt.ylabel(kwargs.get("ylabel", ""))

            if kwargs.get("save_path"):
                plt.savefig(kwargs["save_path"])
            if kwargs.get("show", True):
                plt.show()
            plt.close()
        except Exception as e:
            logger_manager.error(f"視覺化錯誤: {str(e)}")
            raise

    @staticmethod
    def process_data(data: pd.DataFrame, operation: str, **kwargs) -> pd.DataFrame:
        """數據處理"""
        try:
            if operation == "fillna":
                return data.fillna(kwargs.get("value", 0))
            elif operation == "drop_duplicates":
                return data.drop_duplicates()
            elif operation == "normalize":
                return (data - data.mean()) / data.std()
            elif operation == "sort":
                return data.sort_values(by=kwargs["column"])
            return data
        except Exception as e:
            logger_manager.error(f"數據處理錯誤: {str(e)}")
            raise
