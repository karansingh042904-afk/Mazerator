"""Unit tests for ActivityBook Studio font management, registration, and PDF embedding.

Validates that:
1. Noto Sans font files and SIL Open Font License exist locally.
2. ReportLab TrueType font registration succeeds idempotently.
3. Default base font is configured to prevent Base-14 Helvetica preamble injection.
4. Generated PDFs strictly contain 100% embedded and subsetted fonts with zero Base-14 fonts.
"""

from __future__ import annotations

import io
from pathlib import Path
import unittest

from reportlab import rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from activitybook.core.fonts import (
    BOLD_FONT_PATH,
    FONT_BOLD,
    FONT_ITALIC,
    FONT_REGULAR,
    FONTS_DIR,
    ITALIC_FONT_PATH,
    OFL_LICENSE_PATH,
    REGULAR_FONT_PATH,
    format_font_table,
    inspect_pdf_fonts,
    register_activitybook_fonts,
)
from activitybook.core.page_spec import PageSpec
from activitybook.activities.maze_activity import build_road_trip_sample_pdf


class TestFontAssetsAndRegistration(unittest.TestCase):
    """Test local font assets and ReportLab TrueType registration."""

    def test_font_files_and_license_exist(self) -> None:
        """Verify Noto Sans TTF files and OFL license exist and are non-empty."""
        self.assertTrue(FONTS_DIR.is_dir(), f"Fonts directory missing: {FONTS_DIR}")
        for path in (REGULAR_FONT_PATH, BOLD_FONT_PATH, ITALIC_FONT_PATH, OFL_LICENSE_PATH):
            self.assertTrue(path.exists(), f"Missing file: {path}")
            self.assertGreater(path.stat().st_size, 1000, f"File too small: {path}")

    def test_register_activitybook_fonts(self) -> None:
        """Verify idempotent registration with ReportLab pdfmetrics."""
        success = register_activitybook_fonts()
        self.assertTrue(success)

        # Verify all 3 fonts are registered
        for font_name in (FONT_REGULAR, FONT_BOLD, FONT_ITALIC):
            font = pdfmetrics.getFont(font_name)
            self.assertIsNotNone(font)
            self.assertTrue(font._dynamicFont)

        # Verify default base font is configured to FONT_REGULAR
        self.assertEqual(rl_config.canvas_basefontname, FONT_REGULAR)

        # Second call must also return True idempotently without error
        self.assertTrue(register_activitybook_fonts())


class TestPdfFontEmbedding(unittest.TestCase):
    """Test font embedding and absence of Base-14 unembedded fonts in PDFs."""

    def setUp(self) -> None:
        register_activitybook_fonts()

    def test_rendered_canvas_embeds_truetype_font(self) -> None:
        """A canvas using Noto Sans must embed and subset the font without Helvetica."""
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(504, 720), initialFontName=FONT_REGULAR)
        c.setFont(FONT_REGULAR, 12)
        c.drawString(100, 600, "Road Trip Quest - Regular Text")
        c.setFont(FONT_BOLD, 14)
        c.drawString(100, 570, "Road Trip Quest - Bold Header")
        c.setFont(FONT_ITALIC, 10)
        c.drawString(100, 540, "Road Trip Quest - Italic Subtitle")
        c.showPage()
        c.save()

        buf.seek(0)
        fonts = inspect_pdf_fonts(buf)
        self.assertGreaterEqual(len(fonts), 1)

        for f in fonts:
            self.assertTrue(f.embedded, f"Font {f.name} is not embedded")
            self.assertTrue(f.subset, f"Font {f.name} is not subsetted")
            self.assertNotIn("Helvetica", f.name)

    def test_sample_v3_pdf_has_all_fonts_embedded_and_no_helvetica(self) -> None:
        """The 12-page road_trip_mazes_sample_v3.pdf must have 100% embedded fonts."""
        v3_path = Path("output/road_trip_mazes_sample_v3.pdf")
        if not v3_path.exists():
            build_road_trip_sample_pdf(output_path=str(v3_path))

        fonts = inspect_pdf_fonts(v3_path)
        self.assertGreaterEqual(len(fonts), 3, "Expected at least Regular, Bold, and Italic fonts")

        font_names = [f.name for f in fonts]
        for f in fonts:
            self.assertTrue(f.embedded, f"Font {f.name} in v3 PDF is not embedded")
            self.assertTrue(f.subset, f"Font {f.name} in v3 PDF is not subsetted")
            self.assertEqual(f.font_type, "TrueType", f"Font {f.name} must be TrueType")
            self.assertFalse(f.name.startswith("Helvetica"), f"Found unembedded Base-14 font: {f.name}")

        # Check formatted table output
        table_output = format_font_table(fonts)
        self.assertIn("AAAAAA+NotoSans-Regular", table_output)
        self.assertIn("AAAAAA+NotoSans-Bold", table_output)
        self.assertIn("AAAAAA+NotoSans-Italic", table_output)
        self.assertIn("yes yes", table_output)
        self.assertNotIn("Helvetica", table_output)


if __name__ == "__main__":
    unittest.main()
