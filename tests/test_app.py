import pytest
from werkzeug.datastructures import MultiDict

from app import create_app


@pytest.fixture()
def client():
    app = create_app({"TESTING": True, "RATE_LIMIT_PER_MIN": 0})
    return app.test_client(), app.extensions["store"]


def test_home_lists_modules(client):
    c, _ = client
    r = c.get("/")
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert "Core architecture of Azure" in html and "Coming soon" in html
    assert r.headers["Content-Security-Policy"].startswith("default-src 'self'")
    assert r.headers["X-Content-Type-Options"] == "nosniff"


def test_module_pages(client):
    c, _ = client
    ready = c.get("/module/M04").get_data(as_text=True)
    assert "Azure Resource Manager" in ready and "Practice quiz" in ready and "<script>" not in ready.split("<main")[1]
    planned = c.get("/module/M07")
    assert planned.status_code == 200 and "coming soon" in planned.get_data(as_text=True).lower()
    assert c.get("/module/M99").status_code == 404
    assert c.get("/healthz").get_json() == {"status": "ok"}


def test_quiz_page_does_not_leak_answers(client):
    c, store = client
    html = c.get("/module/M04/quiz?seed=42").get_data(as_text=True)
    for q in store.module("M04")["questions"]:
        assert q["explanation"] not in html
        assert q["learn_more"] not in html
    assert "Question 1 of 13" in html
    assert c.get("/module/M07/quiz").status_code == 404


def _perfect_form(store, module_id="M04"):
    data = {"qids": ",".join(q["id"] for q in store.module(module_id)["questions"])}
    multi = []
    for q in store.module(module_id)["questions"]:
        if q["type"] == "yesno":
            for o in q["options"]:
                data[f"q_{q['id']}.{o['id']}"] = "yes" if o["id"] in q["correct"] else "no"
        elif q["type"] == "single":
            data[f"q_{q['id']}"] = q["correct"][0]
        else:
            multi.extend((f"q_{q['id']}", cid) for cid in q["correct"])
    return MultiDict(list(data.items()) + multi)


def test_submit_quiz_perfect_and_empty(client):
    c, store = client
    html = c.post("/module/M04/quiz", data=_perfect_form(store)).get_data(as_text=True)
    assert "13 / 13 correct (100%)" in html
    empty = c.post("/module/M04/quiz", data={"qids": "M04-Q01,M04-Q02"}).get_data(as_text=True)
    assert "0 / 2 correct (0%)" in empty and "Not answered" in empty
    assert c.post("/module/M04/quiz", data={"qids": "nope"}).status_code == 400
    assert c.post("/module/M04/quiz", data={"qids": "M05-Q01"}).status_code == 400


def test_exam_flow(client):
    c, store = client
    page = c.get("/exam?seed=3")
    assert page.status_code == 200 and "data-timer-minutes" in page.get_data(as_text=True)
    res = c.post("/exam", data=_perfect_form(store)).get_data(as_text=True)
    assert "Pass:" in res
    low = c.post("/exam", data={"qids": "M04-Q01,M04-Q02"}).get_data(as_text=True)
    assert "Not yet" in low and "Revisit these modules" in low


def test_api_check(client):
    c, _ = client
    ok = c.post("/api/check", json={"question_id": "M04-Q01", "answer": ["a"]}).get_json()
    assert ok["correct"] is True and ok["explanation"]
    bad = c.post("/api/check", json={"question_id": "M04-Q01", "answer": ["b", "zzz"]}).get_json()
    assert bad["correct"] is False
    yn = c.post("/api/check", json={"question_id": "M04-Q08", "answer": {"s1": False, "s2": True, "s3": True}}).get_json()
    assert yn["correct"] is True
    assert c.post("/api/check", json={"question_id": "nope"}).status_code == 404
    assert c.post("/api/check", data="not json", content_type="text/plain").status_code == 404


def test_xss_in_form_is_escaped(client):
    c, _ = client
    html = c.post("/module/M04/quiz", data={"qids": "M04-Q01", "q_M04-Q01": "<script>alert(1)</script>"}).get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html


def test_rate_limit_and_reviewed_gate():
    app = create_app({"TESTING": True, "RATE_LIMIT_PER_MIN": 2})
    c = app.test_client()
    codes = [c.post("/api/check", json={"question_id": "M04-Q01", "answer": ["a"]}).status_code for _ in range(3)]
    assert codes == [200, 200, 429]
    gated = create_app({"TESTING": True, "RATE_LIMIT_PER_MIN": 0, "REQUIRE_REVIEWED": True}).test_client()
    assert gated.get("/module/M04").status_code == 200           # notes still readable
    assert gated.get("/module/M04/quiz").status_code == 404      # nothing reviewed yet -> no quiz
