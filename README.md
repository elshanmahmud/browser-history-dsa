# Browser history manager

A small Python project that models browser history with a doubly linked list. Each page links to the one before and after it, and a cursor tracks the current page. You can navigate, branch from an earlier page, delete and restore pages, and save or load history in a `.txt` file. The project uses Python's standard library.

## Run

Requires Python 3.9 or later.

```powershell
python src/main.py
```

Enter a homepage when prompted, or press Enter to start at `https://example.com`. Type `help` to see the commands.

## Commands

| Command | What it does |
| --- | --- |
| `visit URL` | Open a page and remove any forward history |
| `back N` / `forward N` | Move through history, stopping at either end |
| `current` / `list` | Show the current page or the full list; `[<]` marks the current page |
| `delete URL` | Delete the first matching URL and add it to the restore stack |
| `restore` | Bring back the most recently deleted page |
| `clear` | Empty history and the restore stack |
| `export FILE.txt` / `import FILE.txt` | Save or load the pages and cursor position |
| `quit` | Exit the program |

History holds up to 50 pages by default. When it fills, the oldest page is removed. Deleting the current page moves the cursor to the previous page, or to the next page if the deleted page was first. Restore puts a page before its original next neighbor when that page is still present. Otherwise it places the page after its original previous neighbor. If neither neighbor remains, it uses the saved index, limited to the current list length. Clearing history also clears the restore stack.

The `.txt` file contains readable JSON with a `browser-history-v1` format marker, page URLs and metadata, and the current cursor index. Import checks the file before replacing the current history. The receiving browser's capacity applies, so older pages may be dropped during import.

## Run the tests

```powershell
python -m unittest discover -s tests -v
```

The tests cover repeated back navigation, branching, capacity limits, deleting and restoring the current page, empty history, and import/export. They also check that import into a smaller history keeps a valid cursor.
