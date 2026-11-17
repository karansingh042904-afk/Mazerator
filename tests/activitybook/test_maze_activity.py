"""Automated test suite for Road Trip Maze Activity and Answer Key (Milestone 2)."""

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pypdf
from reportlab.pdfgen import canvas

from activitybook.activities.maze_activity import (
    MazeData,
    MazeDifficulty,
    ROAD_TRIP_SCENARIOS,
    build_road_trip_sample_pdf,
    generate_road_trip_maze,
    render_maze_page,
)
from activitybook.activities.answer_key import (
    build_answer_key_pages,
    render_answer_key_page,
    render_maze_solution_thumbnail,
)
from activitybook.activities.road_trip_icons import ROAD_TRIP_ICONS
from activitybook.core.page_spec import PageSpec, TRIM_7X10
from maze_generator import generate_mazes as gm


class TestRoadTripMazeGeneration(unittest.TestCase):
    """Test algorithmic generation, difficulty scaling, and spanning-tree invariants."""

    def test_maze_generation_all_difficulty_levels(self):
        """Test Easy, Medium, and Challenging tiers."""
        tiers = [
            (MazeDifficulty.EASY, 10, 0.40),
            (MazeDifficulty.MEDIUM, 15, 0.50),
            (MazeDifficulty.CHALLENGING, 20, 0.60),
        ]
        for diff, expected_n, expected_factor in tiers:
            maze = generate_road_trip_maze("TestMaze", difficulty=diff, seed=12345)
            self.assertEqual(maze.grid_size, expected_n)
            self.assertEqual(len(maze.right), expected_n)
            self.assertEqual(len(maze.down), expected_n)
            min_expected_len = int(expected_n * expected_n * expected_factor)
            self.assertGreaterEqual(
                maze.path_length,
                min_expected_len,
                f"Path length {maze.path_length} < expected min {min_expected_len} for {diff.name}",
            )

    def test_valid_start_and_finish_openings(self):
        """Ensure entrance and exit openings sit on distinct border cells."""
        for seed in range(10):
            maze = generate_road_trip_maze("M", difficulty=MazeDifficulty.EASY, seed=seed)
            n = maze.grid_size

            # Check openings
            self.assertIn(maze.entrance[0], ("top", "bottom", "left", "right"))
            self.assertIn(maze.exit_[0], ("top", "bottom", "left", "right"))

            # Start and goal cells are within grid bounds
            sr, sc = maze.start_cell
            gr, gc = maze.goal_cell
            self.assertTrue(0 <= sr < n and 0 <= sc < n)
            self.assertTrue(0 <= gr < n and 0 <= gc < n)
            self.assertNotEqual(maze.start_cell, maze.goal_cell)

    def test_solution_path_connectivity_and_validity(self):
        """Verify that every step in solution_path moves through an open wall."""
        for seed in (42, 101, 777):
            maze = generate_road_trip_maze("ConnTest", difficulty=MazeDifficulty.MEDIUM, seed=seed)
            path = maze.solution_path

            # First cell must be start_cell, last cell must be goal_cell
            self.assertEqual(path[0], maze.start_cell)
            self.assertEqual(path[-1], maze.goal_cell)

            # Check consecutive step validity
            for i in range(len(path) - 1):
                r1, c1 = path[i]
                r2, c2 = path[i + 1]
                manhattan = abs(r1 - r2) + abs(c1 - c2)
                self.assertEqual(manhattan, 1, f"Non-adjacent step between {path[i]} and {path[i+1]}")

                # Verify open passage
                if r2 == r1 + 1 and c2 == c1:
                    self.assertTrue(maze.down[r1][c1])
                elif r2 == r1 - 1 and c2 == c1:
                    self.assertTrue(maze.down[r2][c1])
                elif c2 == c1 + 1 and r2 == r1:
                    self.assertTrue(maze.right[r1][c1])
                elif c2 == c1 - 1 and r2 == r1:
                    self.assertTrue(maze.right[r1][c2])
                else:
                    self.fail(f"Invalid neighbor step: {path[i]} -> {path[i+1]}")

    def test_no_disconnected_maze_sections(self):
        """Spanning tree check: exactly n*n - 1 passages and 100% reachable cells."""
        maze = generate_road_trip_maze("SpanTest", difficulty=MazeDifficulty.EASY, seed=999)
        n = maze.grid_size
        open_passages = gm.count_open_passages(maze.right, maze.down)
        self.assertEqual(open_passages, n * n - 1)

        # BFS reachability from (0, 0)
        distances = gm.bfs_distances(maze.right, maze.down, n, n, (0, 0))
        self.assertEqual(len(distances), n * n)

    def test_reproducibility_with_fixed_seed(self):
        """Same seed must produce byte-identical maze data."""
        maze1 = generate_road_trip_maze("M1", difficulty=MazeDifficulty.MEDIUM, seed=54321)
        maze2 = generate_road_trip_maze("M1", difficulty=MazeDifficulty.MEDIUM, seed=54321)

        self.assertEqual(maze1.start_cell, maze2.start_cell)
        self.assertEqual(maze1.goal_cell, maze2.goal_cell)
        self.assertEqual(maze1.solution_path, maze2.solution_path)
        self.assertEqual(maze1.right, maze2.right)
        self.assertEqual(maze1.down, maze2.down)

        # Different seed must produce different maze
        maze3 = generate_road_trip_maze("M1", difficulty=MazeDifficulty.MEDIUM, seed=99999)
        self.assertNotEqual(maze1.solution_path, maze3.solution_path)


class TestUniqueRoadTripScenarios(unittest.TestCase):
    """Test that all 10 road-trip scenarios have unique titles and instructions (Fix 3)."""

    def test_ten_scenarios_are_unique(self):
        self.assertEqual(len(ROAD_TRIP_SCENARIOS), 10)
        titles = [s.title for s in ROAD_TRIP_SCENARIOS]
        instructions = [s.instruction for s in ROAD_TRIP_SCENARIOS]

        # Ensure no duplicates in titles or instructions
        self.assertEqual(len(set(titles)), 10, f"Duplicate titles found in scenarios: {titles}")
        self.assertEqual(len(set(instructions)), 10, f"Duplicate instructions found: {instructions}")

    def test_generated_sample_mazes_have_unique_titles_and_instructions(self):
        mazes = [
            generate_road_trip_maze(f"Maze {i+1}", scenario_index=i, seed=100 + i)
            for i in range(10)
        ]
        titles = [m.title for m in mazes]
        instructions = [m.instruction for m in mazes]
        self.assertEqual(len(set(titles)), 10)
        self.assertEqual(len(set(instructions)), 10)


class TestRoadTripIcons(unittest.TestCase):
    """Test that all 8 road trip vector icons execute without error."""

    def test_all_icons_render_on_canvas(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            c = canvas.Canvas(tmp.name, pagesize=(504, 720))
            for name, draw_fn in ROAD_TRIP_ICONS.items():
                draw_fn(c, 252.0, 360.0, 20.0)
                draw_fn(c, 100.0, 100.0, 12.0)
            c.showPage()
            c.save()
            self.assertGreater(Path(tmp.name).stat().st_size, 0)


class TestMarkerSafeAreaCompliance(unittest.TestCase):
    """Test that START and FINISH markers always respect KDP safe margins (Fix 2)."""

    def setUp(self):
        self.spec = PageSpec.kdp_7x10_recommended(page_count=96)

    def test_side_and_top_bottom_marker_compliance_across_seeds(self):
        """Test 25 random mazes covering left, right, top, and bottom openings on both odd/even pages."""
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            c = canvas.Canvas(tmp.name, pagesize=(self.spec.width_points, self.spec.height_points))
            found_edges = set()

            for seed in range(25):
                maze = generate_road_trip_maze("M", difficulty=MazeDifficulty.MEDIUM, seed=seed)
                found_edges.add(maze.entrance[0])
                found_edges.add(maze.exit_[0])

                # Test on both odd page (gutter on left) and even page (gutter on right)
                for page_num in (1, 2):
                    # render_maze_page will raise ValueError via page_spec.validate_rect_safe if invalid
                    render_maze_page(c, page_number=page_num, maze=maze, page_spec=self.spec)
                    c.showPage()

            c.save()
            # Verify we tested all 4 edge orientations
            self.assertTrue({"top", "bottom", "left", "right"}.issubset(found_edges))


class TestAnswerKey(unittest.TestCase):
    """Test answer key generation, multi-up layout, and solution fidelity (Fix 1)."""

    def setUp(self):
        self.spec = PageSpec.kdp_7x10_recommended(page_count=96)
        self.mazes = [
            generate_road_trip_maze(f"Maze {i+1}", scenario_index=i, seed=i)
            for i in range(10)
        ]

    def test_render_answer_key_page_6up(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            c = canvas.Canvas(tmp.name, pagesize=(self.spec.width_points, self.spec.height_points))
            render_answer_key_page(c, page_number=11, mazes=self.mazes[:6], page_spec=self.spec, layout="6-up")
            c.showPage()
            c.save()

            reader = pypdf.PdfReader(tmp.name)
            self.assertEqual(len(reader.pages), 1)
            text = reader.pages[0].extract_text()
            self.assertIn("ANSWER KEY", text)
            self.assertIn("Maze 1", text)
            self.assertIn("Maze 6", text)

    def test_render_answer_key_page_4up_enhanced(self):
        """Verify enhanced 4-up layout with larger thumbnails and title subtitles."""
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            c = canvas.Canvas(tmp.name, pagesize=(self.spec.width_points, self.spec.height_points))
            render_answer_key_page(c, page_number=12, mazes=self.mazes[6:10], page_spec=self.spec, layout="4-up")
            c.showPage()
            c.save()

            reader = pypdf.PdfReader(tmp.name)
            self.assertEqual(len(reader.pages), 1)
            text = reader.pages[0].extract_text()
            self.assertIn("ANSWER KEY", text)
            self.assertIn("Maze 7", text)
            self.assertIn("Maze 10", text)

    def test_build_answer_key_multi_page_uses_4up_for_last_page(self):
        """Test splitting 10 mazes across 2 answer key pages: page 11 (6-up) and page 12 (4-up)."""
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            c = canvas.Canvas(tmp.name, pagesize=(self.spec.width_points, self.spec.height_points))
            pages_created = build_answer_key_pages(c, start_page_num=11, mazes=self.mazes, page_spec=self.spec, per_page=6)
            c.save()

            self.assertEqual(pages_created, 2)
            reader = pypdf.PdfReader(tmp.name)
            self.assertEqual(len(reader.pages), 2)
            # Page 11 has Maze 1 to 6
            text_p11 = reader.pages[0].extract_text()
            self.assertIn("Maze 1", text_p11)
            self.assertIn("Maze 6", text_p11)
            # Page 12 has Maze 7 to 10
            text_p12 = reader.pages[1].extract_text()
            self.assertIn("Maze 7", text_p12)
            self.assertIn("Maze 10", text_p12)


class TestSamplePdfBooklet(unittest.TestCase):
    """Test generating the complete 12-page sample booklet (10 mazes + 2 answer keys)."""

    def test_sample_pdf_build_and_specifications(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_pdf = str(Path(tmp_dir) / "test_sample_v2.pdf")
            pdf_path, mazes = build_road_trip_sample_pdf(out_pdf, master_seed=2026)

            self.assertEqual(len(mazes), 10)
            self.assertTrue(Path(pdf_path).exists())

            reader = pypdf.PdfReader(pdf_path)
            self.assertEqual(len(reader.pages), 12)

            # Check dimensions on all 12 pages
            for idx, page in enumerate(reader.pages):
                box = page.mediabox
                self.assertEqual(float(box.width), 504.0, f"Page {idx+1} width != 504.0 pt")
                self.assertEqual(float(box.height), 720.0, f"Page {idx+1} height != 720.0 pt")

            # Check text on activity pages
            page1_text = reader.pages[0].extract_text()
            self.assertIn("ROAD TRIP QUEST", page1_text)
            self.assertIn("MAZE 1", page1_text)
            self.assertIn("Campsite Arrival", page1_text)
            self.assertIn("START", page1_text)
            self.assertIn("FINISH", page1_text)

            # Check page 10 unique scenario
            page10_text = reader.pages[9].extract_text()
            self.assertIn("MAZE 10", page10_text)
            self.assertIn("The Great Summit Climb", page10_text)

            # Check text on answer key pages
            key_page11 = reader.pages[10].extract_text()
            self.assertIn("ANSWER KEY", key_page11)
            self.assertIn("Maze 1", key_page11)
            self.assertIn("Maze 6", key_page11)

            key_page12 = reader.pages[11].extract_text()
            self.assertIn("ANSWER KEY", key_page12)
            self.assertIn("Maze 7", key_page12)
            self.assertIn("Maze 10", key_page12)


if __name__ == "__main__":
    unittest.main()
