import json
from pathlib import Path

from werkzeug.datastructures import MultiDict

from services.content import ContentStore
from services.quiz import (build_exam, exam_plan, grade_attempt, grade_question, parse_answers,
                           prepare_for_display)
from services.sanitize import render_markdown

CONTENT = Path(__file__).resolve().parent.parent / "content"
store = ContentStore(CONTENT)
QS = store.module("M04")["questions"]
BY_ID = {q["id"]: q for q in QS}


def test_display_hides_answers_and_is_reproducible():
    a = prepare_for_display(QS, seed=7)
    b = prepare_for_display(QS, seed=7)
    c = prepare_for_display(QS, seed=8)
    assert a == b
    assert [q["id"] for q in a] != [q["id"] for q in c] or [q["options"] for q in a] != [q["options"] for q in c]
    blob = json.dumps(a)
    for secret in ("explanation", "why_wrong", "correct", "learn_more"):
        assert f'"{secret}"' not in blob
    assert sorted(q["id"] for q in a) == sorted(q["id"] for q in QS)


def test_grade_single_multi_yesno():
    assert grade_question(BY_ID["M04-Q01"], ["a"])["correct"]
    assert not grade_question(BY_ID["M04-Q01"], ["b"])["correct"]
    assert not grade_question(BY_ID["M04-Q01"], ["a", "b"])["correct"]
    assert grade_question(BY_ID["M04-Q06"], ["b", "a"])["correct"]
    assert not grade_question(BY_ID["M04-Q06"], ["a"])["correct"]
    assert grade_question(BY_ID["M04-Q08"], {"s1": False, "s2": True, "s3": True})["correct"]
    assert not grade_question(BY_ID["M04-Q08"], {"s1": True, "s2": True, "s3": True})["correct"]
    assert not grade_question(BY_ID["M04-Q08"], {"s2": True, "s3": True})["correct"]  # s1 unanswered
    unanswered = grade_question(BY_ID["M04-Q01"], [])
    assert not unanswered["correct"] and not unanswered["answered"]


def test_parse_answers_ignores_unknown_ids():
    form = MultiDict([("q_M04-Q01", "a"), ("q_M04-Q01", "zzz"), ("q_M04-Q08.s1", "no"),
                      ("q_M04-Q08.s2", "maybe"), ("q_M04-Q08.s9", "yes")])
    ans = parse_answers(form, [BY_ID["M04-Q01"], BY_ID["M04-Q08"]])
    assert ans["M04-Q01"] == ["a"]
    assert ans["M04-Q08"] == {"s1": False}


def test_grade_attempt_breakdown():
    answers = {q["id"]: (list(q["correct"]) if q["type"] != "yesno"
                         else {o["id"]: o["id"] in q["correct"] for o in q["options"]}) for q in QS}
    perfect = grade_attempt(QS, answers)
    assert perfect["percent"] == 100 and perfect["weak_objectives"] == []
    empty = grade_attempt(QS, {})
    assert empty["score"] == 0 and set(empty["weak_objectives"]) == {f"M04-O{i}" for i in range(1, 6)}
    assert empty["weak_modules"] == ["M04"]


def test_exam_plan_and_build():
    assert exam_plan(store, 40) == {"M04": len(QS)}   # capped by availability
    assert exam_plan(store, 5) == {"M04": 5}
    exam = build_exam(store, 5, seed=1)
    assert len(exam) == 5 and len({q["id"] for q in exam}) == 5
    assert [q["id"] for q in build_exam(store, 5, seed=1)] == [q["id"] for q in exam]


def test_sanitiser_removes_scripts_and_keeps_code():
    html, toc = render_markdown("# T\n\n## Sec\n\n<script>alert(1)</script><img src=x onerror=alert(1)>\n\n```bash\naz group create\n```\n")
    assert "<script" not in html and "onerror" not in html
    assert "az group create" in html and "<pre>" in html
    assert toc == [{"id": "sec", "name": "Sec"}]
