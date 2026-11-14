"""Command-line interface for browser history."""

from browser_history import BrowserHistory
from history_manager import HistoryManager


def run():
    homepage = input("Homepage URL [https://example.com]: ").strip() or "https://example.com"
    browser = BrowserHistory(homepage)
    manager = HistoryManager(browser)
    print("Browser history. Type 'help' to see the commands.")
    while True:
        command = input("\nhistory> ").strip()
        if not command:
            continue
        parts = command.split(maxsplit=1)
        action = parts[0].lower()
        argument = parts[1].strip() if len(parts) > 1 else ""
        try:
            if action in {"quit", "exit", "q"}:
                print("Goodbye.")
                return
            if action == "help":
                print("visit URL | back N | forward N | current | list | delete URL | restore | clear | export FILE.txt | import FILE.txt | quit")
            elif action == "visit":
                if not argument:
                    print("Usage: visit URL")
                else:
                    print(f"Visited {browser.visit(argument)}")
            elif action in {"back", "forward"}:
                steps = int(argument or "1")
                page = browser.back(steps) if action == "back" else browser.forward(steps)
                print(f"Current page: {page}" if page is not None else "History is empty.")
            elif action == "current":
                page = browser.current_page()
                print(f"Current page: {page['url']} | Metadata: {page['metadata']}" if page else "History is empty.")
            elif action in {"list", "history"}:
                manager.display_history()
            elif action == "delete":
                if not argument:
                    print("Usage: delete URL")
                elif not manager.delete_url(argument):
                    print(f"No history entry found for '{argument}'.")
            elif action == "restore":
                manager.restore_node()
            elif action in {"clear", "delete-all"}:
                manager.delete_history()
            elif action == "export":
                if not argument:
                    print("Usage: export FILE.txt")
                else:
                    browser.export_txt(argument)
                    print(f"History exported to {argument}")
            elif action == "import":
                if not argument:
                    print("Usage: import FILE.txt")
                else:
                    browser.import_txt(argument)
                    manager.restore_stack.clear()
                    print(f"History imported from {argument}")
            else:
                print("Unknown command. Type 'help' to see the available commands.")
        except (ValueError, OSError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    run()
