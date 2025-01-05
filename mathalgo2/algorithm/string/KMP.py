class KMP:
    def __init__(self, pattern: str):
        """初始化 KMP 算法

        Args:
            pattern: 要搜尋的模式字串
        """
        if not pattern:
            raise ValueError("Pattern cannot be empty")

        self.pattern = pattern
        self.pattern_length = len(pattern)

    def compute_lps(self) -> list[int]:
        """計算最長相同前後綴數組（Longest Proper Prefix which is also Suffix）

        Returns:
            list[int]: LPS 數組
        """
        lps = [0] * self.pattern_length
        length = 0  # 前一個最長相同前後綴的長度
        i = 1

        while i < self.pattern_length:
            if self.pattern[i] == self.pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        return lps

    def search(self, text: str) -> list[int]:
        """在文本中搜尋模式字串

        Args:
            text: 要被搜尋的文本

        Returns:
            list[int]: 所有匹配的起始位置列表
        """
        matches = []
        N = len(text)
        M = self.pattern_length

        if M > N:
            return matches

        lps = self.compute_lps()

        i = 0  # text 的索引
        j = 0  # pattern 的索引

        while i < N:
            if self.pattern[j] == text[i]:
                i += 1
                j += 1

                if j == M:
                    matches.append(i - j)
                    j = lps[j - 1]
            else:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1

        return matches
