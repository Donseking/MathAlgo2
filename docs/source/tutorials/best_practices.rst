最佳實踐指南
==========

代碼風格
-------

1. 類型提示
~~~~~~~~~~

建議使用類型提示來增加代碼可讀性：

.. code-block:: python

    from typing import List, Optional

    def process_data(data: List[float]) -> Optional[float]:
        if not data:
            return None
        return sum(data) / len(data)

2. 錯誤處理
~~~~~~~~~~

使用適當的異常處理機制：

.. code-block:: python

    try:
        result = complex_calculation()
    except ValueError as e:
        logger.error(f"計算錯誤: {e}")
        raise
    except Exception as e:
        logger.critical(f"未預期的錯誤: {e}")
        raise

3. 日誌記錄
~~~~~~~~~~

合理使用日誌級別：

.. code-block:: python

    from mathalgo2.Logger import Logger

    logger = Logger(name="my_module")

    # 不同級別的日誌
    logger.debug("詳細的調試信息")
    logger.info("一般信息")
    logger.warning("警告信息")
    logger.error("錯誤信息")
