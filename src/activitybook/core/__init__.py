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

__all__ = [
    "POINTS_PER_INCH",
    "ContentRect",
    "PageMargins",
    "PageSpec",
    "TrimSize",
    "get_kdp_minimum_gutter_inches",
    "inches_to_points",
    "points_to_inches",
]

