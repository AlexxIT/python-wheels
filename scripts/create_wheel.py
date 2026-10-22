import argparse
import csv
import io
from zipfile import ZIP_DEFLATED, ZipFile


def create_wheel(name: str, version: str, tag: str):
    wheel_name = f"{name}-{version}-{tag}.whl"
    dist_info = f"{name}-{version}.dist-info"

    files = {
        f"{dist_info}/METADATA": (
            "Metadata-Version: 2.1\n"
            f"Name: {name}\n"
            f"Version: {version}\n"
            "Summary: Placeholder package\n"
        ),
        f"{dist_info}/WHEEL": (
            "Wheel-Version: 1.0\n"
            "Generator: fake\n"
            "Root-Is-Purelib: true\n"
            f"Tag: {tag}\n"
        ),
    }

    record_path = f"{dist_info}/RECORD"

    output = io.StringIO(newline="")
    writer = csv.writer(output)

    for path in files:
        writer.writerow([path, "", ""])

    writer.writerow([record_path, "", ""])
    files[record_path] = output.getvalue()

    with ZipFile(wheel_name, "w", ZIP_DEFLATED) as wheel:
        for path, content in files.items():
            wheel.writestr(path, content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a placeholder wheel package")
    parser.add_argument("--name", required=True, help="Package name")
    parser.add_argument("--version", required=True, help="Package version")
    parser.add_argument(
        "--tag", default="py3-none-win_arm64", help="Wheel platform tag"
    )

    args = parser.parse_args()

    create_wheel(args.name, args.version, args.tag)
