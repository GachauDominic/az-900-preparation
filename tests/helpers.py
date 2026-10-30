import json
import shutil
from pathlib import Path

CONTENT = Path(__file__).resolve().parent.parent / "content"


def only_modules(tmp_path, keep: set[str]) -> Path:
    """Copy the content folder and mark every module not in `keep` as 'planned'."""
    dst = tmp_path / "content"
    shutil.copytree(CONTENT, dst)
    p = dst / "syllabus.json"
    s = json.loads(p.read_text("utf-8"))
    for m in s["modules"]:
        if m["id"] not in keep:
            m["status"] = "planned"
    p.write_text(json.dumps(s), "utf-8")
    return dst


def right_answer(q):
    """A fully correct answer in the shape grade_question expects."""
    if q["type"] == "yesno":
        return {o["id"]: o["id"] in q["correct"] for o in q["options"]}
    return list(q["correct"])
