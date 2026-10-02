"""Offline review of direct Python requirements using the packaging grammar."""
from __future__ import annotations
import re
from packaging.requirements import InvalidRequirement, Requirement

HASH = re.compile(r"\s+--hash(?:=|\s+)([^\s]+)")


def _lines(text):
    pending = ""
    start = 0
    for number, raw in enumerate(text.splitlines(), 1):
        line = re.split(r"\s+#", raw, maxsplit=1)[0].strip()
        if not line or line.startswith("#"):
            continue
        if not pending:
            start = number
        continued = line.endswith("\\")
        pending += (" " if pending else "") + (line[:-1].rstrip() if continued else line)
        if not continued:
            yield start, pending
            pending = ""
    if pending:
        raise ValueError("unfinished requirements continuation")


def review_text(text: str) -> list[dict[str, str]]:
    findings = []
    for number, line in _lines(text):
        location = f"line {number}"
        def add(rule, note):
            findings.append({"rule": rule, "location": location, "note": note})
        if line.startswith(("-r", "--requirement", "-c", "--constraint")):
            add("external-include", "Included requirements need a separate local review")
            continue
        if line.startswith("-"):
            add("installer-option", "Installer option needs manual review")
            continue
        if "://" in line or line.startswith(("git+", "./", "../", "/")):
            add("direct-source", "Direct source or URL bypasses a simple package pin")
            continue
        hashes = HASH.findall(line)
        if any(not re.fullmatch(r"(?:sha256:[0-9a-fA-F]{64}|sha384:[0-9a-fA-F]{96}|sha512:[0-9a-fA-F]{128})", value) for value in hashes):
            add("invalid-hash-option", "A hash declaration needs syntax review")
        requirement_line = HASH.sub("", line)
        try:
            requirement = Requirement(requirement_line)
        except InvalidRequirement:
            add("unparsed-line", "Requirement could not be interpreted")
            continue
        if requirement.url is not None:
            add("direct-source", "Direct source bypasses a simple package pin")
            continue
        specifiers = list(requirement.specifier)
        if len(specifiers) != 1 or specifiers[0].operator != "==" or "*" in specifiers[0].version:
            add("not-exactly-pinned", "Direct requirement lacks one exact non-wildcard version")
    return findings
