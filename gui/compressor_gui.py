import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import mimetypes
import csv
from datetime import datetime
from compressor import huffman, lzw, rle
from archive.archive_utils import compress_to_archive, decompress_archive

# ------------------ Smart Auto Algorithm Selector ------------------

def get_media_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "unknown"

def smart_algorithm_selection(file_path):
    mime = get_media_type(file_path)
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

# ------------------ Logging ------------------

def log_compression(filename, algorithm, orig_size, comp_size):
    ratio = round((1 - comp_size / orig_size) * 100, 2) if orig_size else 0
    now = datetime.now()
    os.makedirs("logs", exist_ok=True)
    path = os.path.join("logs", "compression_log.csv")
    is_new = not os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["Filename", "Algorithm", "Original Size", "Compressed Size", "Ratio (%)", "Date", "Time"])
        writer.writerow([os.path.basename(filename), algorithm, orig_size, comp_size, ratio, now.date(), now.strftime("%H:%M:%S")])

# ------------------ Algorithm Map ------------------

ALGO_MAP = {
    "Huffman": {"ext": ".huff", "compress": huffman.compress, "decompress": huffman.decompress},
    "LZW":     {"ext": ".lzw",  "compress": lzw.compress,     "decompress": lzw.decompress},
    "RLE":     {"ext": ".rle",  "compress": rle.compress,     "decompress": rle.decompress},
}

# ------------------ GUI ------------------

class CompressionGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced File Compression Tool")
        self.geometry("600x450")
        self.resizable(False, False)
        self.selected_file = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Advanced File Compression Tool", font=("Arial", 16, "bold")).pack(pady=10)

        # File Browse
        file_frame = tk.Frame(self)
        file_frame.pack(pady=10)
        self.file_label = tk.Label(file_frame, text="No file selected", width=50, anchor="w")
        self.file_label.pack(side=tk.LEFT, padx=5)
        tk.Button(file_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT)

        # Algorithm Selection
        algo_frame = tk.Frame(self)
        algo_frame.pack(pady=10)
        tk.Label(algo_frame, text="Algorithm:").pack(side=tk.LEFT)
        self.algo_var = tk.StringVar(value="Auto")
        algo_menu = ttk.Combobox(algo_frame, textvariable=self.algo_var, values=["Auto", "Huffman", "LZW", "RLE"], state="readonly", width=12)
        algo_menu.pack(side=tk.LEFT, padx=5)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Compress", width=12, command=self.compress_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Decompress", width=12, command=self.decompress_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Archive (.dsz)", width=15, command=self.compress_to_archive_gui).pack(side=tk.LEFT, padx=5)

        # Progress
        self.progress = ttk.Progressbar(self, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=15)

        # Status Box
        self.status_text = tk.Text(self, height=8, width=72, state="disabled", bg="#f4f4f4")
        self.status_text.pack(pady=5)

    def browse_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.selected_file = path
            self.file_label.config(text=os.path.basename(path))
            self.set_status(f"Selected file: {path}")

    def compress_file(self):
        if not self.selected_file:
            messagebox.showwarning("No file", "Please select a file to compress.")
            return
        algo = self.algo_var.get()
        if algo == "Auto":
            algo = smart_algorithm_selection(self.selected_file)
            self.set_status(f"🔍 Auto-selected algorithm: {algo}")
        handler = ALGO_MAP.get(algo)
        if not handler:
            messagebox.showerror("Invalid", f"Algorithm '{algo}' not supported.")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=handler["ext"], filetypes=[(f"{algo} Compressed", f"*{handler['ext']}")])
        if not output_path:
            return
        try:
            self.set_status(f"Compressing with {algo}...")
            self.simulate_progress()
            handler["compress"](self.selected_file, output_path)
            log_compression(self.selected_file, algo, os.path.getsize(self.selected_file), os.path.getsize(output_path))
            self.show_size_stats(self.selected_file, output_path)
            self.set_status("✅ Compression completed!")
        except Exception as e:
            self.set_status(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Compression failed: {str(e)}")

    def decompress_file(self):
        if not self.selected_file:
            messagebox.showwarning("No file", "Please select a file to decompress.")
            return
        ext = os.path.splitext(self.selected_file)[1].lower()
        if ext == ".dsz":
            answer = messagebox.askyesno("Extract Options", "Save all files into one folder?")
            if answer:
                folder = filedialog.askdirectory(title="Select Folder")
                if not folder:
                    return
                self.set_status("📦 Decompressing archive to folder...")
                self.simulate_progress()
                decompress_archive(self.selected_file, save_mode="folder", destination=folder, gui=self)
            else:
                self.set_status("📦 Decompressing archive individually...")
                self.simulate_progress()
                decompress_archive(self.selected_file, save_mode="individual", gui=self)
            self.set_status("✅ Archive decompression complete!")
            return

        algo = next((k for k, v in ALGO_MAP.items() if v["ext"] == ext), None)
        if not algo:
            messagebox.showerror("Unsupported", f"No decompressor found for {ext}")
            return
        handler = ALGO_MAP[algo]
        output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
        if not output_path:
            return
        try:
            self.set_status(f"Decompressing with {algo}...")
            self.simulate_progress()
            handler["decompress"](self.selected_file, output_path)
            self.show_size_stats(self.selected_file, output_path)
            self.set_status("✅ Decompression completed!")
        except Exception as e:
            self.set_status(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Decompression failed: {str(e)}")

    def compress_to_archive_gui(self):
        file_paths = filedialog.askopenfilenames(title="Select 2–5 files to archive")
        if not file_paths or len(file_paths) < 2 or len(file_paths) > 5:
            messagebox.showwarning("Invalid Selection", "Please select 2–5 files.")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".dsz", filetypes=[("DSZ Archive", "*.dsz")])
        if not output_path:
            return
        try:
            self.set_status("📦 Compressing files to archive...")
            self.simulate_progress()
            compress_to_archive(file_paths, output_path)
            self.set_status("✅ Archive created successfully!")
        except Exception as e:
            self.set_status(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Archive compression failed: {str(e)}")

    def simulate_progress(self):
        self.progress['value'] = 0
        for i in range(0, 101, 10):
            self.progress['value'] = i
            self.update_idletasks()
            self.after(30)

    def show_size_stats(self, original, new):
        size1 = os.path.getsize(original)
        size2 = os.path.getsize(new)
        ratio = (1 - size2 / size1) * 100 if size1 else 0
        self.set_status(f"Original Size: {size1} bytes")
        self.set_status(f"Compressed Size: {size2} bytes")
        self.set_status(f"Compression Ratio: {ratio:.2f}%")

    def set_status(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")

# ------------------ Run the GUI ------------------

if __name__ == "__main__":
    app = CompressionGUI()
    app.mainloop()
