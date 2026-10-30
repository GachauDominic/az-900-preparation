"""Loads the syllabus, notes and questions from the content/ folder."""
import json
from pathlib import Path

from .sanitize import render_markdown


class ContentStore:
    def __init__(self, content_dir, require_reviewed: bool = False):
        self.dir = Path(content_dir)
        self.require_reviewed = require_reviewed
        self.syllabus = json.loads((self.dir / "syllabus.json").read_text("utf-8"))
        self._modules: dict[str, dict] = {}
        self._objectives: dict[str, str] = {}
        self._questions: dict[str, dict] = {}
        self._load()

    # -- loading ---------------------------------------------------------
    def _load(self):
        for m in self.syllabus["modules"]:
            folder = self.dir / "modules" / f"{m['id']}-{m['slug']}"
            notes_path, q_path = folder / "notes.md", folder / "questions.json"
            ready = m.get("status") == "ready" and notes_path.exists()
            questions = []
            if ready and q_path.exists():
                questions = json.loads(q_path.read_text("utf-8"))
                if self.require_reviewed:
                    questions = [q for q in questions if q.get("reviewed")]
            for o in m.get("objectives", []):
                self._objectives[o["id"]] = o["title"]
            notes_html, toc = ("", [])
            if ready:
                notes_html, toc = render_markdown(notes_path.read_text("utf-8"))
            module = {**m, "ready": ready, "questions": questions,
                      "has_quiz": bool(questions), "notes_html": notes_html, "toc": toc}
            self._modules[m["id"]] = module
            for q in questions:
                self._questions[q["id"]] = q

    # -- queries ---------------------------------------------------------
    @property
    def modules(self) -> list[dict]:
        return list(self._modules.values())

    def module(self, module_id: str):
        return self._modules.get(module_id)

    def domains(self) -> list[dict]:
        return [{**d, "modules": [m for m in self.modules if m["domain"] == d["id"]]}
                for d in self.syllabus["domains"]]

    def neighbor(self, module_id: str, step: int):
        """Next (step=1) or previous (step=-1) ready module in syllabus order, or None."""
        ids = [m["id"] for m in self.modules]
        if module_id not in ids:
            return None
        i = ids.index(module_id) + step
        while 0 <= i < len(ids):
            if self._modules[ids[i]]["ready"]:
                return self._modules[ids[i]]
            i += step
        return None

    def quiz_modules(self) -> list[dict]:
        return [m for m in self.modules if m["has_quiz"]]

    def question(self, question_id: str):
        return self._questions.get(question_id)

    def questions_by_ids(self, ids):
        return [self._questions[i] for i in ids if i in self._questions]

    def objective_title(self, objective_id: str) -> str:
        return self._objectives.get(objective_id, objective_id)

    def module_title(self, module_id: str) -> str:
        m = self._modules.get(module_id)
        return m["title"] if m else module_id

    @property
    def exam_settings(self) -> dict:
        return self.syllabus.get("exam_simulation", {"questions": 40, "minutes": 45, "pass_percent": 70})
