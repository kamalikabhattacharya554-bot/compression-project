import heapq
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_tree(text):
    freq = Counter(text)
    heap = [Node(ch, f) for ch, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]


def generate_codes(node, prefix="", codebook={}):
    if node:
        if node.char:
            codebook[node.char] = prefix
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook


def compress(text):
    root = build_tree(text)
    codes = generate_codes(root, "", {})
    encoded = ''.join(codes[ch] for ch in text)
    return encoded, codes, root


def decompress(encoded, root):
    result = ""
    node = root

    for bit in encoded:
        node = node.left if bit == '0' else node.right

        if node.char:
            result += node.char
            node = root

    return result
