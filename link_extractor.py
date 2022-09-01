import requests
import queue


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
            shared_queue.put(extracted_data)
            print("Done")

    shared_queue.put(None)


if __name__ == "__main__":
    urls = ["https://google.com", ]
    html_queue = queue.Queue()
    producer(html_queue, urls)
