
import requests
from unittest.mock import Mock, patch

from lab_guidelines.web_source import fetch_html


def test_fetch_html_success():
    response = Mock()
    response.text = "<html><body>Laboratory guidelines</body></html>"
    response.headers = {
        "Content-Type": "text/html; charset=utf-8"
    }

    with patch(
        "lab_guidelines.web_source.requests.get",
        return_value=response
    ):
        result = fetch_html()

    assert result == response.text


def test_fetch_html_connection_error():
    with patch(
        "lab_guidelines.web_source.requests.get",
        side_effect=requests.ConnectionError("Connection failed")
    ):
        try:
            fetch_html()
            assert False, "Expected RuntimeError"
        except RuntimeError as error:
            assert "Unable to retrieve laboratory guidelines" in str(error)


def test_fetch_html_http_error():
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError(
        "404 Not Found"
    )

    with patch(
        "lab_guidelines.web_source.requests.get",
        return_value=response
    ):
        try:
            fetch_html()
            assert False, "Expected RuntimeError"
        except RuntimeError as error:
            assert "Unable to retrieve laboratory guidelines" in str(error)


def test_fetch_html_rejects_non_html():
    response = Mock()
    response.headers = {
        "Content-Type": "application/json"
    }

    with patch(
        "lab_guidelines.web_source.requests.get",
        return_value=response
    ):
        try:
            fetch_html()
            assert False, "Expected ValueError"
        except ValueError as error:
            assert "not HTML" in str(error)
