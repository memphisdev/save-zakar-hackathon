import random

import pandas as pd
import plotly.express as px
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import connection
from pyecharts import options as opts
from pyecharts.charts import EffectScatter, Gauge, HeatMap, Line
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker
from pyecharts.globals import SymbolType
from streamlit_echarts import st_echarts, st_pyecharts

import streamlit as st

WATER_COLOR = "#566D74"


st.set_page_config(layout="wide")


def main(con: connection) -> None:
    st.header("Save Zakar Hackathon!")
    temp = fetch_sql(
        con,
        sql="""
            SELECT
                *
            FROM raw.temperature_readings;""",
    )
    tweets = fetch_sql(
        con,
        """
        WITH top_tweets AS (
            SELECT
                t.geospatial_x,
                t.geospatial_y,
                t.tweet,
                ROW_NUMBER() OVER(PARTITION BY
                    t.geospatial_x,
                    t.geospatial_y
                ORDER BY t.day DESC) AS rank
        FROM raw.tweets t)
    SELECT * FROM top_tweets WHERE rank <= 3""",
    )
    st.dataframe(tweets)
    l, left, right, r = st.columns([1, 35, 35, 1], gap="small")
    h = plot_heatmap(temp)
    with left:
        values = st_pyecharts(
            h,
            events={"click": "function(params) {return params.value}"},
            width=700,
            height=500,
        )
        geo = values[:2] if values else [0, 0]
        st.text(f"Currently selected coordinates: {geo[0], geo[1]}")
        df_filtered = temp.query(f"(geospatial_x=={geo[0]}) & (geospatial_y=={geo[1]})")

    with right:
        inner_left, inner_right = st.columns([0.1, 0.9])
        with inner_left:
            tweet_icon()
        with inner_right:
            st.subheader("Tweets")
        st.write("---")
        st.write(tweets.iloc[0, 2])
        st.write("---")
        st.write(tweets.iloc[1, 2])
        st.write("---")
        st.write(tweets.iloc[2, 2])
        st.write("---")
    st.empty()
    st_pyecharts(
        plot_line(df_filtered, geo),
        # height=300,
        # width=700,
    )


def tweet_icon(width=50):
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Logo_of_Twitter.svg/512px-Logo_of_Twitter.svg.png?20220821125553",
        width=width,
    )


def fire_icon(width=50):
    st.image(
        "https://media.tenor.com/8McIGu0Tf_QAAAAi/fire-joypixels.gif",
        width=width,
    )


def plot_heatmap(df):
    return (
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
            title_opts=opts.TitleOpts(is_show=False),
            legend_opts=opts.LegendOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(
                is_show=False,
                type_="category",
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True,
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
                axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
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
                        width=700,
                        height=500,
                        # opacity=0.4,
                    ),
                )
            ],
        )
    )

    return h
    # df2 = df[df["day"] == name]
    # with center:
    #     st.dataframe(df)
    # st.write(df2)


def plot_line(df, geo) -> Line:
    start_date = pd.to_datetime("01-04-2030")
    return (
        Line(
            init_opts=opts.InitOpts(
                animation_opts=opts.AnimationOpts(
                    animation_duration_update=500, animation_duration=2000
                )
            )
        ).add_xaxis(pd.date_range(start=start_date, periods=df["day"].max()))
        # .add_xaxis([1, 2, 3])
        .add_yaxis(
            series_name="°F",
            y_axis=df["temperature"],
            symbol_size=1,
            # is_symbol_show=False,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            color="#FF5733",
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="Mean Temperature")],
                is_silent=False,
                precision=1,
                linestyle_opts=opts.LineStyleOpts(color=WATER_COLOR),
                label_opts=opts.LabelOpts(font_size=16, formatter="{c}°F"),
            ),
        )
        # .set_series_opts(
        #     areastyle_opts=opts.AreaStyleOpts(color="#FF5733", opacity=0.5),
        # )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"Temperature"),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(
                is_scale=True,
                type_="time",
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                position="bottom",
                splitline_opts=opts.SplitLineOpts(is_show=False),
            ),
            yaxis_opts=opts.AxisOpts(
                axisline_opts=opts.AxisLineOpts(is_show=False),
                type_="value",
                splitline_opts=opts.SplitLineOpts(
                    linestyle_opts=opts.LineStyleOpts(is_show=True, width=10)
                ),
            ),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_realtime=True,
                    type_="slider",
                    range_start=0,
                    range_end=33,
                    # xaxis_index=[0, 2500],
                )
            ],
            visualmap_opts=opts.VisualMapOpts(
                # is_show=False,
                pos_left="center",
                pos_top="5",
                # pos_right="50",
                orient="horizontal",
                min_=-10,
                max_=110,
                range_size=2,
                range_text=["Hot", "Freezing"],
                is_piecewise=False,
            ),
        )
    )


@st.cache_resource
def init_connection() -> connection:
    return psycopg2.connect(**st.secrets["postgres"])


@st.cache_data
def fetch_sql(
    _connection: connection, sql: str, parameters: dict[str, str | int] = {}
) -> pd.DataFrame:
    # try:
    with _connection:
        return pd.read_sql(sql, _connection)
    # finally:
    #     _connection.commit()


# con = init_connection()
if __name__ == "__main__":
    with st.sidebar:
        fire_icon(100)
        st.caption("By Kristian André Jakobsen & Alessandra Oshiro")
    con = init_connection()
    main(con)
    # con.close()
