import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from browser_history import BrowserHistory
from history_file import export_history, import_history
from history_manager import HistoryManager
from main import main


class HistoryTests(unittest.TestCase):
    def test_back_stops_at_first_page(self):
        browser = BrowserHistory("home")
        browser.visit("news")
        for _ in range(100):
            self.assertEqual(browser.back(1), "home")
        self.assertEqual(browser.forward(1), "news")
        self.assertEqual(browser.back(100), "home")

    def test_visit_from_middle_clears_forward_history(self):
        browser = BrowserHistory("home")
        browser.visit("news")
        browser.visit("sports")
        browser.back(1)
        browser.visit("music")
        self.assertEqual(browser.forward(100), "music")
        self.assertEqual(browser.back(1), "news")
        self.assertEqual(browser.dll.size, 3)

    def test_capacity_removes_oldest_page(self):
        browser = BrowserHistory("home", capacity=2)
        browser.visit("news")
        browser.visit("sports")
        self.assertEqual(browser.current_page()["url"], "sports")
        self.assertEqual(browser.back(100), "news")
        self.assertEqual(browser.dll.size, 2)

    def test_delete_and_restore(self):
        browser = BrowserHistory("home")
        browser.visit("news", {"title": "News"})
        manager = HistoryManager(browser)
        with redirect_stdout(io.StringIO()):
            manager.delete_url("news")
            self.assertEqual(browser.current_page()["url"], "home")
            self.assertEqual(browser.forward(1), "home")
            manager.restore_node()
        self.assertEqual(browser.forward(1), "news")
        self.assertEqual(browser.current_page()["metadata"], {"title": "News"})

    def test_menu_handles_empty_history(self):
        commands = ["home", "clear", "current", "back 100", "forward", "list",
                    "restore", "visit news", "current", "quit"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=commands), redirect_stdout(output):
            main()
        self.assertEqual(output.getvalue().count("History is empty."), 3)
        self.assertIn("Browsing history is empty.", output.getvalue())
        self.assertEqual(output.getvalue().splitlines()[-1], "news")

    def test_text_file_round_trip(self):
        browser = BrowserHistory("home")
        browser.visit("news", {"title": "News"})
        browser.visit("sports")
        browser.back(1)
        loaded = BrowserHistory("placeholder")
        with TemporaryDirectory() as folder:
            path = Path(folder) / "history.txt"
            export_history(browser, path)
            import_history(loaded, path)
        self.assertEqual(loaded.current_page(), browser.current_page())
        self.assertEqual(loaded.forward(1), "sports")
        self.assertEqual(loaded.back(2), "home")
        self.assertEqual(loaded.dll.size, 3)

    def test_empty_history_round_trip(self):
        browser = BrowserHistory("home")
        with redirect_stdout(io.StringIO()):
            HistoryManager(browser).delete_history()
        loaded = BrowserHistory("placeholder")
        with TemporaryDirectory() as folder:
            path = Path(folder) / "empty.txt"
            export_history(browser, path)
            import_history(loaded, path)
        self.assertIsNone(loaded.current)
        self.assertEqual(loaded.dll.size, 0)

    def test_menu_saves_and_loads_history(self):
        output = io.StringIO()
        with TemporaryDirectory() as folder:
            path = Path(folder) / "my history.txt"
            commands = [
                "home", "visit news", "back", f"export {path}",
                "clear", f"import {path}", "current", "forward", "quit",
            ]
            with patch("builtins.input", side_effect=commands), redirect_stdout(output):
                main()
            self.assertTrue(path.is_file())
        self.assertEqual(output.getvalue().splitlines()[-2:], ["home", "news"])

    def test_bad_file_keeps_existing_history(self):
        browser = BrowserHistory("home")
        with TemporaryDirectory() as folder:
            path = Path(folder) / "bad.txt"
            path.write_text('{"pages": [{"url": "news"}], "current_index": 5}', encoding="utf-8")
            with self.assertRaises(ValueError):
                import_history(browser, path)
        self.assertEqual(browser.current_page()["url"], "home")


if __name__ == "__main__":
    unittest.main()
