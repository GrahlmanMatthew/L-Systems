import pytest

from l_systems.core.grammar import LSystem


def test_expand_zero_iterations_returns_axiom():
    system = LSystem(axiom="F", rules={"F": "FF"}, angle=90.0)
    assert system.expand(0) == "F"


def test_expand_single_iteration():
    system = LSystem(axiom="F", rules={"F": "FF"}, angle=90.0)
    assert system.expand(1) == "FF"


def test_expand_two_iterations():
    system = LSystem(axiom="F", rules={"F": "FF"}, angle=90.0)
    assert system.expand(2) == "FFFF"


def test_expand_symbol_without_rule_is_kept():
    system = LSystem(axiom="FX", rules={"F": "FF"}, angle=90.0)
    assert system.expand(1) == "FFX"


def test_expand_multiple_rules():
    system = LSystem(axiom="AB", rules={"A": "AB", "B": "A"}, angle=0.0)
    assert system.expand(1) == "ABA"
    assert system.expand(2) == "ABAAB"


def test_expand_branching_symbols_preserved():
    system = LSystem(axiom="F[+F][-F]", rules={"F": "FF"}, angle=25.0)
    result = system.expand(1)
    assert "[" in result
    assert "]" in result
    assert result.count("F") == 6


def test_expand_growth_rate():
    system = LSystem(axiom="F", rules={"F": "F+F-F-F+F"}, angle=90.0)
    result = system.expand(3)
    assert len(result) > len(system.expand(2)) > len(system.expand(1))


@pytest.mark.parametrize("iterations", [1, 2, 3, 4])
def test_expand_produces_non_empty_string(iterations: int):
    system = LSystem(axiom="X", rules={"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}, angle=25.0)
    assert len(system.expand(iterations)) > 0
