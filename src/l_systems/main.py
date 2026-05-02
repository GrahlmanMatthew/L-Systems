import logging
import os
from dataclasses import dataclass, replace
from datetime import datetime

import pygame

from l_systems.config.constants import (
    BACKGROUND_COLOR,
    HUD_BG_COLOR,
    LINE_COLOR,
    SPEED_MAX,
    SPEED_MIN,
    SPEED_STEP,
    UI_COLOR,
    UI_DIM_COLOR,
    UI_FONT_SIZE,
    UI_PADDING,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)
from l_systems.config.settings import FPS_TARGET, SEGMENTS_PER_FRAME
from l_systems.core.presets import get_preset, preset_count
from l_systems.renderer.turtle_renderer import Segment, build_segments

logging.basicConfig(
    level=logging.DEBUG if os.environ.get("DEBUG") else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger(__name__)

_HINT_TEXT = "[1-6] preset  [Space] pause  [R] restart  [+/-] speed  [S] save  [Esc] quit"


@dataclass
class AppState:
    preset_index: int
    segments: list[Segment]
    drawn_count: int
    is_animating: bool
    segments_per_frame: int


def load_preset(index: int) -> AppState:
    preset = get_preset(index)
    l_string = preset.system.expand(preset.iterations)
    segments = build_segments(
        l_string,
        start_x=WINDOW_WIDTH * preset.start_x_ratio,
        start_y=WINDOW_HEIGHT * preset.start_y_ratio,
        start_heading=preset.start_heading,
        segment_length=preset.segment_length,
        angle=preset.system.angle,
    )
    logger.info(
        "Loaded preset %d/%d '%s' — %d segments",
        index + 1,
        preset_count(),
        preset.name,
        len(segments),
    )
    return AppState(
        preset_index=index,
        segments=segments,
        drawn_count=0,
        is_animating=True,
        segments_per_frame=SEGMENTS_PER_FRAME,
    )


def handle_events(
    events: list[pygame.event.Event],
    state: AppState,
) -> AppState:
    for event in events:
        if event.type == pygame.QUIT:
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                raise SystemExit

            preset_keys = (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6)
            if event.key in preset_keys:
                index = event.key - pygame.K_1
                if index < preset_count():
                    state = load_preset(index)

            elif event.key == pygame.K_SPACE:
                state = replace(state, is_animating=not state.is_animating)

            elif event.key == pygame.K_r:
                state = replace(state, drawn_count=0, is_animating=True)

            elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                new_speed = min(state.segments_per_frame * SPEED_STEP, SPEED_MAX)
                state = replace(state, segments_per_frame=new_speed)

            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                new_speed = max(state.segments_per_frame // SPEED_STEP, SPEED_MIN)
                state = replace(state, segments_per_frame=new_speed)

            elif event.key == pygame.K_s:
                _save_screenshot(pygame.display.get_surface())

    return state


def update(state: AppState) -> AppState:
    if not state.is_animating or state.drawn_count >= len(state.segments):
        return state
    new_count = min(state.drawn_count + state.segments_per_frame, len(state.segments))
    return replace(state, drawn_count=new_count)


def draw(surface: pygame.Surface, state: AppState) -> None:
    surface.fill(BACKGROUND_COLOR)
    for seg in state.segments[: state.drawn_count]:
        pygame.draw.line(surface, LINE_COLOR, (seg.x1, seg.y1), (seg.x2, seg.y2), 1)
    draw_hud(surface, state)


def draw_hud(surface: pygame.Surface, state: AppState) -> None:
    font = pygame.font.SysFont("monospace", UI_FONT_SIZE)
    preset = get_preset(state.preset_index)

    top_lines = [
        f"{state.preset_index + 1} / {preset_count()} — {preset.name}",
        f"{state.drawn_count:,} / {len(state.segments):,} segments",
        f"Speed: {state.segments_per_frame} seg/frame",
        "PAUSED" if not state.is_animating else "",
    ]

    rendered = [font.render(line, True, UI_COLOR) for line in top_lines if line]
    box_w = max(r.get_width() for r in rendered) + UI_PADDING * 2
    box_h = sum(r.get_height() for r in rendered) + UI_PADDING * 2 + (len(rendered) - 1) * 4

    hud_surface = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    hud_surface.fill(HUD_BG_COLOR)
    surface.blit(hud_surface, (UI_PADDING, UI_PADDING))

    y = UI_PADDING * 2
    for r in rendered:
        surface.blit(r, (UI_PADDING * 2, y))
        y += r.get_height() + 4

    hint = font.render(_HINT_TEXT, True, UI_DIM_COLOR)
    hint_x = (WINDOW_WIDTH - hint.get_width()) // 2
    hint_y = WINDOW_HEIGHT - hint.get_height() - UI_PADDING
    surface.blit(hint, (hint_x, hint_y))


def _save_screenshot(surface: pygame.Surface) -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"output/screenshot_{timestamp}.png"
    pygame.image.save(surface, path)
    logger.info("Screenshot saved to %s", path)


def main() -> None:
    logger.info("Starting %s v0.1.0", WINDOW_TITLE)
    pygame.init()
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    state = load_preset(0)

    while True:
        events = pygame.event.get()
        state = handle_events(events, state)
        state = update(state)
        draw(surface, state)
        pygame.display.flip()
        clock.tick(FPS_TARGET)


if __name__ == "__main__":
    main()
