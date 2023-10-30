from __future__ import annotations

from math import floor
from pathlib import Path
from typing import Any

import pandas as pd
import plotly

plotly.io.kaleido.scope.mathjax = None


def plot_dataframe(
    df: pd.Series | pd.DataFrame,
    print_index: bool = True,
    title: dict | None = None,
    tbl_header_visible: bool = True,
    tbl_header: dict | None = None,
    tbl_cells: dict | None = None,
    row_fill_colors: list[str] | None = None,
    col_width: int | float | list[int | float] | None = None,
    fig_size: tuple[int, int] | None = None,
    show_fig: bool = True,
    plotly_renderer: str = "png",
    **layout_kwargs: Any,
) -> plotly.graph_objects.Figure:
    def _alternate_row_colors() -> list[str] | None:
        color_list = None
        # alternate row colors
        row_count = len(df)
        if row_fill_colors is not None:
            color_list = row_fill_colors

        return color_list

    def _tbl_values() -> tuple[list[str], list[str]]:
        if print_index:
            header_values = [
                "<b>" + x + "<b>"
                for x in [
                    df.index.name if df.index.name is not None else "",
                    *df.columns,
                ]
            ]
            cell_values = [df.index, *[df[col] for col in df]]
        else:
            header_values = ["<b>" + x + "<b>" for x in df.columns.to_list()]
            cell_values = [df[col] for col in df]

        return header_values, cell_values

    row_color_list = _alternate_row_colors()
    header_vals, cell_vals = _tbl_values()

    if not tbl_header:
        tbl_header = {}
    tbl_header.update(values=header_vals)

    if not tbl_header_visible:
        tbl_header.update(
            fill_color="white", font_color="white", line_color="white", height=1
        )

    if not tbl_cells:
        tbl_cells = {}
    tbl_cells.update(
        values=cell_vals,
        fill_color=[row_fill_colors] * len(df) if row_fill_colors else tbl_cells.get("fill_color"),
    )

    fig = plotly.graph_objs.Figure(
        data=[plotly.graph_objs.Table(header=tbl_header, cells=tbl_cells)]
    )

    fig.data[0]["columnwidth"] = col_width if col_width else None

    if not title:
        title = {}
    title.update(
        x=0.01 if title.get("x") is None else title.get("x"),
        xanchor="left" if title.get("xanchor") is None else title.get("xanchor"),
    )

    fig.update_layout(
        title=title,
        margin={
            "autoexpand": False,
            "b": 5,
            "l": 5,
            "r": 5,
            "t": 40 if title.get("text") else 5,
        },
        width=fig_size[0] if fig_size else None,
        height=fig_size[1] if fig_size else None,
        autosize=False if col_width else None,
        **layout_kwargs,
    )

    if show_fig:
        fig.show(renderer=plotly_renderer)

    return fig


def save_dataframe(fig: plotly.graph_objects.Figure, filename: Path) -> None:
    fig.write_image(filename)

    return None
