#!/usr/bin/env python3
"""
Unit tests for E067 environment specification classifiers.
Tests that the assessment logic returns known values for synthetic fixtures.
"""

import unittest
import tempfile
import os
import sys

# Add the experiment directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from classifier import (
    assess_dockerfile,
    assess_conda_env,
    assess_pip_requirements,
    assess_pyproject_toml,
    assess_readme,
    classify_arm,
)
from dataclasses import dataclass


class TestDockerfileAssessment(unittest.TestCase):
    def test_pinned_base_and_deps(self):
        content = """FROM python:3.10-slim
RUN pip install numpy==1.24.0 pandas==2.0.0
RUN apt-get update && apt-get install -y git=1:2.39.0"""
        has_base, pinned = assess_dockerfile(content)
        self.assertTrue(has_base)
        self.assertGreater(pinned, 0.5)

    def test_unpinned_base(self):
        content = """FROM python:latest
RUN pip install numpy pandas"""
        has_base, pinned = assess_dockerfile(content)
        self.assertFalse(has_base)
        self.assertEqual(pinned, 0.0)

    def test_no_base_tag(self):
        content = """FROM python
RUN pip install numpy==1.24.0"""
        has_base, pinned = assess_dockerfile(content)
        self.assertFalse(has_base)  # No tag at all
        self.assertGreater(pinned, 0)

    def test_partial_pinning(self):
        content = """FROM python:3.10
RUN pip install numpy==1.24.0 pandas requests"""
        has_base, pinned = assess_dockerfile(content)
        self.assertTrue(has_base)
        self.assertAlmostEqual(pinned, 1/3, places=1)  # 1 of 3 pinned


class TestCondaEnvAssessment(unittest.TestCase):
    def test_fully_pinned(self):
        content = """name: test
dependencies:
  - python=3.10.12
  - numpy=1.24.0
  - pandas=2.0.0
  - pytorch=2.0.1"""
        pinned = assess_conda_env(content)
        self.assertEqual(pinned, 1.0)

    def test_partially_pinned(self):
        content = """dependencies:
  - python=3.10
  - numpy
  - pandas=2.0"""
        pinned = assess_conda_env(content)
        self.assertAlmostEqual(pinned, 2/3, places=1)

    def test_unpinned(self):
        content = """dependencies:
  - python
  - numpy
  - pandas"""
        pinned = assess_conda_env(content)
        self.assertEqual(pinned, 0.0)


class TestPipRequirementsAssessment(unittest.TestCase):
    def test_fully_pinned(self):
        content = """numpy==1.24.0
pandas==2.0.0
requests==2.31.0"""
        pinned = assess_pip_requirements(content)
        self.assertEqual(pinned, 1.0)

    def test_partially_pinned(self):
        content = """numpy==1.24.0
pandas>=2.0
requests
flask~=2.3"""
        pinned = assess_pip_requirements(content)
        self.assertAlmostEqual(pinned, 0.25, places=1)  # 1 of 4 pinned

    def test_all_unpinned(self):
        content = """numpy
pandas
requests"""
        pinned = assess_pip_requirements(content)
        self.assertEqual(pinned, 0.0)

    def test_with_comments_and_empty(self):
        content = """# This is a comment
numpy==1.24.0

pandas>=2.0
# Another comment
requests==2.31.0"""
        pinned = assess_pip_requirements(content)
        self.assertAlmostEqual(pinned, 2/3, places=1)


class TestPyprojectTomlAssessment(unittest.TestCase):
    def test_pinned_deps(self):
        content = """[project]
dependencies = [
    "numpy==1.24.0",
    "pandas==2.0.0",
]
"""
        pinned = assess_pyproject_toml(content)
        self.assertGreater(pinned, 0.5)

    def test_unpinned_deps(self):
        content = """[tool.poetry.dependencies]
numpy = "^1.24"
pandas = ">=2.0"
"""
        pinned = assess_pyproject_toml(content)
        self.assertEqual(pinned, 0.0)


class TestReadmeAssessment(unittest.TestCase):
    def test_has_install_instructions(self):
        content = """# My Project
## Installation
```bash
pip install -r requirements.txt
```
Or use conda:
```bash
conda env create -f environment.yml
```"""
        self.assertTrue(assess_readme(content))

    def test_no_install_instructions(self):
        content = """# My Project
This is a cool project that does things."""
        self.assertFalse(assess_readme(content))

    def test_docker_instructions(self):
        content = """## Quickstart
```bash
docker build -t myapp .
docker run myapp
```"""
        self.assertTrue(assess_readme(content))


class TestArmClassification(unittest.TestCase):
    def test_A1_docker(self):
        self.assertEqual(classify_arm('docker', 0.8), 'A1')

    def test_A1_conda(self):
        self.assertEqual(classify_arm('conda', 0.9), 'A1')

    def test_A1_pip(self):
        self.assertEqual(classify_arm('pip', 1.0), 'A1')

    def test_A2_docker_partial(self):
        self.assertEqual(classify_arm('docker_partial', 0.3), 'A2')

    def test_A2_conda_partial(self):
        self.assertEqual(classify_arm('conda_partial', 0.4), 'A2')

    def test_A2_pip_partial(self):
        self.assertEqual(classify_arm('pip_partial', 0.2), 'A2')

    def test_A2_lockfile(self):
        self.assertEqual(classify_arm('lockfile_only', 0.5), 'A2')

    def test_A3_readme(self):
        self.assertEqual(classify_arm('readme', 0.0), 'A3')

    def test_A4_none(self):
        self.assertEqual(classify_arm('none', 0.0), 'A4')

    def test_A4_error(self):
        self.assertEqual(classify_arm('none', 0.0), 'A4')


if __name__ == '__main__':
    unittest.main()