import os, sys
from pathlib import Path

# Adds root project directory to PYTHONPATH for all tests
project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root))