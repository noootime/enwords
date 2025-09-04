from typing import Tuple


class ViewportCalculator:

    @staticmethod
    def calculate_viewport(focus_row: int, total_rows: int, viewport_size: int = 8) -> Tuple[int, int]:
        if total_rows <= viewport_size:
            return 0, total_rows

        ideal_start = focus_row - (viewport_size - 2)
        start_row = max(0, min(ideal_start, total_rows - viewport_size))
        end_row = min(start_row + viewport_size, total_rows)

        return start_row, end_row