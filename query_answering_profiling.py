import os
import sys
import time
import random
import pprint
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from magic_google import MagicGoogle
import trafilatura

import logging
logging.getLogger("trafilatura").setLevel(logging.WARNING)
PROXY = None

# Or MagicGoogle()
mg = MagicGoogle(PROXY)
data = []

questions = [
    "What are the symptoms of Corona Viral illness?",
    "How long does the elected Mayor and the Chairman hold office?",
    "How can I subscribe to Connecticut's emergency alert system?",
    "When was the Corona virus outbreak detected?",
    "Who is Purnendu Mukherjee?"
]

print("Search a question:")
start_time = time.time()
initial_urls = list(mg.search_url(query=questions[0]))
end_time = time.time()
for url in initial_urls:
    print(url)
print("Total time: ", end_time-start_time)

print("Avg time for all question")
total_time = 0
all_urls = []
for question in questions:
    start_time = time.time()
    urls = list(mg.search_url(query=question))
    end_time = time.time()
    total_time += end_time - start_time
    #print(question+": "+urls[0])
    all_urls.append(urls)
print("Total time: ", total_time)
print("Average time: ", (total_time/len(questions)))

print("Time for extracting text from a page: ")
start_time = time.time()
result = trafilatura.extract(trafilatura.fetch_url(
    initial_urls[0]), include_comments=False)
end_time = time.time()
print("Time required for first question: ", (end_time-start_time))

print("Average time for extracting text from the urls...")
total_time = 0
for urls in all_urls:
    start_time = time.time()
    result = trafilatura.extract(
        trafilatura.fetch_url(urls[0]), include_comments=False)
    end_time = time.time()
    total_time += end_time - start_time
print("Total time: ", total_time)
print("Average time: ", (total_time/len(all_urls)))
