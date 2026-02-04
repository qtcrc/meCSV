import subprocess
import sys


def test_program_require_params_negative():
    result = subprocess.run(
        [sys.executable, "main.py"],
        capture_output=True,
        text=True
    )

    assert result.returncode != 0


def test_program_require_params_positive():
    result = subprocess.run(
        [sys.executable, "main.py",
         "-f", "./data/economic1.csv", "-r", "average-gdp"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0


def test_program_require_valid_files():
    result = subprocess.run(
        [sys.executable, "main.py",
         "-f", "invalid-path", "-r", "average-gdp"],
        capture_output=True,
        text=True
    )

    assert result.returncode != 0
