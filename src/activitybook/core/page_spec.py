"""KDP page geometry, trim sizes, mirrored margins, and safe-area validation.

This module provides the geometry foundations for generating print-ready
Amazon KDP books (such as 7 × 10-inch children's activity books).
It calculates precise PostScript point measurements, manages mirrored
gutter margins between left-hand (even) and right-hand (odd) pages, and
enforces safe-area boundary constraints to ensure no content is clipped
during commercial printing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

# PostScript / PDF standard: 72 points per inch.
POINTS_PER_INCH: float = 72.0


def inches_to_points(inches: float) -> float:
    """Convert measurement in inches to PostScript points (72 pt / in)."""
    return round(inches * POINTS_PER_INCH, 6)


def points_to_inches(points: float) -> float:
    """Convert measurement in PostScript points to inches."""
    return round(points / POINTS_PER_INCH, 6)


def get_kdp_minimum_gutter_inches(page_count: int) -> float:
    """Return Amazon KDP minimum inside (gutter) margin in inches by page count.

    Amazon KDP Guidelines (No Bleed):
    - 24 to 150 pages:  0.375 in (27.0 pt)
    - 151 to 300 pages: 0.500 in (36.0 pt)
    - 301 to 500 pages: 0.625 in (45.0 pt)
    - 501 to 700 pages: 0.750 in (54.0 pt)
    - 701 to 828 pages: 0.875 in (63.0 pt)
    """
    if page_count < 24:
        raise ValueError(
            f"Amazon KDP paperback requires at least 24 pages (got {page_count})"
        )
    if page_count > 828:
        raise ValueError(
            f"Amazon KDP paperback supports at most 828 pages (got {page_count})"
        )

    if page_count <= 150:
        return 0.375
    elif page_count <= 300:
        return 0.500
    elif page_count <= 500:
        return 0.625
    elif page_count <= 700:
        return 0.750
    else:
        return 0.875


# KDP minimum outside, top, and bottom margins for no-bleed books.
KDP_MIN_OUTSIDE_MARGIN_INCHES: float = 0.25
KDP_MIN_TOP_MARGIN_INCHES: float = 0.25
KDP_MIN_BOTTOM_MARGIN_INCHES: float = 0.25


@dataclass(frozen=True)
class TrimSize:
    """Trim dimensions for a book interior."""

    width_inches: float
    height_inches: float
    name: str = ""

    @property
    def width_points(self) -> float:
        return inches_to_points(self.width_inches)

    @property
    def height_points(self) -> float:
        return inches_to_points(self.height_inches)


# Standard Amazon KDP Trim Size Presets
TRIM_7X10 = TrimSize(7.0, 10.0, "7 x 10 in")
TRIM_8_5X11 = TrimSize(8.5, 11.0, "8.5 x 11 in")
TRIM_6X9 = TrimSize(6.0, 9.0, "6 x 9 in")
TRIM_8X10 = TrimSize(8.0, 10.0, "8 x 10 in")


class PageMargins(NamedTuple):
    """Calculated margins in points for a specific page."""

    left: float
    right: float
    top: float
    bottom: float


@dataclass(frozen=True)
class ContentRect:
    """Printable content rectangle in PDF canvas coordinates (bottom-left origin).

    Attributes:
        x0: Left boundary in points.
        y0: Bottom boundary in points.
        x1: Right boundary in points.
        y1: Top boundary in points.
    """

    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def width(self) -> float:
        """Width of the printable content rectangle."""
        return round(self.x1 - self.x0, 6)

    @property
    def height(self) -> float:
        """Height of the printable content rectangle."""
        return round(self.y1 - self.y0, 6)

    def contains_point(self, x: float, y: float, tolerance: float = 1e-4) -> bool:
        """Check if a point (x, y) is inside or on the boundary of this rectangle."""
        return (
            (self.x0 - tolerance) <= x <= (self.x1 + tolerance)
            and (self.y0 - tolerance) <= y <= (self.y1 + tolerance)
        )

    def contains_rect(
        self,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        tolerance: float = 1e-4,
    ) -> bool:
        """Check if the given rectangle [x0, y0, x1, y1] is completely inside this content area."""
        min_x = min(x0, x1)
        max_x = max(x0, x1)
        min_y = min(y0, y1)
        max_y = max(y0, y1)
        return (
            (self.x0 - tolerance) <= min_x
            and max_x <= (self.x1 + tolerance)
            and (self.y0 - tolerance) <= min_y
            and max_y <= (self.y1 + tolerance)
        )


@dataclass(frozen=True)
class PageSpec:
    """Specification for KDP book page geometry and mirrored margins.

    Default configuration is standard for Amazon KDP Children's Activity Books:
    7.0 × 10.0 inches (504 × 720 points), 96 pages, with generous safe margins.
    """

    trim_size: TrimSize = TRIM_7X10
    page_count: int = 96
    inside_margin_inches: float = 0.50   # Recommended generous gutter
    outside_margin_inches: float = 0.50  # Recommended generous outside
    top_margin_inches: float = 0.50      # Recommended generous top
    bottom_margin_inches: float = 0.50   # Recommended generous bottom
    bleed_inches: float = 0.0            # No bleed for standard activity interiors

    @property
    def width_inches(self) -> float:
        return self.trim_size.width_inches

    @property
    def height_inches(self) -> float:
        return self.trim_size.height_inches

    @property
    def width_points(self) -> float:
        """Total page width in PostScript points."""
        return self.trim_size.width_points

    @property
    def height_points(self) -> float:
        """Total page height in PostScript points."""
        return self.trim_size.height_points

    @property
    def inside_margin_points(self) -> float:
        """Inside (gutter) margin in points."""
        return inches_to_points(self.inside_margin_inches)

    @property
    def outside_margin_points(self) -> float:
        """Outside margin in points."""
        return inches_to_points(self.outside_margin_inches)

    @property
    def top_margin_points(self) -> float:
        """Top margin in points."""
        return inches_to_points(self.top_margin_inches)

    @property
    def bottom_margin_points(self) -> float:
        """Bottom margin in points."""
        return inches_to_points(self.bottom_margin_inches)

    @classmethod
    def kdp_7x10_recommended(cls, page_count: int = 96) -> PageSpec:
        """Factory for 7 × 10-inch book with recommended safe margins (0.5 in)."""
        min_gutter = get_kdp_minimum_gutter_inches(page_count)
        inside = max(0.50, min_gutter)
        return cls(
            trim_size=TRIM_7X10,
            page_count=page_count,
            inside_margin_inches=inside,
            outside_margin_inches=0.50,
            top_margin_inches=0.50,
            bottom_margin_inches=0.50,
            bleed_inches=0.0,
        )

    @classmethod
    def kdp_7x10_minimum(cls, page_count: int = 96) -> PageSpec:
        """Factory for 7 × 10-inch book with strict KDP minimum margins."""
        inside = get_kdp_minimum_gutter_inches(page_count)
        return cls(
            trim_size=TRIM_7X10,
            page_count=page_count,
            inside_margin_inches=inside,
            outside_margin_inches=KDP_MIN_OUTSIDE_MARGIN_INCHES,
            top_margin_inches=KDP_MIN_TOP_MARGIN_INCHES,
            bottom_margin_inches=KDP_MIN_BOTTOM_MARGIN_INCHES,
            bleed_inches=0.0,
        )

    def validate_kdp_compliance(self) -> list[str]:
        """Validate margins against Amazon KDP requirements.

        Returns a list of violation messages (empty list if 100% compliant).
        """
        violations: list[str] = []
        try:
            min_gutter = get_kdp_minimum_gutter_inches(self.page_count)
            if self.inside_margin_inches < min_gutter:
                violations.append(
                    f"Inside margin ({self.inside_margin_inches:.3f} in) is below KDP minimum "
                    f"of {min_gutter:.3f} in for {self.page_count} pages."
                )
        except ValueError as exc:
            violations.append(str(exc))

        if self.outside_margin_inches < KDP_MIN_OUTSIDE_MARGIN_INCHES:
            violations.append(
                f"Outside margin ({self.outside_margin_inches:.3f} in) is below KDP minimum "
                f"of {KDP_MIN_OUTSIDE_MARGIN_INCHES:.3f} in."
            )
        if self.top_margin_inches < KDP_MIN_TOP_MARGIN_INCHES:
            violations.append(
                f"Top margin ({self.top_margin_inches:.3f} in) is below KDP minimum "
                f"of {KDP_MIN_TOP_MARGIN_INCHES:.3f} in."
            )
        if self.bottom_margin_inches < KDP_MIN_BOTTOM_MARGIN_INCHES:
            violations.append(
                f"Bottom margin ({self.bottom_margin_inches:.3f} in) is below KDP minimum "
                f"of {KDP_MIN_BOTTOM_MARGIN_INCHES:.3f} in."
            )

        # Check that content area is positive
        content_w = self.width_inches - (self.inside_margin_inches + self.outside_margin_inches)
        content_h = self.height_inches - (self.top_margin_inches + self.bottom_margin_inches)
        if content_w <= 0:
            violations.append(
                f"Horizontal margins ({self.inside_margin_inches + self.outside_margin_inches:.2f} in) "
                f"exceed page width ({self.width_inches:.2f} in)."
            )
        if content_h <= 0:
            violations.append(
                f"Vertical margins ({self.top_margin_inches + self.bottom_margin_inches:.2f} in) "
                f"exceed page height ({self.height_inches:.2f} in)."
            )

        return violations

    @staticmethod
    def is_right_hand_page(page_number: int) -> bool:
        """Return True if page_number is a right-hand page (recto / odd).

        Page 1 is a right-hand page. The book spine is on the LEFT edge.
        """
        if page_number < 1:
            raise ValueError(f"page_number must be >= 1 (got {page_number})")
        return (page_number % 2) == 1

    @staticmethod
    def is_left_hand_page(page_number: int) -> bool:
        """Return True if page_number is a left-hand page (verso / even).

        Page 2 is a left-hand page. The book spine is on the RIGHT edge.
        """
        if page_number < 1:
            raise ValueError(f"page_number must be >= 1 (got {page_number})")
        return (page_number % 2) == 0

    def get_margins_for_page(self, page_number: int) -> PageMargins:
        """Calculate mirrored margins in points for a specific page number.

        - For Odd / Right-hand pages (1, 3, 5...):
          The spine is on the LEFT edge, so:
            left_margin = inside_margin (gutter)
            right_margin = outside_margin

        - For Even / Left-hand pages (2, 4, 6...):
          The spine is on the RIGHT edge, so:
            left_margin = outside_margin
            right_margin = inside_margin (gutter)

        Top and bottom margins are identical on all pages.
        """
        if self.is_right_hand_page(page_number):
            left = self.inside_margin_points
            right = self.outside_margin_points
        else:
            left = self.outside_margin_points
            right = self.inside_margin_points

        return PageMargins(
            left=left,
            right=right,
            top=self.top_margin_points,
            bottom=self.bottom_margin_points,
        )

    def get_content_rect(self, page_number: int) -> ContentRect:
        """Calculate the printable content bounding box in points for page_number."""
        margins = self.get_margins_for_page(page_number)
        x0 = margins.left
        y0 = margins.bottom
        x1 = self.width_points - margins.right
        y1 = self.height_points - margins.top
        return ContentRect(x0=round(x0, 6), y0=round(y0, 6), x1=round(x1, 6), y1=round(y1, 6))

    def is_point_safe(self, x: float, y: float, page_number: int) -> bool:
        """Return True if (x, y) point is inside the printable safe content rectangle."""
        rect = self.get_content_rect(page_number)
        return rect.contains_point(x, y)

    def is_rect_safe(
        self,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        page_number: int,
    ) -> bool:
        """Return True if bounding box [x0, y0, x1, y1] is completely inside the safe area."""
        rect = self.get_content_rect(page_number)
        return rect.contains_rect(x0, y0, x1, y1)

    def validate_rect_safe(
        self,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        page_number: int,
    ) -> None:
        """Validate that a bounding box is within safe margins; raise ValueError if not."""
        rect = self.get_content_rect(page_number)
        min_x = min(x0, x1)
        max_x = max(x0, x1)
        min_y = min(y0, y1)
        max_y = max(y0, y1)

        errors: list[str] = []
        if min_x < rect.x0 - 1e-4:
            errors.append(f"Left edge ({min_x:.2f} pt) enters left margin (min safe: {rect.x0:.2f} pt)")
        if max_x > rect.x1 + 1e-4:
            errors.append(f"Right edge ({max_x:.2f} pt) enters right margin (max safe: {rect.x1:.2f} pt)")
        if min_y < rect.y0 - 1e-4:
            errors.append(f"Bottom edge ({min_y:.2f} pt) enters bottom margin (min safe: {rect.y0:.2f} pt)")
        if max_y > rect.y1 + 1e-4:
            errors.append(f"Top edge ({max_y:.2f} pt) enters top margin (max safe: {rect.y1:.2f} pt)")

        if errors:
            page_type = "Right-hand (Odd)" if self.is_right_hand_page(page_number) else "Left-hand (Even)"
            raise ValueError(
                f"Content on Page {page_number} ({page_type}) violates KDP safe margins:\n"
                + "\n".join(f" - {err}" for err in errors)
            )

