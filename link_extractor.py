import requests
import queue

from html.parser import HTMLParser


class HyperlinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == "href":
                self.links.append(attr[1])


def producer(shared_queue, input_urls):
    for url in input_urls:
        try:
            print("Extracting HTML from", url)
            extracted_data = requests.get(url).text
        except requests.exceptions.MissingSchema:
            print("Error:", url, "misshapen. Skipping")
        else:
            print("Done")
            print("Queuing HTMl from", url)
            shared_queue.put((url, extracted_data))
            print("Done")

    shared_queue.put(None)


def consumer(shared_queue):
    while True:
        parser = HyperlinkParser()
        item = shared_queue.get()
        if item is None:
            break

        parser.feed(item[1])

        print(item[0], ":\n", parser.links, sep='')

    print("Consumer done")


if __name__ == "__main__":
    urls = ["https://google.com", ]
    html_queue = queue.Queue()
    producer(html_queue, urls)
    consumer(html_queue)
