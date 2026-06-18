from __future__ import annotations

import sys
from pathlib import Path


PACKAGE_NAME = "cli-anything-pieces"
PACKAGE_VERSION = "1.0.0"


def _handle_metadata_query(argv: list[str]) -> bool:
    if len(argv) != 2:
        return False
    if argv[1] == "--name":
        print(PACKAGE_NAME)
        return True
    if argv[1] == "--version":
        print(PACKAGE_VERSION)
        return True
    return False


if __name__ == "__main__" and _handle_metadata_query(sys.argv):
    raise SystemExit(0)

from setuptools import find_namespace_packages, setup


ROOT = Path(__file__).parent
README = ROOT / "README.md"
LONG_DESCRIPTION = README.read_text(encoding="utf-8") if README.exists() else ""

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author="黎昊",
    author_email="lizhiyuan1234@163.com",
    description="CLI harness for Pieces OS — long-term memory for developers. Search, create, and manage memory assets via the Pieces OS REST API.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/goddardenoven110907/cli-anything-pieces",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    python_requires=">=3.10",
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "cli-anything-pieces=cli_anything.pieces.pieces_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cli_anything.pieces": ["skills/*.md"],
    },
    zip_safe=False,
)
