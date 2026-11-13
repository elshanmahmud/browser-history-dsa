class Node:
    def __init__(self, url, metadata):
        self.url = url
        self.metadata = metadata
        self.prev = None
        self.next = None