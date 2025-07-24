import os
import pickle
from compressor import huffman, lzw, rle
from utils.file_utils import smart_algorithm_selection
from tkinter import filedialog, messagebox

# Maps algorithm names to modules
ALGO_MODULES = {
    "Huffman": huffman,
    "LZW": lzw,
    "RLE": rle
}

def compress_to_archive(file_paths, output_path):
    """
    Compress multiple files and store them in a single .dsz archive.
    """
    archive_content = []

    for file_path in file_paths:
        algo = smart_algorithm_selection(file_path)
        compressor = ALGO_MODULES[algo]

        with open(file_path, 'rb') as f:
            original_data = f.read()

        # Temporarily compress to memory using file-based function
        temp_file = f"{file_path}.temp_comp"
        compressor.compress(file_path, temp_file)
        with open(temp_file, 'rb') as f:
            compressed_data = f.read()
        os.remove(temp_file)

        archive_content.append({
            "filename": os.path.basename(file_path),
            "algorithm": algo,
            "compressed_data": compressed_data
        })

    # Save entire archive
    with open(output_path, 'wb') as f:
        pickle.dump(archive_content, f)

def decompress_archive(archive_path, save_mode="folder", destination=None, gui=None):
    """
    Decompress .dsz archive and extract all original files.
    Supports saving to a folder or individually prompted paths.
    """
    with open(archive_path, 'rb') as f:
        archive_content = pickle.load(f)

    if save_mode == "folder" and destination:
        os.makedirs(destination, exist_ok=True)

    for entry in archive_content:
        filename = entry["filename"]
        algo = entry["algorithm"]
        compressed_data = entry["compressed_data"]

        decompressor = ALGO_MODULES[algo]

        # Save compressed data to temp file
        temp_input = os.path.join(destination if save_mode == "folder" else os.getcwd(), filename + ".temp_input")
        with open(temp_input, 'wb') as f:
            f.write(compressed_data)

        if save_mode == "folder":
            output_file = os.path.join(destination, filename)
        else:
            output_file = filedialog.asksaveasfilename(initialfile=filename)
            if not output_file:
                continue

        decompressor.decompress(temp_input, output_file)
        os.remove(temp_input)

        if gui:
            gui.set_status(f"✅ Decompressed {filename} using {algo}")
