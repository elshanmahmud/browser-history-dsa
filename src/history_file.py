"""Save and load browser history as JSON in a text file."""

import json
from pathlib import Path

from doubly_linked_list import DoublyLinkedList


def text_path(filename):
    path = Path(filename)
    if path.suffix.lower() != ".txt":
        raise ValueError("Choose a file ending in .txt.")
    return path


def export_history(browser, filename):
    path = text_path(filename)
    pages = []
    current_index = None
    node = browser.dll.head
    while node is not None:
        if node is browser.current:
            current_index = len(pages)
        pages.append({"url": node.url, "metadata": node.metadata})
        node = node.next

    data = {"pages": pages, "current_index": current_index}
    contents = json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False)
    path.write_text(contents + "\n", encoding="utf-8")


def import_history(browser, filename):
    data = json.loads(text_path(filename).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("pages"), list):
        raise ValueError("The file needs a list of history pages.")

    pages = data["pages"]
    current_index = data.get("current_index")
    if pages:
        if type(current_index) is not int or not 0 <= current_index < len(pages):
            raise ValueError("The current page position is outside the history.")
    elif current_index is not None:
        raise ValueError("Empty history cannot have a current page.")

    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get("url"), str):
            raise ValueError("Each page needs a URL stored as text.")

    # Keep the newest pages if this session has a smaller limit.
    first_page = max(0, len(pages) - browser.capacity)
    if current_index is not None:
        current_index = max(first_page, current_index)

    history = DoublyLinkedList()
    current = None
    for index in range(first_page, len(pages)):
        page = pages[index]
        node = history.append(page["url"], page.get("metadata"))
        if index == current_index:
            current = node

    browser.dll = history
    browser.current = current
