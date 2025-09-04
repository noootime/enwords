from rich.console import RenderableType
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

class BaseLayout:
    def __init__(self):
        self.layout = Layout()
        self.layout.split_column(
            Layout(name="blank", size=1),
            Layout(name="header", size=5),
            Layout(name="content", size=20),
            Layout(name="footer", size=3)
        )
        self.layout["blank"].update("")
        self.update_header(Text.assemble("Welcome to use ", ("ENWORDS!", "bold red"), "!", justify="center"))
        self.update_content("Developing...")
        self.update_footer(Text.assemble("Powered by Shawn Niu", justify="right"))

    def update_content(self, content: RenderableType) -> None:
        self.layout["content"].update(Panel(content))

    def update_header(self, header: RenderableType) -> None:
        self.layout["header"].update(Panel(header, padding=1))

    def update_footer(self, footer: RenderableType) -> None:
        self.layout["footer"].update(Panel(footer))