import json
from pathlib import Path

from helpers import CONTENT, only_modules
from validate_content import validate


def test_shipped_content_has_no_errors():
    errors, _ = validate(CONTENT)
    assert errors == []


def test_all_modules_are_ready_with_enough_questions():
    syl = json.loads((CONTENT / "syllabus.json").read_text("utf-8"))
    assert len(syl["modules"]) == 13
    assert all(m["status"] == "ready" for m in syl["modules"])
    assert syl["meta"]["outline_verified"] is True
    for m in syl["modules"]:
        qs = json.loads((CONTENT / "modules" / f"{m['id']}-{m['slug']}" / "questions.json").read_text("utf-8"))
        assert len(qs) >= 12, m["id"]


def test_correct_answer_letters_are_not_predictable():
    """The option id is visible in the page source, so the right id must vary."""
    letters = set()
    for q_path in (CONTENT / "modules").glob("*/questions.json"):
        for q in json.loads(q_path.read_text("utf-8")):
            if q["type"] == "single":
                letters.add(q["correct"][0])
    assert len(letters) >= 3


def test_validator_catches_bad_questions(tmp_path):
    dst = only_modules(tmp_path, {"M04"})
    qp = dst / "modules" / "M04-core-architecture" / "questions.json"
    qs = json.loads(qp.read_text("utf-8"))
    qs[0]["correct"] = []
    qs[1]["objective_id"] = "M04-O99"
    qs[2]["options"][0]["text"] = "All of the above"
    qs[3]["explanation"] = ""
    qs[4]["learn_more"] = "https://example.com/x"
    qs[5]["id"] = qs[6]["id"]
    qp.write_text(json.dumps(qs), "utf-8")
    errors = "\n".join(validate(dst)[0])
    for needle in ("exactly one correct", "unknown objective_id", "all/none of the above",
                   "empty explanation", "learn.microsoft.com", "duplicate question id"):
        assert needle in errors


def test_validator_catches_missing_notes_sections(tmp_path):
    dst = only_modules(tmp_path, {"M04"})
    (dst / "modules" / "M04-core-architecture" / "notes.md").write_text("# Title\n\n## Key ideas\n\ntext\n", "utf-8")
    errors = "\n".join(validate(dst)[0])
    assert "missing section '## Exam tips'" in errors and "Last reviewed" in errors


def test_every_objective_has_questions_and_every_module_maps_to_a_learn_module():
    syl = json.loads((CONTENT / "syllabus.json").read_text("utf-8"))
    learn = set()
    for m in syl["modules"]:
        qs = json.loads((CONTENT / "modules" / f"{m['id']}-{m['slug']}" / "questions.json").read_text("utf-8"))
        used = {q["objective_id"] for q in qs}
        assert {o["id"] for o in m["objectives"]} <= used, m["id"]
        assert m["learn_module"]["url"].startswith("https://learn.microsoft.com/training/modules/")
        learn.add(m["learn_module"]["url"])
    assert len(learn) == 12      # the three Microsoft Learn paths contain 3 + 5 + 4 modules
    assert {d["learn_path"]["url"].split("/")[-2] for d in syl["domains"]} == {
        "microsoft-azure-fundamentals-describe-cloud-concepts",
        "azure-fundamentals-describe-azure-architecture-services",
        "describe-azure-management-governance"}
