from dataclasses import dataclass


@dataclass
class LSystem:
    axiom: str
    rules: dict[str, str]
    angle: float  # degrees per + / - symbol

    def expand(self, iterations: int) -> str:
        current = self.axiom
        for _ in range(iterations):
            current = self._apply_rules(current)
        return current

    def _apply_rules(self, current: str) -> str:
        return "".join(self.rules.get(ch, ch) for ch in current)


@dataclass
class Preset:
    name: str
    system: LSystem
    iterations: int
    segment_length: float
    start_heading: float  # degrees; 90 = pointing up
    start_x_ratio: float  # fraction of window width
    start_y_ratio: float  # fraction of window height
