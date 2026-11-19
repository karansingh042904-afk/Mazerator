"""Core geometry, layout, and document models for ActivityBook Studio."""

from .page_spec import (
    POINTS_PER_INCH,
    ContentRect,
    PageMargins,
    PageSpec,
    TrimSize,
    get_kdp_minimum_gutter_inches,
    inches_to_points,
    points_to_inches,
)
from .fonts import (
    FONT_BOLD,
    FONT_ITALIC,
    FONT_REGULAR,
    FontInspectionResult,
    format_font_table,
    inspect_pdf_fonts,
    register_activitybook_fonts,
)

__all__ = [
    "POINTS_PER_INCH",
    "ContentRect",
    "PageMargins",
    "PageSpec",
    "TrimSize",
    "get_kdp_minimum_gutter_inches",
    "inches_to_points",
    "points_to_inches",
    "FONT_BOLD",
    "FONT_ITALIC",
    "FONT_REGULAR",
    "FontInspectionResult",
    "format_font_table",
    "inspect_pdf_fonts",
    "register_activitybook_fonts",
]

