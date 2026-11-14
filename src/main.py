"""Run the browser history command prompt."""

from browser_history import BrowserHistory
from history_manager import HistoryManager
from history_file import export_history, import_history


COMMANDS = (
    "visit URL | back [N] | forward [N] | current | list\n"
    "delete URL | restore | clear | export FILE.txt | import FILE.txt | quit"
)


def main():
    try:
        homepage = input("Homepage [example.com]: ").strip() or "example.com"
        browser = BrowserHistory(homepage)
        manager = HistoryManager(browser)
        print("Type help to see the commands.")

        while True:
            parts = input("history> ").strip().split(maxsplit=1)
            if not parts:
                continue
            command = parts[0].lower()
            argument = parts[1] if len(parts) == 2 else ""

            if command == "quit":
                return
            if command == "help":
                print(COMMANDS)
            elif command == "visit" and argument:
                print(browser.visit(argument))
            elif command in {"back", "forward", "current"}:
                if browser.current is None:
                    print("History is empty.")
                elif command == "current":
                    print(browser.current_page()["url"])
                else:
                    try:
                        steps = int(argument) if argument else 1
                        move = browser.back if command == "back" else browser.forward
                        print(move(steps))
                    except ValueError:
                        print("Enter a whole number of steps, zero or more.")
            elif command == "list":
                manager.display_history()
            elif command == "delete" and argument:
                manager.delete_url(argument)
            elif command == "restore":
                manager.restore_node()
                if browser.current is None:
                    browser.current = browser.dll.head
            elif command == "clear":
                manager.delete_history()
            elif command in {"export", "import"}:
                if not argument:
                    print(f"Usage: {command} FILE.txt")
                    continue
                try:
                    if command == "export":
                        export_history(browser, argument)
                        print(f"Saved history to {argument}.")
                    else:
                        import_history(browser, argument)
                        manager.restore_stack.clear()
                        print(f"Loaded history from {argument}.")
                except (OSError, ValueError, TypeError) as error:
                    print(f"Could not {command} history: {error}")
            elif command in {"visit", "delete"}:
                print(f"Usage: {command} URL")
            else:
                print("Unknown command. Type help to see the commands.")
    except (EOFError, KeyboardInterrupt):
        print()


if __name__ == "__main__":
    main()
