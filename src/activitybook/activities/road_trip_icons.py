"""Road-trip-themed black-and-white vector icons and line-art decorations.

All icons are drawn using pure ReportLab vector primitives (lines, curves, arcs,
rectangles, and polygons) for razor-sharp monochrome printing without pixelation.
"""

from __future__ import annotations

import math
from typing import Callable


def _setup_stroke(c, lw: float = 1.4, fill_white: bool = True) -> None:
    """Standard stroke and fill setup for black-and-white line art."""
    c.setLineWidth(lw)
    c.setLineCap(1)   # Round cap
    c.setLineJoin(1)  # Round join
    c.setStrokeColorRGB(0, 0, 0)
    if fill_white:
        c.setFillColorRGB(1, 1, 1)  # White fill so overlapping shapes stay clean
    else:
        c.setFillColorRGB(0, 0, 0)


def draw_car(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a friendly road-trip passenger car centered at (cx, cy) with scale s."""
    _setup_stroke(c, lw, fill_white=True)

    # Car body dimensions
    bw = s * 1.6
    bh = s * 0.5
    base_y = cy - s * 0.35

    # Main lower chassis
    c.roundRect(cx - bw * 0.5, base_y, bw, bh, s * 0.15, stroke=1, fill=1)

    # Cabin (roof & windows)
    cw = bw * 0.65
    ch = s * 0.45
    cabin_y = base_y + bh - s * 0.05
    c.roundRect(cx - cw * 0.45, cabin_y, cw, ch, s * 0.12, stroke=1, fill=1)

    # Windows (split into front and rear)
    win_w = cw * 0.38
    win_h = ch * 0.65
    win_y = cabin_y + ch * 0.18
    c.rect(cx - cw * 0.4, win_y, win_w, win_h, stroke=1, fill=0)
    c.rect(cx + cw * 0.05, win_y, win_w, win_h, stroke=1, fill=0)

    # Wheels (two circles with inner hubs)
    wheel_r = s * 0.22
    hub_r = s * 0.08
    wheel_y = base_y
    for wx in (cx - bw * 0.3, cx + bw * 0.3):
        c.setFillColorRGB(1, 1, 1)
        c.circle(wx, wheel_y, wheel_r, stroke=1, fill=1)
        c.setFillColorRGB(0, 0, 0)
        c.circle(wx, wheel_y, hub_r, stroke=1, fill=1)

    # Headlight & taillight
    c.line(cx + bw * 0.48, base_y + bh * 0.6, cx + bw * 0.52, base_y + bh * 0.6)
    c.line(cx - bw * 0.52, base_y + bh * 0.6, cx - bw * 0.48, base_y + bh * 0.6)


def draw_camper_van(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a classic adventure camper van / RV centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    bw = s * 1.8
    bh = s * 0.95
    base_y = cy - s * 0.45

    # Van body (boxy with rounded front)
    c.roundRect(cx - bw * 0.5, base_y, bw, bh, s * 0.18, stroke=1, fill=1)

    # Pop-top / roof rack
    c.roundRect(cx - bw * 0.35, base_y + bh, bw * 0.7, s * 0.18, s * 0.06, stroke=1, fill=1)

    # Windshield (slanted front)
    c.roundRect(cx + bw * 0.15, base_y + bh * 0.5, bw * 0.28, bh * 0.38, s * 0.08, stroke=1, fill=0)

    # Side window with curtains
    sw_x = cx - bw * 0.4
    sw_y = base_y + bh * 0.5
    sw_w = bw * 0.45
    sw_h = bh * 0.38
    c.rect(sw_x, sw_y, sw_w, sw_h, stroke=1, fill=0)
    # Curtain lines
    c.line(sw_x + sw_w * 0.5, sw_y, sw_x + sw_w * 0.5, sw_y + sw_h)

    # Body horizontal trim stripe
    c.line(cx - bw * 0.5, base_y + bh * 0.38, cx + bw * 0.5, base_y + bh * 0.38)

    # Wheels
    wheel_r = s * 0.24
    hub_r = s * 0.09
    wheel_y = base_y
    for wx in (cx - bw * 0.32, cx + bw * 0.32):
        c.setFillColorRGB(1, 1, 1)
        c.circle(wx, wheel_y, wheel_r, stroke=1, fill=1)
        c.setFillColorRGB(0, 0, 0)
        c.circle(wx, wheel_y, hub_r, stroke=1, fill=1)


def draw_mountain(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw twin mountain peaks with snow caps centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    # Main peak (center-left)
    p1 = c.beginPath()
    p1.moveTo(cx - s * 1.1, cy - s * 0.6)
    p1.lineTo(cx - s * 0.15, cy + s * 0.85)
    p1.lineTo(cx + s * 0.7, cy - s * 0.6)
    p1.close()
    c.drawPath(p1, stroke=1, fill=1)

    # Main peak snowcap
    c.line(cx - s * 0.38, cy + s * 0.48, cx - s * 0.25, cy + s * 0.42)
    c.line(cx - s * 0.25, cy + s * 0.42, cx - s * 0.15, cy + s * 0.5)
    c.line(cx - s * 0.15, cy + s * 0.5, cx + s * 0.05, cy + s * 0.4)

    # Secondary peak (right)
    p2 = c.beginPath()
    p2.moveTo(cx + s * 0.1, cy - s * 0.6)
    p2.lineTo(cx + s * 0.65, cy + s * 0.5)
    p2.lineTo(cx + s * 1.15, cy - s * 0.6)
    p2.close()
    c.drawPath(p2, stroke=1, fill=1)

    # Secondary peak snowcap
    c.line(cx + s * 0.48, cy + s * 0.25, cx + s * 0.65, cy + s * 0.22)
    c.line(cx + s * 0.65, cy + s * 0.22, cx + s * 0.85, cy + s * 0.26)


def draw_pine_tree(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a classic evergreen pine tree centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    # Trunk
    trunk_w = s * 0.22
    trunk_h = s * 0.35
    trunk_y = cy - s * 0.75
    c.rect(cx - trunk_w * 0.5, trunk_y, trunk_w, trunk_h, stroke=1, fill=1)

    # 3 stacked triangle foliage layers (bottom to top)
    # Bottom tier
    p1 = c.beginPath()
    p1.moveTo(cx - s * 0.8, trunk_y + trunk_h * 0.6)
    p1.lineTo(cx, cy + s * 0.1)
    p1.lineTo(cx + s * 0.8, trunk_y + trunk_h * 0.6)
    p1.close()
    c.drawPath(p1, stroke=1, fill=1)

    # Middle tier
    p2 = c.beginPath()
    p2.moveTo(cx - s * 0.65, cy - s * 0.1)
    p2.lineTo(cx, cy + s * 0.45)
    p2.lineTo(cx + s * 0.65, cy - s * 0.1)
    p2.close()
    c.drawPath(p2, stroke=1, fill=1)

    # Top tier
    p3 = c.beginPath()
    p3.moveTo(cx - s * 0.45, cy + s * 0.25)
    p3.lineTo(cx, cy + s * 0.85)
    p3.lineTo(cx + s * 0.45, cy + s * 0.25)
    p3.close()
    c.drawPath(p3, stroke=1, fill=1)


def draw_traffic_sign(c, cx: float, cy: float, s: float, lw: float = 1.4, sign_type: str = "winding") -> None:
    """Draw a highway warning diamond sign or interstate shield centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    # Sign pole
    c.line(cx, cy - s * 0.8, cx, cy - s * 0.3)

    # Diamond warning sign rotated 45 degrees
    p = c.beginPath()
    p.moveTo(cx, cy + s * 0.65)
    p.lineTo(cx + s * 0.65, cy)
    p.lineTo(cx, cy - s * 0.65)
    p.lineTo(cx - s * 0.65, cy)
    p.close()
    c.drawPath(p, stroke=1, fill=1)

    # Inner border
    p_in = c.beginPath()
    r = s * 0.52
    p_in.moveTo(cx, cy + r)
    p_in.lineTo(cx + r, cy)
    p_in.lineTo(cx, cy - r)
    p_in.lineTo(cx - r, cy)
    p_in.close()
    c.drawPath(p_in, stroke=1, fill=0)

    # Winding road curve inside
    road = c.beginPath()
    road.moveTo(cx - s * 0.22, cy - s * 0.25)
    road.curveTo(cx - s * 0.1, cy - s * 0.1, cx + s * 0.15, cy - s * 0.1, cx + s * 0.15, cy + s * 0.05)
    road.curveTo(cx + s * 0.15, cy + s * 0.2, cx - s * 0.1, cy + s * 0.15, cx - s * 0.1, cy + s * 0.3)
    c.drawPath(road, stroke=1, fill=0)


def draw_campsite(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a tent and campfire campsite scene centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    # Tent (A-frame with open flap)
    tent_w = s * 1.3
    tent_h = s * 0.9
    base_y = cy - s * 0.55

    # Main tent triangle
    p = c.beginPath()
    p.moveTo(cx - tent_w * 0.5, base_y)
    p.lineTo(cx - s * 0.05, base_y + tent_h)
    p.lineTo(cx + tent_w * 0.35, base_y)
    p.close()
    c.drawPath(p, stroke=1, fill=1)

    # Tent flap opening
    p_flap = c.beginPath()
    p_flap.moveTo(cx - tent_w * 0.2, base_y)
    p_flap.lineTo(cx - s * 0.05, base_y + tent_h * 0.75)
    p_flap.lineTo(cx + tent_w * 0.1, base_y)
    c.drawPath(p_flap, stroke=1, fill=0)

    # Campfire next to tent
    fx = cx + s * 0.65
    fy = base_y
    # Crossed logs
    c.line(fx - s * 0.2, fy, fx + s * 0.2, fy + s * 0.1)
    c.line(fx - s * 0.2, fy + s * 0.1, fx + s * 0.2, fy)
    # Flame outline
    flame = c.beginPath()
    flame.moveTo(fx - s * 0.1, fy + s * 0.08)
    flame.curveTo(fx - s * 0.15, fy + s * 0.25, fx, fy + s * 0.45, fx, fy + s * 0.45)
    flame.curveTo(fx, fy + s * 0.45, fx + s * 0.15, fy + s * 0.25, fx + s * 0.1, fy + s * 0.08)
    flame.close()
    c.drawPath(flame, stroke=1, fill=1)


def draw_traffic_cone(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a striped safety traffic cone centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    base_w = s * 1.1
    base_h = s * 0.15
    base_y = cy - s * 0.6

    # Base plate
    c.roundRect(cx - base_w * 0.5, base_y, base_w, base_h, s * 0.05, stroke=1, fill=1)

    # Cone tapered body
    p = c.beginPath()
    p.moveTo(cx - s * 0.4, base_y + base_h)
    p.lineTo(cx - s * 0.08, base_y + s * 1.15)
    p.lineTo(cx + s * 0.08, base_y + s * 1.15)
    p.lineTo(cx + s * 0.4, base_y + base_h)
    p.close()
    c.drawPath(p, stroke=1, fill=1)

    # Stripe 1
    c.line(cx - s * 0.3, base_y + s * 0.38, cx + s * 0.3, base_y + s * 0.38)
    c.line(cx - s * 0.24, base_y + s * 0.58, cx + s * 0.24, base_y + s * 0.58)

    # Stripe 2
    c.line(cx - s * 0.18, base_y + s * 0.78, cx + s * 0.18, base_y + s * 0.78)
    c.line(cx - s * 0.13, base_y + s * 0.95, cx + s * 0.13, base_y + s * 0.95)


def draw_compass(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a navigation compass rose centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    r = s * 0.75
    # Outer circle
    c.circle(cx, cy, r, stroke=1, fill=1)
    # Inner ring
    c.circle(cx, cy, r * 0.85, stroke=1, fill=0)

    # 4-point compass star
    # North needle (filled black on left side)
    p_n = c.beginPath()
    p_n.moveTo(cx, cy + r * 0.78)
    p_n.lineTo(cx - r * 0.2, cy)
    p_n.lineTo(cx, cy)
    p_n.close()
    c.setFillColorRGB(0, 0, 0)
    c.drawPath(p_n, stroke=1, fill=1)

    p_n_right = c.beginPath()
    p_n_right.moveTo(cx, cy + r * 0.78)
    p_n_right.lineTo(cx + r * 0.2, cy)
    p_n_right.lineTo(cx, cy)
    p_n_right.close()
    c.setFillColorRGB(1, 1, 1)
    c.drawPath(p_n_right, stroke=1, fill=1)

    # South needle
    p_s = c.beginPath()
    p_s.moveTo(cx, cy - r * 0.78)
    p_s.lineTo(cx + r * 0.2, cy)
    p_s.lineTo(cx, cy)
    p_s.close()
    c.setFillColorRGB(0, 0, 0)
    c.drawPath(p_s, stroke=1, fill=1)

    # East and West points
    c.line(cx - r * 0.65, cy, cx + r * 0.65, cy)

    # "N" label at top
    c.setFont("Helvetica-Bold", s * 0.28)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(cx, cy + r + 2.0, "N")


# Registry of Road Trip Icons
ROAD_TRIP_ICONS: dict[str, Callable] = {
    "car": draw_car,
    "camper_van": draw_camper_van,
    "mountain": draw_mountain,
    "pine_tree": draw_pine_tree,
    "traffic_sign": draw_traffic_sign,
    "campsite": draw_campsite,
    "traffic_cone": draw_traffic_cone,
    "compass": draw_compass,
}

