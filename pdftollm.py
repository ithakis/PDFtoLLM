#!/usr/bin/env python3
"""
pdftollm.py — Premium PDF-to-Markdown converter.

Supports three conversion backends:
  • Marker   (OCR, math via texify/surya)
  • Docling  (OCR, table structure, formula enrichment)
  • Simple   (PyMuPDF direct text extraction — no AI)

Usage:
    Interactive:   python pdftollm.py
    Programmatic:  python pdftollm.py document.pdf --method marker --mode full -y

API:
    from pdftollm import convert
    convert("document.pdf", method="marker", mode="full")
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import threading
from pathlib import Path
from typing import Optional, Literal

# ── Rich imports ────────────────────────────────────────────────────────────
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.rule import Rule
from rich.columns import Columns
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
    TaskProgressColumn,
)
from rich.prompt import Prompt, IntPrompt
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
from rich import box

# ── Constants ───────────────────────────────────────────────────────────────
ACCENT    = "#7C3AED"   # violet-600
ACCENT2   = "#06B6D4"   # cyan-500
SUCCESS   = "#10B981"   # emerald-500
WARN      = "#F59E0B"   # amber-500
ERR       = "#EF4444"   # red-500
DIM       = "#6B7280"   # gray-500

console = Console()

# ════════════════════════════════════════════════════════════════════════════
#  Banner
# ════════════════════════════════════════════════════════════════════════════
BANNER = r"""[bold #7C3AED]
  ╔═══════════════════════════════════════════════╗
  ║        [bold white]⚡ PDF → LLM  Converter ⚡[/bold white]           ║
  ║  [dim #06B6D4]Marker · Docling · Simple Extraction[/dim #06B6D4]   ║
  ╚═══════════════════════════════════════════════╝[/bold #7C3AED]"""


# ════════════════════════════════════════════════════════════════════════════
#  Interactive menus
# ════════════════════════════════════════════════════════════════════════════
def ask_pdf_path() -> str:
    """Prompt for a valid PDF path."""
    while True:
        path = Prompt.ask(f"\n [{ACCENT}]📄 PDF file path[/{ACCENT}]")
        path = path.strip().strip("'\"")
        if os.path.isfile(path) and path.lower().endswith(".pdf"):
            return path
        console.print(f"  [{ERR}]✗ Not a valid PDF:[/{ERR}] {path}")


def ask_method() -> str:
    """Prompt for the conversion engine."""
    table = Table(
        title="[bold]Select Engine[/bold]",
        box=box.ROUNDED,
        border_style=ACCENT,
        title_style=f"bold {ACCENT}",
        show_lines=True,
        padding=(0, 1),
    )
    table.add_column("#", style="bold white", width=3, justify="center")
    table.add_column("Engine", style=f"bold {ACCENT2}", min_width=12)
    table.add_column("Description", style="white", ratio=1)
    table.add_column("Speed", style=DIM, width=10, justify="center")
    table.add_column("Math", style=DIM, width=6, justify="center")

    table.add_row("1", "Marker",  "Full OCR · math via texify · layout analysis",     "●●○○", "✓✓")
    table.add_row("2", "Docling", "Full OCR · TableFormer · formula enrichment",       "●●○○", "✓✓")
    table.add_row("3", "Simple",  "Direct text extraction — no AI, no models needed",  "●●●●", "✗")

    console.print()
    console.print(table)
    choice = Prompt.ask(f"  [{ACCENT}]Engine[/{ACCENT}]", choices=["1", "2", "3"], default="1")
    return {"1": "marker", "2": "docling", "3": "simple"}[choice]


def ask_mode(method: str) -> str:
    """Prompt for conversion mode (only relevant for OCR engines)."""
    if method == "simple":
        return "full"  # irrelevant but kept consistent

    table = Table(
        title="[bold]Select Mode[/bold]",
        box=box.ROUNDED,
        border_style=ACCENT2,
        title_style=f"bold {ACCENT2}",
        show_lines=True,
        padding=(0, 1),
    )
    table.add_column("#", style="bold white", width=3, justify="center")
    table.add_column("Mode", style=f"bold {ACCENT2}", min_width=14)
    table.add_column("Description", style="white", ratio=1)

    table.add_row("1", "Full",       "OCR + table recognition + math equations")
    table.add_row("2", "No Tables",  "OCR + math — skip table structure (faster)")

    console.print()
    console.print(table)
    choice = Prompt.ask(f"  [{ACCENT2}]Mode[/{ACCENT2}]", choices=["1", "2"], default="1")
    return {"1": "full", "2": "no_tables"}[choice]


# ════════════════════════════════════════════════════════════════════════════
#  Progress-bar helper
# ════════════════════════════════════════════════════════════════════════════
def _make_progress() -> Progress:
    """Create a styled dual-bar progress widget."""
    return Progress(
        SpinnerColumn("dots", style=ACCENT),
        TextColumn("[progress.description]{task.description}", style="bold white"),
        BarColumn(bar_width=40, style=DIM, complete_style=ACCENT, finished_style=SUCCESS),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
        expand=False,
    )


# ════════════════════════════════════════════════════════════════════════════
#  Conversion back-ends
# ════════════════════════════════════════════════════════════════════════════

# ── Simple ──────────────────────────────────────────────────────────────────
def convert_simple(pdf_path: str, output_path: str) -> None:
    """Blazing-fast text extraction via PyMuPDF — no AI models."""
    import fitz  # type: ignore

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    parts: list[str] = []

    progress = _make_progress()
    with progress:
        total_task = progress.add_task(f"[{ACCENT2}]Total pages", total=total_pages)
        page_task  = progress.add_task(f"[{ACCENT}]Current page", total=1, visible=True)

        for idx, page in enumerate(doc):
            progress.update(page_task, completed=0, total=1,
                            description=f"[{ACCENT}]Page {idx+1}/{total_pages}")
            text = page.get_text()
            parts.append(text)
            progress.update(page_task, completed=1)
            progress.update(total_task, advance=1)

    _write_output(output_path, "\n\n".join(parts))


# ── Marker ──────────────────────────────────────────────────────────────────
def convert_marker(pdf_path: str, output_path: str, *, tables: bool = True) -> None:
    """Convert with Marker (surya + texify)."""
    _status("Loading Marker models …")

    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered
    from marker.config.parser import ConfigParser

    parser = ConfigParser({"force_ocr": True})
    converter = PdfConverter(
        config=parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
    )

    progress = _make_progress()
    with progress:
        total_task = progress.add_task(f"[{ACCENT2}]Converting", total=None)
        rendered = converter(pdf_path)
        text, _, _ = text_from_rendered(rendered)
        progress.update(total_task, total=1, completed=1)

    _write_output(output_path, text)


# ── Docling ─────────────────────────────────────────────────────────────────
def convert_docling(pdf_path: str, output_path: str, *, tables: bool = True) -> None:
    """Convert with Docling (IBM TableFormer + formula enrichment)."""
    _status("Loading Docling models …")

    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions

    opts = PdfPipelineOptions()
    opts.do_table_structure    = tables
    opts.do_ocr                = True
    opts.do_formula_enrichment = True  # decode math → LaTeX

    doc_converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}
    )

    progress = _make_progress()
    with progress:
        total_task = progress.add_task(f"[{ACCENT2}]Processing", total=None)
        result = doc_converter.convert(pdf_path)
        md = result.document.export_to_markdown()
        progress.update(total_task, total=1, completed=1)

    _write_output(output_path, md)


# ════════════════════════════════════════════════════════════════════════════
#  Helpers
# ════════════════════════════════════════════════════════════════════════════
def _status(msg: str) -> None:
    console.print(f"  [{WARN}]⏳ {msg}[/{WARN}]")


def _write_output(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _show_summary(pdf_path: str, output_path: str, method: str, mode: str, elapsed: float) -> None:
    """Print a beautiful completion summary panel."""
    out = Path(output_path)
    size_kb = out.stat().st_size / 1024 if out.exists() else 0

    tbl = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    tbl.add_column(style=f"bold {ACCENT2}")
    tbl.add_column(style="white")
    tbl.add_row("Input",    str(pdf_path))
    tbl.add_row("Output",   str(output_path))
    tbl.add_row("Engine",   method.capitalize())
    tbl.add_row("Mode",     mode.replace("_", " ").title())
    tbl.add_row("Size",     f"{size_kb:.1f} KB")
    tbl.add_row("Time",     f"{elapsed:.2f}s")

    panel = Panel(
        tbl,
        title=f"[bold {SUCCESS}]✓ Conversion complete[/bold {SUCCESS}]",
        border_style=SUCCESS,
        box=box.DOUBLE,
        padding=(1, 2),
    )
    console.print()
    console.print(panel)


# ════════════════════════════════════════════════════════════════════════════
#  Public API
# ════════════════════════════════════════════════════════════════════════════
def convert(
    pdf_path: str,
    *,
    method: Literal["marker", "docling", "simple"] = "marker",
    mode: Literal["full", "no_tables"] = "full",
    output_path: str | None = None,
) -> str:
    """
    Programmatic entry-point.

    Parameters
    ----------
    pdf_path : str
        Path to the source PDF.
    method : {"marker", "docling", "simple"}
        Which conversion engine to use.
    mode : {"full", "no_tables"}
        Whether to enable table recognition (ignored for simple).
    output_path : str, optional
        Where to save the Markdown.  Defaults to ``<pdf_stem>.md``
        in the same directory as the source PDF.

    Returns
    -------
    str  – the path of the generated Markdown file.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(pdf_path)

    if output_path is None:
        output_path = str(Path(pdf_path).with_suffix(".md"))

    tables = mode == "full"

    if method == "simple":
        convert_simple(pdf_path, output_path)
    elif method == "marker":
        convert_marker(pdf_path, output_path, tables=tables)
    elif method == "docling":
        convert_docling(pdf_path, output_path, tables=tables)
    else:
        raise ValueError(f"Unknown method: {method!r}")

    return output_path


# ════════════════════════════════════════════════════════════════════════════
#  CLI
# ════════════════════════════════════════════════════════════════════════════
def main() -> None:
    console.print(BANNER)

    parser = argparse.ArgumentParser(
        description="PDF → Markdown converter (Marker / Docling / Simple)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path", nargs="?", help="Path to PDF file")
    parser.add_argument(
        "--method", "-m",
        choices=["marker", "docling", "simple"],
        help="Conversion engine",
    )
    parser.add_argument(
        "--mode",
        choices=["full", "no_tables"],
        default="full",
        help="Conversion mode (default: full)",
    )
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")
    parser.add_argument("-o", "--output", help="Output Markdown file path")
    args = parser.parse_args()

    # ── 1. PDF path ───────────────────────────────────────────────────────
    pdf_path = args.path or ask_pdf_path()
    if not os.path.isfile(pdf_path):
        console.print(f"  [{ERR}]✗ File not found:[/{ERR}] {pdf_path}")
        sys.exit(1)

    # ── 2. Engine ─────────────────────────────────────────────────────────
    method = args.method or ask_method()

    # ── 3. Mode ───────────────────────────────────────────────────────────
    mode = args.mode if args.method else ask_mode(method)

    # ── 4. Output path ────────────────────────────────────────────────────
    output_path = args.output or str(Path(pdf_path).with_suffix(".md"))

    # ── 5. Confirmation ──────────────────────────────────────────────────
    _show_config(pdf_path, output_path, method, mode)
    if not args.yes:
        console.print()
        answer = Prompt.ask(f"  [{ACCENT}]Start conversion?[/{ACCENT}] (y/n)", default="y")
        if answer.lower() not in ("y", "yes"):
            console.print(f"  [{WARN}]Aborted.[/{WARN}]")
            return

    # ── 6. Convert ────────────────────────────────────────────────────────
    console.print()
    console.print(Rule(f"[bold {ACCENT}]Processing[/bold {ACCENT}]", style=ACCENT))
    start = time.time()

    try:
        convert(pdf_path, method=method, mode=mode, output_path=output_path)
    except Exception as exc:
        console.print(f"\n  [{ERR}]✗ Conversion failed:[/{ERR}] {exc}")
        import traceback; traceback.print_exc()
        sys.exit(1)

    elapsed = time.time() - start
    _show_summary(pdf_path, output_path, method, mode, elapsed)


def _show_config(pdf_path: str, output_path: str, method: str, mode: str) -> None:
    """Display a pre-flight config panel."""
    import fitz  # type: ignore
    doc = fitz.open(pdf_path)
    n_pages = len(doc)
    size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    doc.close()

    tbl = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    tbl.add_column(style=f"bold {ACCENT2}")
    tbl.add_column(style="white")
    tbl.add_row("Input",   f"{pdf_path}  ({n_pages} pages, {size_mb:.1f} MB)")
    tbl.add_row("Output",  output_path)
    tbl.add_row("Engine",  method.capitalize())
    tbl.add_row("Mode",    mode.replace("_", " ").title())

    panel = Panel(
        tbl,
        title=f"[bold {ACCENT}]Configuration[/bold {ACCENT}]",
        border_style=ACCENT,
        box=box.ROUNDED,
        padding=(0, 1),
    )
    console.print()
    console.print(panel)


if __name__ == "__main__":
    main()
