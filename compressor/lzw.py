import os
import pickle


def compress(input_path: str, output_path: str):
    with open(input_path, 'r', encoding='utf-8') as file:
        data = file.read()

    if not data:
        raise ValueError("File is empty")

    # Initialize dictionary with single characters
    dictionary = {chr(i): i for i in range(256)}
    next_code = 256
    current = ""
    result = []

    for char in data:
        combined = current + char
        if combined in dictionary:
            current = combined
        else:
            result.append(dictionary[current])
            dictionary[combined] = next_code
            next_code += 1
            current = char

    if current:
        result.append(dictionary[current])

    with open(output_path, 'wb') as f:
        pickle.dump(result, f)


def decompress(input_path: str, output_path: str):
    with open(input_path, 'rb') as f:
        compressed = pickle.load(f)

    if not compressed:
        raise ValueError("Compressed file is empty or invalid")

    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256

    current = chr(compressed[0])
    result = [current]

    for code in compressed[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = current + current[0]
        else:
            raise ValueError("Bad LZW compressed file.")

        result.append(entry)
        dictionary[next_code] = current + entry[0]
        next_code += 1
        current = entry

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(result))