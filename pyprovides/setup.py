from setuptools import setup, find_packages

setup(
    name="pyprovides",
    version="0.1.0",
    description="which distribution provides this module, with nothing installed",
    packages=find_packages(),
    py_modules=["pyprovides_cli", "fix_import", "known_aliases", "core", "find"],
    entry_points={
        "console_scripts": [
            "pyprovides=pyprovides_cli:main",
        ],
    },
    python_requires=">=3.8",
)