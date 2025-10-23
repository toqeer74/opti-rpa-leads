import requests
from bs4 import BeautifulSoup


def get_companies_and_people():
    """Demo: returns dummy scraped data; extend later."""
    # Example using public automation partner pages
    urls = [
        "https://www.uipath.com/partners/technology",
        "https://www.blueprism.com/partners",
    ]
    results = []
    for u in urls:
        html = requests.get(u, timeout=20).text
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.select("a[href]"):
            href = a["href"]
            name = a.get_text(strip=True)
            if "@" in href:
                results.append(
                    {
                        "company": name or "Unknown",
                        "email": href.replace("mailto:", ""),
                        "source_url": u,
                    }
                )
    return results or [
        {"company": "DemoCo", "email": "cto@democo.com", "source_url": "demo"}
    ]

