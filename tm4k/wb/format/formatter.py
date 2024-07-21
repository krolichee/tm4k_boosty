from openpyxl.cell.cell import Cell
class Formatter:
    format_list = {}
    style = {}

    # @trace
    def apply(self, cell: Cell):
        for k, v in self.format_list.items():
            cell.__setattr__(k, v)

    def __init__(self, format_list):
        self.format_list = format_list