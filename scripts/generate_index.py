import argparse
from html import escape
from pathlib import Path
from urllib.parse import quote


def generate_index(wheels_dir: Path, output: Path) -> None:
    wheels = sorted(wheels_dir.glob("*.whl"))

    lines = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '    <meta charset="UTF-8">',
        "    <title>Python Wheels</title>",
        "</head>",
        "<body>",
    ]

    lines.extend(
        f'    <a href="{quote(wheels_dir.name + "/" + wheel.name, safe="/")}"><br>'
        f"{escape(wheel.name)}</a>"
        for wheel in wheels
    )

    lines.extend(["</body>", "</html>", ""])

    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {output} with {len(wheels)} wheels")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--wheels-dir",
        type=Path,
        default=Path("wheels"),
        help="Directory containing .whl files",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("index.html"),
        help="Output HTML file",
    )

    args = parser.parse_args()
    generate_index(args.wheels_dir, args.output)
