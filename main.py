import questionary
from prompt_toolkit.document import Document
from questionary import Validator, ValidationError
from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.controllers import DictationController
from src.core import VocabularyManager
from src.views import Render

vocabulary_manager = VocabularyManager()

render = Render()

def main():
    with render.console.screen() as screen:
        init_layout()
        vocabularies = vocabulary_manager.list_vocabularies()
        show_vocabulary_list(vocabularies)

        selected_idx = select_vocabulary(vocabularies)
        vocabulary = vocabularies[selected_idx]

        controller = DictationController(vocabulary, render)
        controller.start_dictation()

def init_layout():
    layout = Layout(size=20)
    layout.split_column(
        Layout(name="header", size=5),
        Layout(name="content", size=20),
        Layout(name="footer", size=3)
    )

    welcome_text = Text.assemble("Welcome to use ", ("ENWORDS!", "bold red"), "!", justify="center")
    welcome = Panel(welcome_text, padding=1)
    layout["header"].update(welcome)
    footer_text = Text.assemble("Powered by Shawn Niu", justify="right")
    footer = Panel(footer_text)
    layout["footer"].update(footer)

def show_vocabulary_list(vocabularies):
    table = Table(title="Vocabulary List")
    table.add_column("ID", justify="right", style="", no_wrap=True)
    table.add_column("NAME", justify="left", style="green", no_wrap=True)
    table.add_column("COUNT", justify="center", style="red", no_wrap=True)
    for v in vocabularies:
        table.add_row(str(v.idx), v.name, str(len(v.words)))

    render.layout.update_content(Align(table, align="center"))
    render.refresh_screen()

def select_vocabulary(vocabularies):
    idx = questionary.text(f"Please select one vocabulary [{1}/{len(vocabularies)}]",
                           validate=lambda text: validate_index_input(text, len(vocabularies))).ask()
    return int(idx) - 1

def validate_index_input(idx: str, total_count: int):
    if not idx.isdigit():
        return 'Please enter a valid number'
    idx = int(idx)
    valid_range = range(1, total_count + 1)
    if idx not in valid_range:
        return f'Invalid index'
    return True


class IndexTextValidator(Validator):
    def validate(self, document: Document) -> None:
        if len(document.text) == 0:
            raise ValidationError(message="Please enter a valid number")


if __name__ == '__main__':
    main()
