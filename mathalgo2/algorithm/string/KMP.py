class KMP:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.lps = self._compute_lps()

    def _compute_lps(self):
        """Compute Longest Proper Prefix which is also Suffix"""
        lps = [0] * len(self.pattern)
        length = 0
        i = 1

        while i < len(self.pattern):
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

    def search(self, text: str) -> list:
        matches = []
        i = j = 0
        
        while i < len(text):
            if self.pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == len(self.pattern):
                matches.append(i - j)
                j = self.lps[j - 1]
            elif i < len(text) and self.pattern[j] != text[i]:
                if j != 0:
                    j = self.lps[j - 1]
                else:
                    i += 1
                    
        return matches
