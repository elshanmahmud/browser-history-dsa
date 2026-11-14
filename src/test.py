from browser_history import BrowserHistory
from history_manager import HistoryManager

bh = BrowserHistory("google.com")
bh.visit("github.com", {"type": "code"})
bh.visit("stackoverflow.com", {"type": "q&a"})

manager = HistoryManager(bh)

manager.display_history()
manager.delete_url("github.com")
manager.display_history()
manager.restore_node()
manager.display_history()