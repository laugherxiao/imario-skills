#!/usr/bin/env python3
"""Check the eval scenarios are well formed and that every file they cite exists.

Usage: python evals/check_evals.py

Each eval is a JSON file with the shape Anthropic's skill authoring guide uses:
{"skills": [...], "query": "...", "files": [...], "expected_behavior": [...]}.
A scenario may add "negative": true to say the skill must NOT be used.
Exit code 1 means at least one eval is broken.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SKILLS = EVALS.parent / "skills"
REQUIRED = ("skills", "query", "files", "expected_behavior")


def check(path: Path) -> list[str]:
    problems: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path.name}: not valid JSON ({exc})"]
    for key in REQUIRED:
        if key not in data:
            problems.append(f"{path.name}: missing '{key}'")
    for skill in data.get("skills", []):
        if not (SKILLS / skill / "SKILL.md").is_file():
            problems.append(f"{path.name}: skill '{skill}' has no SKILL.md under skills/")
    for rel in data.get("files", []):
        if not (EVALS / rel).is_file():
            problems.append(f"{path.name}: cited file '{rel}' does not exist under evals/")
    if not data.get("query", "").strip():
        problems.append(f"{path.name}: empty query")
    if not data.get("expected_behavior"):
        problems.append(f"{path.name}: no expected_behavior")
    return problems


def main() -> int:
    files = sorted(EVALS.glob("*.json"))
    if len(files) < 3:
        print(f"only {len(files)} evals; the authoring guide asks for at least three")
        return 1
    problems = [p for f in files for p in check(f)]
    negatives = sum(1 for f in files if json.loads(f.read_text()).get("negative"))
    for p in problems:
        print(p)
    print(f"{len(files)} evals checked, {negatives} negative, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
