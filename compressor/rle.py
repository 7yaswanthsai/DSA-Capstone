import os


def compress(input_path: str, output_path: str):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = f.read()

    if not data:
        raise ValueError("File is empty")

    encoded = []
    count = 1

    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded.append(data[i - 1] + str(count))
            count = 1

    # Append the last run
    encoded.append(data[-1] + str(count))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(encoded))


def decompress(input_path: str, output_path: str):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = f.read()

    if not data:
        raise ValueError("File is empty")

    decoded = []
    i = 0
    while i < len(data):
        char = data[i]
        i += 1
        count = ''

        while i < len(data) and data[i].isdigit():
            count += data[i]
            i += 1

        decoded.append(char * int(count))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(decoded))
