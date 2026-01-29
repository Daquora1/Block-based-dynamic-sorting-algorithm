import math
import random
class Block:
    def __init__(self, values):
        self.values = sorted(values)
        self.min = self.values[0]
        self.max = self.values[-1]
        self.last_index = len(self.values) // 2

    def insert(self, n):
        i = self.last_index

        # bidirectional linear search
        if n >= self.values[i]:
            while i < len(self.values) - 1 and self.values[i] < n:
                i += 1
        else:
            while i > 0 and self.values[i - 1] > n:
                i -= 1

        self.values.insert(i, n)
        self.last_index = i
        self.min = self.values[0]
        self.max = self.values[-1]

    def split(self):
        mid = len(self.values) // 2
        left = Block(self.values[:mid])
        right = Block(self.values[mid:])
        return left, right


class BlockSorter:
    def __init__(self):
        self.blocks = []
        self.k = 0

    def max_block_size(self):
        if self.k == 0:
            return 32
        X = 32 * math.floor(math.log2(self.k) / 2 + 1)
        return min(X, 128)

    def insert(self, n):
        self.k += 1
        X = self.max_block_size()

        if not self.blocks:
            self.blocks.append(Block([n]))
            return

        for i, block in enumerate(self.blocks):
            if n <= block.max:
                block.insert(n)

                if len(block.values) > X:
                    left, right = block.split()
                    self.blocks[i:i+1] = [left, right]
                return

        self.blocks.append(Block([n]))

    def to_list(self):
        result = []
        for block in self.blocks:
            result.extend(block.values)
        return result

data = [random.randint(0, 10000) for _ in range(1000)]

sorter = BlockSorter()

for n in data:
    sorter.insert(n)

print(sorter.to_list())
