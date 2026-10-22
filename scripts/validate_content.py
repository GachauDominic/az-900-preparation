#!/usr/bin/env python3
"""Validate the course content. Exit code 1 if any error is found.

    python scripts/validate_content.py [content_dir]
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

MIN_QUESTIONS = 12
REQUIRED_SECTIONS = ["What you will learn", "Key ideas", "How it looks in real life",
                     "Compare and contrast", "Exam tips", "Quick recap", "Go deeper"]
TYPES = {"single", "multi", "yesno"}
DIFFICULTIES = {"easy", "medium", "hard"}
BANNED = ("all of the above", "none of the above")
FIELDS = ["id", "module", "objective_id", "type", "difficulty", "prompt", "options",
          "correct", "explanation", "why_wrong", "learn_more", "reviewed"]


def validate(content_dir) -> tuple[list[str], list[str]]:
    root = Path(content_dir)
    errors: list[str] = []
    warnings: list[str] = []
    try:
        syl = json.loads((root / "syllabus.json").read_text("utf-8"))
    except Exception as e:  # noqa: BLE001
        return [f"syllabus.json: cannot read ({e})"], []

    if not syl.get("meta", {}).get("outline_verified"):
        warnings.append("syllabus.json: outline_verified is false; reconcile with the official AZ-900 outline.")
    domain_ids = {d["id"] for d in syl.get("domains", [])}
    seen_modules, seen_questions, unreviewed, planned = set(), set(), 0, 0

    for m in syl.get("modules", []):
        mid = m.get("id", "?")
        if mid in seen_modules:
            errors.append(f"{mid}: duplicate module id")
        seen_modules.add(mid)
        if m.get("domain") not in domain_ids:
            errors.append(f"{mid}: unknown domain {m.get('domain')!r}")
        if m.get("status") != "ready":
            planned += 1
            continue

        folder = root / "modules" / f"{mid}-{m['slug']}"
        objectives = {o["id"] for o in m.get("objectives", [])}
        if not objectives:
            errors.append(f"{mid}: ready module has no objectives")

        # ---- notes -----------------------------------------------------
        notes_path = folder / "notes.md"
        if not notes_path.exists():
            errors.append(f"{mid}: notes.md missing")
        else:
            notes = notes_path.read_text("utf-8")
            for sec in REQUIRED_SECTIONS:
                if not re.search(rf"^##\s+{re.escape(sec)}\s*$", notes, re.M):
                    errors.append(f"{mid}: notes.md missing section '## {sec}'")
            if not re.search(r"^Last reviewed:\s*\d{4}-\d{2}-\d{2}\s*$", notes, re.M):
                errors.append(f"{mid}: notes.md missing 'Last reviewed: YYYY-MM-DD' line")
            for url in re.findall(r"\]\((https?://[^)\s]+)\)", notes):
                if urlparse(url).hostname != "learn.microsoft.com":
                    errors.append(f"{mid}: notes link not on learn.microsoft.com: {url}")

        # ---- questions ---------------------------------------------------
        q_path = folder / "questions.json"
        if not q_path.exists():
            errors.append(f"{mid}: questions.json missing")
            continue
        try:
            questions = json.loads(q_path.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            errors.append(f"{mid}: questions.json is not valid JSON ({e})")
            continue
        if len(questions) < MIN_QUESTIONS:
            errors.append(f"{mid}: only {len(questions)} questions (minimum {MIN_QUESTIONS})")

        for q in questions:
            qid = q.get("id", "?")
            where = f"{mid}/{qid}"
            for f in FIELDS:
                if f not in q:
                    errors.append(f"{where}: missing field '{f}'")
            if qid in seen_questions:
                errors.append(f"{where}: duplicate question id")
            seen_questions.add(qid)
            if not str(qid).startswith(f"{mid}-"):
                errors.append(f"{where}: id must start with '{mid}-'")
            if q.get("module") != mid:
                errors.append(f"{where}: module field is {q.get('module')!r}")
            if q.get("objective_id") not in objectives:
                errors.append(f"{where}: unknown objective_id {q.get('objective_id')!r}")
            if q.get("type") not in TYPES:
                errors.append(f"{where}: type must be one of {sorted(TYPES)}")
                continue
            if q.get("difficulty") not in DIFFICULTIES:
                errors.append(f"{where}: difficulty must be one of {sorted(DIFFICULTIES)}")
            if not str(q.get("prompt", "")).strip():
                errors.append(f"{where}: empty prompt")
            if not str(q.get("explanation", "")).strip():
                errors.append(f"{where}: empty explanation")
            if not q.get("reviewed"):
                unreviewed += 1

            options = q.get("options", [])
            ids = [o.get("id") for o in options]
            if len(set(ids)) != len(ids):
                errors.append(f"{where}: duplicate option ids")
            correct = q.get("correct", [])
            if not set(correct) <= set(ids):
                errors.append(f"{where}: 'correct' contains ids that are not options")
            for o in options:
                text = str(o.get("text", "")).lower()
                if not text.strip():
                    errors.append(f"{where}: option {o.get('id')} has empty text")
                if any(b in text for b in BANNED):
                    errors.append(f"{where}: option {o.get('id')} uses 'all/none of the above'")

            if q["type"] == "single":
                if len(options) < 4:
                    errors.append(f"{where}: single-answer questions need at least 4 options")
                if len(correct) != 1:
                    errors.append(f"{where}: single-answer question needs exactly one correct id")
            elif q["type"] == "multi":
                if len(options) < 4:
                    errors.append(f"{where}: multi-select questions need at least 4 options")
                if len(correct) < 2:
                    errors.append(f"{where}: multi-select question needs at least two correct ids")
            else:  # yesno
                if len(options) < 2:
                    errors.append(f"{where}: yes/no items need at least 2 statements")

            why = q.get("why_wrong", {})
            needed = ids if q["type"] == "yesno" else [i for i in ids if i not in correct]
            for i in needed:
                if not str(why.get(i, "")).strip():
                    errors.append(f"{where}: why_wrong missing for option {i}")
            link = q.get("learn_more", "")
            if not link or urlparse(link).hostname != "learn.microsoft.com":
                errors.append(f"{where}: learn_more must be a learn.microsoft.com URL")

    if planned:
        warnings.append(f"{planned} module(s) are still 'planned' (no notes or questions yet).")
    if unreviewed:
        warnings.append(f"{unreviewed} question(s) are not yet marked reviewed:true "
                        "(they are hidden when REQUIRE_REVIEWED=1).")
    return errors, warnings


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent / "content"
    errors, warnings = validate(root)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error:   {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
