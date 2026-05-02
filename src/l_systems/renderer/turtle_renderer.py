import math
from dataclasses import dataclass

_FIT_PADDING: float = 0.06


@dataclass
class Segment:
    x1: float
    y1: float
    x2: float
    y2: float


def fit_segments(
    segments: list[Segment],
    screen_width: int,
    screen_height: int,
) -> list[Segment]:
    """Scale and translate segments to fill the screen with uniform padding."""
    if not segments:
        return segments

    min_x = min(min(s.x1, s.x2) for s in segments)
    max_x = max(max(s.x1, s.x2) for s in segments)
    min_y = min(min(s.y1, s.y2) for s in segments)
    max_y = max(max(s.y1, s.y2) for s in segments)

    content_w = max_x - min_x
    content_h = max_y - min_y
    if content_w == 0 and content_h == 0:
        return segments

    avail_w = screen_width * (1 - 2 * _FIT_PADDING)
    avail_h = screen_height * (1 - 2 * _FIT_PADDING)
    if content_h == 0:
        scale = avail_w / content_w
    elif content_w == 0:
        scale = avail_h / content_h
    else:
        scale = min(avail_w / content_w, avail_h / content_h)

    offset_x = (screen_width - content_w * scale) / 2 - min_x * scale
    offset_y = (screen_height - content_h * scale) / 2 - min_y * scale

    return [
        Segment(
            s.x1 * scale + offset_x,
            s.y1 * scale + offset_y,
            s.x2 * scale + offset_x,
            s.y2 * scale + offset_y,
        )
        for s in segments
    ]


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
