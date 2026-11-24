
from lab_guidelines.guideline_parser import parse_guidelines


SAMPLE_HTML = """
<html>
<body>
    <h2>Whole Blood Specimens</h2>
    <p>Whole blood collection information.</p>
    <ul>
        <li>Example storage information.</li>
        <li>Example transportation information.</li>
    </ul>

    <h2>Serum and Plasma Specimens</h2>
    <p>Serum and plasma collection information.</p>
    <ul>
        <li>Example serum storage information.</li>
    </ul>

    <h2>Sputum Specimens</h2>
    <p>Sputum information.</p>
</body>
</html>
"""


def test_whole_blood_extraction():
    result = parse_guidelines(SAMPLE_HTML, "whole blood")

    assert result is not None
    assert result["section"] == "Whole Blood Specimens"


def test_serum_extraction():
    result = parse_guidelines(SAMPLE_HTML, "serum")

    assert result is not None
    assert result["section"] == "Serum and Plasma Specimens"


def test_plasma_extraction():
    result = parse_guidelines(SAMPLE_HTML, "plasma")

    assert result is not None
    assert result["section"] == "Serum and Plasma Specimens"


def test_unknown_specimen():
    result = parse_guidelines(SAMPLE_HTML, "urine")

    assert result is None


def test_missing_section():
    html = "<html><body><h2>Other Section</h2></body></html>"

    result = parse_guidelines(html, "whole blood")

    assert result is None


def test_empty_html():
    result = parse_guidelines("", "whole blood")

    assert result is None


def test_section_without_content():
    html = """
    <html>
    <body>
        <h2>Whole Blood Specimens</h2>
        <h2>Other Section</h2>
    </body>
    </html>
    """

    result = parse_guidelines(html, "whole blood")

    assert result is None


def test_heading_with_nested_element():
    html = """
    <html>
    <body>
        <h3><span>Whole Blood Specimens</span></h3>
        <p>Whole blood collection information.</p>
    </body>
    </html>
    """

    result = parse_guidelines(html, "whole blood")

    assert result is not None
    assert result["section"] == "Whole Blood Specimens"
