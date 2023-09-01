# coding: utf-8
"""
Use the following command from a terminal window to generate the whl with source code
python setup.py bdist_wheel
"""

import re
from pathlib import Path

import setuptools

ROOT = Path(__file__).parent.absolute()
VERSION_FILE = ROOT / "baron" / "_version.py"


def parse_requirements(filename: str) -> list:
    """
    Load requirements (one per line) from a pip requirements.txt-like file
    """
    lineiter = (line.strip() for line in open(filename, encoding='utf-8'))
    return [line for line in lineiter if line and not line.startswith("#")]


def get_version(version_file: Path, vsre: str = r"^__version__ = ['\"]([^'\"]*)['\"]") -> str:
    """
    Retrieves the version from a given file (typically _version.py) given a pattern
    """
    verstrline = version_file.read_text()
    groups = re.search(vsre, verstrline, re.M)
    if groups:
        return groups.group(1)
    else:
        raise RuntimeError(f"Unable to find version string in {version_file}")


setup_args = dict(
    name="baron",
    version=get_version(version_file=VERSION_FILE),
    author="Matteo Giani",
    author_email="matteo.giani.87@gmail.com",
    description="Baron Duquesne",
    long_description=(ROOT / "Readme.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    packages=setuptools.find_namespace_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    # MG this utils package is a requirement for the addons.
    # However, we need to handle https authentication details with some logic
    # that cannot be expressed in plain-text requirements.txt.
    install_requires=parse_requirements(ROOT / "requirements.txt"),
    extras_require={
        "dev": parse_requirements(ROOT / "requirements-dev.txt"),
    },
    python_requires=">=3.8",
)

setuptools.setup(**setup_args)
