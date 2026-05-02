from l_systems.core.grammar import LSystem, Preset

PRESETS: list[Preset] = [
    Preset(
        name="Fractal Plant",
        system=LSystem(
            axiom="X",
            rules={
                "X": "F+[[X]-X]-F[-FX]+X",
                "F": "FF",
            },
            angle=25.0,
        ),
        iterations=5,
        segment_length=6.0,
        start_heading=90.0,
        start_x_ratio=0.5,
        start_y_ratio=0.95,
    ),
    Preset(
        name="Fractal Tree",
        system=LSystem(
            axiom="F",
            rules={
                "F": "F[+F]F[-F]F",
            },
            angle=25.7,
        ),
        iterations=5,
        segment_length=7.0,
        start_heading=90.0,
        start_x_ratio=0.5,
        start_y_ratio=0.95,
    ),
    Preset(
        name="Fern",
        system=LSystem(
            axiom="X",
            rules={
                "X": "F+[[X]-X]-F[-FX]+X",
                "F": "FF",
            },
            angle=22.5,
        ),
        iterations=6,
        segment_length=4.0,
        start_heading=90.0,
        start_x_ratio=0.5,
        start_y_ratio=0.97,
    ),
    Preset(
        name="Sierpinski Triangle",
        system=LSystem(
            axiom="F-G-G",
            rules={
                "F": "F-G+F+G-F",
                "G": "GG",
            },
            angle=120.0,
        ),
        iterations=6,
        segment_length=6.0,
        start_heading=0.0,
        start_x_ratio=0.15,
        start_y_ratio=0.8,
    ),
    Preset(
        name="Koch Snowflake",
        system=LSystem(
            axiom="F++F++F",
            rules={
                "F": "F-F++F-F",
            },
            angle=60.0,
        ),
        iterations=4,
        segment_length=5.0,
        start_heading=0.0,
        start_x_ratio=0.15,
        start_y_ratio=0.65,
    ),
    Preset(
        name="Dragon Curve",
        system=LSystem(
            axiom="FX",
            rules={
                "X": "X+YF+",
                "Y": "-FX-Y",
            },
            angle=90.0,
        ),
        iterations=12,
        segment_length=8.0,
        start_heading=0.0,
        start_x_ratio=0.45,
        start_y_ratio=0.55,
    ),
    Preset(
        name="Lévy C Curve",
        system=LSystem(
            axiom="F",
            rules={
                "F": "+F--F+",
            },
            angle=45.0,
        ),
        iterations=14,
        segment_length=6.0,
        start_heading=0.0,
        start_x_ratio=0.2,
        start_y_ratio=0.5,
    ),
    Preset(
        name="Algae Bush",
        system=LSystem(
            axiom="F",
            rules={
                "F": "FF-[-F+F+F]+[+F-F-F]",
            },
            angle=22.5,
        ),
        iterations=4,
        segment_length=8.0,
        start_heading=90.0,
        start_x_ratio=0.5,
        start_y_ratio=0.95,
    ),
    Preset(
        name="Hilbert Curve",
        system=LSystem(
            axiom="A",
            rules={
                "A": "+BF-AFA-FB+",
                "B": "-AF+BFB+FA-",
            },
            angle=90.0,
        ),
        iterations=6,
        segment_length=8.0,
        start_heading=0.0,
        start_x_ratio=0.1,
        start_y_ratio=0.1,
    ),
    Preset(
        name="Crystal",
        system=LSystem(
            axiom="F+F+F+F",
            rules={
                "F": "FF+F++F+F",
            },
            angle=90.0,
        ),
        iterations=4,
        segment_length=8.0,
        start_heading=0.0,
        start_x_ratio=0.1,
        start_y_ratio=0.5,
    ),
]


def get_preset(index: int) -> Preset:
    return PRESETS[index % len(PRESETS)]


def preset_count() -> int:
    return len(PRESETS)
