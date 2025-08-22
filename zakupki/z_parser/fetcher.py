# fetcher.py
import logging
import requests
from typing import Tuple, Optional

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
}

# Возвращаем кортеж (content, error). Если error is None — всё ок.
def get_html_content(url: str, timeout: float = 10.0) -> Tuple[Optional[str], Optional[str]]:
    logger.info("Fetching URL %s", url)
    try:
        response = requests.get(url, timeout=timeout,headers=DEFAULT_HEADERS)
        response.raise_for_status()
        logger.debug("Fetched %d bytes from %s", len(response.text), url)
        # Явно указываем кодировку, если сервер не корректно её прислал
        if response.encoding is None:
            response.encoding = response.apparent_encoding
        return response.text, None
    except requests.Timeout as e:
        logger.exception("Request timed out for %s: %s", url, e)
        return None, "TimeoutError: запрос превысил время ожидания"
    except requests.ConnectionError as e:
        logger.exception("Connection error for %s: %s", url, e)
        return None, "ConnectionError: проблема с соединением"
    except requests.HTTPError as e:
        status = getattr(e.response, "status_code", "unknown")
        logger.exception("HTTP error for %s: %s (status=%s)", url, e, status)
        return None, f"HTTPError: {e} (status={status})"
    except requests.RequestException as e:
        logger.exception("Request failed for %s: %s", url, e)
        return None, f"RequestException: {e}"
