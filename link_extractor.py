import requests
import queue
from threading import Thread
import sys

from html.parser import HTMLParser


class HyperlinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == "href":
                self.links.append(attr[1])


def producer(shared_queue, input_path):
    with open(input_path) as input_file:
        for line in input_file:
            url = line.strip()
            try:
                print("Producer - Extracting HTML from", url)
                extracted_data = requests.get(url, timeout=(3.10, 5)).text
            except requests.exceptions.MissingSchema:
                print("Producer - Error (", url, "): Schema missing. Skipping...", sep="", file=sys.stderr)
            except requests.exceptions.ConnectTimeout:
                print("Producer - Error (", url, "): Timeout while trying to connect. Skipping...", sep="", file=sys.stderr)
            except requests.exceptions.ConnectionError:
                print("Producer - Error (", url, "): Connection failed. Skipping...", sep="", file=sys.stderr)
            else:
                print("Producer - Extraction done")
                print("Producer - Queuing HTMl from", url)
                shared_queue.put((url, extracted_data))
                print("Producer - Queuing done")

    print("Producer done")

    shared_queue.put(None)


def consumer(shared_queue, output_file):
    while True:
        parser = HyperlinkParser()
        item = shared_queue.get()
        if item is None:
            break

        print("Consumer - Parsing HTML from", item[0])
        parser.feed(item[1])
        print("Consumer - Parser done")

        print(item[0], ":\n", parser.links, sep='', file=output_file)
        print("Consumer -", item[0], "links outputted")

    print("Consumer done")


if __name__ == "__main__":
    html_queue = queue.Queue()
    input_path = "files/input.txt"

    producer = Thread(target=producer, args=(html_queue, input_path))
    producer.start()

    output_file = open("files/output.txt", 'w')
    consumer = Thread(target=consumer, args=(html_queue, output_file))
    consumer.start()

    producer.join()
    producer.join()

    output_file.close()
