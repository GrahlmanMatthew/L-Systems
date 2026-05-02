import pytest

from l_systems.core.presets import PRESETS, get_preset, preset_count


def test_preset_count_matches_list():
    assert preset_count() == len(PRESETS)


def test_preset_count_is_ten():
    assert preset_count() == 10


@pytest.mark.parametrize("index", range(10))
def test_get_preset_returns_correct_preset(index: int):
    assert get_preset(index) is PRESETS[index]


def test_get_preset_wraps_on_overflow():
    assert get_preset(10) is PRESETS[0]
    assert get_preset(11) is PRESETS[1]


@pytest.mark.parametrize("preset", PRESETS)
def test_preset_has_non_empty_name(preset):
    assert preset.name


@pytest.mark.parametrize("preset", PRESETS)
def test_preset_has_non_empty_axiom(preset):
    assert preset.system.axiom


@pytest.mark.parametrize("preset", PRESETS)
def test_preset_has_positive_iterations(preset):
    assert preset.iterations > 0


@pytest.mark.parametrize("preset", PRESETS)
def test_preset_has_positive_segment_length(preset):
    assert preset.segment_length > 0


@pytest.mark.parametrize("preset", PRESETS)
def test_preset_position_ratios_in_range(preset):
    assert 0.0 <= preset.start_x_ratio <= 1.0
    assert 0.0 <= preset.start_y_ratio <= 1.0


@pytest.mark.parametrize("preset", PRESETS)
def test_preset_expands_without_error(preset):
    result = preset.system.expand(preset.iterations)
    assert isinstance(result, str)
    assert len(result) > 0
