import requests

OPENALEX_URL = "https://api.openalex.org/works"


def search_paper(
    topic: str,
    year_from: int | None = None,
    year_to: int | None = None,
    min_citations: int | None = None,
    max_citations: int | None = None,
    max_papers: int = 15,
) -> list[dict]:
    filters = search_paper_filters(year_from, year_to, min_citations, max_citations)
    filters.insert(0, f"title_and_abstract.search:{topic}")

    params = {
        "filter": ",".join(filters),
        "per_page": max_papers,
    }

    try:
        response = requests.get(OPENALEX_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return [{"error": f"OpenAlex API: {e}"}]

    papers = []
    for paper in data.get("results", []):
        papers.append(
            {
                "title": paper.get("title") or "",
                "authors": [
                    a["author"]["display_name"] for a in paper.get("authorships", [])
                ][:5],
                "publication_year": paper.get("publication_year"),
                "citation_count": paper.get("cited_by_count"),
                "url": paper.get("id"),
                "doi": paper.get("doi"),
                "abstract": abstract_format(paper.get("abstract_inverted_index"))[:600],
                "citation_count_source": "OpenAlex",
            }
        )

    if not papers:
        return [
            {
                "error": "No matching paper was found",
            }
        ]

    return papers


def search_paper_filters(year_from, year_to, min_citations, max_citations) -> list[str]:
    filters = []
    if year_from is not None:
        filters.append(f"publication_year:>{year_from}")
    if year_to is not None:
        filters.append(f"publication_year:<{year_to}")
    if min_citations is not None:
        filters.append(f"cited_by_count:>{min_citations}")
    if max_citations is not None:
        filters.append(f"cited_by_count:<{max_citations}")

    return filters


def abstract_format(inverted_index) -> str:
    if not inverted_index:
        return ""

    items = [
        (i, w) for w, item_position in inverted_index.items() for i in item_position
    ]
    items.sort()

    return " ".join(w for _, w in items)


if __name__ == "__main__":
    results = search_paper(
        topic="LLM agents software engineering",
        year_from=2022,
        min_citations=99,
        max_papers=15,
    )

    for paper in results:
        print("Title:", paper["title"])
        print("Year:", paper["publication_year"])
        print("Citations:", paper["citation_count"])
        print("Citation source:", paper["citation_count_source"])
        print("URL:", paper["url"])
        print("DOI:", paper["doi"])
        print("---")