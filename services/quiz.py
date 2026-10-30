"""Quiz logic: display preparation, deterministic grading, exam sampling.

The LLM is not involved anywhere: grading compares learner answers with the
`correct` ids stored in questions.json.
"""
import random

WEAK_PERCENT = 70
PRIVATE_FIELDS = {"correct", "explanation", "why_wrong", "learn_more", "difficulty", "objective_id"}


def prepare_for_display(questions: list[dict], seed: int) -> list[dict]:
    """Shuffle questions and options (reproducibly from `seed`) and strip answers."""
    rng = random.Random(f"{seed}:order")
    ordered = list(questions)
    rng.shuffle(ordered)
    shown = []
    for q in ordered:
        opts = list(q["options"])
        random.Random(f"{seed}:{q['id']}").shuffle(opts)
        item = {k: v for k, v in q.items() if k not in PRIVATE_FIELDS}
        item["options"] = opts
        shown.append(item)
    return shown


def parse_answers(form, questions: list[dict]) -> dict:
    """Turn submitted form data into {question_id: answer}.
    single/multi -> list of option ids; yesno -> {option_id: bool}.
    Only ids that belong to the question are kept."""
    answers = {}
    for q in questions:
        valid = {o["id"] for o in q["options"]}
        if q["type"] == "yesno":
            given = {}
            for oid in valid:
                v = form.get(f"q_{q['id']}.{oid}")
                if v in ("yes", "no"):
                    given[oid] = v == "yes"
            answers[q["id"]] = given
        else:
            answers[q["id"]] = [v for v in form.getlist(f"q_{q['id']}") if v in valid]
    return answers


def grade_question(q: dict, answer) -> dict:
    correct_ids = set(q["correct"])
    rows = []
    if q["type"] == "yesno":
        answer = answer or {}
        ok = all(o["id"] in answer and answer[o["id"]] == (o["id"] in correct_ids) for o in q["options"])
        answered = bool(answer)
        for o in q["options"]:
            expected = o["id"] in correct_ids
            given = answer.get(o["id"])
            rows.append({"id": o["id"], "text": o["text"], "expected": "Yes" if expected else "No",
                         "given": None if given is None else ("Yes" if given else "No"),
                         "ok": given is not None and given == expected,
                         "note": q.get("why_wrong", {}).get(o["id"], "")})
    else:
        selected = set(answer or [])
        ok = selected == correct_ids
        answered = bool(selected)
        for o in q["options"]:
            rows.append({"id": o["id"], "text": o["text"], "is_correct": o["id"] in correct_ids,
                         "selected": o["id"] in selected,
                         "note": q.get("why_wrong", {}).get(o["id"], "")})
    return {"id": q["id"], "module": q["module"], "type": q["type"], "prompt": q["prompt"],
            "objective_id": q["objective_id"], "correct": ok, "answered": answered, "rows": rows,
            "explanation": q["explanation"], "learn_more": q.get("learn_more", "")}


def _bucket(results, key):
    buckets: dict[str, dict] = {}
    for r in results:
        b = buckets.setdefault(r[key], {"correct": 0, "total": 0})
        b["total"] += 1
        b["correct"] += int(r["correct"])
    for b in buckets.values():
        b["percent"] = round(100 * b["correct"] / b["total"])
    return buckets


def grade_attempt(questions: list[dict], answers: dict) -> dict:
    results = [grade_question(q, answers.get(q["id"])) for q in questions]
    score = sum(r["correct"] for r in results)
    total = len(results)
    by_objective = _bucket(results, "objective_id")
    by_module = _bucket(results, "module")
    return {
        "results": results, "score": score, "total": total,
        "percent": round(100 * score / total) if total else 0,
        "by_objective": by_objective, "by_module": by_module,
        "weak_objectives": [k for k, v in by_objective.items() if v["percent"] < WEAK_PERCENT],
        "weak_modules": [k for k, v in by_module.items() if v["percent"] < WEAK_PERCENT],
    }


def _apportion(total: int, weights: dict) -> dict:
    """Split `total` whole items in proportion to `weights` (largest-remainder method)."""
    s = sum(weights.values())
    raw = {k: total * v / s for k, v in weights.items()}
    counts = {k: int(v) for k, v in raw.items()}
    for k in sorted(raw, key=lambda k: raw[k] - counts[k], reverse=True)[: total - sum(counts.values())]:
        counts[k] += 1
    return counts


def exam_plan(store, n: int) -> dict[str, int]:
    """How many questions to draw from each module that has a quiz.
    Questions are shared out between domains by the weights in syllabus.json (or by
    module count if a weight is missing), then equally between modules in a domain."""
    mods = store.quiz_modules()
    if not mods or n <= 0:
        return {}
    by_domain: dict[str, list] = {}
    for m in mods:
        by_domain.setdefault(m["domain"], []).append(m)
    dom_w = {d["id"]: d.get("weight") for d in store.syllabus["domains"]}
    use_weights = all(isinstance(dom_w.get(d), (int, float)) and dom_w[d] > 0 for d in by_domain)
    per_domain = _apportion(n, {d: (dom_w[d] if use_weights else len(ms)) for d, ms in by_domain.items()})
    counts: dict[str, int] = {}
    for d, ms in by_domain.items():
        counts.update(_apportion(per_domain[d], {m["id"]: 1 for m in ms}))
    for m in mods:
        counts[m["id"]] = min(counts[m["id"]], len(m["questions"]))
    return counts


def build_exam(store, n: int, seed: int) -> list[dict]:
    rng = random.Random(f"{seed}:exam")
    picked = []
    for mid, count in exam_plan(store, n).items():
        picked.extend(rng.sample(store.module(mid)["questions"], count))
    return picked
