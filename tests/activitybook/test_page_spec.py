"""Unit tests for ActivityBook Studio KDP page geometry and safe-area validation."""

from pathlib import Path
import sys

# Ensure src/ is on sys.path so activitybook is importable during tests
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import unittest

from activitybook.core.page_spec import (
    POINTS_PER_INCH,
    ContentRect,
    PageMargins,
    PageSpec,
    TrimSize,
    TRIM_6X9,
    TRIM_7X10,
    TRIM_8_5X11,
    get_kdp_minimum_gutter_inches,
    inches_to_points,
    points_to_inches,
)


class TestUnitConversions(unittest.TestCase):
    """Test standard PostScript point and inch conversions."""

    def test_inches_to_points_exact(self):
        self.assertEqual(inches_to_points(1.0), 72.0)
        self.assertEqual(inches_to_points(7.0), 504.0)
        self.assertEqual(inches_to_points(10.0), 720.0)
        self.assertEqual(inches_to_points(0.5), 36.0)
        self.assertEqual(inches_to_points(0.375), 27.0)
        self.assertEqual(inches_to_points(0.25), 18.0)

    def test_points_to_inches_exact(self):
        self.assertEqual(points_to_inches(72.0), 1.0)
        self.assertEqual(points_to_inches(504.0), 7.0)
        self.assertEqual(points_to_inches(720.0), 10.0)
        self.assertEqual(points_to_inches(36.0), 0.5)
        self.assertEqual(points_to_inches(27.0), 0.375)
        self.assertEqual(points_to_inches(18.0), 0.25)

    def test_roundtrip_conversion(self):
        for val in (0.125, 0.25, 0.375, 0.5, 1.0, 7.0, 8.5, 10.0, 11.0):
            self.assertAlmostEqual(points_to_inches(inches_to_points(val)), val, places=5)


class TestKdpMinimumGutter(unittest.TestCase):
    """Test official Amazon KDP interior gutter requirements by page count."""

    def test_tier_24_to_150_pages(self):
        self.assertEqual(get_kdp_minimum_gutter_inches(24), 0.375)
        self.assertEqual(get_kdp_minimum_gutter_inches(96), 0.375)
        self.assertEqual(get_kdp_minimum_gutter_inches(150), 0.375)

    def test_tier_151_to_300_pages(self):
        self.assertEqual(get_kdp_minimum_gutter_inches(151), 0.500)
        self.assertEqual(get_kdp_minimum_gutter_inches(300), 0.500)

    def test_tier_301_to_500_pages(self):
        self.assertEqual(get_kdp_minimum_gutter_inches(301), 0.625)
        self.assertEqual(get_kdp_minimum_gutter_inches(500), 0.625)

    def test_tier_501_to_700_pages(self):
        self.assertEqual(get_kdp_minimum_gutter_inches(501), 0.750)
        self.assertEqual(get_kdp_minimum_gutter_inches(700), 0.750)

    def test_tier_701_to_828_pages(self):
        self.assertEqual(get_kdp_minimum_gutter_inches(701), 0.875)
        self.assertEqual(get_kdp_minimum_gutter_inches(828), 0.875)

    def test_page_count_out_of_bounds(self):
        with self.assertRaises(ValueError):
            get_kdp_minimum_gutter_inches(23)
        with self.assertRaises(ValueError):
            get_kdp_minimum_gutter_inches(0)
        with self.assertRaises(ValueError):
            get_kdp_minimum_gutter_inches(829)


class TestKdpPageSpec7x10(unittest.TestCase):
    """Test 7 × 10 inch KDP page specifications and acceptance criteria."""

    def test_default_dimensions_are_7x10_and_504x720(self):
        spec = PageSpec()
        self.assertEqual(spec.width_inches, 7.0)
        self.assertEqual(spec.height_inches, 10.0)
        self.assertEqual(spec.width_points, 504.0)
        self.assertEqual(spec.height_points, 720.0)
        self.assertEqual(spec.page_count, 96)

    def test_kdp_compliance_for_recommended_and_minimum(self):
        rec_spec = PageSpec.kdp_7x10_recommended(96)
        self.assertEqual(rec_spec.validate_kdp_compliance(), [])

        min_spec = PageSpec.kdp_7x10_minimum(96)
        self.assertEqual(min_spec.validate_kdp_compliance(), [])
        self.assertEqual(min_spec.inside_margin_inches, 0.375)
        self.assertEqual(min_spec.outside_margin_inches, 0.25)
        self.assertEqual(min_spec.top_margin_inches, 0.25)
        self.assertEqual(min_spec.bottom_margin_inches, 0.25)

    def test_kdp_compliance_catches_violations(self):
        # Inside margin too small for 96 pages (0.375 required, 0.20 provided)
        bad_gutter = PageSpec(
            trim_size=TRIM_7X10,
            page_count=96,
            inside_margin_inches=0.20,
        )
        violations = bad_gutter.validate_kdp_compliance()
        self.assertTrue(any("Inside margin" in v for v in violations))

        # Outside margin too small (0.25 required, 0.10 provided)
        bad_outside = PageSpec(
            trim_size=TRIM_7X10,
            page_count=96,
            outside_margin_inches=0.10,
        )
        violations = bad_outside.validate_kdp_compliance()
        self.assertTrue(any("Outside margin" in v for v in violations))

        # Top/bottom margin too small
        bad_vertical = PageSpec(
            trim_size=TRIM_7X10,
            page_count=96,
            top_margin_inches=0.10,
            bottom_margin_inches=0.15,
        )
        violations = bad_vertical.validate_kdp_compliance()
        self.assertTrue(any("Top margin" in v for v in violations))
        self.assertTrue(any("Bottom margin" in v for v in violations))


class TestMirroredMarginsAndContentRect(unittest.TestCase):
    """Test mirrored gutter margins between left-hand (even) and right-hand (odd) pages."""

    def setUp(self):
        # Asymmetric margins to clearly differentiate inside vs outside
        self.spec = PageSpec(
            trim_size=TRIM_7X10,
            page_count=96,
            inside_margin_inches=0.50,   # 36.0 pt gutter
            outside_margin_inches=0.25,  # 18.0 pt outside
            top_margin_inches=0.375,     # 27.0 pt top
            bottom_margin_inches=0.375,  # 27.0 pt bottom
        )

    def test_page_parity_classification(self):
        self.assertTrue(self.spec.is_right_hand_page(1))
        self.assertFalse(self.spec.is_left_hand_page(1))

        self.assertTrue(self.spec.is_left_hand_page(2))
        self.assertFalse(self.spec.is_right_hand_page(2))

        self.assertTrue(self.spec.is_right_hand_page(95))
        self.assertTrue(self.spec.is_left_hand_page(96))

        with self.assertRaises(ValueError):
            self.spec.is_right_hand_page(0)

    def test_odd_page_mirrored_margins(self):
        """Page 1 (Right-hand / Recto): Spine is on the LEFT edge."""
        margins = self.spec.get_margins_for_page(1)
        self.assertEqual(margins.left, 36.0)    # inside (gutter)
        self.assertEqual(margins.right, 18.0)   # outside
        self.assertEqual(margins.top, 27.0)
        self.assertEqual(margins.bottom, 27.0)

        rect = self.spec.get_content_rect(1)
        self.assertEqual(rect.x0, 36.0)
        self.assertEqual(rect.x1, 504.0 - 18.0)  # 486.0
        self.assertEqual(rect.y0, 27.0)
        self.assertEqual(rect.y1, 720.0 - 27.0)  # 693.0
        self.assertEqual(rect.width, 450.0)
        self.assertEqual(rect.height, 666.0)

    def test_even_page_mirrored_margins(self):
        """Page 2 (Left-hand / Verso): Spine is on the RIGHT edge."""
        margins = self.spec.get_margins_for_page(2)
        self.assertEqual(margins.left, 18.0)    # outside
        self.assertEqual(margins.right, 36.0)   # inside (gutter)
        self.assertEqual(margins.top, 27.0)
        self.assertEqual(margins.bottom, 27.0)

        rect = self.spec.get_content_rect(2)
        self.assertEqual(rect.x0, 18.0)
        self.assertEqual(rect.x1, 504.0 - 36.0)  # 468.0
        self.assertEqual(rect.y0, 27.0)
        self.assertEqual(rect.y1, 720.0 - 27.0)  # 693.0
        self.assertEqual(rect.width, 450.0)
        self.assertEqual(rect.height, 666.0)

    def test_content_rect_widths_and_heights_match_across_spread(self):
        """Even and odd pages must have identical printable dimensions, only x0 shifted."""
        rect_odd = self.spec.get_content_rect(1)
        rect_even = self.spec.get_content_rect(2)

        self.assertEqual(rect_odd.width, rect_even.width)
        self.assertEqual(rect_odd.height, rect_even.height)
        # Shift amount is exactly inside_margin - outside_margin
        self.assertEqual(rect_odd.x0 - rect_even.x0, 36.0 - 18.0)


class TestSafeAreaValidation(unittest.TestCase):
    """Test point and bounding box safe-area validation."""

    def setUp(self):
        self.spec = PageSpec.kdp_7x10_recommended(96)
        # Inside=36.0, Outside=36.0, Top=36.0, Bottom=36.0
        # ContentRect: x0=36.0, y0=36.0, x1=468.0, y1=684.0

    def test_is_point_safe(self):
        # Safe center
        self.assertTrue(self.spec.is_point_safe(252.0, 360.0, page_number=1))
        # Exact corners
        self.assertTrue(self.spec.is_point_safe(36.0, 36.0, page_number=1))
        self.assertTrue(self.spec.is_point_safe(468.0, 684.0, page_number=1))

        # Unsafe inside gutter margin
        self.assertFalse(self.spec.is_point_safe(20.0, 360.0, page_number=1))
        # Unsafe inside top margin
        self.assertFalse(self.spec.is_point_safe(252.0, 700.0, page_number=1))

    def test_is_rect_safe(self):
        # Fully inside
        self.assertTrue(self.spec.is_rect_safe(50.0, 50.0, 400.0, 600.0, page_number=1))
        # Touching boundary
        self.assertTrue(self.spec.is_rect_safe(36.0, 36.0, 468.0, 684.0, page_number=1))
        # Crossing left margin
        self.assertFalse(self.spec.is_rect_safe(25.0, 50.0, 400.0, 600.0, page_number=1))
        # Crossing top margin
        self.assertFalse(self.spec.is_rect_safe(50.0, 50.0, 400.0, 710.0, page_number=1))

    def test_validate_rect_safe_raises_with_detailed_message(self):
        # Valid rect does not raise
        self.spec.validate_rect_safe(50.0, 50.0, 400.0, 600.0, page_number=1)

        # Invalid rect raises ValueError with page and violation info
        with self.assertRaises(ValueError) as ctx:
            self.spec.validate_rect_safe(10.0, 10.0, 400.0, 600.0, page_number=1)
        err = str(ctx.exception)
        self.assertIn("Page 1 (Right-hand (Odd))", err)
        self.assertIn("Left edge", err)
        self.assertIn("Bottom edge", err)


class TestAlternateTrimSizes(unittest.TestCase):
    """Test support for other common Amazon KDP trim sizes."""

    def test_8_5x11_dimensions(self):
        spec = PageSpec(trim_size=TRIM_8_5X11)
        self.assertEqual(spec.width_points, 612.0)
        self.assertEqual(spec.height_points, 792.0)

    def test_6x9_dimensions(self):
        spec = PageSpec(trim_size=TRIM_6X9)
        self.assertEqual(spec.width_points, 432.0)
        self.assertEqual(spec.height_points, 648.0)


if __name__ == "__main__":
    unittest.main()
