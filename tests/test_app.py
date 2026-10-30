import pytest
from werkzeug.datastructures import MultiDict

from app import create_app
from helpers import only_modules, right_answer


@pytest.fixture()
def client():
    app = create_app({"TESTING": True, "RATE_LIMIT_PER_MIN": 0})
    return app.test_client(), app.extensions["store"]


def test_home_lists_every_module_and_headers(client):
    c, store = client
    r = c.get("/")
    html = r.get_data(as_text=True)
    assert r.status_code == 200 and "Coming soon" not in html
    for m in store.modules:
        assert m["title"] in html
    assert r.headers["Content-Security-Policy"].startswith("default-src 'self'")
    assert r.headers["X-Content-Type-Options"] == "nosniff"


def test_every_module_page_and_quiz_loads(client):
    c, store = client
    for m in store.modules:
        page = c.get(f"/module/{m['id']}")
        assert page.status_code == 200 and "Practice quiz" in page.get_data(as_text=True)
        assert c.get(f"/module/{m['id']}/quiz?seed=1").status_code == 200
        assert c.get(f"/module/{m['id']}/quiz?mode=exam&seed=1").status_code == 200
    assert c.get("/module/M99").status_code == 404
    assert c.get("/healthz").get_json() == {"status": "ok"}


def test_module_navigation_links(client):
    c, _ = client
    html = c.get("/module/M04").get_data(as_text=True)
    assert "Next: Compute services" in html and "Previous: Cloud service types" in html
    assert "Previous" not in c.get("/module/M01").get_data(as_text=True).split('class="pager"')[1].split("</nav>")[0]


def test_planned_module_shows_coming_soon(tmp_path):
    app = create_app({"TESTING": True, "RATE_LIMIT_PER_MIN": 0, "CONTENT_DIR": only_modules(tmp_path, {"M04"})})
    c = app.test_client()
    assert "coming soon" in c.get("/module/M07").get_data(as_text=True).lower()
    assert c.get("/module/M07/quiz").status_code == 404
    assert "Coming soon" in c.get("/").get_data(as_text=True)


def test_quiz_pages_do_not_leak_answers(client):
    c, store = client
    for mid in ("M04", "M09"):
        html = c.get(f"/module/{mid}/quiz?seed=42").get_data(as_text=True)
        for q in store.module(mid)["questions"]:
            assert q["explanation"] not in html and q["learn_more"] not in html
    n = len(store.module("M04")["questions"])
    assert f"Question 1 of {n}" in c.get("/module/M04/quiz?seed=42").get_data(as_text=True)


def _perfect_form(store, module_id="M04"):
    qs = store.module(module_id)["questions"]
    pairs = [("qids", ",".join(q["id"] for q in qs))]
    for q in qs:
        a = right_answer(q)
        if q["type"] == "yesno":
            pairs += [(f"q_{q['id']}.{k}", "yes" if v else "no") for k, v in a.items()]
        else:
            pairs += [(f"q_{q['id']}", v) for v in a]
    return MultiDict(pairs)


def test_submit_quiz_perfect_and_empty_with_next_link(client):
    c, store = client
    html = c.post("/module/M04/quiz", data=_perfect_form(store)).get_data(as_text=True)
    n = len(store.module("M04")["questions"])
    assert f"{n} / {n} correct (100%)" in html and "Next module: Compute services" in html
    empty = c.post("/module/M04/quiz", data={"qids": "M04-Q01,M04-Q02"}).get_data(as_text=True)
    assert "0 / 2 correct (0%)" in empty and "Not answered" in empty
    assert c.post("/module/M04/quiz", data={"qids": "nope"}).status_code == 400
    assert c.post("/module/M04/quiz", data={"qids": "M05-Q01"}).status_code == 400
    last = c.post("/module/M13/quiz", data=_perfect_form(store, "M13")).get_data(as_text=True)
    assert "Next module" not in last


def test_exam_flow(client):
    c, store = client
    page = c.get("/exam?seed=3").get_data(as_text=True)
    assert "data-timer-minutes" in page and "Question 40 of 40" in page
    res = c.post("/exam", data=_perfect_form(store)).get_data(as_text=True)
    assert "Pass:" in res
    low = c.post("/exam", data={"qids": "M04-Q01,M04-Q02"}).get_data(as_text=True)
    assert "Not yet" in low and "Revisit these modules" in low


def test_api_check(client):
    c, store = client
    q = store.module("M04")["questions"][0]
    ok = c.post("/api/check", json={"question_id": q["id"], "answer": right_answer(q)}).get_json()
    assert ok["correct"] is True and ok["explanation"]
    wrong = next(o["id"] for o in q["options"] if o["id"] not in q["correct"])
    assert c.post("/api/check", json={"question_id": q["id"], "answer": [wrong, "zzz"]}).get_json()["correct"] is False
    y = next(x for x in store.module("M04")["questions"] if x["type"] == "yesno")
    assert c.post("/api/check", json={"question_id": y["id"], "answer": right_answer(y)}).get_json()["correct"] is True
    assert c.post("/api/check", json={"question_id": "nope"}).status_code == 404
    assert c.post("/api/check", data="not json", content_type="text/plain").status_code == 404


def test_xss_in_form_is_escaped(client):
    c, _ = client
    html = c.post("/module/M04/quiz", data={"qids": "M04-Q01", "q_M04-Q01": "<script>alert(1)</script>"}).get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html


def test_rate_limit_and_reviewed_gate():
    app = create_app({"TESTING": True, "RATE_LIMIT_PER_MIN": 2})
    c = app.test_client()
    codes = [c.post("/api/check", json={"question_id": "M04-Q01", "answer": []}).status_code for _ in range(3)]
    assert codes == [200, 200, 429]
    gated = create_app({"TESTING": True, "RATE_LIMIT_PER_MIN": 0, "REQUIRE_REVIEWED": True}).test_client()
    assert gated.get("/module/M04").status_code == 200
    assert gated.get("/module/M04/quiz").status_code == 404


def test_learn_path_and_module_links_are_shown(client):
    c, _ = client
    home = c.get("/").get_data(as_text=True)
    for title in ("Describe cloud concepts", "Describe Azure architecture and services", "Describe Azure management and governance"):
        assert f"Introduction to Cloud Infrastructure: {title}" in home
    page = c.get("/module/M09").get_data(as_text=True)
    assert "Describe Azure identity, access, and security" in page and "learn.microsoft.com/training/modules/" in page
