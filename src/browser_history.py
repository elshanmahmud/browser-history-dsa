from doubly_linked_list import DoublyLinkedList


class BrowserHistory:
    def __init__(self, homepage, capacity=50):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")

        self.capacity = capacity
        self.dll = DoublyLinkedList()
        self.current = self.dll.append(homepage)

    def visit(self, url, metadata=None):
        self.dll.cut_after(self.current)
        self.current = self.dll.append(url, metadata)

        if self.dll.size > self.capacity:
            self.dll.remove_head()

        return self.current.url

    def back(self, steps):
        if steps < 0:
            raise ValueError("steps must be non-negative")

        node = self.current
        while steps > 0 and node.prev is not None:
            node = node.prev
            steps -= 1

        self.current = node
        return self.current.url

    def forward(self, steps):
        if steps < 0:
            raise ValueError("steps must be non-negative")

        node = self.current
        while steps > 0 and node.next is not None:
            node = node.next
            steps -= 1

        self.current = node
        return self.current.url

    def current_page(self):
        return {"url": self.current.url, "metadata": self.current.metadata}