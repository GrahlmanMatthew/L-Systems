import math

import pytest

from l_systems.renderer.turtle_renderer import Segment, build_segments, fit_segments


def test_empty_string_returns_no_segments():
    result = build_segments("", 0, 0, 0, 10, 90)
    assert result == []


def test_single_f_produces_one_segment():
    result = build_segments("F", 0.0, 0.0, 0.0, 10.0, 90.0)
    assert len(result) == 1


def test_segment_starts_at_origin():
    result = build_segments("F", 0.0, 0.0, 0.0, 10.0, 90.0)
    assert result[0].x1 == pytest.approx(0.0)
    assert result[0].y1 == pytest.approx(0.0)


def test_f_heading_zero_moves_right():
    result = build_segments("F", 0.0, 0.0, 0.0, 10.0, 90.0)
    assert result[0].x2 == pytest.approx(10.0, abs=1e-6)
    assert result[0].y2 == pytest.approx(0.0, abs=1e-6)


def test_f_heading_90_moves_up():
    result = build_segments("F", 0.0, 0.0, 90.0, 10.0, 90.0)
    assert result[0].x2 == pytest.approx(0.0, abs=1e-6)
    assert result[0].y2 == pytest.approx(-10.0, abs=1e-6)  # pygame y-axis is inverted


def test_turn_right_changes_direction():
    result_straight = build_segments("FF", 0.0, 0.0, 0.0, 10.0, 90.0)
    result_turned = build_segments("F+F", 0.0, 0.0, 0.0, 10.0, 90.0)
    assert result_straight[1].x2 != pytest.approx(result_turned[1].x2, abs=1e-6)


def test_turn_left_changes_direction():
    result_straight = build_segments("FF", 0.0, 0.0, 0.0, 10.0, 90.0)
    result_turned = build_segments("F-F", 0.0, 0.0, 0.0, 10.0, 90.0)
    assert result_straight[1].x2 != pytest.approx(result_turned[1].x2, abs=1e-6)


def test_push_pop_restores_position():
    # F draws first segment, then branch [+F] returns to same point, then F continues
    result = build_segments("F[+F]F", 0.0, 0.0, 0.0, 10.0, 90.0)
    # Third segment (after pop) should start where first ended
    assert result[2].x1 == pytest.approx(result[0].x2, abs=1e-6)
    assert result[2].y1 == pytest.approx(result[0].y2, abs=1e-6)


def test_g_symbol_draws_segment():
    result = build_segments("G", 0.0, 0.0, 0.0, 10.0, 90.0)
    assert len(result) == 1


def test_lowercase_f_moves_without_drawing():
    result = build_segments("fF", 0.0, 0.0, 0.0, 10.0, 90.0)
    assert len(result) == 1
    assert result[0].x1 == pytest.approx(10.0, abs=1e-6)


def test_segment_length_scales_correctly():
    result_short = build_segments("F", 0.0, 0.0, 0.0, 5.0, 90.0)
    result_long = build_segments("F", 0.0, 0.0, 0.0, 20.0, 90.0)
    seg_short = result_short[0]
    seg_long = result_long[0]
    short_len = math.dist((seg_short.x1, seg_short.y1), (seg_short.x2, seg_short.y2))
    long_len = math.dist((seg_long.x1, seg_long.y1), (seg_long.x2, seg_long.y2))
    assert long_len == pytest.approx(short_len * 4, abs=1e-6)


def test_unmatched_pop_does_not_crash():
    result = build_segments("]F", 0.0, 0.0, 0.0, 10.0, 90.0)
    assert len(result) == 1


def test_multiple_branches_correct_count():
    # F[+F][-F]F = 4 forward segments
    result = build_segments("F[+F][-F]F", 0.0, 0.0, 0.0, 10.0, 30.0)
    assert len(result) == 4


# --- fit_segments ---


def test_fit_segments_empty_returns_empty():
    assert fit_segments([], 800, 600) == []


def test_fit_segments_centers_within_screen():
    segs = [Segment(0.0, 0.0, 100.0, 0.0)]
    result = fit_segments(segs, 800, 600)
    mid_x = (result[0].x1 + result[0].x2) / 2
    assert mid_x == pytest.approx(400.0, abs=1.0)


def test_fit_segments_preserves_count():
    segs = build_segments("F[+F][-F]F", 0.0, 0.0, 0.0, 10.0, 30.0)
    result = fit_segments(segs, 1920, 1080)
    assert len(result) == len(segs)


def test_fit_segments_stays_within_screen():
    segs = build_segments("F+F+F+F", 0.0, 0.0, 0.0, 1000.0, 90.0)
    result = fit_segments(segs, 800, 600)
    for seg in result:
        assert 0 <= seg.x1 <= 800
        assert 0 <= seg.x2 <= 800
        assert 0 <= seg.y1 <= 600
        assert 0 <= seg.y2 <= 600


def test_fit_segments_scales_uniformly():
    segs = [Segment(0.0, 0.0, 10.0, 0.0), Segment(0.0, 0.0, 0.0, 10.0)]
    result = fit_segments(segs, 800, 800)
    horiz = abs(result[0].x2 - result[0].x1)
    vert = abs(result[1].y2 - result[1].y1)
    assert horiz == pytest.approx(vert, rel=1e-6)
