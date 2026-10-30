# AZ-900 Academy

A small, fast study site for **Microsoft Exam AZ-900 (Azure Fundamentals)**: course notes for each module, a quiz per module with instant feedback and explanations, and a timed exam simulation. Progress is kept in the learner's browser. There is **no database, no login and no LLM**: notes and questions are reviewed files, and quizzes are graded by plain code.

> Independent study resource. Not affiliated with or endorsed by Microsoft.

## Status

| Piece | State |
|---|---|
| App, quiz engine, exam simulation, validator, tests | Done |
| All 13 modules (notes + 12 to 18 questions each, 188 questions in total) | Written, **need your review** |
| Exam skills outline | Reconciled with the official study guide, "Skills measured as of July 20, 2026" |
| Microsoft Learn learning paths | Covers the three "Introduction to Cloud Infrastructure" paths (Describe cloud concepts; Describe Azure architecture and services; Describe Azure management and governance). See `docs/COVERAGE.md` |

Modules follow the three skill areas: cloud concepts (M01-M03), Azure architecture and services (M04-M09) and Azure management and governance (M10-M13). Each notes page links to the Microsoft Learn module it matches. Finish a module's quiz and the results page offers the next module; notes pages also have Previous and Next links.

## Run it locally

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python -m pytest                                        # 25 tests
python scripts/validate_content.py                      # checks notes and questions
flask --app app run --debug                             # http://127.0.0.1:5000
```

No API keys are needed.

## Project layout

```
app.py                  Flask app factory and routes
config.py               Environment-based settings
services/
  content.py            Loads syllabus, notes, questions
  quiz.py               Shuffle, grading, exam sampling (deterministic)
  sanitize.py           Markdown to sanitised HTML (nh3)
  ratelimit.py          In-memory per-IP limiter
content/
  syllabus.json         Domains, modules, objectives, exam settings
  modules/M04-core-architecture/
    notes.md            Course notes
    questions.json      Quiz questions
scripts/validate_content.py
docs/COVERAGE.md       Learn unit to project module map
templates/  static/  tests/
render.yaml             Render deployment
```

## How the quiz works

- **Practice mode:** pick an answer, press *Check answer*, see the explanation straight away (the browser asks `/api/check`). Finish to get a full results page.
- **Exam style / exam simulation:** no feedback until the end. The simulation draws questions from every module that has a quiz, with a countdown timer. It submits itself when time runs out.
- Correct answers are **never in the page source** before you check or submit.
- Results show a score, a breakdown by objective, which modules to revisit, and an explanation for every question.
- Question types: `single` (one answer), `multi` (choose several), `yesno` (a set of statements, each Yes or No; the item is correct only if every statement is right).

## Add or edit a module

1. In `content/syllabus.json`, set the module's `status` to `"ready"` and turn its `topics` into `objectives` with ids like `M05-O1`.
2. Add a `learn_module` (title and learn.microsoft.com URL) to the module in `syllabus.json`. Create `content/modules/<id>-<slug>/notes.md` using the same sections as M04 (the validator lists them) and a `Last reviewed: YYYY-MM-DD` line.
3. Create `questions.json` with at least 12 questions. Do not always make the first option the correct one: option ids are visible in the page source, so vary which id is correct. Fields: `id`, `module`, `objective_id`, `type`, `difficulty`, `prompt`, `options`, `correct`, `explanation`, `why_wrong`, `learn_more` (a learn.microsoft.com URL) and `reviewed`.
4. Run `python scripts/validate_content.py` and `python -m pytest`.

Authoring rules: write in your own words, never copy Microsoft Learn text or real exam questions, use current product names (Microsoft Entra ID, Microsoft Defender for Cloud, Microsoft Purview), and describe anything that changes often (prices, limits) conceptually.

## Content review gate

Every question ships with `"reviewed": false`. Locally all questions are shown, with an "Unreviewed" badge. In production (`REQUIRE_REVIEWED=1`, set in `render.yaml`) **only questions with `"reviewed": true` are served**. Check each question and note against Microsoft Learn, then flip the flag (or flip them all once you have reviewed a module). The Microsoft Learn links in the notes and questions have not been checked for reachability, so click through them during review.

The module map matches the official skills outline as of July 20, 2026, and each domain's `weight` is the midpoint of Microsoft's published range (25-30%, 35-40%, 30-35%). The exam simulation shares its questions between domains in that proportion. Microsoft updates the outline from time to time, so re-check <https://learn.microsoft.com/credentials/certifications/resources/study-guides/az-900> and edit `content/syllabus.json` (and the notes) if it changes.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `PORT` | 5000 | Used by `python app.py` |
| `REQUIRE_REVIEWED` | 0 | Serve only reviewed questions |
| `TRUST_PROXY` | 0 | Trust `X-Forwarded-For` (set to 1 on Render) |
| `RATE_LIMIT` | 60 | POST requests per minute per IP (0 turns it off) |
| `EXAM_QUESTIONS`, `EXAM_MINUTES` | from syllabus.json | Override exam simulation settings |

## Deploy to Render

Push to GitHub, create a **Blueprint** on Render from this repo (it reads `render.yaml`), and deploy. The start command is `gunicorn "app:create_app()"`. The rate limiter is per worker process, which is fine at this scale.

## Security notes

Rendered HTML is sanitised; user input is escaped; quiz submissions are validated server-side; there is a Content-Security-Policy with no inline scripts or styles; request bodies are capped at 64 KB; POST endpoints are rate limited.

## Later ideas

- An optional offline script that asks an LLM for *draft* questions into `content/drafts/` (git-ignored, never served) for you to review.
- Drag-and-drop and matching question types.
- More modules, then the sovereign-cloud and cost-calculator labs.
