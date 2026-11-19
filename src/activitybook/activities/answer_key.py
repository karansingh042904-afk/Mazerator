"""Answer key generator for ActivityBook Studio.

Generates compact, print-ready multi-up solution pages (4-up or 6-up)
displaying the exact solution paths for generated mazes with clear
identifiers, start/finish markers, and 7 × 10-inch KDP-compliant margins.
"""

from __future__ import annotations

import math
from typing import Sequence

from reportlab.pdfgen import canvas

from activitybook.core.fonts import (
    FONT_BOLD,
    FONT_ITALIC,
    FONT_REGULAR,
    register_activitybook_fonts,
)
from activitybook.core.page_spec import PageSpec
from activitybook.activities.maze_activity import MazeData
from maze_generator import generate_mazes as gm


def render_maze_solution_thumbnail(
    c: canvas.Canvas,
    x0: float,
    y0: float,
    side: float,
    maze: MazeData,
    solution_lw: float = 2.2,
) -> None:
    """Render a miniature maze grid with the actual solution path drawn bold."""
    register_activitybook_fonts()
    n = maze.grid_size
    cw = side / float(n)
    ch = side / float(n)

    def gx(col: int) -> float:
        return x0 + col * cw

    def gy(row: int) -> float:
        return y0 + side - row * ch

    def cell_center(r: int, col: int) -> tuple[float, float]:
        return gx(col) + cw / 2.0, gy(row=r) - ch / 2.0

    # 1. Internal Maze Walls (fine line)
    c.setLineWidth(0.65)
    c.setLineCap(1)
    c.setLineJoin(1)
    c.setStrokeColorRGB(0.2, 0.2, 0.2)

    for r in range(n):
        for col in range(n - 1):
            if not maze.right[r][col]:
                xx = gx(col + 1)
                c.line(xx, gy(r), xx, gy(r + 1))
    for r in range(n - 1):
        for col in range(n):
            if not maze.down[r][col]:
                yy = gy(r + 1)
                c.line(gx(col), yy, gx(col + 1), yy)

    # 2. Outer Border (leaving openings for entrance & exit)
    top_y = gy(0)
    bottom_y = gy(n)
    left_x = gx(0)
    right_x = gx(n)
    skip = {maze.entrance, maze.exit_}

    c.setLineWidth(1.0)
    c.setStrokeColorRGB(0.0, 0.0, 0.0)

    for col in range(n):
        if ("top", col) not in skip:
            c.line(gx(col), top_y, gx(col + 1), top_y)
        if ("bottom", col) not in skip:
            c.line(gx(col), bottom_y, gx(col + 1), bottom_y)
    for r in range(n):
        if ("left", r) not in skip:
            c.line(left_x, gy(r), left_x, gy(r + 1))
        if ("right", r) not in skip:
            c.line(right_x, gy(r), right_x, gy(r + 1))

    # 3. Bold Solution Path
    if maze.solution_path:
        c.setLineWidth(solution_lw)
        c.setLineCap(1)
        c.setLineJoin(1)
        c.setStrokeColorRGB(0.0, 0.0, 0.0)

        path = c.beginPath()
        start_x, start_y = cell_center(*maze.solution_path[0])
        path.moveTo(start_x, start_y)
        for cell in maze.solution_path[1:]:
            cx, cy = cell_center(*cell)
            path.lineTo(cx, cy)
        c.drawPath(path, stroke=1, fill=0)

        # Start Marker (small filled circle with 'S')
        marker_r = min(cw * 0.42, 6.0)
        c.setFillColorRGB(0.0, 0.0, 0.0)
        c.circle(start_x, start_y, marker_r, stroke=1, fill=1)
        c.setFont(FONT_BOLD, marker_r * 1.3)
        c.setFillColorRGB(1.0, 1.0, 1.0)
        c.drawCentredString(start_x, start_y - marker_r * 0.45, "S")

        # Goal Marker (small white circle with border and 'F')
        goal_x, goal_y = cell_center(*maze.solution_path[-1])
        c.setFillColorRGB(1.0, 1.0, 1.0)
        c.circle(goal_x, goal_y, marker_r, stroke=1, fill=1)
        c.setFont(FONT_BOLD, marker_r * 1.3)
        c.setFillColorRGB(0.0, 0.0, 0.0)
        c.drawCentredString(goal_x, goal_y - marker_r * 0.45, "F")


def render_answer_key_page(
    c: canvas.Canvas,
    page_number: int,
    mazes: Sequence[MazeData],
    page_spec: PageSpec,
    title: str = "ANSWER KEY: ROAD TRIP MAZES",
    total_pages: int | None = None,
    layout: str = "auto",
) -> None:
    """Render a multi-up answer key page on a 7 × 10-inch sheet.

    Supported layouts:
    - '6-up': 2 columns × 3 rows (up to 6 solutions per page)
    - '4-up': 2 columns × 2 rows (up to 4 solutions per page, larger thumbnails, balanced vertical distribution)
    - 'auto': automatically chooses '4-up' if len(mazes) <= 4, otherwise '6-up'.
    """
    content = page_spec.get_content_rect(page_number)
    register_activitybook_fonts()

    # 1. Header
    header_y = content.y1 - 12.0
    c.setFont(FONT_BOLD, 14.0)
    c.setFillColorRGB(0.0, 0.0, 0.0)
    c.drawCentredString(content.x0 + content.width / 2.0, header_y, title)

    # Subtitle line
    c.setFont(FONT_REGULAR, 9.0)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawCentredString(
        content.x0 + content.width / 2.0,
        header_y - 14.0,
        "Check your paths! Every maze has exactly one true route.",
    )

    # Horizontal divider rule
    c.setLineWidth(0.8)
    c.setStrokeColorRGB(0.5, 0.5, 0.5)
    c.line(content.x0 + 20.0, header_y - 22.0, content.x1 - 20.0, header_y - 22.0)

    # 2. Grid Parameters
    avail_top = header_y - 28.0
    avail_bottom = content.y0 + 26.0
    avail_height = avail_top - avail_bottom
    avail_width = content.width

    # Automatic layout selection
    resolved_layout = layout
    if resolved_layout == "auto":
        resolved_layout = "4-up" if len(mazes) <= 4 else "6-up"

    if resolved_layout == "4-up":
        cols_count = 2
        rows_count = 2
        thumb_side = 180.0
        solution_lw = 2.6
    else:  # default '6-up'
        cols_count = 2
        rows_count = 3
        thumb_side = 135.0
        solution_lw = 2.0

    col_width = avail_width / float(cols_count)
    row_height = avail_height / float(rows_count)

    # 3. Draw each maze solution thumbnail
    for idx, maze in enumerate(mazes[: cols_count * rows_count]):
        col_idx = idx % cols_count
        row_idx = idx // cols_count

        cell_x0 = content.x0 + col_idx * col_width
        cell_y_top = avail_top - row_idx * row_height

        if resolved_layout == "4-up":
            # Enhanced 4-up: larger thumbnails vertically centered in each row
            block_h = 13.0 + 11.0 + 8.0 + thumb_side
            v_pad = (row_height - block_h) / 2.0

            label_y = cell_y_top - v_pad - 11.0
            c.setFont(FONT_BOLD, 10.5)
            c.setFillColorRGB(0.0, 0.0, 0.0)
            c.drawCentredString(
                cell_x0 + col_width / 2.0,
                label_y,
                f"{maze.maze_id} ({maze.difficulty.display_name})",
            )

            # Scenario title line
            sub_y = label_y - 12.0
            c.setFont(FONT_ITALIC, 8.5)
            c.setFillColorRGB(0.3, 0.3, 0.3)
            c.drawCentredString(
                cell_x0 + col_width / 2.0,
                sub_y,
                maze.title,
            )

            thumb_x0 = cell_x0 + (col_width - thumb_side) / 2.0
            thumb_y0 = sub_y - 7.0 - thumb_side
        else:
            # 6-up layout
            block_h = 12.0 + 8.0 + thumb_side
            v_pad = (row_height - block_h) / 2.0

            label_y = cell_y_top - v_pad - 10.0
            c.setFont(FONT_BOLD, 9.5)
            c.setFillColorRGB(0.0, 0.0, 0.0)
            c.drawCentredString(
                cell_x0 + col_width / 2.0,
                label_y,
                f"{maze.maze_id} ({maze.difficulty.display_name})",
            )

            thumb_x0 = cell_x0 + (col_width - thumb_side) / 2.0
            thumb_y0 = label_y - 8.0 - thumb_side

        render_maze_solution_thumbnail(
            c,
            thumb_x0,
            thumb_y0,
            thumb_side,
            maze,
            solution_lw=solution_lw,
        )

        # Validate that thumbnail bounding box is safely within page content rect
        page_spec.validate_rect_safe(thumb_x0, thumb_y0, thumb_x0 + thumb_side, thumb_y0 + thumb_side, page_number)

    # 4. Footer
    footer_y = content.y0 + 8.0
    c.setFont(FONT_REGULAR, 9.0)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    page_str = f"Page {page_number}" if total_pages is None else f"Page {page_number} of {total_pages}"
    c.drawCentredString(content.x0 + content.width / 2.0, footer_y, page_str)


def build_answer_key_pages(
    c: canvas.Canvas,
    start_page_num: int,
    mazes: Sequence[MazeData],
    page_spec: PageSpec,
    per_page: int = 6,
    total_book_pages: int | None = None,
) -> int:
    """Render one or more answer key pages for a sequence of mazes.

    Automatically uses '4-up' if a page batch contains <= 4 solutions.
    Returns the number of answer key pages created.
    """
    pages_created = 0
    cur_page = start_page_num

    for i in range(0, len(mazes), per_page):
        batch = mazes[i : i + per_page]
        layout = "4-up" if len(batch) <= 4 else "6-up"
        render_answer_key_page(
            c,
            page_number=cur_page,
            mazes=batch,
            page_spec=page_spec,
            total_pages=total_book_pages,
            layout=layout,
        )
        c.showPage()
        cur_page += 1
        pages_created += 1

    return pages_created
