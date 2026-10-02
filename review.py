"""Offline review of direct Python requirements pins."""

from __future__ import annotations

import re

NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*(?:\[[A-Za-z0-9,._-]+\])?")
EXACT = re.compile(r"(?<![<>=!~])==(?!=)[^\s,;]+")


def review_text(text: str) -> list[dict[str, str]]:
    findings = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        location = f"line {number}"
        if line.startswith(("-r", "--requirement", "-c", "--constraint")):
            findings.append({"rule": "external-include", "location": location, "note": "Included requirements need a separate local review"})
            continue
        if line.startswith("-"):
            findings.append({"rule": "installer-option", "location": location, "note": "Installer option needs manual review"})
            continue
        if "://" in line or line.startswith(("git+", "./", "../")):
            findings.append({"rule": "direct-source", "location": location, "note": "Direct source or URL bypasses a simple package pin"})
            continue
        name = NAME.match(line)
        if not name:
            findings.append({"rule": "unparsed-line", "location": location, "note": "Requirement could not be interpreted"})
            continue
        remainder = line[name.end():].strip()
        if remainder.startswith(";"):
            remainder = ""
        if not EXACT.search(remainder):
            findings.append({"rule": "not-exactly-pinned", "location": location, "note": "Direct requirement lacks a single exact version"})
    return findings
