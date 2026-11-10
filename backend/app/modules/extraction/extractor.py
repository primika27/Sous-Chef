from recipe_scrapers import scrape_html, scrape_me


def scrape_recipe(url: str):
    scraper = scrape_me(url)
    return {
        "title": scraper.title(),
        "instructions": scraper.instructions(), # returns string of all steps
        "ingredients": scraper.ingredients(),
        # Some scrapers support reviews/notes; fallback to empty if missing:
        "notes": getattr(scraper, "notes", lambda: "")(),
    }
