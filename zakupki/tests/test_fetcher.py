# test_fetcher.py
import pytest
from fetcher import get_html_content

def test_fetch_success(requests_mock):
    url = "https://example.com/test"
    html = "<html><body>ok</body></html>"
    requests_mock.get(url, text=html, status_code=200)

    content, error = get_html_content(url)
    assert error is None
    assert content is not None
    assert "ok" in content

def test_fetch_404(requests_mock):
    url = "https://example.com/notfound"
    requests_mock.get(url, status_code=404, text="Not Found")

    content, error = get_html_content(url)
    assert content is None
    assert error is not None
    assert "HTTPError" in error
