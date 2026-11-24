
import re
from bs4 import BeautifulSoup

def normalize_text(text):
    """Clean whitespace from extracted webpage text."""

    return re.sub(r"\s+", " ", text).strip()

def extract_section(soup, section_name):
    """Extract content belonging to a particular heading from the laboratory guidelines page."""

    headings = soup.find_all(
        re.compile(r"^h[1-6]$"),
        string=lambda text: (text is not None
            and normalize_text(text).casefold()
            == section_name.casefold()))

    if not headings:
        return None

    extracted_items = []

    for heading in headings:

        heading_level = int(heading.name[1])

        for element in heading.find_all_next(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li"]):

            # Stop when another heading at the same
            # or a higher level begins.
            if element.name.startswith("h"):
                next_level = int(element.name[1])

                if next_level <= heading_level:
                    break

                continue

            # Avoid extracting paragraphs twice when they are already contained inside a list item.
            if element.name == "p" and element.find_parent("li"):
                continue

            text = normalize_text(
                element.get_text(" ", strip=True)
            )

            if text and text not in extracted_items:
                extracted_items.append(text)

    if not extracted_items:
        return None

    return {"section": section_name, "content": extracted_items}


def parse_guidelines(html, sample_type):
    """Parse the webpage and return the requested blood specimen guidance."""

    soup = BeautifulSoup(html, "html.parser")

    sections = {
        "whole blood": "Whole Blood Specimens",
        "serum": "Serum and Plasma Specimens",
        "plasma": "Serum and Plasma Specimens"}

    selected_type = sample_type.strip().casefold()

    section_name = sections.get(selected_type)

    if section_name is None:
        return None

    return extract_section(soup, section_name)
