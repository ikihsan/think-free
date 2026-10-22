from setuptools import setup

setup(
    entry_points={
        "console_scripts": [
            "fedmarket = fedmarket.cli:main",
            "fedmarket-decide = fedmarket.decide_cli:main",
        ],
    },
)