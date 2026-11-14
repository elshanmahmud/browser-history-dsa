# Browser History Project

A command-line browser history manager built with a from-scratch doubly linked list. It supports back/forward navigation, branching, a configurable capacity, delete/restore, and readable text-file import/export. It uses only the Python standard library.

## Run

Requires Python 3.9 or later.

```powershell
python src/main.py
```

At the prompt, enter a homepage or press Enter for `https://example.com`. Type `help` to see the command list.

## Commands

| Command | Action |
| --- | --- |
| `visit URL` | Visit a page and discard forward history |
| `back N` / `forward N` | Move by N pages; movement stops at either end |
| `current` / `list` | Show the current page or all pages (`[<]` marks the cursor) |
| `delete URL` | Delete the first matching URL and save it for restoration |
| `restore` | Restore the most recently deleted page |
| `clear` | Clear pages and the restore stack |
| `export FILE.txt` / `import FILE.txt` | Save or load history and cursor position |
| `quit` | Exit |

The default history capacity is 50. When capacity is exceeded, the oldest page is removed. If deleting the current page, the cursor moves to its previous page, or to its next page if there is no previous page. Restoring inserts the page before its surviving original next neighbor, otherwise after its surviving previous neighbor. If both are gone, it uses the saved index, clamped to the current list. Restoring does not change the cursor unless the list had no current page.

The `.txt` export contains readable, indented JSON with a `browser-history-v1` format marker, URL/metadata entries, and the cursor index. Import validates the file before replacing the current history. The receiving instance's capacity applies; oldest entries are pruned when needed.

## Test

```powershell
python -m unittest discover -s tests -v
```

The suite covers back 100 times on two pages, branching, capacity pruning, deleting/restoring the current page, empty-history behavior, and import/export round trips.
