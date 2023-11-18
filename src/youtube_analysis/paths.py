"""Python module for finding useful paths"""

from pathlib import Path
import os

PARENT_DIR = Path(__file__).parent.resolve().parent.parent
DATA_DIR = PARENT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
TRANSFORMED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
INTERIM_DATA_DIR = DATA_DIR / "interim"

REPORTS_DIR = PARENT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

if not Path(DATA_DIR).exists():
    os.mkdir(DATA_DIR)

if not Path(RAW_DATA_DIR).exists():
    os.mkdir(RAW_DATA_DIR)

if not Path(TRANSFORMED_DATA_DIR).exists():
    os.mkdir(TRANSFORMED_DATA_DIR)

if not Path(REPORTS_DIR).exists():
    os.mkdir(REPORTS_DIR)

if not Path(FIGURES_DIR).exists():
    os.mkdir(FIGURES_DIR)
