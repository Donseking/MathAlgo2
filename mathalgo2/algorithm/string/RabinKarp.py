class RabinKarp:
    def __init__(self, pattern: str):
        """初始化 Rabin-Karp 算法

        Args:
            pattern: 要搜尋的模式字串
        """
        if not pattern:
            raise ValueError("Pattern cannot be empty")

        self.pattern = pattern
        self.pattern_length = len(pattern)
        self.d = 256  # 字符集大小
        self.q = 101  # 一個質數

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

        # 計算模式字串的雜湊值
        pattern_hash = 0
        text_hash = 0
        h = pow(self.d, M - 1) % self.q

        # 計算第一個窗口的雜湊值
        for i in range(M):
            pattern_hash = (self.d * pattern_hash + ord(self.pattern[i])) % self.q
            text_hash = (self.d * text_hash + ord(text[i])) % self.q

        # 滑動窗口
        for i in range(N - M + 1):
            if pattern_hash == text_hash:
                # 雜湊值相同時，進行字符比對
                if text[i : i + M] == self.pattern:
                    matches.append(i)

            # 計算下一個窗口的雜湊值
            if i < N - M:
                text_hash = (
                    self.d * (text_hash - ord(text[i]) * h) + ord(text[i + M])
                ) % self.q
                if text_hash < 0:
                    text_hash += self.q

        return matches
