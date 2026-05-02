import math
from dataclasses import dataclass


@dataclass
class Segment:
    x1: float
    y1: float
    x2: float
    y2: float


def build_segments(
    l_string: str,
    start_x: float,
    start_y: float,
    start_heading: float,
    segment_length: float,
    angle: float,
) -> list[Segment]:
    segments: list[Segment] = []
    stack: list[tuple[float, float, float]] = []

    x, y = start_x, start_y
    heading = start_heading
    angle_rad = math.radians(angle)

    for ch in l_string:
        if ch in ("F", "G"):
            nx = x + segment_length * math.cos(math.radians(heading))
            ny = y - segment_length * math.sin(math.radians(heading))
            segments.append(Segment(x, y, nx, ny))
            x, y = nx, ny
        elif ch == "f":
            x += segment_length * math.cos(math.radians(heading))
            y -= segment_length * math.sin(math.radians(heading))
        elif ch == "+":
            heading += math.degrees(angle_rad)
        elif ch == "-":
            heading -= math.degrees(angle_rad)
        elif ch == "[":
            stack.append((x, y, heading))
        elif ch == "]":
            if stack:
                x, y, heading = stack.pop()

    return segments
