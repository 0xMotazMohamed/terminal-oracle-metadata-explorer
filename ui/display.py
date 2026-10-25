"""
ui/display.py

Turns query results into text on the screen.
"""

import config


def _format_cell(value):
    """Make one value printable: None -> '-', one line only, not too wide."""
    if value is None:
        return "-"
    text = str(value).replace("\r", " ").replace("\n", " ").strip() # converts numbers and dates to text
    
    if len(text) > config.MAX_CELL_WIDTH: # Validation for Text longer is cut.
        text = text[: config.MAX_CELL_WIDTH - 3] + "..."
    return text


def print_table(columns, rows):
    """Print rows as an aligned table with a header line."""
    if not rows:
        print("\nNo data found.")
        return

    table = [[ _format_cell(value) for value in row] for row in rows]

    # Each column is as wide as its longest cell (or its header).
    widths = [len(name) for name in columns]
    for row in table:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    print()
    print(" | ".join(name.ljust(w) for name, w in zip(columns, widths)))
    print("-+-".join("-" * w for w in widths))
    for row in table:
        print(" | ".join(cell.ljust(w) for cell, w in zip(row, widths)))

    print(f"\n{len(rows)} row(s)")
    if len(rows) >= config.MAX_ROWS:
        print(f"(output limited to {config.MAX_ROWS} rows)")


def print_text(rows):
    """Print the first value of the first row as raw text (e.g. a view's SQL)."""
    if not rows:
        print("\nNo data found.")
        return
    print()
    print(str(rows[0][0]).strip())