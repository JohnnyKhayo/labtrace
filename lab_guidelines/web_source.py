
import requests


SOURCE_URL = ("https://www.dshs.texas.gov/laboratory-services/"
    "laboratory-testing-services-manual-introduction/"
    "guidelines-specimen-collection-submission")

def fetch_html(url=SOURCE_URL):
    """
    Retrieve HTML content from the laboratory
    guidelines webpage.
    """

    try:
        response = requests.get(
            url,
            timeout=(5, 15),
            headers={"User-Agent": "LabTrace/1.0 (Educational Project)"})

        response.raise_for_status()

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Unable to retrieve laboratory guidelines: {error}"
        ) from error

    content_type = response.headers.get("Content-Type", "")

    if "text/html" not in content_type.lower():
        raise ValueError("The requested webpage is not HTML.")

    return response.text
