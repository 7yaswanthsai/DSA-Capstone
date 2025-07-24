import heapq
import os
import pickle


class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_frequency_map(data: str):
    freq = {}
    for char in data:
        freq[char] = freq.get(char, 0) + 1
    return freq


def build_huffman_tree(freq_map):
    heap = [Node(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]


def build_codes(root):
    codes = {}

    def traverse(node, path):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = path
            return
        traverse(node.left, path + "0")
        traverse(node.right, path + "1")

    traverse(root, "")
    return codes


def compress(input_path: str, output_path: str):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = f.read()

    if not data:
        raise ValueError("File is empty")

    freq_map = build_frequency_map(data)
    root = build_huffman_tree(freq_map)
    codes = build_codes(root)

    encoded_data = ''.join(codes[c] for c in data)

    # Add padding so it's divisible by 8
    padding = (8 - len(encoded_data) % 8) % 8
    encoded_data += '0' * padding

    byte_data = bytearray()
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i + 8]
        byte_data.append(int(byte, 2))

    with open(output_path, 'wb') as f:
        pickle.dump({
            'root': root,
            'padding': padding,
            'data': byte_data
        }, f)


def decompress(input_path: str, output_path: str):
    with open(input_path, 'rb') as f:
        obj = pickle.load(f)

    root = obj['root']
    padding = obj['padding']
    byte_data = obj['data']

    bit_string = ''.join(f"{byte:08b}" for byte in byte_data)
    if padding:
        bit_string = bit_string[:-padding]

    decoded = []
    node = root
    for bit in bit_string:
        node = node.left if bit == '0' else node.right
        if node.char is not None:
            decoded.append(node.char)
            node = root

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(decoded))
