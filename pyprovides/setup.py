from setuptools import setup, find_packages

setup(
    name="pyprovides",
    version="0.1.0",
    description="which distribution provides this module, with nothing installed",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pyprovides = pyprovides.pyprovides_cli:main",
        ],
    },
)