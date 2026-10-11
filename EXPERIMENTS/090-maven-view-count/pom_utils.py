#!/usr/bin/env python3
"""E090 helper: POM fetch, parse, classification, and activity detection for Maven Central."""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from collections import Counter


# ── Curated control items (for G2, waived in automated run) ──────────────

SEDED_CONTROLS = {
    "s1": "org.apache.commons:commons-lang3:3.12.0",  # served
    "s2": "org.codehaus.plexus:plexus-utils:3.6.0",    # served
    "u1": "net.sourceforge.bytecode:bytecode-utils:1.2.3",  # unserved-open-like
    "u2": "net.sourceforge.ssu:simple-utils:0.9.0",        # unserved-open-like
}


# ── POM fetch ──────────────────────────────────────────────────────────


def fetch_pom(group_id, artifact_id, version):
    """Fetch POM XML for a Maven artifact. Returns raw XML text or None."""
    url = f"https://repo1.maven.org/maven2/{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}.pom"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Think-Free-Mission-E090)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # artifact not found
        raise
    except URLError as e:
        print(f"URL error for {group_id}:{artifact_id}:{version}: {e}", file=sys.stderr)
        return None


# ── POM parse ──────────────────────────────────────────────────────────


def parse_pom(xml_text):
    """Parse POM XML and return a dict of key fields."""
    if xml_text is None:
        return None
    try:
        root = ET.fromstring(xml_text)
        ns = {"m": "http://maven.apache.org/POM/4.0.0"}
        name = root.findtext("m:name", "", ns) or ""
        packaging = root.findtext("m:packaging", "jar", ns)
        # Extract download count if present
        downloads_elem = root.find("m:downloads", ns)
        downloads = None
        if downloads_elem is not None:
            try:
                downloads = int(downloads_elem.text or "0")
            except ValueError:
                downloads = None
        # Count distinct historical versions visible in POM hierarchy
        version_count = 1  # the current version itself
        # Look for <parent> element
        parent = root.find("m:parent", ns)
        if parent is not None:
            parent_version = parent.findtext("m:version", "", ns)
            if parent_version and parent_version != "" and not parent_version.endswith("-SNAPSHOT"):
                version_count += 1
        # Look at <dependencyManagement> entries as a history proxy
        dep_mgmt = root.find("m:dependencyManagement", ns)
        if dep_mgmt is not None:
            version_count += len(dep_mgmt.findall("m:dependency", ns))
        # Check for developers section
        developers = root.find("m:developers", ns) is not None
        # Check for <issueManagement>
        issue_mgmt = root.find("m:issueManagement", ns) is not None
        return {
            "name": name,
            "packaging": packaging,
            "downloads": downloads,
            "version_count": version_count,
            "has_developers": developers,
            "has_issue_mgmt": issue_mgmt,
        }
    except ET.ParseError as e:
        print(f"XML parse error: {e}", file=sys.stderr)
        return None


# ── Classification ─────────────────────────────────────────────────────


def classify_need_related(artifact_id, name):
    """Classify a package as need-related based on artifactId/name tokens."""
    # Build token set from artifactId
    tokens = set(artifact_id.lower().replace("-", "_").split("_"))
    # Also add tokens from the package name
    if name:
        tokens.update(name.lower().split())
    # Need-related categories (heuristic keyword matching)
    need_keywords = {
        "parser", "parse", "read", "write", "io", "stream",
        "compress", "decompress", "zip", "gzip", "unzip", "tar",
        "date", "time", "calendar", "format", "period", "duration",
        "text", "string", "filter", "transform", "codec", "encode", "decode",
        "math", "numeric", "calc", "stat", "random", "probability",
        "file", "resource", "path",
        "util", "collection",
        "json", "xml", "pull", "stax", "dom4j", "owl",
        "h2", "database",
    }
    # Exclude generic terms
    excluded = {"core", "common", "base", "api", "framework", "simple", "platform",
                "junit", "mockito", "log4j", "slf4j", "logback"}
    relevant_matches = tokens.intersection(need_keywords) - excluded
    if len(relevant_matches) >= 1:
        return True  # need-related
    return False  # random


# ── Activity detection ─────────────────────────────────────────────────


def is_active(pom_data):
    """Determine if a package is 'active' based on POM metadata."""
    if pom_data is None:
        return False
    # Active if: downloads > 0 OR ≥2 visible versions OR has developers section
    if pom_data["downloads"] is not None and pom_data["downloads"] > 0:
        return True
    if pom_data["version_count"] >= 2:
        return True
    if pom_data["has_developers"]:
        return True
    return False