#!/usr/bin/env python3
"""Validate storage analysis JSON before building or serving the report.

Usage:
    validate_analysis.py <analysis.json>

This script is intentionally conservative. It validates the report shape and
guards the most important safety contracts:
- green items must expose concrete trash_paths
- direct-delete candidates must remain under the user's home directory
- tier summary values should be parseable
"""
import json
import os
import re
import sys


SIZE_RE = re.compile(r"([\d.]+)\s*(TB|GB|MB)?", re.I)


def fail(msg):
    print(f"INVALID: {msg}")
    sys.exit(1)


def parse_size(value):
    if not value:
        return None
    m = SIZE_RE.search(str(value))
    if not m:
        return None
    n = float(m.group(1))
    unit = (m.group(2) or "GB").upper()
    if unit == "TB":
        n *= 1024
    elif unit == "MB":
        n /= 1024
    return n


def ensure_list(obj, field, label):
    value = obj.get(field)
    if value is None:
        return []
    if not isinstance(value, list):
        fail(f"{label}.{field} must be a list")
    return value


def ensure_text(obj, field, label, required=False):
    value = obj.get(field)
    if value in (None, ""):
        if required:
            fail(f"{label}.{field} is required")
        return ""
    if not isinstance(value, str):
        fail(f"{label}.{field} must be a string")
    return value


def validate_summary(data):
    summary = data.get("summary") or {}
    tier_stats = summary.get("tier_stats") or {}
    for key in ("green", "yellow", "red"):
        if key in tier_stats and parse_size(tier_stats[key]) is None:
            fail(f"summary.tier_stats.{key} must start with a parseable size")
    for key in ("priority", "cleanup_notes", "risk_factors", "long_term"):
        if key in summary and not isinstance(summary[key], list):
            fail(f"summary.{key} must be a list")


def validate_green(items, home):
    for idx, item in enumerate(items):
        label = f"green[{idx}]"
        ensure_text(item, "name", label, required=True)
        ensure_text(item, "path", label, required=True)
        ensure_text(item, "size_estimate", label, required=True)
        trash_paths = ensure_list(item, "trash_paths", label)
        if not trash_paths:
            fail(f"{label}.trash_paths must not be empty")
        for p in trash_paths:
            if not isinstance(p, str):
                fail(f"{label}.trash_paths must contain strings")
            rp = os.path.realpath(os.path.expanduser(p))
            if not (rp == home or rp.startswith(home + os.sep)):
                fail(f"{label}.trash_paths contains path outside home: {p}")
        for key in ("evidence", "kill_processes"):
            ensure_list(item, key, label)


def validate_yellow(items):
    for idx, item in enumerate(items):
        label = f"yellow[{idx}]"
        for field in ("name", "path", "size", "content_profile", "why_manual", "disposal", "risk"):
            ensure_text(item, field, label, required=True)
        for key in ("trash_paths", "evidence"):
            ensure_list(item, key, label)


def validate_red(items):
    for idx, item in enumerate(items):
        label = f"red[{idx}]"
        for field in ("name", "path", "why_keep", "indirect_release"):
            ensure_text(item, field, label, required=True)
        for key in ("app_paths", "evidence"):
            ensure_list(item, key, label)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)

    system = data.get("system") or {}
    home = os.path.realpath(os.path.expanduser(system.get("home") or "~"))
    if not system:
        fail("system section is required")

    validate_summary(data)
    validate_green(data.get("green") or [], home)
    validate_yellow(data.get("yellow") or [])
    validate_red(data.get("red") or [])
    print("VALID")


if __name__ == "__main__":
    main()
