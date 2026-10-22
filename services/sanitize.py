"""Render Markdown notes to sanitised HTML."""
import markdown
import nh3

_ATTRIBUTES = {
    "a": {"href", "title"},
    "code": {"class"},
    "pre": {"class"},
    "h2": {"id"},
    "h3": {"id"},
    "th": {"align"},
    "td": {"align"},
}


def clean_html(html: str) -> str:
    """Strip anything dangerous. nh3's default tag allow-list covers normal prose,
    tables and code blocks; scripts, iframes and event handlers are removed."""
    return nh3.clean(html, attributes=_ATTRIBUTES, url_schemes={"http", "https", "mailto"})


def _flatten_h2(tokens, out):
    for t in tokens:
        if t["level"] == 2:
            out.append({"id": t["id"], "name": t["name"]})
        _flatten_h2(t.get("children", []), out)
    return out


def render_markdown(text: str):
    """Return (sanitised_html, toc) where toc is a list of {id, name} for H2 headings."""
    md = markdown.Markdown(extensions=["fenced_code", "tables", "toc", "sane_lists"])
    html = clean_html(md.convert(text))
    return html, _flatten_h2(md.toc_tokens, [])
