class RabinKarp:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.pattern_hash = self._hash(pattern)
        self.pattern_length = len(pattern)
        self.prime = 101
        self.d = 256  # Number of characters in input alphabet

    def _hash(self, string: str, start: int = 0, end: int = None) -> int:
        if end is None:
            end = len(string)
        hash_value = 0
        for i in range(start, end):
            hash_value = (hash_value * self.d + ord(string[i])) % self.prime
        return hash_value

    def search(self, text: str) -> list:
        matches = []
        n, m = len(text), self.pattern_length
        if n < m:
            return matches

        text_hash = self._hash(text, 0, m)
        h = pow(self.d, m-1) % self.prime

        for i in range(n - m + 1):
            if text_hash == self.pattern_hash:
                if text[i:i+m] == self.pattern:
                    matches.append(i)
            
            if i < n - m:
                text_hash = (self.d * (text_hash - ord(text[i]) * h) + 
                           ord(text[i + m])) % self.prime
                if text_hash < 0:
                    text_hash += self.prime

        return matches