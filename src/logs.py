from typing import Any

import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()


def print_info(content: Any) -> None:
    console.print(f"[cyan]{content}[/cyan]")


def print_warning(content: Any) -> None:
    console.print(f"[yellow]{content}[/yellow]")


def print_error(content: Any) -> None:
    console.print(f"[red]{content}[/red]")


def print_df_as_table(df: pd.DataFrame) -> None:
    console = Console()
    table = Table(show_header=True, header_style="bold cyan")

    for column in df.columns:
        table.add_column(str(column))

    for _, row in df.iterrows():  # type: ignore
        rich_row: list[Any] = []
        for value in row:  # type: ignore
            if isinstance(value, str) and value.startswith("http"):
                text = Text(text=value, style="underline magenta", justify="left")
                text.stylize(style="link " + value)
                rich_row.append(text)
            else:
                rich_row.append(str(value))  # type: ignore

        table.add_row(*rich_row)
    console.print(table)
