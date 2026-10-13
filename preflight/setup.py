from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("LICENSE", "r", encoding="utf-8") as fh:
    license_text = fh.read()

setup(
    name="preflight-eval",
    version="0.1.0",
    author="Think Free",
    author_email="",
    description="Three checks on the instrument that produces an evaluation rate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ikihsan/think-free",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "yaml": ["pyyaml>=6.0"],
    },
    entry_points={
        "console_scripts": [
            "preflight=preflight.__main__:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)