# ⚡ PDFtoLLM: Premium PDF-to-Markdown Converter ⚡

**PDFtoLLM** is a high-performance, Python-based tool designed to convert PDF documents into clean, structured Markdown. It is optimized for Large Language Model (LLM) workflows (RAG, training, analysis) and supports multiple best-in-class conversion engines.

---

## 🚀 Features

- **Multiple Engines**: Choose the best tool for your specific document type:
    - **Marker**: High-accuracy OCR, specialized in mathematical formulas and academic papers. Uses `surya` for layout analysis and `texify` for math.
    - **Docling**: Advanced document understanding with `TableFormer` for precise table extraction and formula enrichment.
    - **Simple**: Blazing-fast text extraction using `PyMuPDF` (no AI models), perfect for simple text documents.
- **Interactive Mode**: Beautiful Terminal User Interface (TUI) powered by `rich` to guide you through file selection and configuration.
- **Command-Line Interface (CLI)**: Full CLI support for batch processing and automated pipelines.
- **Optimized Output**: Generates clean Markdown that preserves document structure, tables, and equations.

---

## 🛠️ Installation

We recommend using **Conda** or **Mamba** to manage dependencies and creating a dedicated environment.

### 1. Prerequisites

Ensure you have [Conda](https://docs.conda.io/en/latest/) or [Mamba](https://github.com/mamba-org/mamba) installed.

### 2. Create the Environment

Create a new environment named `marker_env` with Python 3.10:

```bash
mamba create -n marker_env python=3.10
mamba activate marker_env
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install rich marker-pdf docling pymupdf
```

> **Note**: `marker-pdf` requires PyTorch. If you are on a specific hardware (like CUDA), ensure you install the correct PyTorch version first. For macOS (M1/M2/M3), the default installation usually works fine with MPS acceleration.

---

## 📖 Usage

### Interactive Mode (Recommended)

Simply run the script without arguments to launch the interactive menu:

```bash
python pdftollm.py
```

Follow the prompts to:
1.  Enter the path to your PDF file.
2.  Select the conversion engine (`Marker`, `Docling`, or `Simple`).
3.  Choose the mode (e.g., `Full` for complete OCR/Tables, or `No Tables` for faster processing).

### Command-Line Interface (CLI)

For automation or power users, you can pass arguments directly:

#### Basic Syntax
```bash
python pdftollm.py <path_to_pdf> --method <engine> --mode <mode>
```

#### Examples

**Convert using Marker (default):**
```bash
python pdftollm.py documents/research_paper.pdf --method marker
```

**Convert using Docling (best for tables):**
```bash
python pdftollm.py documents/financial_report.pdf --method docling
```

**Convert using Simple extraction (fastest):**
```bash
python pdftollm.py documents/novel.pdf --method simple
```

**Skip confirmation prompt:**
```bash
python pdftollm.py documents/automated.pdf --method marker -y
```

### Output

The script will generate a Markdown file in the same directory as the source PDF by default (e.g., `document.md`). You can specify a custom output path using the `-o` flag:

```bash
python pdftollm.py input.pdf -o output/folder/result.md
```

---

## 🧩 Engines Comparison

| Feature | Marker | Docling | Simple |
| :--- | :---: | :---: | :---: |
| **OCR Capability** | ✅ High | ✅ High | ❌ None |
| **Math / Equations** | ✅ Excellent | ✅ Good | ❌ Basic |
| **Table Structure** | ⚠️ Okay | ✅ Excellent | ❌ Poor |
| **Speed** | 🐢 Slow | 🐢 Slow | ⚡ Instant |
| **Hardware Req.** | High (GPU rec.) | High (GPU rec.) | Low |
