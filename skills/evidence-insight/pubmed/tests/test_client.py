from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(ROOT))

from pubmed_tool.client import NCBIClient, RateLimiter
from pubmed_tool.errors import ResponseError, TransportError


class Response:
    def __init__(self, body: bytes, content_type: str = "application/json"):
        self.body = body
        self.headers = {"Content-Type": content_type}

    def read(self) -> bytes:
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None


class RateLimiterTests(unittest.TestCase):
    def test_spaces_request_starts_at_configured_rate(self):
        state = {"time": 0.0}
        sleeps = []

        def clock():
            return state["time"]

        def sleep(delay):
            sleeps.append(delay)
            state["time"] += delay

        limiter = RateLimiter(2, clock=clock, sleeper=sleep)
        limiter.wait()
        limiter.wait()
        limiter.wait()
        self.assertEqual(sleeps, [0.5, 0.5])


class ClientTests(unittest.TestCase):
    def test_retries_429_and_honors_retry_after(self):
        calls = []
        sleeps = []

        def opener(request, timeout):
            calls.append(request.full_url)
            if len(calls) == 1:
                raise HTTPError(
                    request.full_url, 429, "rate", {"Retry-After": "2"}, None
                )
            return Response(b'{"ok": true}')

        client = NCBIClient(
            email="agent@example.org",
            api_key="SECRET",
            opener=opener,
            sleeper=sleeps.append,
        )
        client.limiter.wait = lambda: None
        self.assertEqual(client.request("test.fcgi", {"db": "pubmed"}), b'{"ok": true}')
        self.assertEqual(sleeps, [2.0])
        self.assertEqual(len(calls), 2)
        self.assertIn("tool=rc-skills-pubmed", calls[0])
        self.assertIn("email=agent%40example.org", calls[0])

    def test_does_not_retry_a_400_response(self):
        calls = []

        def opener(request, timeout):
            calls.append(request.full_url)
            raise HTTPError(request.full_url, 400, "bad request", {}, None)

        client = NCBIClient(opener=opener, sleeper=lambda delay: None)
        client.limiter.wait = lambda: None
        with self.assertRaises(TransportError) as caught:
            client.request("test.fcgi", {})
        if caught.exception.__cause__ is not None:
            caught.exception.__cause__.close()
        self.assertEqual(len(calls), 1)

    def test_rejects_empty_and_html_responses(self):
        for response in (Response(b""), Response(b"<html/>", "text/html")):
            with self.subTest(response=response):
                client = NCBIClient(
                    opener=lambda request, timeout, value=response: value,
                    sleeper=lambda delay: None,
                )
                client.limiter.wait = lambda: None
                with self.assertRaises(ResponseError):
                    client.request("test.fcgi", {})

    def test_rejects_malformed_json(self):
        client = NCBIClient(
            opener=lambda request, timeout: Response(b"{bad"),
            sleeper=lambda delay: None,
        )
        client.limiter.wait = lambda: None
        with self.assertRaises(ResponseError):
            client.json("test.fcgi", {})

    def test_retries_one_transient_malformed_json_response(self):
        responses = [
            Response(b"<ERROR>temporary</ERROR>", "text/xml"),
            Response(b'{"ok": true}'),
        ]
        sleeps = []
        client = NCBIClient(
            opener=lambda request, timeout: responses.pop(0), sleeper=sleeps.append
        )
        client.limiter.wait = lambda: None
        self.assertEqual(client.json("test.fcgi", {}), {"ok": True})
        self.assertEqual(len(responses), 0)
        self.assertEqual(len(sleeps), 1)


if __name__ == "__main__":
    unittest.main()
