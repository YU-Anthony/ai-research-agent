"""Read-only discovery from the official arXiv Atom API."""
import re
from datetime import datetime, timezone
import httpx
from defusedxml import ElementTree as ET

API = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom"}
ID = re.compile(r"(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?$")


def parse_feed(xml: str) -> list[dict]:
    root = ET.fromstring(xml)
    papers = []
    for entry in root.findall("a:entry", NS):
        def field(name):
            return " ".join((entry.findtext(f"a:{name}", default="", namespaces=NS)).split())
        identifier = field("id").split("/abs/")[-1]
        if not ID.fullmatch(identifier):
            raise ValueError("arXiv returned an invalid paper identifier or API error")
        paper = {"id": identifier, "title": field("title"), "abstract": field("summary"),
                 "authors": [a.findtext("a:name", namespaces=NS) for a in entry.findall("a:author", NS)],
                 "published": field("published"), "updated": field("updated"),
                 "url": f"https://arxiv.org/abs/{identifier}", "source": API,
                 "retrieved_at": datetime.now(timezone.utc).isoformat()}
        if not all(paper[k] for k in ("title", "abstract", "authors", "published")):
            raise ValueError("Incomplete arXiv metadata")
        if identifier not in {p['id'] for p in papers}:
            papers.append(paper)
    return papers


def search(query: str, count: int = 10) -> list[dict]:
    if not query.strip() or not 1 <= count <= 10:
        raise ValueError("Provide a query and a count between 1 and 10")
    with httpx.Client(timeout=45, follow_redirects=False) as client:
        response = client.get(API, params={"search_query": query, "start": 0, "max_results": count * 2,
                                         "sortBy": "relevance"}, headers={"User-Agent": "AIResearchAgent/0.1"})
        response.raise_for_status()
    candidates = parse_feed(response.text)
    papers = []
    seen_titles = set()
    for paper in candidates:
        title = re.sub(r'\W+', '', paper['title'].casefold())
        if title not in seen_titles:
            papers.append(paper)
            seen_titles.add(title)
        if len(papers) == count:
            break
    if len(papers) != count:
        raise ValueError(f"Requested {count} papers, received {len(papers)}; broaden the query")
    return papers
