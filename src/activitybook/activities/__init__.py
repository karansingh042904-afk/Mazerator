"""Activity generators and answer key modules for ActivityBook Studio."""

from .maze_activity import (
    MazeData,
    MazeDifficulty,
    build_road_trip_sample_pdf,
    generate_road_trip_maze,
    render_maze_page,
)
from .answer_key import (
    build_answer_key_pages,
    render_answer_key_page,
    render_maze_solution_thumbnail,
)
from .road_trip_icons import (
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

__all__ = [
    "MazeData",
    "MazeDifficulty",
    "generate_road_trip_maze",
    "render_maze_page",
    "build_answer_key_pages",
    "render_answer_key_page",
    "render_maze_solution_thumbnail",
    "ROAD_TRIP_ICONS",
    "draw_camper_van",
    "draw_campsite",
    "draw_car",
    "draw_compass",
    "draw_mountain",
    "draw_pine_tree",
    "draw_traffic_cone",
    "draw_traffic_sign",
]
