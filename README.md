# Browser history manager

This Python program stores browser history in a doubly linked list. Each page has links to the previous and next pages. The cursor keeps track of which page you are on.

You can move through your history, visit a new page after going back, or delete and restore pages. You can also save history to a `.txt` file and load it later. No extra Python packages are needed.

## Run

Use Python 3.9 or later. Run this command from the project folder:

```powershell
python src/main.py
```

Enter a homepage when prompted, or press Enter to start at `https://example.com`. Type `help` to see the commands.

## Commands

| Command | What it does |
| --- | --- |
| `visit URL` | Add a page to history and remove any forward history |
| `back N` / `forward N` | Move through history, stopping at either end |
| `current` / `list` | Show the current page or the full list; `[<]` marks the current page |
| `delete URL` | Delete the first matching URL and add it to the restore stack |
| `restore` | Bring back the most recently deleted page |
| `clear` | Empty history and the restore stack |
| `export FILE.txt` / `import FILE.txt` | Save or load the pages and cursor position |
| `quit` | Exit the program |

History holds 50 pages by default. Adding another page removes the oldest one.

If you delete the current page, the cursor moves to the previous page. If there is no previous page, it moves to the next one.

Restore brings back the last page you deleted. It goes before the page that originally followed it, if that page is still in history. Otherwise, it goes after the page that originally came before it. If both pages are gone, restore uses the saved position or the end of the list if the list is now shorter. Clearing history also empties the restore stack.

Export saves readable JSON inside the `.txt` file. It includes the `browser-history-v1` format marker, URLs, metadata, and the position of the current page. Import checks these entries before replacing history. If the file has more pages than the browser can hold, import removes the oldest ones.

## Run the tests

```powershell
python -m unittest discover -s tests -v
```

The tests check navigation past the first page, visiting a new page from the middle of history, and removing old pages when history is full. They also cover deleting and restoring a page, clearing history, and saving and loading files. A separate case checks what happens when an imported file has more pages than the browser can hold.
