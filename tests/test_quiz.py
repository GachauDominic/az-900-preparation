import json

from werkzeug.datastructures import MultiDict

from helpers import CONTENT, only_modules, right_answer
from services.content import ContentStore
from services.quiz import (build_exam, exam_plan, grade_attempt, grade_question, parse_answers,
                           prepare_for_display)
from services.sanitize import render_markdown

store = ContentStore(CONTENT)
QS = store.module("M04")["questions"]
first = lambda t: next(q for q in QS if q["type"] == t)


def test_display_hides_answers_and_is_reproducible():
    a, b, c = (prepare_for_display(QS, s) for s in (7, 7, 8))
    assert a == b and a != c
    blob = json.dumps(a)
    for secret in ("explanation", "why_wrong", "correct", "learn_more"):
        assert f'"{secret}"' not in blob
    assert sorted(q["id"] for q in a) == sorted(q["id"] for q in QS)


def test_grade_single_multi_yesno():
    s, m, y = first("single"), first("multi"), first("yesno")
    wrong = next(o["id"] for o in s["options"] if o["id"] not in s["correct"])
    assert grade_question(s, right_answer(s))["correct"]
    assert not grade_question(s, [wrong])["correct"]
    assert not grade_question(s, [*s["correct"], wrong])["correct"]
    assert grade_question(m, list(reversed(right_answer(m))))["correct"]
    assert not grade_question(m, right_answer(m)[:1])["correct"]
    ans = right_answer(y)
    assert grade_question(y, ans)["correct"]
    flipped = dict(ans); k = next(iter(flipped)); flipped[k] = not flipped[k]
    assert not grade_question(y, flipped)["correct"]
    partial = dict(ans); partial.pop(k)
    assert not grade_question(y, partial)["correct"]
    empty = grade_question(s, [])
    assert not empty["correct"] and not empty["answered"]


def test_parse_answers_ignores_unknown_ids():
    s, y = first("single"), first("yesno")
    good = s["options"][0]["id"]; sid = y["options"][0]["id"]
    form = MultiDict([(f"q_{s['id']}", good), (f"q_{s['id']}", "zzz"), (f"q_{y['id']}.{sid}", "no"),
                      (f"q_{y['id']}.{y['options'][1]['id']}", "maybe"), (f"q_{y['id']}.s9", "yes")])
    ans = parse_answers(form, [s, y])
    assert ans[s["id"]] == [good] and ans[y["id"]] == {sid: False}


def test_grade_attempt_breakdown():
    perfect = grade_attempt(QS, {q["id"]: right_answer(q) for q in QS})
    assert perfect["percent"] == 100 and perfect["weak_objectives"] == []
    empty = grade_attempt(QS, {})
    assert empty["score"] == 0 and set(empty["weak_objectives"]) == {q["objective_id"] for q in QS}
    assert empty["weak_modules"] == ["M04"]


def test_exam_plan_covers_all_modules_and_follows_weights():
    plan = exam_plan(store, 40)
    assert sum(plan.values()) == 40 and set(plan) == {m["id"] for m in store.modules}
    assert all(0 < n <= len(store.module(k)["questions"]) for k, n in plan.items())
    dom = {d["id"]: sum(plan[m["id"]] for m in d["modules"]) for d in store.domains()}
    assert dom["D2"] > dom["D3"] > dom["D1"]            # 37.5 > 32.5 > 27.5
    assert sum(exam_plan(store, 5).values()) == 5


def test_exam_build_and_single_module_fallback(tmp_path):
    exam = build_exam(store, 40, seed=1)
    assert len(exam) == 40 and len({q["id"] for q in exam}) == 40
    assert [q["id"] for q in build_exam(store, 40, seed=1)] == [q["id"] for q in exam]
    one = ContentStore(only_modules(tmp_path, {"M04"}))
    assert exam_plan(one, 40) == {"M04": len(QS)}


def test_neighbors(tmp_path):
    assert store.neighbor("M04", 1)["id"] == "M05" and store.neighbor("M04", -1)["id"] == "M03"
    assert store.neighbor("M13", 1) is None and store.neighbor("M01", -1) is None
    sparse = ContentStore(only_modules(tmp_path, {"M04", "M07"}))
    assert sparse.neighbor("M04", 1)["id"] == "M07"


def test_sanitiser_removes_scripts_and_keeps_code():
    html, toc = render_markdown("# T\n\n## Sec\n\n<script>alert(1)</script><img src=x onerror=alert(1)>\n\n```bash\naz group create\n```\n")
    assert "<script" not in html and "onerror" not in html
    assert "az group create" in html and "<pre>" in html
    assert toc == [{"id": "sec", "name": "Sec"}]
