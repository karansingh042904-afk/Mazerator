"""Everyday Adventures black-and-white vector icons and line-art decorations.

All icons are drawn using pure ReportLab vector primitives (lines, curves, arcs,
rectangles, circles, and polygons) with thick, clear outlines (1.3–1.6 pt) and
white-filled backgrounds for razor-sharp monochrome printing without pixelation.

Designed specifically for children aged 6–9: bold, distinct, and immediately
recognizable at both activity page size and miniature answer-key thumbnail size.
"""

from __future__ import annotations

import math
from typing import Callable

from activitybook.core.fonts import FONT_BOLD, register_activitybook_fonts
from activitybook.activities.road_trip_icons import (
    ROAD_TRIP_ICONS,
    draw_camper_van,
    draw_campsite,
    draw_car,
    draw_compass,
    draw_mountain,
    draw_pine_tree,
    draw_traffic_cone,
    draw_traffic_sign,
)


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


# =============================================================================
# SCENARIO 1: Animal Adventures (Puppy & Bone)
# =============================================================================

def draw_puppy(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a friendly puppy face centered at (cx, cy) with scale s."""
    _setup_stroke(c, lw, fill_white=True)

    # Head
    hr = s * 0.72
    c.circle(cx, cy, hr, stroke=1, fill=1)

    # Floppy ears (left and right)
    ear_w = s * 0.35
    ear_h = s * 0.65
    # Left ear
    p_left = c.beginPath()
    p_left.moveTo(cx - hr * 0.7, cy + hr * 0.4)
    p_left.curveTo(cx - hr * 1.3, cy + hr * 0.2, cx - hr * 1.2, cy - hr * 0.5, cx - hr * 0.6, cy - hr * 0.4)
    p_left.close()
    c.drawPath(p_left, stroke=1, fill=1)

    # Right ear
    p_right = c.beginPath()
    p_right.moveTo(cx + hr * 0.7, cy + hr * 0.4)
    p_right.curveTo(cx + hr * 1.3, cy + hr * 0.2, cx + hr * 1.2, cy - hr * 0.5, cx + hr * 0.6, cy - hr * 0.4)
    p_right.close()
    c.drawPath(p_right, stroke=1, fill=1)

    # Eyes (two filled circles)
    eye_r = s * 0.10
    eye_offset = s * 0.28
    c.setFillColorRGB(0, 0, 0)
    c.circle(cx - eye_offset, cy + s * 0.15, eye_r, stroke=1, fill=1)
    c.circle(cx + eye_offset, cy + s * 0.15, eye_r, stroke=1, fill=1)

    # Snout / Muzzle
    c.setFillColorRGB(1, 1, 1)
    c.roundRect(cx - s * 0.3, cy - s * 0.35, s * 0.6, s * 0.38, s * 0.15, stroke=1, fill=1)

    # Nose (black rounded triangle)
    nose = c.beginPath()
    nose.moveTo(cx - s * 0.12, cy - s * 0.08)
    nose.lineTo(cx + s * 0.12, cy - s * 0.08)
    nose.lineTo(cx, cy - s * 0.22)
    nose.close()
    c.setFillColorRGB(0, 0, 0)
    c.drawPath(nose, stroke=1, fill=1)

    # Smile
    c.line(cx, cy - s * 0.22, cx, cy - s * 0.28)
    c.line(cx - s * 0.12, cy - s * 0.32, cx, cy - s * 0.28)
    c.line(cx, cy - s * 0.28, cx + s * 0.12, cy - s * 0.32)


def draw_bone(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a classic dog bone centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    bw = s * 1.4
    bh = s * 0.32
    r = s * 0.22

    # Draw end knobs first (2 circles on left, 2 circles on right)
    left_x = cx - bw * 0.42
    right_x = cx + bw * 0.42
    for x in (left_x, right_x):
        c.circle(x, cy + r * 0.7, r, stroke=1, fill=1)
        c.circle(x, cy - r * 0.7, r, stroke=1, fill=1)

    # Middle horizontal bar
    c.roundRect(cx - bw * 0.5, cy - bh * 0.5, bw, bh, bh * 0.4, stroke=1, fill=1)


# =============================================================================
# SCENARIO 2: Playground Fun (Scooter & Slide)
# =============================================================================

def draw_scooter(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a child's kick scooter centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    base_y = cy - s * 0.4
    # Wheels (front and back)
    wr = s * 0.22
    rear_x = cx - s * 0.65
    front_x = cx + s * 0.55

    for wx in (rear_x, front_x):
        c.circle(wx, base_y, wr, stroke=1, fill=1)
        c.setFillColorRGB(0, 0, 0)
        c.circle(wx, base_y, s * 0.08, stroke=1, fill=1)
        c.setFillColorRGB(1, 1, 1)

    # Footboard
    c.roundRect(rear_x + wr * 0.5, base_y + wr * 0.3, (front_x - rear_x) - wr, s * 0.14, s * 0.05, stroke=1, fill=1)

    # Steering column (upright angled slightly back)
    c.line(front_x, base_y + wr * 0.5, front_x - s * 0.1, cy + s * 0.7)

    # T-bar handlebars
    hx = front_x - s * 0.1
    hy = cy + s * 0.7
    c.line(hx - s * 0.35, hy, hx + s * 0.35, hy)
    # Grips
    c.circle(hx - s * 0.35, hy, s * 0.06, stroke=1, fill=1)
    c.circle(hx + s * 0.35, hy, s * 0.06, stroke=1, fill=1)


def draw_slide(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a playground slide with ladder centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    ladder_x = cx - s * 0.65
    base_y = cy - s * 0.6
    top_y = cy + s * 0.75

    # Ladder rails
    c.line(ladder_x - s * 0.12, base_y, ladder_x - s * 0.12, top_y)
    c.line(ladder_x + s * 0.12, base_y, ladder_x + s * 0.12, top_y)

    # Ladder rungs
    for step_y in (base_y + s * 0.25, base_y + s * 0.55, base_y + s * 0.85, top_y - s * 0.15):
        c.line(ladder_x - s * 0.12, step_y, ladder_x + s * 0.12, step_y)

    # Platform at top
    c.roundRect(ladder_x - s * 0.18, top_y, s * 0.45, s * 0.12, s * 0.04, stroke=1, fill=1)

    # Slide chute curve
    slide_p = c.beginPath()
    slide_p.moveTo(ladder_x + s * 0.25, top_y + s * 0.05)
    slide_p.curveTo(cx - s * 0.1, top_y - s * 0.1, cx + s * 0.2, cy - s * 0.1, cx + s * 0.85, base_y + s * 0.08)
    slide_p.lineTo(cx + s * 0.85, base_y)
    slide_p.curveTo(cx + s * 0.15, cy - s * 0.22, cx - s * 0.15, top_y - s * 0.22, ladder_x + s * 0.25, top_y - s * 0.08)
    slide_p.close()
    c.drawPath(slide_p, stroke=1, fill=1)


# =============================================================================
# SCENARIO 3: Garden Discovery (Bee & Beehive)
# =============================================================================

def draw_bee(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a friendly bumblebee centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    # Wings (two teardrop ovals at top)
    w_left = c.beginPath()
    w_left.moveTo(cx - s * 0.1, cy + s * 0.15)
    w_left.curveTo(cx - s * 0.45, cy + s * 0.8, cx + s * 0.1, cy + s * 0.75, cx, cy + s * 0.2)
    w_left.close()
    c.drawPath(w_left, stroke=1, fill=1)

    w_right = c.beginPath()
    w_right.moveTo(cx + s * 0.1, cy + s * 0.15)
    w_right.curveTo(cx + s * 0.55, cy + s * 0.75, cx + s * 0.2, cy + s * 0.75, cx + s * 0.05, cy + s * 0.2)
    w_right.close()
    c.drawPath(w_right, stroke=1, fill=1)

    # Body (oval)
    bw = s * 0.95
    bh = s * 0.65
    c.roundRect(cx - bw * 0.5, cy - bh * 0.5, bw, bh, bh * 0.45, stroke=1, fill=1)

    # Stripes
    c.line(cx - s * 0.15, cy - bh * 0.48, cx - s * 0.15, cy + bh * 0.48)
    c.line(cx + s * 0.12, cy - bh * 0.48, cx + s * 0.12, cy + bh * 0.48)

    # Stinger
    stinger = c.beginPath()
    stinger.moveTo(cx - bw * 0.5, cy - s * 0.08)
    stinger.lineTo(cx - bw * 0.7, cy)
    stinger.lineTo(cx - bw * 0.5, cy + s * 0.08)
    stinger.close()
    c.setFillColorRGB(0, 0, 0)
    c.drawPath(stinger, stroke=1, fill=1)

    # Eye & Antennae
    c.circle(cx + bw * 0.28, cy + s * 0.1, s * 0.08, stroke=1, fill=1)
    # Antenna
    c.line(cx + bw * 0.35, cy + s * 0.25, cx + bw * 0.45, cy + s * 0.55)
    c.circle(cx + bw * 0.45, cy + s * 0.55, s * 0.05, stroke=1, fill=1)


def draw_beehive(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a classic skep beehive centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    base_y = cy - s * 0.55
    # 4 rounded stacked tiers
    tiers = [
        (s * 1.3, s * 0.25),   # bottom
        (s * 1.15, s * 0.26),  # mid-lower
        (s * 0.92, s * 0.25),  # mid-upper
        (s * 0.60, s * 0.25),  # top dome
    ]

    cur_y = base_y
    for tw, th in tiers:
        c.roundRect(cx - tw * 0.5, cur_y, tw, th, th * 0.45, stroke=1, fill=1)
        cur_y += th * 0.85

    # Small branch handle at very top
    c.line(cx, cur_y + s * 0.02, cx, cur_y + s * 0.15)
    c.circle(cx, cur_y + s * 0.16, s * 0.06, stroke=1, fill=1)

    # Entrance hole (arched black opening at bottom center)
    p_hole = c.beginPath()
    p_hole.moveTo(cx - s * 0.16, base_y)
    p_hole.lineTo(cx - s * 0.16, base_y + s * 0.22)
    p_hole.curveTo(cx - s * 0.16, base_y + s * 0.34, cx + s * 0.16, base_y + s * 0.34, cx + s * 0.16, base_y + s * 0.22)
    p_hole.lineTo(cx + s * 0.16, base_y)
    p_hole.close()
    c.setFillColorRGB(0, 0, 0)
    c.drawPath(p_hole, stroke=1, fill=1)


# =============================================================================
# SCENARIO 4: School Day Adventures (Backpack & Trophy)
# =============================================================================

def draw_backpack(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a school backpack centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    bw = s * 1.15
    bh = s * 1.2
    base_y = cy - s * 0.6

    # Top loop handle
    c.roundRect(cx - s * 0.22, base_y + bh - s * 0.05, s * 0.44, s * 0.25, s * 0.1, stroke=1, fill=0)

    # Main backpack body
    c.roundRect(cx - bw * 0.5, base_y, bw, bh, s * 0.25, stroke=1, fill=1)

    # Front pocket
    pw = bw * 0.72
    ph = bh * 0.42
    p_y = base_y + s * 0.08
    c.roundRect(cx - pw * 0.5, p_y, pw, ph, s * 0.12, stroke=1, fill=1)
    # Zipper line
    c.line(cx - pw * 0.4, p_y + ph * 0.8, cx + pw * 0.4, p_y + ph * 0.8)

    # Top flap / zipper curve
    c.line(cx - bw * 0.42, base_y + bh * 0.75, cx + bw * 0.42, base_y + bh * 0.75)


def draw_trophy(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a celebration first-place trophy cup centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    base_y = cy - s * 0.65
    # Base pedestal
    c.roundRect(cx - s * 0.6, base_y, s * 1.2, s * 0.2, s * 0.05, stroke=1, fill=1)
    c.roundRect(cx - s * 0.4, base_y + s * 0.18, s * 0.8, s * 0.16, s * 0.04, stroke=1, fill=1)

    # Stem
    c.rect(cx - s * 0.12, base_y + s * 0.34, s * 0.24, s * 0.22, stroke=1, fill=1)

    # Cup bowl
    cup = c.beginPath()
    cup.moveTo(cx - s * 0.5, cy + s * 0.65)
    cup.lineTo(cx + s * 0.5, cy + s * 0.65)
    cup.curveTo(cx + s * 0.45, cy + s * 0.05, cx + s * 0.25, base_y + s * 0.54, cx, base_y + s * 0.54)
    cup.curveTo(cx - s * 0.25, base_y + s * 0.54, cx - s * 0.45, cy + s * 0.05, cx - s * 0.5, cy + s * 0.65)
    cup.close()
    c.drawPath(cup, stroke=1, fill=1)

    # Handles (left & right ears)
    for sign in (-1, 1):
        h = c.beginPath()
        h.moveTo(cx + sign * s * 0.48, cy + s * 0.55)
        h.curveTo(cx + sign * s * 0.88, cy + s * 0.45, cx + sign * s * 0.85, cy + s * 0.15, cx + sign * s * 0.32, cy + s * 0.15)
        c.drawPath(h, stroke=1, fill=0)

    # Star emblem on trophy
    c.circle(cx, cy + s * 0.35, s * 0.1, stroke=1, fill=1)


# =============================================================================
# SCENARIO 5: Forest Explorers (Acorn & Oak Tree)
# =============================================================================

def draw_acorn(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a forest acorn centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    base_y = cy - s * 0.55
    # Nut body (oval tapering to tip at bottom)
    nut = c.beginPath()
    nut.moveTo(cx - s * 0.42, cy)
    nut.curveTo(cx - s * 0.45, base_y + s * 0.15, cx, base_y, cx, base_y)
    nut.curveTo(cx, base_y, cx + s * 0.45, base_y + s * 0.15, cx + s * 0.42, cy)
    nut.close()
    c.drawPath(nut, stroke=1, fill=1)

    # Textured Cap
    cap = c.beginPath()
    cap.moveTo(cx - s * 0.5, cy - s * 0.05)
    cap.curveTo(cx - s * 0.5, cy + s * 0.45, cx + s * 0.5, cy + s * 0.45, cx + s * 0.5, cy - s * 0.05)
    cap.close()
    c.drawPath(cap, stroke=1, fill=1)

    # Cap crosshatching
    c.line(cx - s * 0.3, cy + s * 0.15, cx + s * 0.3, cy + s * 0.15)
    c.line(cx - s * 0.15, cy + s * 0.3, cx + s * 0.15, cy + s * 0.3)

    # Stem at top
    stem = c.beginPath()
    stem.moveTo(cx, cy + s * 0.38)
    stem.curveTo(cx, cy + s * 0.65, cx + s * 0.18, cy + s * 0.65, cx + s * 0.15, cy + s * 0.65)
    c.drawPath(stem, stroke=1, fill=0)


def draw_oak_tree(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a majestic oak tree with leafy canopy centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    base_y = cy - s * 0.65
    # Trunk
    c.rect(cx - s * 0.14, base_y, s * 0.28, s * 0.5, stroke=1, fill=1)
    # Root flare
    c.line(cx - s * 0.14, base_y, cx - s * 0.28, base_y)
    c.line(cx + s * 0.14, base_y, cx + s * 0.28, base_y)

    # Leafy cloud canopy (5 overlapping circular bumps)
    canopy_y = cy + s * 0.1
    c.circle(cx - s * 0.45, canopy_y - s * 0.1, s * 0.38, stroke=1, fill=1)
    c.circle(cx + s * 0.45, canopy_y - s * 0.1, s * 0.38, stroke=1, fill=1)
    c.circle(cx - s * 0.3, canopy_y + s * 0.3, s * 0.35, stroke=1, fill=1)
    c.circle(cx + s * 0.3, canopy_y + s * 0.3, s * 0.35, stroke=1, fill=1)
    c.circle(cx, canopy_y + s * 0.42, s * 0.40, stroke=1, fill=1)


# =============================================================================
# SCENARIO 6: Underwater Exploration (Submarine & Treasure Chest)
# =============================================================================

def draw_submarine(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw an exploration submarine centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    # Main hull (rounded oblong)
    bw = s * 1.5
    bh = s * 0.75
    c.roundRect(cx - bw * 0.5, cy - bh * 0.5, bw, bh, bh * 0.48, stroke=1, fill=1)

    # Conning tower (sail on top)
    tw = s * 0.45
    th = s * 0.35
    c.roundRect(cx - tw * 0.5, cy + bh * 0.4, tw, th, s * 0.08, stroke=1, fill=1)

    # Periscope
    c.line(cx, cy + bh * 0.4 + th, cx, cy + bh * 0.4 + th + s * 0.22)
    c.line(cx, cy + bh * 0.4 + th + s * 0.22, cx + s * 0.18, cy + bh * 0.4 + th + s * 0.22)

    # Porthole windows (2 round portholes)
    for px in (cx - s * 0.25, cx + s * 0.25):
        c.circle(px, cy, s * 0.15, stroke=1, fill=1)
        c.circle(px, cy, s * 0.07, stroke=1, fill=0)

    # Propeller at stern (left)
    stern_x = cx - bw * 0.5
    c.line(stern_x, cy, stern_x - s * 0.1, cy)
    p_prop = c.beginPath()
    p_prop.moveTo(stern_x - s * 0.15, cy - s * 0.22)
    p_prop.lineTo(stern_x - s * 0.1, cy)
    p_prop.lineTo(stern_x - s * 0.15, cy + s * 0.22)
    p_prop.close()
    c.drawPath(p_prop, stroke=1, fill=1)


def draw_treasure(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a classic treasure chest centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    cw = s * 1.4
    ch = s * 0.65
    base_y = cy - s * 0.5

    # Chest body (lower box)
    c.roundRect(cx - cw * 0.5, base_y, cw, ch, s * 0.08, stroke=1, fill=1)

    # Arched lid
    lid = c.beginPath()
    lid_y = base_y + ch
    lid.moveTo(cx - cw * 0.52, lid_y)
    lid.curveTo(cx - cw * 0.5, lid_y + s * 0.48, cx + cw * 0.5, lid_y + s * 0.48, cx + cw * 0.52, lid_y)
    lid.close()
    c.drawPath(lid, stroke=1, fill=1)

    # Metal reinforcing bands
    for bx in (cx - cw * 0.28, cx + cw * 0.28):
        c.line(bx, base_y, bx, base_y + ch)

    # Lock clasp / keyhole plate
    c.roundRect(cx - s * 0.15, base_y + ch - s * 0.12, s * 0.3, s * 0.24, s * 0.05, stroke=1, fill=1)
    c.circle(cx, base_y + ch, s * 0.05, stroke=1, fill=0)


# =============================================================================
# SCENARIO 7: Friendship Adventures (Bicycle & Treehouse)
# =============================================================================

def draw_bicycle(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a classic child's bicycle centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    wr = s * 0.32
    base_y = cy - s * 0.3
    rear_x = cx - s * 0.6
    front_x = cx + s * 0.6

    # Two wheels
    for wx in (rear_x, front_x):
        c.circle(wx, base_y, wr, stroke=1, fill=1)
        c.circle(wx, base_y, s * 0.08, stroke=1, fill=1)

    # Frame diamond
    bb_x = cx - s * 0.05
    bb_y = base_y
    seat_x = cx - s * 0.25
    seat_y = cy + s * 0.35
    head_x = cx + s * 0.35
    head_y = cy + s * 0.45

    # Chain stays & seat stays
    c.line(rear_x, base_y, bb_x, bb_y)
    c.line(rear_x, base_y, seat_x, seat_y)
    # Seat tube
    c.line(seat_x, seat_y, bb_x, bb_y)
    # Top tube & down tube
    c.line(seat_x, seat_y, head_x, head_y)
    c.line(bb_x, bb_y, head_x, head_y)
    # Fork
    c.line(head_x, head_y, front_x, base_y)

    # Handlebars
    c.line(head_x, head_y, head_x + s * 0.05, head_y + s * 0.18)
    c.line(head_x - s * 0.12, head_y + s * 0.18, head_x + s * 0.18, head_y + s * 0.18)

    # Seat saddle
    c.line(seat_x - s * 0.15, seat_y + s * 0.05, seat_x + s * 0.15, seat_y + s * 0.05)


def draw_treehouse(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a treehouse cabin in branches centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    base_y = cy - s * 0.65
    # Tree trunk
    c.rect(cx - s * 0.16, base_y, s * 0.32, s * 0.5, stroke=1, fill=1)

    # Cabin platform
    pw = s * 1.3
    c.roundRect(cx - pw * 0.5, cy - s * 0.15, pw, s * 0.12, s * 0.04, stroke=1, fill=1)

    # Cabin house
    hw = s * 0.9
    hh = s * 0.6
    c.rect(cx - hw * 0.5, cy - s * 0.03, hw, hh, stroke=1, fill=1)

    # Pitched roof
    roof = c.beginPath()
    roof.moveTo(cx - s * 0.58, cy + hh - s * 0.03)
    roof.lineTo(cx, cy + hh + s * 0.35)
    roof.lineTo(cx + s * 0.58, cy + hh - s * 0.03)
    roof.close()
    c.drawPath(roof, stroke=1, fill=1)

    # Window
    c.rect(cx - s * 0.15, cy + s * 0.15, s * 0.3, s * 0.25, stroke=1, fill=0)
    c.line(cx, cy + s * 0.15, cx, cy + s * 0.4)

    # Rope ladder hanging below platform
    ladder_x = cx + s * 0.42
    c.line(ladder_x - s * 0.08, cy - s * 0.15, ladder_x - s * 0.08, base_y + s * 0.1)
    c.line(ladder_x + s * 0.08, cy - s * 0.15, ladder_x + s * 0.08, base_y + s * 0.1)
    for ly in (cy - s * 0.28, cy - s * 0.42, base_y + s * 0.18):
        c.line(ladder_x - s * 0.08, ly, ladder_x + s * 0.08, ly)


# =============================================================================
# SCENARIO 8: Space Adventures (Rocket & Planet)
# =============================================================================

def draw_rocket(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a cartoon space rocket ship centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    base_y = cy - s * 0.5
    rw = s * 0.65
    rh = s * 1.1

    # Fins (left and right)
    fin_l = c.beginPath()
    fin_l.moveTo(cx - rw * 0.5, base_y + s * 0.4)
    fin_l.lineTo(cx - rw * 0.95, base_y - s * 0.08)
    fin_l.lineTo(cx - rw * 0.4, base_y + s * 0.1)
    fin_l.close()
    c.drawPath(fin_l, stroke=1, fill=1)

    fin_r = c.beginPath()
    fin_r.moveTo(cx + rw * 0.5, base_y + s * 0.4)
    fin_r.lineTo(cx + rw * 0.95, base_y - s * 0.08)
    fin_r.lineTo(cx + rw * 0.4, base_y + s * 0.1)
    fin_r.close()
    c.drawPath(fin_r, stroke=1, fill=1)

    # Main Fuselage (bullet shape)
    body = c.beginPath()
    body.moveTo(cx - rw * 0.5, base_y + s * 0.1)
    body.lineTo(cx - rw * 0.5, base_y + rh * 0.6)
    body.curveTo(cx - rw * 0.45, base_y + rh * 0.9, cx, base_y + rh + s * 0.25, cx, base_y + rh + s * 0.25)
    body.curveTo(cx, base_y + rh + s * 0.25, cx + rw * 0.45, base_y + rh * 0.9, cx + rw * 0.5, base_y + rh * 0.6)
    body.lineTo(cx + rw * 0.5, base_y + s * 0.1)
    body.close()
    c.drawPath(body, stroke=1, fill=1)

    # Porthole window
    c.circle(cx, cy + s * 0.2, s * 0.18, stroke=1, fill=1)
    c.circle(cx, cy + s * 0.2, s * 0.09, stroke=1, fill=0)

    # Engine nozzle
    c.roundRect(cx - s * 0.22, base_y - s * 0.05, s * 0.44, s * 0.15, s * 0.04, stroke=1, fill=1)


def draw_planet(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a Saturn-like ringed planet centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    r = s * 0.55

    # Back half of ring
    ring_back = c.beginPath()
    ring_back.moveTo(cx - s * 1.15, cy)
    ring_back.curveTo(cx - s * 0.8, cy + s * 0.45, cx + s * 0.8, cy + s * 0.45, cx + s * 1.15, cy)
    c.drawPath(ring_back, stroke=1, fill=0)

    # Main planet globe
    c.circle(cx, cy, r, stroke=1, fill=1)

    # Surface stripes
    c.line(cx - r * 0.85, cy + s * 0.15, cx + r * 0.85, cy + s * 0.15)
    c.line(cx - r * 0.92, cy - s * 0.12, cx + r * 0.92, cy - s * 0.12)

    # Front half of ring
    ring_front = c.beginPath()
    ring_front.moveTo(cx - s * 1.15, cy)
    ring_front.curveTo(cx - s * 0.8, cy - s * 0.45, cx + s * 0.8, cy - s * 0.45, cx + s * 1.15, cy)
    c.drawPath(ring_front, stroke=1, fill=0)


# =============================================================================
# SCENARIO 9: Dinosaur Discovery (Dino Footprint & Dinosaur)
# =============================================================================

def draw_footprint(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a 3-toed dinosaur footprint centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    # Heel pad
    c.circle(cx, cy - s * 0.25, s * 0.28, stroke=1, fill=1)

    # 3 Toes with claws
    # Center toe
    t_center = c.beginPath()
    t_center.moveTo(cx - s * 0.12, cy - s * 0.1)
    t_center.lineTo(cx, cy + s * 0.75)
    t_center.lineTo(cx + s * 0.12, cy - s * 0.1)
    t_center.close()
    c.drawPath(t_center, stroke=1, fill=1)

    # Left toe
    t_left = c.beginPath()
    t_left.moveTo(cx - s * 0.22, cy - s * 0.18)
    t_left.lineTo(cx - s * 0.65, cy + s * 0.45)
    t_left.lineTo(cx - s * 0.08, cy + s * 0.05)
    t_left.close()
    c.drawPath(t_left, stroke=1, fill=1)

    # Right toe
    t_right = c.beginPath()
    t_right.moveTo(cx + s * 0.08, cy + s * 0.05)
    t_right.lineTo(cx + s * 0.65, cy + s * 0.45)
    t_right.lineTo(cx + s * 0.22, cy - s * 0.18)
    t_right.close()
    c.drawPath(t_right, stroke=1, fill=1)


def draw_dinosaur(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a friendly cartoon sauropod dinosaur centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    base_y = cy - s * 0.55
    # Legs
    for lx in (cx - s * 0.35, cx - s * 0.1, cx + s * 0.15, cx + s * 0.38):
        c.roundRect(lx, base_y, s * 0.15, s * 0.4, s * 0.05, stroke=1, fill=1)

    # Body (broad round horizontal shape)
    c.roundRect(cx - s * 0.5, base_y + s * 0.22, s * 1.0, s * 0.55, s * 0.25, stroke=1, fill=1)

    # Long neck curving up to head on the right
    neck = c.beginPath()
    neck.moveTo(cx + s * 0.35, base_y + s * 0.55)
    neck.curveTo(cx + s * 0.65, base_y + s * 0.85, cx + s * 0.6, cy + s * 0.85, cx + s * 0.6, cy + s * 0.85)
    # Head
    neck.lineTo(cx + s * 0.85, cy + s * 0.85)
    neck.curveTo(cx + s * 0.95, cy + s * 0.85, cx + s * 0.95, cy + s * 0.65, cx + s * 0.8, cy + s * 0.65)
    neck.curveTo(cx + s * 0.55, cy + s * 0.65, cx + s * 0.5, base_y + s * 0.4, cx + s * 0.48, base_y + s * 0.4)
    neck.close()
    c.drawPath(neck, stroke=1, fill=1)

    # Eye
    c.circle(cx + s * 0.75, cy + s * 0.78, s * 0.05, stroke=1, fill=0)

    # Tail curving down and left
    tail = c.beginPath()
    tail.moveTo(cx - s * 0.45, base_y + s * 0.55)
    tail.curveTo(cx - s * 0.85, base_y + s * 0.55, cx - s * 0.95, base_y + s * 0.15, cx - s * 0.9, base_y + s * 0.05)
    tail.curveTo(cx - s * 0.8, base_y + s * 0.15, cx - s * 0.45, base_y + s * 0.35, cx - s * 0.45, base_y + s * 0.35)
    tail.close()
    c.drawPath(tail, stroke=1, fill=1)


# =============================================================================
# SCENARIO 10: Nature Explorers (Binoculars & Mountain Lookout)
# =============================================================================

def draw_binoculars(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw field explorer binoculars centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    base_y = cy - s * 0.55
    bw = s * 0.42
    bh = s * 1.1

    # Left barrel
    c.roundRect(cx - s * 0.55, base_y, bw, bh, s * 0.12, stroke=1, fill=1)
    # Right barrel
    c.roundRect(cx + s * 0.13, base_y, bw, bh, s * 0.12, stroke=1, fill=1)

    # Eyepieces at top
    c.roundRect(cx - s * 0.5, base_y + bh, s * 0.32, s * 0.15, s * 0.04, stroke=1, fill=1)
    c.roundRect(cx + s * 0.18, base_y + bh, s * 0.32, s * 0.15, s * 0.04, stroke=1, fill=1)

    # Objective lens rims at bottom
    c.roundRect(cx - s * 0.58, base_y - s * 0.08, s * 0.48, s * 0.14, s * 0.04, stroke=1, fill=1)
    c.roundRect(cx + s * 0.1, base_y - s * 0.08, s * 0.48, s * 0.14, s * 0.04, stroke=1, fill=1)

    # Center focus bridge
    c.rect(cx - s * 0.13, cy - s * 0.1, s * 0.26, s * 0.4, stroke=1, fill=1)
    # Focus wheel
    c.roundRect(cx - s * 0.16, cy + s * 0.05, s * 0.32, s * 0.18, s * 0.05, stroke=1, fill=1)


def draw_lookout(c, cx: float, cy: float, s: float, lw: float = 1.4) -> None:
    """Draw a mountain peak observation deck / lookout tower centered at (cx, cy)."""
    _setup_stroke(c, lw, fill_white=True)

    base_y = cy - s * 0.65
    # Mountain ridge base
    ridge = c.beginPath()
    ridge.moveTo(cx - s * 1.1, base_y)
    ridge.lineTo(cx, base_y + s * 0.28)
    ridge.lineTo(cx + s * 1.1, base_y)
    ridge.close()
    c.drawPath(ridge, stroke=1, fill=1)

    # Support stilts
    for sx in (cx - s * 0.38, cx - s * 0.12, cx + s * 0.12, cx + s * 0.38):
        c.line(sx, base_y + s * 0.2, sx, cy + s * 0.15)

    # Deck railing
    dw = s * 1.1
    c.roundRect(cx - dw * 0.5, cy + s * 0.15, dw, s * 0.18, s * 0.04, stroke=1, fill=1)
    c.line(cx - dw * 0.5, cy + s * 0.32, cx + dw * 0.5, cy + s * 0.32)

    # Roof supports & pitched canopy
    c.line(cx - s * 0.42, cy + s * 0.32, cx - s * 0.42, cy + s * 0.55)
    c.line(cx + s * 0.42, cy + s * 0.32, cx + s * 0.42, cy + s * 0.55)

    roof = c.beginPath()
    roof.moveTo(cx - s * 0.62, cy + s * 0.55)
    roof.lineTo(cx, cy + s * 0.88)
    roof.lineTo(cx + s * 0.62, cy + s * 0.55)
    roof.close()
    c.drawPath(roof, stroke=1, fill=1)


# =============================================================================
# DECORATIVE CORNER ACCENTS (Balanced, Theme-Harmonious Motifs)
# =============================================================================

def draw_star_badge(c, cx: float, cy: float, s: float, lw: float = 1.2) -> None:
    """Draw a neat decorative 5-pointed star accent."""
    _setup_stroke(c, lw, fill_white=True)
    p = c.beginPath()
    for i in range(10):
        angle = i * math.pi / 5.0 - math.pi / 2.0
        r = s * 0.9 if i % 2 == 0 else s * 0.42
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        if i == 0:
            p.moveTo(px, py)
        else:
            p.lineTo(px, py)
    p.close()
    c.drawPath(p, stroke=1, fill=1)


def draw_leaf_accent(c, cx: float, cy: float, s: float, lw: float = 1.2) -> None:
    """Draw a decorative twin-leaf nature accent."""
    _setup_stroke(c, lw, fill_white=True)
    p = c.beginPath()
    p.moveTo(cx - s * 0.6, cy - s * 0.5)
    p.curveTo(cx - s * 0.6, cy + s * 0.3, cx + s * 0.3, cy + s * 0.6, cx + s * 0.6, cy + s * 0.6)
    p.curveTo(cx + s * 0.6, cy - s * 0.2, cx - s * 0.3, cy - s * 0.5, cx - s * 0.6, cy - s * 0.5)
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    c.line(cx - s * 0.5, cy - s * 0.4, cx + s * 0.5, cy + s * 0.5)


def draw_paw_print(c, cx: float, cy: float, s: float, lw: float = 1.0) -> None:
    """Draw a subtle decorative paw print accent."""
    _setup_stroke(c, lw, fill_white=True)
    # Main pad
    c.circle(cx, cy - s * 0.15, s * 0.38, stroke=1, fill=1)
    # 3 toe dots
    c.circle(cx - s * 0.45, cy + s * 0.28, s * 0.18, stroke=1, fill=1)
    c.circle(cx, cy + s * 0.52, s * 0.18, stroke=1, fill=1)
    c.circle(cx + s * 0.45, cy + s * 0.28, s * 0.18, stroke=1, fill=1)


def draw_sun_accent(c, cx: float, cy: float, s: float, lw: float = 1.0) -> None:
    """Draw a subtle playground sun accent with mini rays."""
    _setup_stroke(c, lw, fill_white=True)
    r = s * 0.42
    c.circle(cx, cy, r, stroke=1, fill=1)
    for i in range(8):
        angle = i * math.pi / 4.0
        c.line(
            cx + r * 1.25 * math.cos(angle),
            cy + r * 1.25 * math.sin(angle),
            cx + r * 1.8 * math.cos(angle),
            cy + r * 1.8 * math.sin(angle),
        )


def draw_flower_blossom(c, cx: float, cy: float, s: float, lw: float = 1.0) -> None:
    """Draw a subtle garden flower blossom accent."""
    _setup_stroke(c, lw, fill_white=True)
    # 5 petals
    pr = s * 0.35
    for i in range(5):
        angle = i * 2.0 * math.pi / 5.0 - math.pi / 2.0
        px = cx + s * 0.45 * math.cos(angle)
        py = cy + s * 0.45 * math.sin(angle)
        c.circle(px, py, pr, stroke=1, fill=1)
    # Center core
    c.circle(cx, cy, s * 0.25, stroke=1, fill=1)


def draw_pencil_accent(c, cx: float, cy: float, s: float, lw: float = 1.0) -> None:
    """Draw a subtle school pencil accent."""
    _setup_stroke(c, lw, fill_white=True)
    # Slanted body
    w = s * 0.3
    h = s * 1.0
    c.roundRect(cx - w * 0.5, cy - h * 0.4, w, h * 0.7, s * 0.05, stroke=1, fill=1)
    # Eraser top
    c.roundRect(cx - w * 0.5, cy + h * 0.3, w, h * 0.2, s * 0.04, stroke=1, fill=1)
    # Pointed tip
    tip = c.beginPath()
    tip.moveTo(cx - w * 0.5, cy - h * 0.4)
    tip.lineTo(cx, cy - h * 0.75)
    tip.lineTo(cx + w * 0.5, cy - h * 0.4)
    tip.close()
    c.drawPath(tip, stroke=1, fill=1)


def draw_bubble_cluster(c, cx: float, cy: float, s: float, lw: float = 1.0) -> None:
    """Draw subtle ocean bubble accents."""
    _setup_stroke(c, lw, fill_white=True)
    c.circle(cx - s * 0.22, cy - s * 0.15, s * 0.38, stroke=1, fill=1)
    c.circle(cx + s * 0.32, cy + s * 0.28, s * 0.24, stroke=1, fill=1)


def draw_sparkle_cluster(c, cx: float, cy: float, s: float, lw: float = 1.0) -> None:
    """Draw subtle cosmic sparkle star accents."""
    _setup_stroke(c, lw, fill_white=True)
    for ox, oy, scale in ((-s * 0.15, -s * 0.1, s * 0.6), (s * 0.35, s * 0.35, s * 0.38)):
        p = c.beginPath()
        p.moveTo(cx + ox, cy + oy - scale)
        p.curveTo(cx + ox, cy + oy, cx + ox, cy + oy, cx + ox + scale, cy + oy)
        p.curveTo(cx + ox, cy + oy, cx + ox, cy + oy, cx + ox, cy + oy + scale)
        p.curveTo(cx + ox, cy + oy, cx + ox, cy + oy, cx + ox - scale, cy + oy)
        p.curveTo(cx + ox, cy + oy, cx + ox, cy + oy, cx + ox, cy + oy - scale)
        c.drawPath(p, stroke=1, fill=1)


def draw_fern_accent(c, cx: float, cy: float, s: float, lw: float = 1.0) -> None:
    """Draw a subtle prehistoric fern leaf accent."""
    _setup_stroke(c, lw, fill_white=True)
    c.line(cx - s * 0.5, cy - s * 0.5, cx + s * 0.5, cy + s * 0.5)
    for off in (-s * 0.25, 0.0, s * 0.25):
        c.line(cx + off, cy + off, cx + off - s * 0.25, cy + off + s * 0.15)
        c.line(cx + off, cy + off, cx + off + s * 0.15, cy + off - s * 0.25)


def draw_mountain_accent(c, cx: float, cy: float, s: float, lw: float = 1.0) -> None:
    """Draw a subtle nature mountain peak accent."""
    _setup_stroke(c, lw, fill_white=True)
    p = c.beginPath()
    p.moveTo(cx - s * 0.7, cy - s * 0.4)
    p.lineTo(cx - s * 0.1, cy + s * 0.5)
    p.lineTo(cx + s * 0.6, cy - s * 0.4)
    p.close()
    c.drawPath(p, stroke=1, fill=1)


def draw_scenario_corner_decorations(c, content, title: str) -> None:
    """Draw subtle, original black-and-white themed decorative details in corner zones."""
    # Safe corner positions
    tl = (content.x0 + 16.0, content.y1 - 65.0)
    tr = (content.x1 - 18.0, content.y1 - 65.0)
    bl = (content.x0 + 16.0, content.y0 + 34.0)
    br = (content.x1 - 18.0, content.y0 + 34.0)

    # Theme-tailored accents
    if "Puppy" in title:
        draw_paw_print(c, tl[0], tl[1], 7.5)
        draw_paw_print(c, tr[0], tr[1], 7.5)
        draw_star_badge(c, bl[0], bl[1], 7.5)
        draw_paw_print(c, br[0], br[1], 7.5)
    elif "Playground" in title:
        draw_sun_accent(c, tl[0], tl[1], 7.0)
        draw_star_badge(c, tr[0], tr[1], 7.5)
        draw_star_badge(c, bl[0], bl[1], 7.5)
        draw_sun_accent(c, br[0], br[1], 7.0)
    elif "Bee" in title:
        draw_flower_blossom(c, tl[0], tl[1], 7.5)
        draw_flower_blossom(c, tr[0], tr[1], 7.5)
        draw_leaf_accent(c, bl[0], bl[1], 7.5)
        draw_flower_blossom(c, br[0], br[1], 7.5)
    elif "Science" in title:
        draw_star_badge(c, tl[0], tl[1], 7.5)
        draw_pencil_accent(c, tr[0], tr[1], 7.5)
        draw_pencil_accent(c, bl[0], bl[1], 7.5)
        draw_star_badge(c, br[0], br[1], 7.5)
    elif "Acorn" in title:
        draw_leaf_accent(c, tl[0], tl[1], 8.0)
        draw_leaf_accent(c, tr[0], tr[1], 8.0)
        draw_leaf_accent(c, bl[0], bl[1], 8.0)
        draw_star_badge(c, br[0], br[1], 7.5)
    elif "Submarine" in title:
        draw_bubble_cluster(c, tl[0], tl[1], 7.5)
        draw_bubble_cluster(c, tr[0], tr[1], 7.5)
        draw_bubble_cluster(c, bl[0], bl[1], 7.5)
        draw_star_badge(c, br[0], br[1], 7.5)
    elif "Treehouse" in title:
        draw_leaf_accent(c, tl[0], tl[1], 8.0)
        draw_star_badge(c, tr[0], tr[1], 7.5)
        draw_star_badge(c, bl[0], bl[1], 7.5)
        draw_leaf_accent(c, br[0], br[1], 8.0)
    elif "Rocket" in title or "Space" in title:
        draw_sparkle_cluster(c, tl[0], tl[1], 8.0)
        draw_sparkle_cluster(c, tr[0], tr[1], 8.0)
        draw_star_badge(c, bl[0], bl[1], 7.5)
        draw_sparkle_cluster(c, br[0], br[1], 8.0)
    elif "Dinosaur" in title or "Fossil" in title:
        draw_fern_accent(c, tl[0], tl[1], 7.5)
        draw_star_badge(c, tr[0], tr[1], 7.5)
        draw_fern_accent(c, bl[0], bl[1], 7.5)
        draw_star_badge(c, br[0], br[1], 7.5)
    elif "Mountain" in title or "Lookout" in title:
        draw_mountain_accent(c, tl[0], tl[1], 7.5)
        draw_mountain_accent(c, tr[0], tr[1], 7.5)
        draw_leaf_accent(c, bl[0], bl[1], 7.5)
        draw_star_badge(c, br[0], br[1], 7.5)
    else:
        # Default balanced accents
        draw_star_badge(c, tl[0], tl[1], 7.5)
        draw_star_badge(c, tr[0], tr[1], 7.5)
        draw_leaf_accent(c, bl[0], bl[1], 7.5)
        draw_star_badge(c, br[0], br[1], 7.5)


# =============================================================================
# ICON REGISTRY
# =============================================================================

ADVENTURE_ICONS: dict[str, Callable] = {
    # Scenario 1
    "puppy": draw_puppy,
    "bone": draw_bone,
    # Scenario 2
    "scooter": draw_scooter,
    "slide": draw_slide,
    # Scenario 3
    "bee": draw_bee,
    "beehive": draw_beehive,
    # Scenario 4
    "backpack": draw_backpack,
    "trophy": draw_trophy,
    # Scenario 5
    "acorn": draw_acorn,
    "oak_tree": draw_oak_tree,
    # Scenario 6
    "submarine": draw_submarine,
    "treasure": draw_treasure,
    # Scenario 7
    "bicycle": draw_bicycle,
    "treehouse": draw_treehouse,
    # Scenario 8
    "rocket": draw_rocket,
    "planet": draw_planet,
    # Scenario 9
    "footprint": draw_footprint,
    "dinosaur": draw_dinosaur,
    # Scenario 10
    "binoculars": draw_binoculars,
    "lookout": draw_lookout,
    # Accents
    "star_badge": draw_star_badge,
    "leaf_accent": draw_leaf_accent,
    "paw_print": draw_paw_print,
    "sun_accent": draw_sun_accent,
    "flower_blossom": draw_flower_blossom,
    "pencil_accent": draw_pencil_accent,
    "bubble_cluster": draw_bubble_cluster,
    "sparkle_cluster": draw_sparkle_cluster,
    "fern_accent": draw_fern_accent,
    "mountain_accent": draw_mountain_accent,
    # Backward-compatible road-trip icons
    **ROAD_TRIP_ICONS,
}
