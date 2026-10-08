#!/usr/bin/env python3
"""
Environment specification classifiers for E067.

Pure functions for assessing Dockerfile, conda, pip, pyproject.toml, and README
content for pinned version specifications. No external dependencies.
"""

import re
from typing import Tuple


def assess_dockerfile(content: str) -> Tuple[bool, float]:
    """Assess a Dockerfile for pinned base image and dependencies.

    Returns:
        (has_pinned_base, pinned_fraction)
    """
    lines = content.split('\n')
    has_pinned_base = False
    pinned_deps = 0
    total_deps = 0

    for line in lines:
        line = line.strip()
        # Check FROM line
        if line.upper().startswith('FROM '):
            # Check if base image has a tag (not latest, not bare)
            parts = line.split()
            if len(parts) >= 2:
                image = parts[1]
                if ':' in image and not image.endswith(':latest'):
                    has_pinned_base = True
        # Check RUN pip install / apt-get install / apk add
        # Extract package specifications after the install command
        install_match = re.search(r'(?:pip|apt-get|apk)\s+install\s+(.+)', line)
        if install_match:
            packages = install_match.group(1)
            # Split by whitespace, filter out flags starting with -
            pkgs = [p for p in packages.split() if not p.startswith('-')]
            for pkg in pkgs:
                total_deps += 1
                if '==' in pkg or re.match(r'^[\w\-]+=\d', pkg):
                    pinned_deps += 1

    pinned_frac = pinned_deps / max(total_deps, 1)
    return has_pinned_base, pinned_frac


def assess_conda_env(content: str) -> float:
    """Assess conda environment.yml for pinned versions.

    Returns pinned fraction (0.0 to 1.0).
    """
    lines = content.split('\n')
    in_deps = False
    pinned = 0
    total = 0

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('dependencies:'):
            in_deps = True
            continue
        if in_deps and stripped.startswith('-'):
            dep = stripped[1:].strip()
            if dep and not dep.startswith('#'):
                total += 1
                # Check for version pinning (contains = followed by version)
                if re.search(r'=\d', dep) or '==' in dep:
                    pinned += 1
        elif in_deps and stripped and not stripped.startswith('-') and not stripped.startswith('#'):
            # End of dependencies section
            break

    return pinned / max(total, 1)


def assess_pip_requirements(content: str) -> float:
    """Assess requirements.txt for pinned versions.

    Returns pinned fraction (0.0 to 1.0).
    """
    lines = content.split('\n')
    pinned = 0
    total = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        # Skip editable installs, URLs, etc.
        if line.startswith('-e ') or line.startswith('http'):
            continue
        # Check for version specifier
        total += 1
        if '==' in line:
            pinned += 1
        elif re.match(r'^[a-zA-Z0-9_\-]+$', line):
            # Bare package name - unpinned
            pass

    return pinned / max(total, 1)


def assess_pyproject_toml(content: str) -> float:
    """Assess pyproject.toml for pinned dependencies.

    Returns pinned fraction (0.0 to 1.0).
    """
    pinned = 0
    total = 0

    # Find [project] or [tool.poetry.dependencies] sections
    in_deps = False
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('[') and ('dependencies' in line or 'project' in line):
            in_deps = True
            continue
        if line.startswith('[') and in_deps:
            in_deps = False
            continue
        if in_deps and '=' in line and not line.startswith('#'):
            total += 1
            # Check for pinned version
            if '==' in line or re.search(r'"[^"]*==', line) or re.search(r"'[^']*==", line):
                pinned += 1
            elif re.search(r'[>=<~^]', line):
                # Has version specifier but not pinned
                pass

    return pinned / max(total, 1)


def assess_readme(content: str) -> bool:
    """Check if README has installation instructions.

    Returns True if install-related keywords found.
    """
    content_lower = content.lower()
    keywords = ['install', 'setup', 'requirements', 'dependenc', 'conda', 'docker', 'pip install', 'poetry install', 'uv sync']
    return any(kw in content_lower for kw in keywords)


def classify_arm(env_type: str, pinned_score: float) -> str:
    """Classify environment spec into experiment arm.

    Args:
        env_type: One of 'docker', 'conda', 'pip', 'docker_partial', 'conda_partial',
                  'pip_partial', 'lockfile_only', 'readme', 'none'
        pinned_score: Fraction of dependencies pinned (0.0 to 1.0)

    Returns:
        Arm label: 'A1', 'A2', 'A3', 'A4'
    """
    if env_type in ('docker', 'conda', 'pip'):
        return 'A1'  # machine-runnable
    elif env_type in ('docker_partial', 'conda_partial', 'pip_partial', 'lockfile_only'):
        return 'A2'  # partial
    elif env_type == 'readme':
        return 'A3'  # documentation only
    else:
        return 'A4'  # no environment info