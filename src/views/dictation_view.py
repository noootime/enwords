from rich.table import Table
from src.models.word_grid import WordGrid
from src.views.viewport import ViewportCalculator

class DictationTableView:

    def __init__(self, word_grid: WordGrid, viewport_size: int = 8, cols: int = 6):
        self.word_grid = word_grid
        self.viewport_size = viewport_size
        self.cols = cols

    def create_table(self, focus_index: int = 0) -> Table:
        focus_row, _ = self.word_grid.get_position(focus_index)
        grid_data = self.word_grid.get_grid()
        total_rows = len(grid_data)

        start_row, end_row = ViewportCalculator.calculate_viewport(
            focus_row, total_rows, self.viewport_size
        )

        table = Table(show_header=False, leading=True, expand=False)
        column_width = 12
        no_wrap = True

        for i in range(self.cols):
            table.add_column(f"{i + 1:02d}", no_wrap=no_wrap, width=column_width)

        for row_data in grid_data[start_row:end_row]:
            while len(row_data) < self.cols:
                row_data.append("")
            table.add_row(*row_data)

        return table


