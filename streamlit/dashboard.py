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


def main(con: connection) -> None:
    df = fetch_sql(
        con,
        sql="""
            SELECT
                day,
                geospatial_x,
                geospatial_y,
                TRUNC(AVG(temperature)
                    OVER(ORDER BY day ROWS BETWEEN 7 PRECEDING AND CURRENT ROW), 2)
                    AS temperature
            FROM raw.temperature_readings;""",
    )
    left, right = st.columns([1, 1], gap="small")
    # temp = {0: 0, 1: 0}
    h = (
        HeatMap()
        .add_xaxis(range(30))
        .add_yaxis(
            "series0",
            range(30),
            [[i, j, i + j] for i in range(30) for j in range(30)],
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(is_show=False),
            legend_opts=opts.LegendOpts(is_show=False),
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
                        right=3,
                        # top=40,
                        # z=-10,
                        bounding="raw",
                        # origin=[75, 75],
                    ),
                    graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
                        image="https://i.imgur.com/G8nxNY6.png",
                        width=1600 / 2.3,
                        height=1200 / 2.3,
                        # opacity=0.4,
                    ),
                )
            ],
        )
    )
    with left:
        values = st_pyecharts(
            h,
            events={"click": "function(params) {return params.value}"},
            width=1600 / 2.5,
            height=1200 / 2.5,
        )
        geo = values[:2] if values else [0, 0]
        df_filtered = df.query(f"(geospatial_x=={geo[0]}) & (geospatial_y=={geo[1]})")

    with right:
        st_pyecharts(
            plot_line(df_filtered),
            height=600,
            width=1200,
        )
    # df2 = df[df["day"] == name]
    # with center:
    #     st.dataframe(df)
    # st.write(df2)


def plot_line(df) -> Line:
    return (
        Line(
            init_opts=opts.InitOpts(
                animation_opts=opts.AnimationOpts(animation_duration=50000)
            )
        ).add_xaxis(range(df["day"].max()))
        # .add_xaxis([1, 2, 3])
        .add_yaxis(
            series_name="°F",
            y_axis=df["temperature"],
            symbol_size=6,
            # is_symbol_show=False,
            # is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            color="#FF5733",
        )
        # .set_series_opts(
        #     areastyle_opts=opts.AreaStyleOpts(color="#FF5733", opacity=0.5),
        # )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Temperature °F"),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(
                is_scale=True,
                type_="category",
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=True),
                position="bottom",
            ),
            yaxis_opts=opts.AxisOpts(
                axisline_opts=opts.AxisLineOpts(is_show=False),
                type_="value",
            ),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_realtime=True,
                    type_="slider",
                    start_value=1,
                    end_value=365,
                    range_start=0,
                    range_end=100,
                    # xaxis_index=[0, 2500],
                )
            ],
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
    st.set_page_config(layout="wide")
    con = init_connection()
    main(con)
    # con.close()
