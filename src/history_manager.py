"""History display, deletion, and LIFO restoration helpers."""


class HistoryManager:
    def __init__(self, browser_history_instance):
        self.browser = browser_history_instance
        # Each entry keeps the original neighbors so restore can return a page
        # to its former position whenever at least one neighbor still exists.
        self.restore_stack = []

    def display_history(self):
        """Return readable rows and print them for compatibility with the demo."""
        rows = []
        node = self.browser.dll.head
        while node is not None:
            marker = " [<] (active)" if node is self.browser.current else ""
            rows.append(f"URL: {node.url} | Metadata: {node.metadata!r}{marker}")
            node = node.next
        if not rows:
            rows = ["Browsing history is empty."]
        print("\nCurrent Browsing History")
        print("\n".join(rows))
        print("------------------------------\n")
        return rows

    def delete_history(self):
        self.browser.dll.clear()
        self.browser.current = None
        self.restore_stack.clear()
        print("Entire browsing history has been deleted.")

    def delete_url(self, target_url):
        node = self.browser.dll.head
        index = 0
        while node is not None and node.url != target_url:
            node = node.next
            index += 1
        if node is None:
            return False

        previous, following = node.prev, node.next
        self.restore_stack.append({
            "url": node.url,
            "metadata": node.metadata,
            "previous": previous,
            "following": following,
            "index": index,
        })
        if node is self.browser.current:
            self.browser.current = previous or following
        self.browser.dll.unlink(node)
        print(f"URL '{target_url}' deleted and saved for restore.")
        return True

    def _contains(self, target):
        node = self.browser.dll.head
        while node is not None:
            if node is target:
                return True
            node = node.next
        return False

    def restore_node(self):
        if not self.restore_stack:
            print("No deleted history to restore.")
            return False

        record = self.restore_stack.pop()
        dll = self.browser.dll
        node = None
        previous = record["previous"]
        following = record["following"]
        if following is not None and self._contains(following):
            # Insert directly before the surviving next neighbor.
            node = dll.append(record["url"], record["metadata"])
            dll.unlink(node)
            prev = following.prev
            node.prev, node.next = prev, following
            following.prev = node
            if prev is not None:
                prev.next = node
            else:
                dll.head = node
            dll.size += 1
        elif previous is not None and self._contains(previous):
            node = dll.append(record["url"], record["metadata"])
            dll.unlink(node)
            node.prev, node.next = previous, previous.next
            if previous.next is not None:
                previous.next.prev = node
            else:
                dll.tail = node
            previous.next = node
            dll.size += 1
        else:
            # Both original neighbors are gone: restore at the saved index,
            # clamped to the current list length.
            node = dll.append(record["url"], record["metadata"])
            dll.unlink(node)
            insertion_index = min(record["index"], dll.size)
            if insertion_index == dll.size:
                node.prev = dll.tail
                if dll.tail is not None:
                    dll.tail.next = node
                else:
                    dll.head = node
                dll.tail = node
            else:
                following = dll.head
                for _ in range(insertion_index):
                    following = following.next
                node.prev, node.next = following.prev, following
                if following.prev is not None:
                    following.prev.next = node
                else:
                    dll.head = node
                following.prev = node
            dll.size += 1

        if dll.size > self.browser.capacity:
            removed = dll.remove_head()
            if self.browser.current is None:
                self.browser.current = dll.head
            elif self.browser.current is removed:
                self.browser.current = dll.head
        if self.browser.current is None:
            self.browser.current = node
        print(f"Restored URL '{record['url']}' to its prior position when possible.")
        return True
