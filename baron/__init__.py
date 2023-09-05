"""
Global variables for the baron package.
"""

from pathlib import Path

ROOT = Path(__file__).parents[1].absolute()
DATA = ROOT / "data"
IMAGES = DATA / "images"
AUDIO = DATA / "audio"
TEMPLATES = DATA / 'templates'
