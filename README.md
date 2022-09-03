# web-link-extractor

This is a simple web scraper that sends a get request to a website and then extracts all hyperlinks from the website.
It works with a producer-consumer model, implemented as two functions that run concurrently on
threads.

The producer sends the html it finds to a shared thread-safe queue and the consumer
takes each html page from the queue and parses it to find href attributes in tags.
It puts all hyperlinks from a particular website into a list,
which is output to a file along with the url that the list of links came from.

The script handles schema, connection and timeout errors, printing the error to the terminal and skipping the
broken url. There are a few unit tests to ensure the producer and consumer work as expected.

The dist folder contains an exe to run the script on Windows without needing python. The exe currently
doesn't work by double-clicking, you must run it from a command line.

To run the unit tests, you should have python installed, then run one of the activate scripts in venv\scripts
and then run the test_link_extractor.py script.