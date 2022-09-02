import unittest
import queue
from unittest.mock import patch, mock_open
from io import StringIO
import sys

from link_extractor import producer, consumer, HyperlinkParser


fake_html = "<!doctype html>\n<html>\n<head>\n<title>This is the title of the webpage!</title>\n</head>" \
                    "\n<body>\n<p>This is an example paragraph. Anything in the <strong>body</strong> tag will " \
                    "appear on the page, just like this <strong>p</strong> tag and its contents.</p>\n</body>\n</html>"


def mocked_requests_get(*args):
    class MockResponse:
        def __init__(self, html):
            self.text = html

    if args[0] == "https://test.com":
        return MockResponse(fake_html)


class TestProducer(unittest.TestCase):
    def setUp(self):
        self.html_queue = queue.Queue()

    @patch('link_extractor.requests.get', side_effect=mocked_requests_get)
    @patch("builtins.open", new_callable=mock_open, read_data="https://test.com\n")
    def test_producer_extracts_correctly(self, mocked_get, mocked_open):
        with open("path/to/file") as file:
            producer(self.html_queue, file)
        self.assertEqual(fake_html, self.html_queue.get()[1])


class TestHyperlinkParser(unittest.TestCase):
    def test_parser_finds_link(self):
        parser = HyperlinkParser()
        parser.feed('<a href="https://test.com">')
        self.assertEqual("https://test.com", parser.links[0])

    def test_parser_finds_multiple_links(self):
        parser = HyperlinkParser()
        parser.feed('<a href="https://test.com"><a href="https://google.com">')
        self.assertEqual(["https://test.com", "https://google.com"], parser.links)


class TestConsumer(unittest.TestCase):
    def setUp(self):
        self.html_queue = queue.Queue()

    def test_consumer_extracts_all_links(self):
        output_trap = StringIO()
        old_stdout = sys.stdout
        sys.stdout = output_trap
        self.html_queue.put(("https://input.com", '<a href="https://test.com"><a href="https://google.com">'))
        self.html_queue.put(None)

        consumer(self.html_queue)
        sys.stdout = old_stdout
        self.assertEqual("https://input.com:\n['https://test.com', 'https://google.com']\nConsumer done\n",
                         output_trap.getvalue())
        output_trap.close()


if __name__ == "__main__":
    unittest.main()
