import pandas as pd
import plotly.express as px
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import connection
from pyecharts import options as opts
from pyecharts.charts import EffectScatter, Line
from pyecharts.faker import Faker
from pyecharts.globals import SymbolType
from streamlit_echarts import st_echarts, st_pyecharts

import streamlit as st


def main(con: connection) -> None:
    df = fetch_sql(
        con,
        sql="SELECT * FROM raw.temperature_readings WHERE geospatial_x = geospatial_y AND geospatial_x=0;",
    )
    st.dataframe(df)
    # print(list(df["day"].unique()))
    # st.write(df["day"].unique().flatten().shape)
    # for day in df["day"]:
    # y_values = df.loc[df["day"] <= day, "temperature"]
    # st.dataframe(y_values)
    c = (
        Line(
            init_opts=opts.InitOpts(
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_duration=5000
                )
            )
        )
        .add_xaxis(list(int(d) for d in df["day"].unique()))
        # .add_xaxis([1, 2, 3])
        .add_yaxis(
            "No 1",
            df["temperature"],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Temperature"),
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True, link=[{"xAxisIndex": "x"}]
            ),
            tooltip_opts=opts.TooltipOpts(),
            xaxis_opts=opts.AxisOpts(
                type_="value",
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=True),
                position="bottom",
            ),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_realtime=True,
                    type_="inside",
                    start_value=0,
                    end_value=1000,
                    xaxis_index=[0, 1],
                )
            ],
        )
    )
    name = st_pyecharts(
        c, events={"mouseover": "function(params) {return params.name}"}
    )
    df2 = df[df["day"] == name]
    # st.write(df2)


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
    con = init_connection()
    main(con)
    # con.close()
