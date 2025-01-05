"""
檔案載入模組

提供檔案和目錄載入功能：
- 檔案讀取進度追蹤
- 目錄遍歷
- 檔案存取驗證

Classes:
    ProgressBar: 進度條顯示器

Functions:
    read_folder: 讀取目錄內容
    validate_path: 驗證路徑有效性

Examples:
    >>> from mathalgo2.loading import read_folder
    >>> files = read_folder("./data")
"""

import os
import sys
import threading
import time
from pathlib import Path
from typing import List, Union

from .Logger import Logger, logging

# 設置根目錄和日誌
ROOT_DIR = Path(__file__).parent.parent
log_file = ROOT_DIR / "__log__" / "progress.log"

# 初始化日誌管理器
logger_manager = Logger(
    name="Progress_Bar",
    log_file=str(log_file),
    level=logging.INFO,
    console_output=False,
)


def read_folder(path: str) -> Union[List[str], bool]:
    """
    讀取指定目錄下的所有檔案

    Args:
        path (str): 目錄路徑

    Returns:
        Union[List[str], bool]: 檔案列表或錯誤時返回 False

    Raises:
        FileNotFoundError: 目錄不存在時拋出
        PermissionError: 無存取權限時拋出

    Examples:
        >>> files = read_folder("./data")
        >>> print(files)
        ['file1.txt', 'file2.json']
    """
    logger_manager.info(f"開始處理路徑: {path}")
    try:
        # 檢查路徑是否存在
        if not os.path.exists(path):
            logger_manager.error(f"路徑不存在: {path}")
            print(f"\n錯誤: 路徑不存在 - {path}")
            return False

        if os.path.isfile(path):
            # 讀取單一檔案
            total_size = os.path.getsize(path)
            current_size = 0
            chunk_size = 1024  # 1MB chunks
            filename = os.path.basename(path)

            logger_manager.info(f"開始讀取檔案: {path}")
            logger_manager.debug(f"檔案大小: {total_size} bytes")

            with ProgressBar(total=total_size, desc=f"Reading") as bar:
                logger_manager.debug(f"開始讀取檔案內容，每次讀取 {chunk_size} bytes")
                bar.update(0, filename)  # 初始化時設置檔案名
                with open(path, "rb") as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        current_size += len(chunk)
                        bar.update(current_size, filename)
                        time.sleep(0.1)
                bar.update(total_size, filename)
            logger_manager.info(f"完成讀取檔案: {path}")
            return [path]

        elif os.path.isdir(path):
            # 讀取資料夾內所有檔案
            logger_manager.info(f"掃描資料夾: {path}")
            files = [
                os.path.join(path, f)
                for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))
            ]

            if not files:
                logger_manager.warning(f"資料夾為空: {path}")
                print(f"\n提示: 資料夾為空 - {path}")
                return []

            logger_manager.info(f"找到 {len(files)} 個檔案")
            total_size = sum(os.path.getsize(f) for f in files)
            logger_manager.debug(f"總檔案大小: {total_size} bytes")

            # 讀取資料夾
            current_size = 0
            chunk_size = 1024  # 1B chunks

            logger_manager.info(f"開始讀取資料夾: {path}")
            with ProgressBar(total=total_size, desc=f"Reading") as bar:
                for file_path in files:
                    filename = os.path.basename(file_path)
                    logger_manager.info(f"讀取檔案: {file_path}")
                    with open(file_path, "rb") as f:
                        while True:
                            chunk = f.read(chunk_size)
                            if not chunk:
                                break
                            current_size += len(chunk)
                            bar.update(current_size, filename)
                            time.sleep(0.1)
                bar.update(total_size, "完成")
            logger_manager.info(f"完成讀取資料夾: {path}")
            return files

        logger_manager.error(f"路徑既不是檔案也不是目錄: {path}")
        return False

    except Exception as e:
        logger_manager.exception(f"讀取時發生錯誤: {str(e)}")
        print(f"\n錯誤: {e}")
        return False


class ProgressBar:
    """
    進度條類

    屬性:
        desc (str): 進度條描述
        width (int): 進度條寬度
        total (int): 總大小
        current (int): 當前進度
        start_time (float): 開始時間
        is_running (bool): 是否正在運行
        current_file (str): 當前處理的檔案名
    """

    # 顏色代碼定義
    COLORS = {
        "GREEN": "\033[92m",  # 成功/完成
        "RED": "\033[91m",  # 未完成部分
        "BLUE": "\033[94m",  # 進行中
        "WHITE": "\033[97m",  # 一般文字
        "RESET": "\033[0m",  # 重置顏色
    }

    def __init__(self, total=0, desc="Progress", width=50):
        """
        初始化進度條

        參數:
            total (int): 總大小
            desc (str): 進度條描述
            width (int): 進度條寬度
        """
        self.desc = desc
        self.width = width
        self.total = total
        self.current = 0
        self.start_time = None
        self.is_running = False
        self.current_file = ""

        if sys.platform == "win32":
            os.system("")
        logger_manager.debug(f"初始化進度條: {desc}, 總大小: {total}")

    def __enter__(self):
        self.start_time = time.time()
        self.is_running = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.is_running = False
        sys.stdout.write("\n")
        sys.stdout.flush()
        return True

    def update(self, current, filename=""):
        """
        更新進度

        參數:
            current (int): 當前進度
            filename (str): 當前處理的檔案名
        """
        self.current = current
        self.current_file = filename
        logger_manager.debug(f"更新進度: {current}/{self.total}, 檔案: {filename}")
        self._display_progress()

    def _display_progress(self):
        """顯示進度條"""
        percent = (self.current / self.total) * 100 if self.total > 0 else 0
        filled = int(self.width * (self.current / self.total)) if self.total > 0 else 0

        elapsed = time.time() - self.start_time if self.start_time else 0
        speed = self.current / elapsed if elapsed > 0 else 0
        eta = (
            (self.total - self.current) / speed
            if speed > 0 and speed != float("inf")
            else 0
        )

        # 構建進度條
        if self.current >= self.total:
            # 完成時使用綠色
            bar = f"{self.COLORS['GREEN']}{'-' * self.width}"
        else:
            # 進行中時已完成部分藍色，未完成部分紅色
            bar = (
                f"{self.COLORS['BLUE']}{'-' * filled}"
                f"{self.COLORS['RED']}{'-' * (self.width - filled)}"
            )
        bar += f"{self.COLORS['RESET']}"

        # 添加檔案名到狀態信息
        file_info = f" - {self.current_file}" if self.current_file else ""

        # 構建狀態信息
        status = (
            f"\r{self.COLORS['GREEN']}{self.desc}: "
            f"{bar}{self.COLORS['GREEN']} {percent:.1f}% "
            f"[{self.current}/{self.total}] "
            f"{self._format_speed(speed)} "
            f"ETA: {self._format_time(eta)}"
            f"{file_info}{self.COLORS['RESET']}"
        )

        # 使用 sys.stdout 而不是 print
        sys.stdout.write(status)
        sys.stdout.flush()

    def _format_speed(self, speed):
        """格式化速度顯示"""
        if speed < 1024:
            return f"{speed:.1f}B/s"
        elif speed < 1024 * 1024:
            return f"{speed/1024:.1f}KB/s"
        else:
            return f"{speed/1024/1024:.1f}MB/s"

    def _format_time(self, seconds):
        """格式化時間顯示"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            seconds = seconds % 60
            return f"{minutes}m {seconds:.1f}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"


# 只導出需要的函數
__all__ = ["read_folder"]
