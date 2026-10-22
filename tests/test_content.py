import json
import shutil
from pathlib import Path

from validate_content import validate

CONTENT = Path(__file__).resolve().parent.parent / "content"


def test_shipped_content_has_no_errors():
    errors, _ = validate(CONTENT)
    assert errors == []


def _copy(tmp_path):
    dst = tmp_path / "content"
    shutil.copytree(CONTENT, dst)
    return dst


def test_validator_catches_bad_questions(tmp_path):
    dst = _copy(tmp_path)
    qp = dst / "modules" / "M04-core-architecture" / "questions.json"
    qs = json.loads(qp.read_text("utf-8"))
    qs[0]["correct"] = []                       # single needs exactly one
    qs[1]["objective_id"] = "M04-O99"           # unknown objective
    qs[2]["options"][0]["text"] = "All of the above"
    qs[3]["explanation"] = ""
    qs[4]["learn_more"] = "https://example.com/x"
    qs[5]["id"] = qs[6]["id"]                   # duplicate id
    qp.write_text(json.dumps(qs), "utf-8")
    errors = "\n".join(validate(dst)[0])
    for needle in ("exactly one correct", "unknown objective_id", "all/none of the above",
                   "empty explanation", "learn.microsoft.com", "duplicate question id"):
        assert needle in errors


def test_validator_catches_missing_notes_sections(tmp_path):
    dst = _copy(tmp_path)
    np_ = dst / "modules" / "M04-core-architecture" / "notes.md"
    np_.write_text("# Title\n\n## Key ideas\n\ntext\n", "utf-8")
    errors = "\n".join(validate(dst)[0])
    assert "missing section '## Exam tips'" in errors
    assert "Last reviewed" in errors
