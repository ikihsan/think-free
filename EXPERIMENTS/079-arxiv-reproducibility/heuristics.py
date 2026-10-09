#!/usr/bin/env python3
"""
Version heuristics and import-to-package mappings for E079.
"""

# Known version ranges by year (heuristic)
# Format: package -> {year: (min_version, max_version)}
VERSION_HEURISTICS = {
    "numpy": {
        2020: ("1.18.0", "1.19.5"),
        2021: ("1.20.0", "1.21.6"),
        2022: ("1.22.0", "1.23.5"),
        2023: ("1.24.0", "1.26.4"),
        2024: ("1.26.0", "1.26.4"),
    },
    "pandas": {
        2020: ("1.1.0", "1.2.5"),
        2021: ("1.3.0", "1.3.5"),
        2022: ("1.4.0", "1.5.3"),
        2023: ("2.0.0", "2.1.4"),
        2024: ("2.1.0", "2.2.2"),
    },
    "torch": {
        2020: ("1.6.0", "1.7.1"),
        2021: ("1.8.0", "1.10.2"),
        2022: ("1.11.0", "1.13.1"),
        2023: ("2.0.0", "2.1.2"),
        2024: ("2.2.0", "2.3.1"),
    },
    "tensorflow": {
        2020: ("2.3.0", "2.4.1"),
        2021: ("2.5.0", "2.7.0"),
        2022: ("2.8.0", "2.10.1"),
        2023: ("2.11.0", "2.14.0"),
        2024: ("2.15.0", "2.16.1"),
    },
    "scikit-learn": {
        2020: ("0.23.0", "0.24.2"),
        2021: ("0.24.0", "1.0.2"),
        2022: ("1.1.0", "1.2.2"),
        2023: ("1.3.0", "1.3.2"),
        2024: ("1.4.0", "1.5.0"),
    },
    "scipy": {
        2020: ("1.5.0", "1.5.4"),
        2021: ("1.6.0", "1.7.3"),
        2022: ("1.8.0", "1.9.3"),
        2023: ("1.10.0", "1.11.4"),
        2024: ("1.11.0", "1.13.0"),
    },
}


# Common import-to-package mappings
IMPORT_TO_PACKAGE = {
    "cv2": "opencv-python",
    "PIL": "pillow",
    "sklearn": "scikit-learn",
    "yaml": "pyyaml",
    "dateutil": "python-dateutil",
    "jwt": "pyjwt",
    "requests": "requests",
    "numpy": "numpy",
    "pandas": "pandas",
    "torch": "torch",
    "tensorflow": "tensorflow",
    "scipy": "scipy",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "plotly": "plotly",
    "jax": "jax",
    "flax": "flax",
    "haiku": "dm-haiku",
    "einops": "einops",
    "hydra": "hydra-core",
    "omegaconf": "omegaconf",
    "wandb": "wandb",
    "tqdm": "tqdm",
}


def get_version_range(package: str, year: int):
    """Get heuristic version range for package in given year."""
    if package in VERSION_HEURISTICS and year in VERSION_HEURISTICS[package]:
        return VERSION_HEURISTICS[package][year]
    # Default: last 2 years before paper
    return ("0", "999")


def map_import_to_package(import_name: str) -> str:
    """Map import name to PyPI package name."""
    return IMPORT_TO_PACKAGE.get(import_name, import_name)