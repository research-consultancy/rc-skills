from __future__ import annotations

import json
import os
import random
import threading
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .errors import ResponseError, TransportError


BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
PMC_ID_URL = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
RETRY_STATUSES = {408, 429, 500, 502, 503, 504}


class RateLimiter:
    def __init__(self, rate: float, clock=time.monotonic, sleeper=time.sleep):
        self.interval = 1.0 / rate
        self.clock = clock
        self.sleeper = sleeper
        self._lock = threading.Lock()
        self._next = 0.0

    def wait(self) -> None:
        with self._lock:
            now = self.clock()
            delay = max(0.0, self._next - now)
            if delay:
                self.sleeper(delay)
                now = self.clock()
            self._next = max(now, self._next) + self.interval


class NCBIClient:
    def __init__(
        self,
        email: str | None = None,
        api_key: str | None = None,
        attempts: int = 5,
        timeout: float = 30.0,
        opener=urlopen,
        sleeper=time.sleep,
    ):
        self.email = email or os.environ.get("NCBI_EMAIL")
        self.api_key = api_key or os.environ.get("NCBI_API_KEY")
        self.attempts = attempts
        self.timeout = timeout
        self.opener = opener
        self.sleeper = sleeper
        self.limiter = RateLimiter(10 if self.api_key else 3, sleeper=sleeper)

    def _identity(self) -> dict[str, str]:
        values = {"tool": "rc-skills-pubmed"}
        if self.email:
            values["email"] = self.email
        if self.api_key:
            values["api_key"] = self.api_key
        return values

    def request(
        self,
        endpoint: str,
        params: dict[str, Any],
        *,
        method: str = "GET",
        base_url: str = BASE_URL,
    ) -> bytes:
        encoded_params = {
            k: v for k, v in {**params, **self._identity()}.items() if v is not None
        }
        encoded = urlencode(encoded_params, doseq=True).encode("utf-8")
        url = base_url + endpoint
        request = Request(
            url + ("?" + encoded.decode() if method == "GET" else ""),
            data=encoded if method == "POST" else None,
            headers={"User-Agent": "rc-skills-pubmed/1.0", "Accept": "*/*"},
            method=method,
        )
        last_error: Exception | None = None
        for attempt in range(self.attempts):
            self.limiter.wait()
            try:
                with self.opener(request, timeout=self.timeout) as response:
                    body = response.read()
                    content_type = response.headers.get("Content-Type", "")
                    if not body:
                        raise ResponseError("NCBI returned an empty response")
                    if "text/html" in content_type.lower():
                        raise ResponseError("NCBI returned HTML instead of API data")
                    return body
            except HTTPError as error:
                last_error = error
                if error.code not in RETRY_STATUSES or attempt + 1 == self.attempts:
                    raise TransportError(f"NCBI HTTP error {error.code}") from error
                retry_after = (
                    error.headers.get("Retry-After") if error.headers else None
                )
                delay = (
                    float(retry_after)
                    if retry_after and retry_after.isdigit()
                    else random.uniform(0, min(16, 2**attempt))
                )
            except (URLError, TimeoutError, ConnectionError) as error:
                last_error = error
                if attempt + 1 == self.attempts:
                    raise TransportError(f"NCBI request failed: {error}") from error
                delay = random.uniform(0, min(16, 2**attempt))
            self.sleeper(delay)
        raise TransportError(f"NCBI request failed: {last_error}")

    def json(
        self, endpoint: str, params: dict[str, Any], **kwargs: Any
    ) -> dict[str, Any]:
        last_error: Exception | None = None
        for response_attempt in range(2):
            body = self.request(endpoint, params, **kwargs)
            try:
                value = json.loads(body)
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                last_error = error
                if response_attempt == 0:
                    self.sleeper(random.uniform(0, 1))
                    continue
                raise ResponseError(
                    "NCBI returned malformed JSON after retry"
                ) from error
            if not isinstance(value, dict):
                raise ResponseError("NCBI returned an unexpected JSON value")
            return value
        raise ResponseError("NCBI returned malformed JSON after retry") from last_error
