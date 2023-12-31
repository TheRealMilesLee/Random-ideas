from queue import Queue
from threading import Thread

# A thread that produces data
def producer(out_q):
    while True:
        # Produce some data
        ...
        out_q.put(data)

# A thread that consumes data
def consumer(in_q):
    while True:
# Get some data
        data = in_q.get()
        # Process the data
        ...

# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=consumer, args=(q,))
t2 = Thread(target=producer, args=(q,))
t1.start()
t2.start()
def running():
    # Object that signals shutdown
    _sentinel = object()
    # A thread that produces data
    def producer(out_q):
        while running:
            # Produce some data
            ...
        out_q.put(data)

    # Put the sentinel on the queue to indicate completion
        out_q.put(_sentinel)

# A thread that consumes data
    def consumer(in_q):
        while True:
            # Get some data
            data = in_q.get()

        # Check for termination
            if data is _sentinel:
                in_q.put(_sentinel)
                break

        # Process the data
        ...

from queue import Queue
from threading import Thread

# A thread that produces data
def consumer(out_q):
        while running:
        # Produce some data
            out_q.put(data)

# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data = in_q.get()

        # Process the data
        ...
        # Indicate completion
        in_q.task_done()

# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=consumer, args=(q,))
t2 = Thread(target=producer, args=(q,))
t1.start()
t2.start()

# Wait for all produced items to be consumed
q.join()

from queue import Queue
from threading import Thread, Event

# A thread that produces data
def consumer(out_q):
    while running:
# Produce some data
        ...
# Make an (data, event) pair and hand it to the consumer
        evt = Event()
        out_q.put((data, evt))
        ...
# Wait for the consumer to process the item
        evt.wait()

# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data, evt = in_q.get()
        # Process the data
        ...
        # Indicate completion
        evt.set()

import queue
q = queue.Queue()

try:
    data = q.get(block=False)
except queue.Empty:
    ...

try:
    q.put(item, block=False)
except queue.Full:
    ...

try:
    data = q.get(timeout=5.0)
except queue.Empty:
    ...