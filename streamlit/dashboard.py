import datetime
import random
import time

import pandas as pd
import plotly.express as px
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import connection
from pyecharts import options as opts
from pyecharts.charts import EffectScatter, Gauge, HeatMap, Line, Scatter
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

st.set_page_config(layout="wide")


def main(con: connection) -> None:
    global geo
    geo = [15, 15]
    temp = fetch_sql(
        con,
        sql="""
            SELECT
                *
            FROM raw.temperature_readings;""",
    )
    _, mid, _ = st.columns([1, 5, 1])
    with mid:
        st.header("Welcome to Zakar!")
        st.write(
            """We are in the year 2037 at an idyllic island full of biodiversity and friendly
            people. But despite all the beauty, the small island of
            Zakar is plagued by regular fires. Luckily, by the ingenuity of Zakar's people,
            they have been able to develop an early fire detection system.
            Use this dashboard to understand the trends and patterns of these fires,
            and maybe you will be able to help us improve our alerting system!"""
        )
    l, left, right, r = st.columns([1, 35, 25, 1], gap="small")
    h = plot_heatmap(temp)
    with left:
        st.subheader("Please choose a location on the map")
        values = st_pyecharts(
            h,
            events={"click": "function(params) {return params.value}"},
            width=780,
            height=585,
        )
        geo = values[:2] if values else geo
        df_filtered = temp.query(f"(geospatial_x=={geo[0]}) & (geospatial_y=={geo[1]})")

    with st.sidebar:
        fire_icon(100)
        date = st.date_input(
            label="Choose a date",
            value=MIN_DATE,
            min_value=MIN_DATE,
            max_value=DATE_RANGE["date"].max(),
        )
        st.caption("By Kristian André Jakobsen & Alessandra Oshiro")
    tweets = fetch_tweets(
        con,
        int(DATE_RANGE.loc[DATE_RANGE["date"] == date, "day"].iloc[0]),
        geo[0],
        geo[1],
    )
    with right:
        st.subheader(f"Tweets for {date:%d} {date:%B} {date:%Y} at {geo[0], geo[1]}")
        if tweets.empty:
            st.info("There are no tweets for the selected date and location.")
        for t in tweets["tweet"]:
            st.text("")
            tweet(t)
    st.empty()
    st_pyecharts(
        plot_line(df_filtered, geo),
        # height=300,
        # width=700,
    )


def fetch_tweets(con, day, geo_x, geo_y):
    return fetch_sql(
        con,
        sql="""
        WITH top_tweets AS (
            SELECT
                t.day,
                t.geospatial_x,
                t.geospatial_y,
                t.tweet,
                ROW_NUMBER() OVER(PARTITION BY
                    t.day,
                    t.geospatial_x,
                    t.geospatial_y
                ORDER BY t.day, t.geospatial_x, t.geospatial_y DESC) AS rank
                FROM raw.tweets t)
        SELECT * FROM top_tweets tt
        WHERE rank <= 4
        AND tt.day = %(day)s
        AND tt.geospatial_x = %(geo_x)s
        AND tt.geospatial_y = %(geo_y)s;
        """,
        parameters={
            "day": day,
            "geo_x": geo_x,
            "geo_y": geo_y,
        },
    )


def tweet(text="test", width=650):
    # inner_left, inner_right, _ = st.columns([0.07, 0.85, 0.09])
    st.markdown(
        f"""
        <div style="width:{width}px;">
        <img src="https://i.imgur.com/ZsKRyWw.png" alt="tweet" style="width:100%;">
        <div style="display:inline-block;position:absolute;top:12px;left:45px;width:{width-55}px;">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tweet_icon(width=50):
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Logo_of_Twitter.svg/512px-Logo_of_Twitter.svg.png?20220821125553",
        width=width,
    )


def fire_icon(width=50):
    st.image(
        "https://i.imgur.com/Q06cnvr.gif",
        width=width,
    )


def plot_heatmap(df):
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
                        width=800,
                        height=600,
                        # opacity=0.4,
                    ),
                )
            ],
        )
    )
    s = (
        EffectScatter()
        .add_xaxis([random.randint(0, 29) for _ in range(5)])
        .add_yaxis(
            "",
            [random.randint(0, 29) for _ in range(5)],
            symbol="image://https://media.tenor.com/8McIGu0Tf_QAAAAi/fire-joypixels.gif",
            symbol_size=20,
            effect_opts=opts.EffectOpts(period=2, scale=2, trail_length=0.9),
        )
        .set_global_opts(title_opts=opts.TitleOpts(is_show=False))
    )

    return h
    # df2 = df[df["day"] == name]
    # with center:
    #     st.dataframe(df)
    # st.write(df2)


def plot_line(df, geo) -> Line:
    st.subheader(f"Historical Temperature at {geo[0], geo[1]}")
    return (
        Line(
            init_opts=opts.InitOpts(
                animation_opts=opts.AnimationOpts(animation_duration=3000)
            )
        ).add_xaxis(df["date"])
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
            title_opts=opts.TitleOpts(is_show=False),
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
        df = pd.read_sql(sql, _connection, params=parameters)
        df = df.merge(DATE_RANGE, how="left").sort_values("day")
        return df
    # finally:
    #     _connection.commit()


# con = init_connection()
if __name__ == "__main__":
    con = init_connection()
    main(con)
    # con.close()
