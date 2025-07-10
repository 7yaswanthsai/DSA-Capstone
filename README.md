# 📦 Compresso – Advanced File Compression Tool

> A universal file compressor built using core Data Structures & Algorithms (DSA) in Python.  
> Supports text, image, audio, video, and binary files with GUI + CLI interfaces.

---

## 🚀 Project Overview

**Compresso** is a custom-built file compression tool designed to demonstrate how classic data structures and algorithms like **Huffman Coding**, **LZW**, and **RLE** can be used in real-world file systems.

While general tools like ZIP or RAR are black boxes, Compresso is focused on both **practical usage** and **educational transparency**.

---

## 🧠 Algorithms Implemented

| Algorithm | Description | Best Used For |
|----------|-------------|----------------|
| Huffman Coding | Greedy, frequency-based tree compression | Plain text, source code |
| LZW (Lempel-Ziv-Welch) | Dictionary-based encoding | Structured text, JSON, XML |
| RLE (Run-Length Encoding) | Basic repetition compression | Monochrome images, simple text |

---

## 🖥 Features

- ✅ Compress and decompress using Huffman, LZW, RLE
- ✅ Supports multiple file types: `.txt`, `.csv`, `.pdf`, `.png`, `.mp3`, `.mp4`, `.exe`, etc.
- ✅ Smart algorithm suggestion based on MIME type
- ✅ Simple GUI using Tkinter
- ✅ CLI support for automation and scripting
- ✅ Compression metrics: time, ratio, size
- ✅ Unicode-safe and binary-safe operations

---

## 📂 File Types Supported

| Category      | Examples                            |
|---------------|-------------------------------------|
| Text Files    | `.txt`, `.csv`, `.log`, `.json`     |
| Documents     | `.pdf`, `.docx`, `.pptx`, `.xlsx`   |
| Images        | `.png`, `.bmp`, `.jpeg`, `.tiff`    |
| Audio         | `.mp3`, `.wav`, `.flac`, `.ogg`     |
| Video         | `.mp4`, `.avi`, `.mkv`, `.mov`      |
| Binary        | `.exe`, `.dll`, `.bin`, `.class`    |

---

## 🛠 Tools & Technologies

- **Language**: Python 3.x
- **GUI**: Tkinter
- **Libraries**:
  - `zlib`, `mimetypes` – Generic file handling
  - `Pillow` – Image support
  - `Pydub` – Audio processing
  - `ffmpeg-python` – Video processing
- **Version Control**: Git, GitHub
- **IDE**: VS Code

---
