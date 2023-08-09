import datetime

import numpy as np
import pandas as pd

import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import connection
from pyecharts import options as opts

# from pyecharts import types
from pyecharts.charts import (
    Calendar,
    EffectScatter,
    Gauge,
    HeatMap,
    Line,
    Scatter,
    Timeline,
)
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker
from pyecharts.globals import SymbolType
from streamlit_echarts import st_echarts, st_pyecharts

import streamlit as st

WATER_COLOR = "#566D74"
MIN_DATE = datetime.date(year=2030, month=4, day=1)
N_DAYS = 2549
DATE_RANGE = pd.DataFrame(
    {
        "date": pd.date_range(start=MIN_DATE, periods=N_DAYS).date,
        "day": range(1, N_DAYS + 1),
    }
)
st.set_page_config(
    layout="wide",
    page_icon="streamlit/assets/fire_icon.png",
    page_title="Save Zakar",
)


def main(con):
    with st.sidebar:
        _, mid, _ = st.columns([2, 5, 2])
        with mid:
            fire_icon(150)
        st.caption("By Kristian André Jakobsen & Alessandra Oshiro")

    left, center, _ = st.columns([1, 5, 1])
    with center:
        st.header("Fire Alert System Year by Year")
        st.write(
            """As you can see on the animated map below, our fire alert system is
                almost always right when it does predict there will be a fire, but 
                it has a lot of room for improvement! There are still too many 
                wildfires that go undetected leaving the people of Zakar at a risk."""
        )
    _, center, _ = st.columns([1, 8, 1])
    with center:
        choice = st.radio("Yearly Wildfires", ("Warnings", "Actual"))
        if choice == "Warnings":
            chosen_df = fetch_sql(
                con,
                sql="""
                    SELECT
                        *
                    FROM raw.predictions;""",
            )
            symbol_url = "https://i.imgur.com/vqqZ4bq.png"
        else:
            chosen_df = fetch_sql(
                con,
                sql="""
                    SELECT
                        *
                    FROM raw.fire_alerts;""",
                day_col="event_day",
            )
            symbol_url = "https://media.tenor.com/8McIGu0Tf_QAAAAi/fire-joypixels.gif"
        st_pyecharts(
            plot_heatmap(chosen_df, symbol_url),
            width=1200 * 0.78,
            height=900 * 0.78,
        )


def plot_heatmap(df, url):
    df["year"] = pd.to_datetime(df["date"]).dt.year
    t = Timeline(opts.InitOpts(width=300)).add_schema(pos_bottom=-20, is_auto_play=True)
    for year in df["year"].unique():
        h = (
            HeatMap()
            .add_xaxis(range(30))
            .add_yaxis(
                "series0",
                range(30),
                [[i, j, 0] for i in range(30) for j in range(30)],
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(
                    opacity=0, border_width=2, border_color="#fff"
                ),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    # title="Choose a location on the map", pos_top=-10, pos_right="middle",
                    is_show=False
                ),
                legend_opts=opts.LegendOpts(is_show=False),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                xaxis_opts=opts.AxisOpts(
                    is_show=False,
                    type_="category",
                    axisline_opts=opts.AxisLineOpts(is_show=False),
                    axispointer_opts=opts.AxisPointerOpts(
                        is_show=False,
                        type_="shadow",
                        linestyle_opts=opts.LineStyleOpts(type_="dashed"),
                        label="",
                    ),
                ),
                yaxis_opts=opts.AxisOpts(
                    is_show=False,
                    type_="category",
                    axisline_opts=opts.AxisLineOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                    axispointer_opts=opts.AxisPointerOpts(
                        is_show=False, type_="shadow"
                    ),
                ),
                visualmap_opts=opts.VisualMapOpts(
                    is_show=False,
                    pos_left="center",
                    pos_top="5",
                    # pos_right="50",
                    orient="horizontal",
                    min_=-30,
                    max_=150,
                    range_size=2,
                    range_text=["Hot", "Freezing"],
                    is_piecewise=False,
                ),
                graphic_opts=[
                    opts.GraphicImage(
                        graphic_item=opts.GraphicItem(
                            id_="logo",
                            right=0,
                            # left=0,
                            # top=40,
                            z=-10,
                            bounding="raw",
                            origin=[0, 0],
                        ),
                        graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
                            image="https://i.imgur.com/Qq3UJE9.png",
                            width=1200 * 0.80,
                            height=900 * 0.80,
                            # opacity=0.4,
                        ),
                    )
                ],
            )
        )
        s = (
            EffectScatter()
            .add_xaxis(df.query(f"year == {year}")["geospatial_x"])
            .add_yaxis(
                "",
                df.query(f"year == {year}")["geospatial_y"],
                symbol=f"image://{url}",
                symbol_size=20,
                effect_opts=opts.EffectOpts(period=2, scale=2, trail_length=0.9),
            )
            .set_global_opts(title_opts=opts.TitleOpts(is_show=False))
        )
        t.add(h.overlap(s), year)

    return t


@st.cache_resource
def init_connection() -> connection:
    return psycopg2.connect(**st.secrets["postgres"])


@st.cache_data
def fetch_sql(
    _connection: connection,
    sql: str,
    parameters: dict[str, str | int] = {},
    day_col="day",
) -> pd.DataFrame:
    # try:
    with _connection:
        df = pd.read_sql(sql, _connection, params=parameters).rename(
            columns={day_col: "day"}
        )
        df = df.merge(DATE_RANGE, how="left").sort_values("day")
        return df
    # finally:
    #     _connection.commit()


def fire_icon(width=50):
    st.image(
        "https://i.imgur.com/Q06cnvr.gif",
        width=width,
    )


if __name__ == "__main__":
    con = init_connection()
    main(con)
