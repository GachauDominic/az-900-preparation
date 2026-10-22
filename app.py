"""AZ-900 Academy: notes, quizzes and an exam simulation. No database, no LLM."""
import logging
import random

from flask import Flask, abort, jsonify, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from services.content import ContentStore
from services.quiz import build_exam, grade_attempt, grade_question, parse_answers, prepare_for_display
from services.ratelimit import RateLimiter

log = logging.getLogger("az900")

CSP = ("default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; "
       "base-uri 'none'; form-action 'self'; frame-ancestors 'none'")


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    if app.config["TRUST_PROXY"]:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

    store = ContentStore(app.config["CONTENT_DIR"], app.config["REQUIRE_REVIEWED"])
    limiter = RateLimiter(app.config["RATE_LIMIT_PER_MIN"])
    app.extensions["store"] = store

    exam_cfg = store.exam_settings
    exam_questions = int(app.config.get("EXAM_QUESTIONS") or exam_cfg["questions"])
    exam_minutes = int(app.config.get("EXAM_MINUTES") or exam_cfg["minutes"])
    pass_percent = int(exam_cfg["pass_percent"])

    # ---- cross-cutting -------------------------------------------------
    @app.before_request
    def _limit():
        if request.method == "POST" and not limiter.allow(request.remote_addr or "unknown"):
            abort(429)

    @app.after_request
    def _headers(resp):
        resp.headers["Content-Security-Policy"] = CSP
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return resp

    @app.context_processor
    def _globals():
        return {"store": store}

    def _error(code, title, message):
        return render_template("error.html", code=code, title=title, message=message), code

    @app.errorhandler(404)
    def _404(_):
        return _error(404, "Page not found", "That page does not exist. Go back to the course list and pick a module.")

    @app.errorhandler(413)
    def _413(_):
        return _error(413, "Request too large", "That submission was too large. Try again with your normal answers.")

    @app.errorhandler(429)
    def _429(_):
        return _error(429, "Slow down a little", "Too many requests in a short time. Wait a minute and try again.")

    @app.errorhandler(500)
    def _500(e):
        log.exception("Unhandled error: %s", e)
        return _error(500, "Something went wrong", "The page could not be shown. Try again in a moment.")

    # ---- pages ---------------------------------------------------------
    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.get("/")
    def home():
        return render_template("home.html", domains=store.domains(), exam_minutes=exam_minutes,
                               exam_questions=exam_questions)

    @app.get("/module/<module_id>")
    def module_page(module_id):
        module = store.module(module_id)
        if module is None:
            abort(404)
        return render_template("module.html", module=module)

    def _seed() -> int:
        raw = request.args.get("seed") or request.form.get("seed") or ""
        return int(raw) if raw.isdigit() else random.randrange(1, 10**9)

    def _quiz_page(**ctx):
        return render_template("quiz.html", **ctx)

    @app.route("/module/<module_id>/quiz", methods=["GET", "POST"])
    def module_quiz(module_id):
        module = store.module(module_id)
        if module is None or not module["has_quiz"]:
            abort(404)
        questions = module["questions"]
        if request.method == "GET":
            mode = "exam" if request.args.get("mode") == "exam" else "practice"
            seed = _seed()
            return _quiz_page(title=f"{module['title']}: quiz", heading=module["title"],
                              action=request.path, mode=mode, seed=seed, minutes=None,
                              questions=prepare_for_display(questions, seed),
                              qids=",".join(q["id"] for q in questions), back=f"/module/{module_id}")
        submitted = [i for i in request.form.get("qids", "").split(",") if i]
        asked = [q for q in questions if q["id"] in set(submitted)]
        if not asked:
            abort(400)
        graded = grade_attempt(asked, parse_answers(request.form, asked))
        return render_template("results.html", title=f"{module['title']}: results", kind="module",
                               key=module_id, heading=module["title"], graded=graded,
                               retry=f"/module/{module_id}/quiz", back=f"/module/{module_id}",
                               pass_percent=None)

    @app.route("/exam", methods=["GET", "POST"])
    def exam():
        if not store.quiz_modules():
            abort(404)
        if request.method == "GET":
            seed = _seed()
            questions = build_exam(store, exam_questions, seed)
            return _quiz_page(title="Exam simulation", heading="Exam simulation", action="/exam",
                              mode="exam", seed=seed, minutes=exam_minutes,
                              questions=prepare_for_display(questions, seed),
                              qids=",".join(q["id"] for q in questions), back="/")
        submitted = [i for i in request.form.get("qids", "").split(",") if i][:200]
        asked = store.questions_by_ids(dict.fromkeys(submitted))
        if not asked:
            abort(400)
        graded = grade_attempt(asked, parse_answers(request.form, asked))
        return render_template("results.html", title="Exam simulation: results", kind="exam", key="exam",
                               heading="Exam simulation", graded=graded, retry="/exam", back="/",
                               pass_percent=pass_percent)

    # ---- instant feedback (practice mode) -------------------------------
    @app.post("/api/check")
    def api_check():
        data = request.get_json(silent=True) or {}
        q = store.question(str(data.get("question_id", "")))
        if q is None:
            return jsonify(error="Unknown question"), 404
        raw = data.get("answer")
        valid = {o["id"] for o in q["options"]}
        if q["type"] == "yesno":
            answer = {k: bool(v) for k, v in (raw or {}).items() if k in valid} if isinstance(raw, dict) else {}
        else:
            answer = [v for v in raw if v in valid] if isinstance(raw, list) else []
        r = grade_question(q, answer)
        return jsonify(correct=r["correct"], answered=r["answered"], rows=r["rows"],
                       explanation=r["explanation"], learn_more=r["learn_more"], type=r["type"])

    return app


if __name__ == "__main__":
    import os
    create_app().run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
