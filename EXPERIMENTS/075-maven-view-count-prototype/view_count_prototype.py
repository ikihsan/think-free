#!/usr/bin/env python3
"""
E075: View-Count Prototype

A prototype CLI tool that implements the view-count principle across package
repositories (PyPI, NPM, Maven Central). The view-count principle observes
that packages with higher activity metadata (download/view counts, recent
releases) are systematically more "active" (actively maintained) than random
packages.

This is an exploratory prototype — not a product. It is designed to gather
evidence about the domain boundaries of the view-count principle.

Usage:
    python3 view_count_prototype.py pypi <package-name>
    python3 view_count_prototype.py npm <package-name>
    python3 view_count_prototype.py maven <groupId:artifactId>
"""

import argparse
import json
import math
import sys
import urllib.request
import xml.etree.ElementTree as ET


# === Normal helpers ===

def norm_cdf(x):
    """Standard normal CDF using math.erf."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def wilson_lower(count, n, confidence=0.95):
    """Wilson score interval lower bound."""
    if n == 0:
        return 0.0
    phat = count / n
    z = 1.96  # 95% CI
    return (phat + z * z / (2 * n) - z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n))) / (1 + z * z / n)


# === Platform APIs ===

PYPI_BASE = "https://pypi.org/pypi"
NPM_BASE = "https://registry.npmjs.org"
MAVEN_BASE = "https://repo1.maven.org/maven2"


def pypi_metadata(package_name):
    """Fetch metadata for a PyPI package."""
    url = f"{PYPI_BASE}/{package_name}/json"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = resp.read()
        return json.loads(data)
    except Exception as e:
        return {"error": str(e)}


def npm_metadata(package_name):
    """Fetch metadata for an NPM package."""
    url = f"{NPM_BASE}/{package_name}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = resp.read()
        return json.loads(data)
    except Exception as e:
        return {"error": str(e)}


def maven_metadata(group_artifact):
    """Fetch metadata for a Maven Central artifact (groupId:artifactId)."""
    try:
        group, artifact = group_artifact.split(":", 1)
    except ValueError:
        return {"error": "Invalid group:artifact format, expected GROUP:ARTIFACT"}
    path_group = group.replace(".", "/")
    url = f"{MAVEN_BASE}/{path_group}/{artifact}/maven-metadata.xml"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            xml_data = resp.read().decode('utf-8')
        root = ET.fromstring(xml_data)
        versioning = root.find('versioning')
        latest = versioning.find('latest').text if versioning is not None and versioning.find('latest') is not None else "unknown"
        version_list = versioning.find('versions') if versioning is not None else None
        version_count = len(version_list.findall('version')) if version_list is not None else 0
        last_updated = root.find('.//lastUpdated')
        last_updated_ts = last_updated.text if last_updated is not None else None
        last_updated_date = None
        if last_updated_ts:
            try:
                year = int(last_updated_ts[:4])
                month = int(last_updated_ts[4:6])
                day = int(last_updated_ts[6:8])
                last_updated_date = (year, month, day)
            except:
                pass
        desc = root.find('.//description')
        description = desc.text if desc is not None else ""
        return {
            "latest": latest,
            "version_count": version_count,
            "last_updated_date": last_updated_date,
            "description": description,
            "has_description": bool(description.strip())
        }
    except Exception as e:
        return {"error": str(e)}


# === Activity assessment ===

def assess_pypi(metadata):
    """Assess if a PyPI package is 'active' based on metadata."""
    if "error" in metadata:
        return {"active": False, "reason": "fetch_error", "data": metadata}
    try:
        dist_info = metadata.get("info", {})
        version = dist_info.get("version", "0.0.0")
        project_urls = dist_info.get("project_urls", {})
        has_homepage = any("homepage" in url.lower() for url in project_urls.values())
        is_prerelease = version.startswith(("a", "b", "rc"))
        activity_signals = sum([has_homepage, not is_prerelease])
        active = activity_signals >= 1
        reason_parts = []
        if has_homepage:
            reason_parts.append("has_homepage")
        if not is_prerelease:
            reason_parts.append("release_not_prerelease")
        return {
            "active": active,
            "reason": ", ".join(reason_parts) if reason_parts else "metadata_present",
            "data": {
                "version": version,
                "has_homepage": has_homepage,
                "is_prerelease": is_prerelease,
                "project_urls_count": len(project_urls)
            }
        }
    except Exception as e:
        return {"active": False, "reason": f"parse_error: {e}", "data": metadata}


def assess_npm(metadata):
    """Assess if an NPM package is 'active' based on metadata."""
    if "error" in metadata:
        return {"active": False, "reason": "fetch_error", "data": metadata}
    try:
        version = metadata.get("version", "0.0.0")
        time_data = metadata.get("time", {})
        has_time = bool(time_data)
        is_prerelease = version.startswith(("a", "b", "rc"))
        has_readme = bool(metadata.get("readme"))
        activity_signals = sum([has_time, not is_prerelease, has_readme])
        active = activity_signals >= 2
        reason_parts = []
        if has_time:
            reason_parts.append("has_time_metadata")
        if not is_prerelease:
            reason_parts.append("release_not_prerelease")
        if has_readme:
            reason_parts.append("has_readme")
        return {
            "active": active,
            "reason": ", ".join(reason_parts) if reason_parts else "metadata_present",
            "data": {
                "version": version,
                "has_time": has_time,
                "is_prerelease": is_prerelease,
                "has_readme": has_readme,
                "time_range": f"{min(time_data.keys())}-{max(time_data.keys())}" if time_data else "none"
            }
        }
    except Exception as e:
        return {"active": False, "reason": f"parse_error: {e}", "data": metadata}


def assess_maven(metadata):
    """Assess if a Maven Central artifact is 'active' based on metadata."""
    if "error" in metadata:
        return {"active": False, "reason": "fetch_error", "data": metadata}
    try:
        vc = metadata.get("version_count", 0)
        lu = metadata.get("last_updated_date")
        has_desc = metadata.get("has_description", False)
        recent_active = lu is not None and lu[0] >= 2024
        moderate_vc = vc >= 20
        active = recent_active or moderate_vc
        reason_parts = []
        if recent_active:
            reason_parts.append("recent_update")
        if moderate_vc:
            reason_parts.append(f"vc>={vc}")
        if not recent_active and not moderate_vc:
            reason_parts.append("low_activity")
        return {
            "active": active,
            "reason": ", ".join(reason_parts) if reason_parts else "unknown",
            "data": {
                "version_count": vc,
                "latest_version": metadata.get("latest"),
                "last_updated": metadata.get("last_updated_date"),
                "has_description": has_desc,
                "recent_active": recent_active,
                "moderate_vc": moderate_vc
            }
        }
    except Exception as e:
        return {"active": False, "reason": f"parse_error: {e}", "data": metadata}


# === CLI ===

def cmd_pypi(args):
    """Run view-count assessment for a PyPI package."""
    metadata = pypi_metadata(args.artifact)
    result = assess_pypi(metadata)
    downloads = None
    try:
        url = f"{PYPI_BASE}/pypi/{args.artifact}/statistics"
        with urllib.request.urlopen(url, timeout=10) as resp:
            stat_data = resp.read()
        downloads = "available_from_stat_api"
    except:
        downloads = None
    
    output = {
        "platform": "pypi",
        "package": args.artifact,
        "active": result["active"],
        "reason": result["reason"],
        "version": result["data"].get("version", "unknown"),
        "downloads": downloads,
        "project_urls_count": result["data"].get("project_urls_count", 0),
    }
    print(json.dumps(output, indent=2))


def cmd_npm(args):
    """Run view-count assessment for an NPM package."""
    metadata = npm_metadata(args.artifact)
    result = assess_npm(metadata)
    output = {
        "platform": "npm",
        "package": args.artifact,
        "active": result["active"],
        "reason": result["reason"],
        "version": result["data"].get("version", "unknown"),
        "has_readme": result["data"].get("has_readme", False),
        "has_time": result["data"].get("has_time", False),
    }
    print(json.dumps(output, indent=2))


def cmd_maven(args):
    """Run view-count assessment for a Maven Central artifact."""
    metadata = maven_metadata(args.artifact)
    result = assess_maven(metadata)
    output = {
        "platform": "maven",
        "artifact": args.artifact,
        "active": result["active"],
        "reason": result["reason"],
        "version_count": metadata.get("version_count", 0),
        "latest_version": metadata.get("latest"),
        "last_updated": metadata.get("last_updated_date"),
        "has_description": metadata.get("has_description", False),
    }
    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(description="View-Count Prototype - assess package activity across platforms")
    parser.add_argument("command", choices=["pypi", "npm", "maven"], help="Platform to assess")
    parser.add_argument("artifact", help="Package name (PyPI/NPM) or group:artifact (Maven)")
    
    args = parser.parse_args()
    
    if args.command == "pypi":
        cmd_pypi(args)
    elif args.command == "npm":
        cmd_npm(args)
    elif args.command == "maven":
        cmd_maven(args)


if __name__ == "__main__":
    main()