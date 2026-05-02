import math

import pytest

from l_systems.renderer.turtle_renderer import build_segments


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
