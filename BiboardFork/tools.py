import pandas as pd
import datetime as dt
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams.update(
    {
        "font.family": "Microsoft YaHei",
        "axes.spines.left": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


def GetDate(date, n):
    return str((dt.datetime.strptime(date, "%Y-%m-%d") + dt.timedelta(days=n)).date())


@st.cache
def convert_df(df):
    return df.to_csv().encode("ansi")


def filterDate(df, start_date, end_date, col="pdate"):
    return df.loc[lambda x: (x[col] >= start_date) & (x[col] <= end_date)]


def greenBlackLinePlot(df, cols=None, showCol=None, isShowCol=False, figSize=(10, 5)):
    if not cols:
        cols = list(df.columns)

    colors = ["#00A752", "black", "red"]
    fig, ax = plt.subplots(figsize=figSize)
    for col, color in zip(cols, colors[: len(cols)]):
        ax.plot(
            df.index,
            df[col],
            marker="o",
            mfc="white",
            ms=5,
            label=col,
            color=color,
            linewidth=3,
        )
    if isShowCol:
        ax.plot(
            df.index,
            df[showCol],
            marker="o",
            mfc="white",
            ms=5,
            label=showCol,
            color="gray",
            linewidth=3,
            linestyle='--'
        )
    ax.legend(edgecolor="white", facecolor="white")
    ax.grid(ls="--", lw=0.25, color="#4E616C")
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_edgecolor("#4E616C")
    ax.xaxis.set_tick_params(
        length=5, color="#4E616C", labelcolor="black", labelsize=9
    )
    ax.yaxis.set_tick_params(
        length=5, color="#4E616C", labelcolor="#4E616C", labelsize=12
    )
    ax.set_xticklabels(df.index, rotation=45)
    return fig, ax
