import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()


def serp_tool(query: str) -> str:
    params = {
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "num": 3
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    output = []

    if "organic_results" in results:
        for r in results["organic_results"][:3]:
            title = r.get("title", "")
            snippet = r.get("snippet", "")
            link = r.get("link", "")

            output.append(f"{title}\n{snippet}\nSource: {link}")

    return "\n\n".join(output) if output else "No results found."