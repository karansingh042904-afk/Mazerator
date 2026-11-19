"""Font management, registration, and embedding inspection for ActivityBook Studio.

Registers high-quality TrueType fonts (Google Noto Sans) licensed under the
SIL Open Font License (OFL) to ensure that all typography is 100% embedded
and subsetted in the exported PDF, strictly adhering to Amazon KDP print requirements.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
from typing import BinaryIO, NamedTuple

from reportlab import rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Font identifiers
FONT_REGULAR: str = "NotoSans-Regular"
FONT_BOLD: str = "NotoSans-Bold"
FONT_ITALIC: str = "NotoSans-Italic"

# Package font directory
FONTS_DIR = Path(__file__).resolve().parents[1] / "assets" / "fonts"

REGULAR_FONT_PATH = FONTS_DIR / "NotoSans-Regular.ttf"
BOLD_FONT_PATH = FONTS_DIR / "NotoSans-Bold.ttf"
ITALIC_FONT_PATH = FONTS_DIR / "NotoSans-Italic.ttf"
OFL_LICENSE_PATH = FONTS_DIR / "OFL.txt"

# 6-letter random prefix followed by '+' indicating font subsetting
_SUBSET_PATTERN = re.compile(r"^[A-Z]{6}\+")


def register_activitybook_fonts() -> bool:
    """Register Noto Sans TrueType fonts with ReportLab.

    Registers:
    - NotoSans-Regular (from NotoSans-Regular.ttf)
    - NotoSans-Bold (from NotoSans-Bold.ttf)
    - NotoSans-Italic (from NotoSans-Italic.ttf)

    Returns True if fonts were successfully loaded and registered.
    """
    if not (REGULAR_FONT_PATH.exists() and BOLD_FONT_PATH.exists() and ITALIC_FONT_PATH.exists()):
        return False

    font_specs = [
        (FONT_REGULAR, str(REGULAR_FONT_PATH)),
        (FONT_BOLD, str(BOLD_FONT_PATH)),
        (FONT_ITALIC, str(ITALIC_FONT_PATH)),
    ]

    for font_name, path in font_specs:
        try:
            pdfmetrics.getFont(font_name)
        except KeyError:
            pdfmetrics.registerFont(TTFont(font_name, path))

    # Set canvas default base font so preamble never injects unembedded Base-14 Helvetica
    rl_config.canvas_basefontname = FONT_REGULAR

    return True


class FontInspectionResult(NamedTuple):
    """Metadata describing a font detected in a PDF."""

    name: str
    font_type: str
    embedded: bool
    subset: bool
    encoding: str


def inspect_pdf_fonts(pdf_source: str | Path | BinaryIO) -> list[FontInspectionResult]:
    """Inspect all font resources in a PDF file or stream and return their embedding status."""
    import pypdf

    if isinstance(pdf_source, (str, Path)):
        reader = pypdf.PdfReader(str(pdf_source))
    else:
        reader = pypdf.PdfReader(pdf_source)

    unique_fonts: dict[str, FontInspectionResult] = {}

    for page in reader.pages:
        if "/Resources" not in page:
            continue
        resources = page["/Resources"]
        if "/Font" not in resources:
            continue

        font_dict = resources["/Font"]
        for key in font_dict:
            font_obj = font_dict[key].get_object()
            raw_base_font = str(font_obj.get("/BaseFont", "Unknown"))
            clean_name = raw_base_font.lstrip("/")
            font_type = str(font_obj.get("/Subtype", "Unknown")).lstrip("/")
            encoding = str(font_obj.get("/Encoding", "Standard")).lstrip("/")

            # Check if font descriptor contains embedded font streams
            embedded = False
            desc_ref = font_obj.get("/FontDescriptor")
            if desc_ref:
                desc = desc_ref.get_object()
                embedded = any(k in desc for k in ("/FontFile", "/FontFile2", "/FontFile3"))

            # Check if font name starts with 6-letter subset tag (e.g. AAAAAA+NotoSans-Regular)
            is_subset = bool(_SUBSET_PATTERN.match(clean_name))

            res = FontInspectionResult(
                name=clean_name,
                font_type=font_type,
                embedded=embedded,
                subset=is_subset,
                encoding=encoding,
            )
            unique_fonts[clean_name] = res

    return list(unique_fonts.values())


def format_font_table(fonts: list[FontInspectionResult]) -> str:
    """Format font inspection results as a text table equivalent to `pdffonts`."""
    headers = ["name", "type", "encoding", "emb", "sub"]
    rows = []
    for f in sorted(fonts, key=lambda x: x.name):
        rows.append([
            f.name,
            f.font_type,
            f.encoding,
            "yes" if f.embedded else "no",
            "yes" if f.subset else "no",
        ])

    col_widths = [
        max(len(h), max((len(r[i]) for r in rows), default=0))
        for i, h in enumerate(headers)
    ]
    # Add padding
    col_widths[0] = max(col_widths[0], 36)

    header_str = " ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
    sep_str = " ".join("-" * col_widths[i] for i in range(len(headers)))
    row_strs = [" ".join(f"{r[i]:<{col_widths[i]}}" for i in range(len(headers))) for r in rows]

    return "\n".join([header_str, sep_str] + row_strs)
