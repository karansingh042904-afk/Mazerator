"""Everyday Adventures & Road Trip Maze Activity Generator for children aged 6–9.

Generates 7 × 10-inch KDP-compliant children's maze activity pages with
engaging adventure scenarios (animal quests, playground races, space exploration,
dinosaur digs, underwater diving), accurate solution recording, safe-area
validation, mirrored margins, and 100% embedded Noto Sans typography.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math
from pathlib import Path
import random
from typing import Optional, Sequence

from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from activitybook.core.fonts import (
    FONT_BOLD,
    FONT_ITALIC,
    FONT_REGULAR,
    register_activitybook_fonts,
)
from activitybook.core.page_spec import PageSpec, inches_to_points
from activitybook.activities.adventure_icons import (
    ADVENTURE_ICONS,
    draw_leaf_accent,
    draw_scenario_corner_decorations,
    draw_star_badge,
)
from activitybook.activities.road_trip_icons import (
    ROAD_TRIP_ICONS,
    draw_compass,
    draw_mountain,
    draw_pine_tree,
    draw_traffic_cone,
    draw_traffic_sign,
)
from maze_generator import generate_mazes as gm


class MazeDifficulty(str, Enum):
    """Maze difficulty tier for ages 6–9."""

    EASY = "easy"
    MEDIUM = "medium"
    CHALLENGING = "challenging"

    @property
    def grid_size(self) -> int:
        """Grid dimension (n x n)."""
        if self == MazeDifficulty.EASY:
            return 10
        elif self == MazeDifficulty.MEDIUM:
            return 15
        else:
            return 20

    @property
    def min_path_factor(self) -> float:
        """Minimum solution length as fraction of total cells."""
        if self == MazeDifficulty.EASY:
            return 0.40
        elif self == MazeDifficulty.MEDIUM:
            return 0.50
        else:
            return 0.60

    @property
    def display_name(self) -> str:
        if self == MazeDifficulty.EASY:
            return "Easy"
        elif self == MazeDifficulty.MEDIUM:
            return "Medium"
        else:
            return "Challenging"

    @property
    def stars(self) -> int:
        """Star rating (1 to 3 stars)."""
        if self == MazeDifficulty.EASY:
            return 1
        elif self == MazeDifficulty.MEDIUM:
            return 2
        else:
            return 3


@dataclass(frozen=True)
class AdventureScenario:
    """A distinct thematic scenario and instruction for a children's maze activity."""

    title: str
    instruction: str
    difficulty: MazeDifficulty
    start_icon: str
    goal_icon: str


# Backward-compatible alias
RoadTripScenario = AdventureScenario


# 10 completely unique Everyday Adventures scenarios for children aged 6–9
EVERYDAY_ADVENTURE_SCENARIOS: list[AdventureScenario] = [
    # Pages 1–3: Easy (10x10 grid, 1 Star)
    AdventureScenario(
        title="Puppy's Backyard Quest",
        instruction="Help the playful puppy search the garden paths to find the buried bone!",
        difficulty=MazeDifficulty.EASY,
        start_icon="puppy",
        goal_icon="bone",
    ),
    AdventureScenario(
        title="Playground Slide Dash",
        instruction="Ride your scooter through the playground to reach the giant spiral slide!",
        difficulty=MazeDifficulty.EASY,
        start_icon="scooter",
        goal_icon="slide",
    ),
    AdventureScenario(
        title="Busy Bee's Flower Trail",
        instruction="Guide the buzzing bumblebee through the blooming garden back to the hive!",
        difficulty=MazeDifficulty.EASY,
        start_icon="bee",
        goal_icon="beehive",
    ),
    # Pages 4–7: Medium (15x15 grid, 2 Stars)
    AdventureScenario(
        title="Science Fair Sprint",
        instruction="Pack your backpack and navigate the school hallways to claim the first-place trophy!",
        difficulty=MazeDifficulty.MEDIUM,
        start_icon="backpack",
        goal_icon="trophy",
    ),
    AdventureScenario(
        title="Acorn Treasure Trail",
        instruction="Guide the squirrel through the twisted woodland paths to the great oak tree!",
        difficulty=MazeDifficulty.MEDIUM,
        start_icon="acorn",
        goal_icon="oak_tree",
    ),
    AdventureScenario(
        title="Deep Sea Submarine Dive",
        instruction="Steer the submarine past coral reefs to discover the sunken treasure chest!",
        difficulty=MazeDifficulty.MEDIUM,
        start_icon="submarine",
        goal_icon="treasure",
    ),
    AdventureScenario(
        title="Secret Treehouse Meeting",
        instruction="Pedal your bicycle across the neighborhood to join friends at the secret treehouse!",
        difficulty=MazeDifficulty.MEDIUM,
        start_icon="bicycle",
        goal_icon="treehouse",
    ),
    # Pages 8–10: Challenging (20x20 grid, 3 Stars)
    AdventureScenario(
        title="Cosmic Rocket Odyssey",
        instruction="Fly the rocket ship through starry space lanes to land safely on the ringed planet!",
        difficulty=MazeDifficulty.CHALLENGING,
        start_icon="rocket",
        goal_icon="planet",
    ),
    AdventureScenario(
        title="Jurassic Fossil Expedition",
        instruction="Follow the prehistoric canyon tracks to uncover the giant fossilized dinosaur!",
        difficulty=MazeDifficulty.CHALLENGING,
        start_icon="footprint",
        goal_icon="dinosaur",
    ),
    AdventureScenario(
        title="Mountain Peak Lookout",
        instruction="Hike the high mountain trail with your binoculars to reach the observation deck!",
        difficulty=MazeDifficulty.CHALLENGING,
        start_icon="binoculars",
        goal_icon="lookout",
    ),
]


# Backward-compatible 10 Road Trip scenarios
ROAD_TRIP_SCENARIOS: list[AdventureScenario] = [
    AdventureScenario(
        title="Campsite Arrival",
        instruction="Guide the camper van down the winding road to the campsite!",
        difficulty=MazeDifficulty.EASY,
        start_icon="camper_van",
        goal_icon="campsite",
    ),
    AdventureScenario(
        title="Mountain Pass Expedition",
        instruction="Steer the family car around the rocky curves to reach the mountain peak!",
        difficulty=MazeDifficulty.EASY,
        start_icon="car",
        goal_icon="mountain",
    ),
    AdventureScenario(
        title="Pine Woods Discovery",
        instruction="Help the adventure van follow the trail through the tall pine trees!",
        difficulty=MazeDifficulty.EASY,
        start_icon="camper_van",
        goal_icon="pine_tree",
    ),
    AdventureScenario(
        title="Highway Detour Challenge",
        instruction="Navigate around the road cones to get back on the scenic highway!",
        difficulty=MazeDifficulty.MEDIUM,
        start_icon="traffic_cone",
        goal_icon="traffic_sign",
    ),
    AdventureScenario(
        title="Secret Compass Trail",
        instruction="Use your navigation compass to find the hidden path to the campsite!",
        difficulty=MazeDifficulty.MEDIUM,
        start_icon="compass",
        goal_icon="campsite",
    ),
    AdventureScenario(
        title="Scenic Valley Crossing",
        instruction="Drive through the twisty valley roads to reach the mountain lookout!",
        difficulty=MazeDifficulty.MEDIUM,
        start_icon="car",
        goal_icon="mountain",
    ),
    AdventureScenario(
        title="Wilderness RV Quest",
        instruction="Steer the camper van through the wilderness to the forest ranger station!",
        difficulty=MazeDifficulty.MEDIUM,
        start_icon="camper_van",
        goal_icon="pine_tree",
    ),
    AdventureScenario(
        title="Cross-Country Road Rally",
        instruction="Follow the winding highway signs to complete the cross-country rally!",
        difficulty=MazeDifficulty.CHALLENGING,
        start_icon="car",
        goal_icon="traffic_sign",
    ),
    AdventureScenario(
        title="Lost in the High Woods",
        instruction="Trek through the dense pine maze using your compass to find safety!",
        difficulty=MazeDifficulty.CHALLENGING,
        start_icon="compass",
        goal_icon="pine_tree",
    ),
    AdventureScenario(
        title="The Great Summit Climb",
        instruction="Tackle the ultimate mountain ascent: guide the expedition van to the summit!",
        difficulty=MazeDifficulty.CHALLENGING,
        start_icon="camper_van",
        goal_icon="mountain",
    ),
]

ROAD_TRIP_THEMES = [
    (s.start_icon, s.goal_icon, s.title) for s in ROAD_TRIP_SCENARIOS
]


@dataclass(frozen=True)
class MazeData:
    """Complete data for a generated maze activity with recorded solution path."""

    maze_id: str
    title: str
    instruction: str
    difficulty: MazeDifficulty
    grid_size: int
    seed: int
    right: tuple[tuple[bool, ...], ...]
    down: tuple[tuple[bool, ...], ...]
    entrance: tuple[str, int]
    exit_: tuple[str, int]
    start_cell: tuple[int, int]
    goal_cell: tuple[int, int]
    solution_path: tuple[tuple[int, int], ...]
    path_length: int
    start_icon: str
    goal_icon: str


def _generate_themed_maze(
    maze_id: str,
    scenarios: Sequence[AdventureScenario],
    difficulty: MazeDifficulty = MazeDifficulty.MEDIUM,
    seed: int | None = None,
    title: str | None = None,
    instruction: str | None = None,
    theme_index: int | None = None,
    scenario_index: int | None = None,
) -> MazeData:
    """Core algorithmic helper to generate a perfect maze with guaranteed-long solution."""
    if seed is None:
        seed = random.randint(1, 999_999_999)

    rng = random.Random(seed)

    idx = scenario_index if scenario_index is not None else theme_index
    if idx is not None:
        scenario = scenarios[idx % len(scenarios)]
        resolved_title = title if title is not None else scenario.title
        resolved_inst = instruction if instruction is not None else scenario.instruction
        resolved_diff = difficulty if difficulty != MazeDifficulty.MEDIUM or scenario_index is None else scenario.difficulty
        start_icon = scenario.start_icon
        goal_icon = scenario.goal_icon
    else:
        scenario = rng.choice(scenarios)
        resolved_title = title if title is not None else scenario.title
        resolved_inst = instruction if instruction is not None else scenario.instruction
        resolved_diff = difficulty
        start_icon = scenario.start_icon
        goal_icon = scenario.goal_icon

    n = resolved_diff.grid_size

    # Generate perfect maze with guaranteed-long solution
    right_raw, down_raw, entrance, exit_, _ = gm.generate_long_maze(
        n,
        rng,
        min_path_factor=resolved_diff.min_path_factor,
    )

    start_cell = gm.opening_to_cell(entrance, n, n)
    goal_cell = gm.opening_to_cell(exit_, n, n)

    # Record the actual exact solution path using BFS
    raw_path = gm.find_path(right_raw, down_raw, n, n, start_cell, goal_cell)
    if raw_path is None:
        raise RuntimeError(f"Failed to find solution path for maze {maze_id} (seed {seed})")

    right = tuple(tuple(bool(x) for x in row) for row in right_raw)
    down = tuple(tuple(bool(x) for x in row) for row in down_raw)
    solution_path = tuple(tuple(cell) for cell in raw_path)

    return MazeData(
        maze_id=maze_id,
        title=resolved_title,
        instruction=resolved_inst,
        difficulty=resolved_diff,
        grid_size=n,
        seed=seed,
        right=right,
        down=down,
        entrance=entrance,
        exit_=exit_,
        start_cell=start_cell,
        goal_cell=goal_cell,
        solution_path=solution_path,
        path_length=len(solution_path),
        start_icon=start_icon,
        goal_icon=goal_icon,
    )


def generate_adventure_maze(
    maze_id: str,
    difficulty: MazeDifficulty = MazeDifficulty.MEDIUM,
    seed: int | None = None,
    title: str | None = None,
    instruction: str | None = None,
    scenario_index: int | None = None,
) -> MazeData:
    """Generate an Everyday Adventures maze for ages 6–9 with recorded solution path."""
    return _generate_themed_maze(
        maze_id=maze_id,
        scenarios=EVERYDAY_ADVENTURE_SCENARIOS,
        difficulty=difficulty,
        seed=seed,
        title=title,
        instruction=instruction,
        scenario_index=scenario_index,
    )


def generate_road_trip_maze(
    maze_id: str,
    difficulty: MazeDifficulty = MazeDifficulty.MEDIUM,
    seed: int | None = None,
    title: str | None = None,
    instruction: str | None = None,
    theme_index: int | None = None,
    scenario_index: int | None = None,
) -> MazeData:
    """Backward-compatible generator for Road Trip themed mazes."""
    return _generate_themed_maze(
        maze_id=maze_id,
        scenarios=ROAD_TRIP_SCENARIOS,
        difficulty=difficulty,
        seed=seed,
        title=title,
        instruction=instruction,
        theme_index=theme_index,
        scenario_index=scenario_index,
    )


def _draw_star_rating(c: canvas.Canvas, cx: float, cy: float, stars: int, max_stars: int = 3, r: float = 5.0) -> None:
    """Draw a 1-to-3 star rating badge."""
    spacing = r * 2.8
    total_w = (max_stars - 1) * spacing
    x0 = cx - total_w / 2.0
    for i in range(max_stars):
        fill = (i < stars)
        gm.draw_star(c, x0 + i * spacing, cy, r, lw=1.1, fill=fill)


def render_maze_page(
    c: canvas.Canvas,
    page_number: int,
    maze: MazeData,
    page_spec: PageSpec,
    total_pages: int | None = None,
    book_theme: str | None = None,
) -> None:
    """Render a full print-ready 7 × 10-inch children's maze activity page.

    Enforces 100% KDP margin safety on all elements including START and FINISH badges.
    """
    register_activitybook_fonts()
    content = page_spec.get_content_rect(page_number)
    n = maze.grid_size

    # Resolve theme title for header banner
    if book_theme is not None:
        resolved_theme = book_theme.upper()
    else:
        is_road_trip = any(s.title == maze.title for s in ROAD_TRIP_SCENARIOS)
        resolved_theme = "ROAD TRIP QUEST" if is_road_trip else "EVERYDAY ADVENTURES"

    # 1. Header Band
    # Running category tracker
    subhead_y = content.y1 - 10.0
    c.setFont(FONT_BOLD, 8.0)
    c.setFillColorRGB(0.35, 0.35, 0.35)
    c.drawCentredString(
        content.x0 + content.width / 2.0,
        subhead_y,
        f"{resolved_theme}  •  {maze.maze_id.upper()}",
    )

    # Activity Title
    title_y = subhead_y - 17.0
    c.setFont(FONT_BOLD, 14.0)
    c.setFillColorRGB(0.0, 0.0, 0.0)
    c.drawCentredString(
        content.x0 + content.width / 2.0,
        title_y,
        maze.title,
    )

    # Scenario Instruction (distinct scenario subtitle)
    inst_y = title_y - 14.0
    c.setFont(FONT_ITALIC, 9.0)
    c.setFillColorRGB(0.25, 0.25, 0.25)
    c.drawCentredString(
        content.x0 + content.width / 2.0,
        inst_y,
        maze.instruction,
    )

    # Difficulty stars badge
    stars_y = inst_y - 15.0
    c.setFont(FONT_REGULAR, 8.5)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    label_text = f"Difficulty: {maze.difficulty.display_name}  "
    lw_str = stringWidth(label_text, FONT_REGULAR, 8.5)
    c.drawString(content.x0 + content.width / 2.0 - lw_str - 12.0, stars_y - 2.5, label_text)
    _draw_star_rating(c, content.x0 + content.width / 2.0 + 16.0, stars_y, maze.difficulty.stars, max_stars=3, r=4.0)

    # 2. Maze Grid Placement
    # In 7 x 10 in: content.width = 432 pt. Maze side = 340 pt leaves 46 pt on both left and right.
    # This guarantees plenty of room for side markers to remain strictly inside content_rect.
    maze_side = 340.0
    maze_x0 = content.x0 + (content.width - maze_side) / 2.0
    avail_bottom = content.y0 + 52.0
    avail_top = stars_y - 48.0
    maze_y0 = avail_bottom + (avail_top - avail_bottom - maze_side) / 2.0

    # Line width scaled to cell size
    cw = maze_side / float(n)
    wall_lw = max(1.5, min(2.8, cw * 0.08))

    # Draw the maze grid using Mazerator's draw_maze
    ep, xp = gm.draw_maze(
        c,
        maze_x0,
        maze_y0,
        maze_side,
        n,
        n,
        maze.right,
        maze.down,
        wall_lw,
        maze.entrance,
        maze.exit_,
    )

    # 3. Start and Finish Icon Badges with Complete Safe-Area Protection
    start_icon_fn = ADVENTURE_ICONS.get(maze.start_icon, ADVENTURE_ICONS["puppy"])
    goal_icon_fn = ADVENTURE_ICONS.get(maze.goal_icon, ADVENTURE_ICONS["bone"])

    def _place_safe_badge(opening_pt, icon_fn, label: str):
        px, py, edge = opening_pt
        icon_size = 12.5
        label_font = FONT_BOLD
        label_size = 7.5
        label_w = stringWidth(label, label_font, label_size)

        # Base offsets along outward normal
        if edge == "top":
            ix = px
            iy = py + 25.0
            lx = px
            ly = iy + icon_size + 2.5
            half_w = max(icon_size * 1.5, label_w / 2.0)
            bbox = (ix - half_w, iy - icon_size, ix + half_w, ly + label_size)
        elif edge == "bottom":
            ix = px
            iy = py - 23.0
            lx = px
            ly = iy - icon_size - 8.0
            half_w = max(icon_size * 1.5, label_w / 2.0)
            bbox = (ix - half_w, ly - 2.0, ix + half_w, iy + icon_size)
        elif edge == "left":
            half_w = max(icon_size * 1.3, label_w / 2.0)
            ix = px - 25.0
            iy = py
            lx = ix
            ly = iy - icon_size - 7.5
            bbox = (ix - half_w, ly - 2.0, ix + half_w, iy + icon_size)
        else:  # right
            half_w = max(icon_size * 1.3, label_w / 2.0)
            ix = px + 25.0
            iy = py
            lx = ix
            ly = iy - icon_size - 7.5
            bbox = (ix - half_w, ly - 2.0, ix + half_w, iy + icon_size)

        # Enforce strict safe-area bounds with 3.0 pt safety buffer
        bx0, by0, bx1, by1 = bbox
        dx = 0.0
        dy = 0.0

        safe_min_x = content.x0 + 3.0
        safe_max_x = content.x1 - 3.0
        safe_min_y = content.y0 + 20.0
        safe_max_y = content.y1 - 15.0

        if bx0 < safe_min_x:
            dx = safe_min_x - bx0
        elif bx1 > safe_max_x:
            dx = safe_max_x - bx1

        if by0 < safe_min_y:
            dy = safe_min_y - by0
        elif by1 > safe_max_y:
            dy = safe_max_y - by1

        ix += dx
        lx += dx
        iy += dy
        ly += dy
        final_bbox = (bx0 + dx, by0 + dy, bx1 + dx, by1 + dy)

        # Draw icon
        icon_fn(c, ix, iy, icon_size)
        # Draw label
        c.setFont(label_font, label_size)
        c.setFillColorRGB(0.0, 0.0, 0.0)
        c.drawCentredString(lx, ly, label)

        # Validate that badge is 100% inside safe content rectangle
        page_spec.validate_rect_safe(final_bbox[0], final_bbox[1], final_bbox[2], final_bbox[3], page_number)
        return final_bbox

    _place_safe_badge(ep, start_icon_fn, "START")
    _place_safe_badge(xp, goal_icon_fn, "FINISH")

    # 4. Corner Decorations (Outside maze, safely inside content rectangle)
    if resolved_theme == "ROAD TRIP QUEST":
        draw_pine_tree(c, content.x0 + 16.0, content.y1 - 70.0, 10.0, lw=1.1)
        draw_mountain(c, content.x1 - 18.0, content.y1 - 70.0, 11.0, lw=1.1)
        draw_traffic_cone(c, content.x0 + 16.0, content.y0 + 32.0, 9.5, lw=1.0)
        draw_compass(c, content.x1 - 18.0, content.y0 + 32.0, 9.5, lw=1.0)
    else:
        # Subtle, original themed corner decorations tailored to each scenario
        draw_scenario_corner_decorations(c, content, maze.title)

    # 5. Footer (Page number & reproducibility seed)
    footer_y = content.y0 + 8.0
    c.setFont(FONT_REGULAR, 9.0)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    page_str = f"{page_number}" if total_pages is None else f"{page_number} of {total_pages}"
    c.drawCentredString(content.x0 + content.width / 2.0, footer_y, page_str)

    # Seed reference for exact reproducibility
    c.setFont(FONT_REGULAR, 6.5)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawRightString(content.x1, footer_y, f"Seed: {maze.seed}")

    # Validate that main maze rectangle is 100% inside safe area
    page_spec.validate_rect_safe(maze_x0, maze_y0, maze_x0 + maze_side, maze_y0 + maze_side, page_number)


def build_everyday_adventures_sample_pdf(
    output_path: str = "output/everyday_adventures_sample_v1.pdf",
    page_spec: PageSpec | None = None,
    master_seed: int = 2026,
) -> tuple[str, list[MazeData]]:
    """Build a complete 12-page Everyday Adventures booklet (10 mazes + 2 answer keys) in 7 × 10 in."""
    from activitybook.activities.answer_key import build_answer_key_pages

    if page_spec is None:
        page_spec = PageSpec.kdp_7x10_recommended(page_count=96)

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    rng = random.Random(master_seed)

    mazes: list[MazeData] = []
    for i in range(10):
        scenario = EVERYDAY_ADVENTURE_SCENARIOS[i]
        maze_seed = rng.randint(100_000, 999_999)
        maze = generate_adventure_maze(
            maze_id=f"Maze {i + 1}",
            difficulty=scenario.difficulty,
            seed=maze_seed,
            scenario_index=i,
        )
        mazes.append(maze)

    total_pages = 10 + 2  # 10 maze pages + 2 answer key pages

    register_activitybook_fonts()
    c = canvas.Canvas(
        str(out_file),
        pagesize=(page_spec.width_points, page_spec.height_points),
        initialFontName=FONT_REGULAR,
    )
    c.setTitle("Everyday Adventures - Mazes & Answer Key")

    # Render 10 maze pages
    for i, maze in enumerate(mazes):
        page_num = i + 1
        render_maze_page(
            c,
            page_number=page_num,
            maze=maze,
            page_spec=page_spec,
            total_pages=total_pages,
            book_theme="EVERYDAY ADVENTURES",
        )
        c.showPage()

    # Render answer key pages (Pages 11 and 12 with 5 mazes per page for optimal readability)
    build_answer_key_pages(
        c,
        start_page_num=11,
        mazes=mazes,
        page_spec=page_spec,
        per_page=5,
        total_book_pages=total_pages,
        title="ANSWER KEY: EVERYDAY ADVENTURES",
    )

    c.save()
    return str(out_file), mazes


def build_road_trip_sample_pdf(
    output_path: str = "output/road_trip_mazes_sample_v3.pdf",
    page_spec: PageSpec | None = None,
    master_seed: int = 2026,
) -> tuple[str, list[MazeData]]:
    """Backward-compatible builder for the Road Trip sample booklet."""
    from activitybook.activities.answer_key import build_answer_key_pages

    if page_spec is None:
        page_spec = PageSpec.kdp_7x10_recommended(page_count=96)

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    rng = random.Random(master_seed)

    mazes: list[MazeData] = []
    for i in range(10):
        scenario = ROAD_TRIP_SCENARIOS[i]
        maze_seed = rng.randint(100_000, 999_999)
        maze = generate_road_trip_maze(
            maze_id=f"Maze {i + 1}",
            difficulty=scenario.difficulty,
            seed=maze_seed,
            scenario_index=i,
        )
        mazes.append(maze)

    total_pages = 10 + 2  # 10 maze pages + 2 answer key pages

    register_activitybook_fonts()
    c = canvas.Canvas(
        str(out_file),
        pagesize=(page_spec.width_points, page_spec.height_points),
        initialFontName=FONT_REGULAR,
    )
    c.setTitle("Road Trip Quest - Mazes & Answer Key")

    # Render 10 maze pages
    for i, maze in enumerate(mazes):
        page_num = i + 1
        render_maze_page(
            c,
            page_number=page_num,
            maze=maze,
            page_spec=page_spec,
            total_pages=total_pages,
            book_theme="ROAD TRIP QUEST",
        )
        c.showPage()

    # Render answer key pages (Pages 11 and 12)
    build_answer_key_pages(
        c,
        start_page_num=11,
        mazes=mazes,
        page_spec=page_spec,
        per_page=6,
        total_book_pages=total_pages,
        title="ANSWER KEY: ROAD TRIP MAZES",
    )

    c.save()
    return str(out_file), mazes
