from rich.console import Console
from src.views.base_view import BaseLayout


class Render:
    def __init__(self):
        self.console = Console()
        self.layout = BaseLayout()

    def refresh_screen(self):
        self.console.clear()
        self.console.print(self.layout.layout)