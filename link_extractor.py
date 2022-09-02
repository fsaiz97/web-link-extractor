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


def producer(shared_queue, input_file):
    for line in input_file:
        url = line.strip()
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

    print("Producer done")

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
    html_queue = queue.Queue()
    with open("input/urls.txt") as file:
        producer(html_queue, file)
    consumer(html_queue)
