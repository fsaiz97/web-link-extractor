import unittest
import queue
from unittest.mock import patch

from link_extractor import producer


fake_html = "<!doctype html>\n<html>\n<head>\n<title>This is the title of the webpage!</title>\n</head>" \
                    "\n<body>\n<p>This is an example paragraph. Anything in the <strong>body</strong> tag will " \
                    "appear on the page, just like this <strong>p</strong> tag and its contents.</p>\n</body>\n</html>"


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, html):
            self.text = html

    if args[0] == "http://test.com":
        return MockResponse(fake_html)


class TestProducer(unittest.TestCase):
    def setUp(self):
        self.html_queue = queue.Queue()

    @patch('link_extractor.requests.get', side_effect=mocked_requests_get)
    def test_producer_extracts_correctly(self, mocked_get):
        producer(self.html_queue, ["http://test.com"])
        self.assertEqual(self.html_queue.get(), fake_html)

    def test_producer_handles_invalid_url(self):
        producer(self.html_queue, ["http//test.com"])


if __name__ == "__main__":
    unittest.main()
