import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from browser_history import BrowserHistory
from history_manager import HistoryManager


def urls(browser):
    result = []
    node = browser.dll.head
    while node:
        result.append(node.url)
        node = node.next
    return result


class BrowserHistoryTests(unittest.TestCase):
    def test_back_one_hundred_times_on_two_pages_stops_at_homepage(self):
        browser = BrowserHistory("home")
        browser.visit("page")
        self.assertEqual(browser.back(100), "home")
        self.assertEqual(browser.current_page()["url"], "home")

    def test_branching_from_middle_discards_forward_pages(self):
        browser = BrowserHistory("a")
        browser.visit("b")
        browser.visit("c")
        browser.back(1)
        browser.visit("d")
        self.assertEqual(urls(browser), ["a", "b", "d"])
        self.assertEqual(browser.forward(10), "d")

    def test_capacity_prunes_oldest_and_keeps_cursor_valid(self):
        browser = BrowserHistory("a", capacity=3)
        for url in ["b", "c", "d"]:
            browser.visit(url)
        self.assertEqual(urls(browser), ["b", "c", "d"])
        self.assertEqual(browser.current_page()["url"], "d")
        self.assertEqual(browser.back(100), "b")

    def test_delete_current_and_restore_original_position(self):
        browser = BrowserHistory("a")
        browser.visit("b", {"kind": "test"})
        browser.visit("c")
        manager = HistoryManager(browser)
        self.assertTrue(manager.delete_url("b"))
        self.assertEqual(browser.current_page()["url"], "c")
        self.assertTrue(manager.restore_node())
        self.assertEqual(urls(browser), ["a", "b", "c"])
        self.assertEqual(browser.current_page()["url"], "c")
        self.assertEqual(browser.dll.head.next.metadata, {"kind": "test"})

    def test_delete_history_empty_state_and_new_visit(self):
        browser = BrowserHistory("home")
        manager = HistoryManager(browser)
        manager.delete_history()
        self.assertIsNone(browser.current_page())
        self.assertIsNone(browser.back(100))
        self.assertIsNone(browser.forward(0))
        browser.visit("new")
        self.assertEqual(browser.current_page()["url"], "new")

    def test_txt_export_import_round_trip_keeps_cursor_and_metadata(self):
        browser = BrowserHistory("a")
        browser.visit("b", {"tag": "two"})
        browser.visit("c")
        browser.back(1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.txt"
            browser.export_txt(path)
            restored = BrowserHistory("placeholder")
            restored.import_txt(path)
        self.assertEqual(urls(restored), ["a", "b", "c"])
        self.assertEqual(restored.current_page(), {"url": "b", "metadata": {"tag": "two"}})
        self.assertEqual(restored.forward(1), "c")

    def test_import_into_smaller_capacity_prunes_oldest_and_clamps_cursor(self):
        source = BrowserHistory("a")
        source.visit("b")
        source.visit("c")
        source.back(2)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.txt"
            source.export_txt(path)
            target = BrowserHistory("placeholder", capacity=2)
            target.import_txt(path)
        self.assertEqual(urls(target), ["b", "c"])
        self.assertEqual(target.current_page()["url"], "b")

    def test_delete_all_leaves_no_restorable_pages(self):
        browser = BrowserHistory("a")
        manager = HistoryManager(browser)
        manager.delete_url("a")
        manager.delete_history()
        self.assertFalse(manager.restore_node())
        self.assertEqual(urls(browser), [])


if __name__ == "__main__":
    unittest.main()
