"""Browser navigation backed by a doubly linked list."""

import json
from pathlib import Path

from doubly_linked_list import DoublyLinkedList


class BrowserHistory:
    def __init__(self, homepage, capacity=50):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")

        self.capacity = capacity
        self.dll = DoublyLinkedList()
        self.current = self.dll.append(homepage)

    def visit(self, url, metadata=None):
        if self.current is None:
            self.dll.clear()
        else:
            self.dll.cut_after(self.current)
        self.current = self.dll.append(url, metadata)

        if self.dll.size > self.capacity:
            removed = self.dll.remove_head()
            if removed is self.current:
                self.current = self.dll.head

        return self.current.url

    def back(self, steps):
        if not isinstance(steps, int) or isinstance(steps, bool) or steps < 0:
            raise ValueError("steps must be non-negative")

        node = self.current
        if node is None:
            return None
        while steps > 0 and node.prev is not None:
            node = node.prev
            steps -= 1

        self.current = node
        return self.current.url

    def forward(self, steps):
        if not isinstance(steps, int) or isinstance(steps, bool) or steps < 0:
            raise ValueError("steps must be non-negative")

        node = self.current
        if node is None:
            return None
        while steps > 0 and node.next is not None:
            node = node.next
            steps -= 1

        self.current = node
        return self.current.url

    def current_page(self):
        if self.current is None:
            return None
        return {"url": self.current.url, "metadata": self.current.metadata}

    def export_txt(self, filename):
        """Write history and the current cursor to a readable .txt file."""
        urls = []
        cursor_index = None
        node = self.dll.head
        while node is not None:
            if node is self.current:
                cursor_index = len(urls)
            urls.append({"url": node.url, "metadata": node.metadata})
            node = node.next
        payload = {
            "format": "browser-history-v1",
            "capacity": self.capacity,
            "current_index": cursor_index,
            "history": urls,
        }
        Path(filename).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def import_txt(self, filename):
        """Load a history file after checking its format and entries."""
        payload = json.loads(Path(filename).read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or payload.get("format") != "browser-history-v1":
            raise ValueError("This file is not a supported browser history export")
        items = payload.get("history")
        cursor_index = payload.get("current_index")
        if not isinstance(items, list):
            raise ValueError("History entries must be stored in a list")
        if not items:
            if cursor_index is not None:
                raise ValueError("An empty history must have a null current index")
        elif not isinstance(cursor_index, int) or isinstance(cursor_index, bool) or not 0 <= cursor_index < len(items):
            raise ValueError("The current index is outside the history")
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("url"), str):
                raise ValueError("Each history entry needs a URL string")

        self.dll.clear()
        self.current = None
        # Keep this browser's capacity when loading a file.
        for item in items:
            self.dll.append(item["url"], item.get("metadata"))
        while self.dll.size > self.capacity:
            self.dll.remove_head()
            if cursor_index is not None:
                cursor_index -= 1
        if cursor_index is not None:
            cursor_index = max(0, cursor_index)
            self.current = self.dll.head
            for _ in range(cursor_index):
                self.current = self.current.next
