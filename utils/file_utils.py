import mimetypes
import os

def get_media_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "unknown"

def smart_algorithm_selection(file_path):
    mime = get_media_type(file_path)
    size = os.path.getsize(file_path)

    if mime.startswith("text"):
        if file_path.endswith((".json", ".xml", ".csv")):
            return "LZW"
        elif file_path.endswith(".txt"):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.read(5000)
                if len(set(data)) < 10:
                    return "RLE"
                elif len(set(data)) > 200:
                    return "Huffman"
                else:
                    return "LZW"
        else:
            return "Huffman"
    elif mime in ["image/bmp", "image/pbm"]:
        return "RLE"
    elif mime in ["application/json"]:
        return "LZW"
    elif mime in ["application/octet-stream"]:
        return "Huffman"
    return "Huffman"
