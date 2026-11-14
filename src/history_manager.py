from browser_history import BrowserHistory

class HistoryManager:
    def __init__(self, browser_history_instance):
        self.browser = browser_history_instance
        self.restore_stack = []

    def display_history(self):
        curr = self.browser.dll.head
        if not curr:
            print("Browsing history is empty.")
            return
            
        print("\n Current Browsing History")
        while curr:
            active = " [<] (active)" if curr == self.browser.current else ""
            print(f"URL: {curr.url} | Metadata: {getattr(curr, 'metadata', 'N/A')}{active}")
            curr = curr.next
        print("--------------------------------\n")

    def delete_history(self):
        self.browser.dll.clear()
        self.browser.current = None
        self.restore_stack.clear()
        print("Entire browsing history has been deleted.")

    def delete_url(self, target_url):
        curr = self.browser.dll.head
        while curr and curr.url != target_url:
            curr = curr.next

        if not curr:
            print(f"URL '{target_url}' not found in history.")
            return

        if curr == self.browser.current:
            self.browser.current = curr.prev or curr.next

        removed_node = self.browser.dll.unlink(curr)
        if removed_node:
            self.restore_stack.append(removed_node)
            print(f"URL '{target_url}' deleted and pushed to restore stack.")

    def restore_node(self):
        if not self.restore_stack:
            print("No deleted history to restore.")
            return

        node = self.restore_stack.pop()
        self.browser.dll.append(node.url, node.metadata)
        print(f"Restored URL '{node.url}' to history.")