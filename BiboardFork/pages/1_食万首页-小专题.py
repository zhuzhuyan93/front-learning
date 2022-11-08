import datetime
import os
import sys
import pandas as pd
import streamlit as st
import tools
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_icon="⛵", page_title="食万首页-小专题模块专项指标")
dataPath = "./data/page1/dataRaw"

rowdataLs = [i for i in os.listdir(dataPath) if i.endswith("csv")]
clickLs, expLs = [], []
for file in [i for i in rowdataLs if i.startswith("subject_menu_click")]:
    clickLs.append(pd.read_csv(os.path.join(dataPath, file), encoding="utf-8"))
for file in [i for i in rowdataLs if i.startswith("subject_exp")]:
    expLs.append(pd.read_csv(os.path.join(dataPath, file), encoding="utf-8"))

# 曝光点击数据
df_click, df_exp = pd.concat(clickLs, axis=0), pd.concat(expLs, axis=0)
datesAll = list(sorted(df_exp.pdate.unique()))

# 页面名称
st.title("食万首页-小专题模块专项指标")
st.markdown("搜推指标[AIOT后台管理系统](https://bigdata-portal.tineco.com/#/td3-AlgMonitoring)")

# 曝光点击数据下载
tab1, tab2 = st.tabs(["曝光数据", "点击数据"])
with tab1:
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"🦍 **时间范围**: {datesAll[0]}-{datesAll[-1]}")
    col2.markdown(f"🦍️ **命中数据**: {df_exp.shape[0]}条")
    col3.markdown(f"🦍 **命中人数**: {df_exp.user_id.nunique()} 人")
    with st.expander(f"⭕点击展开原始数据: "):
        data = tools.convert_df(df_exp)
        st.download_button(
            label="下载曝光数据",
            data=data,
            file_name=f"曝光数据_{datesAll[0]}-{datesAll[-1]}.csv",
        )
        st.dataframe(df_exp)
with tab2:
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"🦍 **时间范围**: {datesAll[0]}-{datesAll[-1]}")
    col2.markdown(f"🦍️ **命中数据**: {df_click.shape[0]}条")
    col3.markdown(f"🦍 **命中人数**: {df_click.user_id.nunique()} 人")
    with st.expander(f"⭕点击展开原始数据: "):
        data = tools.convert_df(df_click)
        st.download_button(
            label="下载点击数据",
            data=data,
            file_name=f"曝光数据_{datesAll[0]}-{datesAll[-1]}.csv",
        )
        st.dataframe(df_click)

"---"


# 选择显示的日期范围
col1, col2 = st.columns(2)
start_date = col1.selectbox("选择开始日期", datesAll)
end_date = col2.selectbox("选择开始日期", list(sorted(datesAll, reverse=True)))
if start_date >= end_date:
    start_date, end_date = end_date, start_date
st.info(f"👉 选择的日期范围: " f"{start_date} - {end_date}")
"---"

plotDataPath = "./data/page1/dataPlot"
col1, col2 = st.columns(2)  # 指标1，2
# 指标1
with col1:
    st.subheader("🔎整体曝光PV")
    st.write("专题菜谱10月27日之后都为5, 10月26日之前实验组为3和对照组为10")
    df1 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part1.csv"), encoding="utf-8",),
        start_date,
        end_date,
    )
    choose11 = st.radio("曝光维度", ("专题曝光", "菜谱曝光"), horizontal=True)
    choose12 = st.checkbox("显示汇总", key=12)
    fig, ax = tools.greenBlackLinePlot(
        df1.set_index("pdate"),
        cols=[f"实验组{choose11}", f"对照组{choose11}"],
        showCol=f"{choose11}汇总",
        isShowCol=choose12,
    )
    st.pyplot(fig)

# 指标2
with col2:
    st.subheader("🔎整体曝光UV")
    choose21 = st.checkbox("显示汇总", key=21)
    df2 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part2.csv"), encoding="utf-8",),
        start_date,
        end_date,
    )

    fig, ax = tools.greenBlackLinePlot(
        df2.set_index("pdate"), cols=["实验组", "对照组"], showCol="总曝光", isShowCol=choose21,
    )
    # 数据下载按钮
    data = tools.convert_df(df2)
    st.download_button(
        label="下载曝光UV数据", data=data, file_name=f"曝光UV_{start_date}-{end_date}.csv"
    )
    for _ in range(3):
        st.text("")
    st.pyplot(fig)

col1, col2 = st.columns(2)  # 指标3 指标4
# 指标3
with col1:
    st.subheader("🔎曝光请求时间透视")
    choose31 = st.multiselect("分组", ["实验组", "对照组"], ["实验组", "对照组"])
    df3 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part3.csv"), encoding="utf-8",).assign(
            second=lambda x: x["second"].astype(int)
        ),
        start_date,
        end_date,
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    for group, color in zip(choose31, ["#40c057", "#868e96"][: len(choose31)]):
        group_ = {"实验组": "A", "对照组": "B"}.get(group)
        ax.hist(
            df3.loc[lambda x: x["shunt_name"] == group_]["second"],
            bins=48,
            color=color,
            label=group,
        )
    ax.grid(ls="--", lw=0.25, color="#4E616C")
    ax.legend(edgecolor="white", facecolor="white")
    ax.set_xlim(0, 1440)
    ax.set_xticks(range(0, 1441, 60))
    ax.set_xticklabels([str(i) + "时" for i in range(0, 25)], rotation=80)
    ax.spines["bottom"].set_edgecolor("#4E616C")
    ax.xaxis.set_tick_params(
        length=5, color="#4E616C", labelcolor="black", labelsize=10
    )
    ax.yaxis.set_tick_params(
        length=5, color="#4E616C", labelcolor="#4E616C", labelsize=10
    )
    st.pyplot(fig)

# 指标4
with col2:
    st.subheader("🔎曝光请求分布(专题维度)")
    df4 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part4.csv"), encoding="utf-8",),
        start_date,
        end_date,
    )
    datesSelected = list(sorted(df4.pdate.unique(), reverse=True))
    choose41 = st.selectbox("日期", datesSelected)
    choose42 = st.multiselect("呈现分组", ["实验组", "对照组"], ["实验组", "对照组"], key=42)
    choose43 = st.radio("统计方式", ["曝光UV", "曝光PV"], horizontal=True)
    df4 = df4.loc[lambda x: x["pdate"] == choose41]
    df4.index = range(len(df4))

    fig, ax = plt.subplots(figsize=(8.5, 5))
    if len(choose42) == 1:
        ax.bar(
            df4.index,
            df4[choose42[0] + choose43],
            width=0.4,
            label=choose42[0] + choose43,
            color="#00A752",
        )
    else:
        i = -0.2
        for group, color in zip(choose42, ["#00A752", "black", "red"][: len(choose42)]):
            ax.bar(
                df4.index + i,
                df4[group + choose43],
                width=0.4,
                label=group + choose43,
                color=color,
            )
            i += 0.4
    ax.set_xticks(df4.index)
    ax.set_xticklabels(df4["专题名称"], rotation=60)
    ax.legend(edgecolor="white", facecolor="white", loc=1)
    ax.grid(ls="--", lw=0.25, color="#4E616C")
    ax.spines["bottom"].set_edgecolor("#4E616C")
    ax.xaxis.set_tick_params(
        length=5, color="#4E616C", labelcolor="black", labelsize=11
    )
    ax.yaxis.set_tick_params(
        length=5, color="#4E616C", labelcolor="#4E616C", labelsize=10
    )
    st.pyplot(fig)


col1, col2 = st.columns(2)  # 指标5 指标6
# 指标5
with col1:
    st.subheader("🔎整体点击PV")
    df5_1 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part5_f1.csv"), encoding="utf-8",),
        start_date,
        end_date,
    )
    df5_2 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part5_f2.csv"), encoding="utf-8",),
        start_date,
        end_date,
    )
    df5_3 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part5_f3.csv"), encoding="utf-8",),
        start_date,
        end_date,
    )
    choose51 = st.radio(
        "统计方式", ["专题点击（专题粒度去重）", "专题点击（菜谱粒度去重）", "专题菜谱点击"], horizontal=True
    )
    if choose51 == "专题点击（专题粒度去重）":
        fig, ax = tools.greenBlackLinePlot(df5_1.set_index("pdate"))
    elif choose51 == "专题点击（菜谱粒度去重）":
        fig, ax = tools.greenBlackLinePlot(df5_2.set_index("pdate"))
    else:
        fig, ax = tools.greenBlackLinePlot(df5_3.set_index("pdate"))
    st.pyplot(fig)

# 指标6
with col2:
    st.subheader("🔎专题点击PV")
    df6_1 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part6_f1.csv"), encoding="utf-8",),
        start_date,
        end_date,
    )
    df6_2 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part6_f2.csv"), encoding="utf-8",),
        start_date,
        end_date,
    )
    df6_3 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part6_f3.csv"), encoding="utf-8",),
        start_date,
        end_date,
    )
    datesSelected = list(sorted(df6_1.pdate.unique(), reverse=True))
    choose61 = st.radio("统计维度", ["专题点击", "菜谱点击", "菜谱点击(绑定专题)"], horizontal=True)
    choose62 = st.multiselect("日期", datesSelected, max(datesSelected))
    if choose61 == "专题点击":
        df_plot = df6_1.loc[lambda x: x["pdate"].isin(choose62)]
        df_plot = (
            df_plot.groupby(["subject_name"])
            .sum()
            .sort_values(["B", "A"], ascending=False)
        )
        fig, ax = tools.greenBlackLinePlot(df_plot, cols=["A", "B"])
        ax.legend(["实验组", "对照组"], edgecolor="white", facecolor="white")
        ax.xaxis.set_tick_params(
            length=5, color="#4E616C", labelcolor="black", labelsize=11
        )

    elif choose61 == "菜谱点击":
        df_plot = df6_2.loc[lambda x: x["pdate"].isin(choose62)]
        df_plot = (
            df_plot.groupby(["menu_name"])
            .sum()
            .assign(sum=lambda x: x["A"].fillna(0) + x["B"].fillna(0))
            .sort_values(["sum"], ascending=False)
            .rename(columns={"A": "实验组", "B": "对照组"})
            .head(40)
        )
        fig, ax = tools.greenBlackLinePlot(df_plot, cols=["实验组", "对照组"])
        ax.set_xticklabels(df_plot.index, rotation=90)
        data = tools.convert_df(df_plot)
        st.download_button(
            label="下载菜谱点击数据",
            data=data,
            file_name=f"menu_click_{min(datesSelected)}-{max(datesSelected)}.csv",
        )

    else:
        df_plot = df6_3.loc[lambda x: x["pdate"].isin(choose62)]
        df_plot = (
            df_plot.groupby(["menu_name_sub"])
            .sum()
            .assign(sum=lambda x: x["A"].fillna(0) + x["B"].fillna(0))
            .sort_values(["sum"], ascending=False)
            .rename(columns={"A": "实验组", "B": "对照组"})
            .head(40)
        )
        fig, ax = tools.greenBlackLinePlot(df_plot, cols=["实验组", "对照组"])
        ax.set_xticklabels(df_plot.index, rotation=90)
        data = tools.convert_df(df_plot)
        st.download_button(
            label="下载菜谱点击数据(绑定专题)",
            data=data,
            file_name=f"menu_click_{min(datesSelected)}-{max(datesSelected)}.csv",
        )

    st.pyplot(fig)

col1, col2 = st.columns(2)  # 指标7 指标8
# 指标7
with col1:
    st.subheader("🔎点击UV分布及留存")
    st.write("新老用户判断基于2022年10月20日之后数据，留存分析区间始于2022年10月27日")
    df7_1 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part7_f1.csv"), encoding="utf-8",),
        start_date,
        end_date,
    )
    df7_2 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part7_f2.csv"), encoding="utf-8",),
        start_date,
        end_date,
        col="日期",
    )
    df7_3 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part7_f3.csv"), encoding="utf-8",),
        start_date,
        end_date,
        col="日期",
    )
    df7_4 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part7_f4.csv"), encoding="utf-8",),
        start_date,
        end_date,
        col="日期",
    )
    df7_5 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part7_f5.csv"), encoding="utf-8",),
        start_date,
        end_date,
        col="日期",
    )
    tab1, tab2, tab3 = st.tabs(["点击UV分布", "全量留存", "新用户留存"])
    with tab1:
        fig, ax = tools.greenBlackLinePlot(
            df7_1.set_index("pdate").rename(columns={"A": "实验组", "B": "对照组"}),
            cols=["实验组", "对照组"],
        )
        st.pyplot(fig)

    with tab2:
        choose71 = st.radio("统计方式：", ["存量", "存率"], horizontal=True)
        if choose71 == "存量":
            st.dataframe(df7_2)
        else:
            st.dataframe(df7_3)

    with tab3:
        choose72 = st.radio("统计方式：", ["存量", "存率"], key=72, horizontal=True)
        if choose72 == "存量":
            st.dataframe(df7_4)
        else:
            st.dataframe(df7_5)


# 指标8
with col2:
    st.subheader("🔎用户点击活跃情况")
    tab1, tab2 = st.tabs(["用户点击次数分布", "活跃用户占比分布"])
    df8_1 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part8_f1.csv"), encoding="utf-8",),
        start_date,
        end_date,
    )
    df8_2 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part8_f2.csv"), encoding="utf-8",),
        start_date,
        end_date,
    )
    df8_3 = tools.filterDate(
        pd.read_csv(os.path.join(plotDataPath, "part8_f3.csv"), encoding="utf-8",),
        start_date,
        end_date,
    )
    datesSelected = list(sorted(df8_1.pdate.unique(), reverse=True))
    with tab1:
        data = tools.convert_df(df8_1.rename(columns={"menu_id": "clk_num"}))
        st.download_button(
            label="下载用户点击次数明细数据",
            data=data,
            file_name=f"user_click_data_{min(datesSelected)}-{max(datesSelected)}.csv",
        )
        choose81 = st.radio("显示", ["UV", "UV占比"], horizontal=True)
        choose82 = st.selectbox("日期", datesSelected, key=82)
        if choose81 == "UV":
            df_plot = df8_2.loc[lambda x: x["pdate"] == choose82][
                ["pdate", "menu_id", "A", "B"]
            ]
            df_plot.columns = ["pdate", "点击次数", "实验组", "对照组"]
        else:
            df_plot = df8_2.loc[lambda x: x["pdate"] == choose82][
                ["pdate", "menu_id", "A_rate", "B_rate"]
            ]
            df_plot.columns = ["pdate", "点击次数", "实验组", "对照组"]
        fig, ax = tools.greenBlackLinePlot(
            df_plot.set_index("点击次数"), cols=["实验组", "对照组"]
        )
        ax.set_xticks(df_plot["点击次数"])
        ax.set_xticklabels(df_plot["点击次数"],)
        data_for_output_p8_1 = tools.convert_df(df_plot)
        st.download_button(
            label="下载当天点击次数分布明细数据",
            data=data_for_output_p8_1,
            file_name=f"user_click_data_{min(datesSelected)}-{max(datesSelected)}.csv",
        )
        st.pyplot(fig)

    with tab2:
        datesSelected = list(sorted(df8_3.pdate.unique(), reverse=True))
        choose83 = st.selectbox("日期", datesSelected)
        N = st.selectbox("活跃考察天数", sorted(df8_3.n_day.unique()))
        df_plot = df8_3.loc[lambda x: (x["pdate"] == choose83) & (x["n_day"] == N)]
        choose84 = st.radio("显示方式", ["UV", "UV占比"], horizontal=True, key=3243)
        if choose84 == "UV":
            df_plot = df_plot[["c_num", "A", "B"]]
            df_plot.columns = ["点击次数", "实验组", "对照组"]
        else:
            df_plot = df_plot[["c_num", "A_rate", "B_rate"]]
            df_plot.columns = ["点击次数", "实验组", "对照组"]
        df_plot.index = range(len(df_plot))
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(
            df_plot.index - 0.2,
            df_plot["实验组"],
            width=0.4,
            label="实验组",
            color="#00A752",
        )
        ax.bar(
            df_plot.index + 0.2, df_plot["对照组"], width=0.4, label="实验组", color="black",
        )
        ax.set_xticks(df_plot.index)
        ax.set_xticklabels(df_plot["点击次数"], rotation=60)
        ax.legend(edgecolor="white", facecolor="white", loc=1)
        ax.grid(ls="--", lw=0.25, color="#4E616C")
        ax.spines["bottom"].set_edgecolor("#4E616C")
        ax.xaxis.set_tick_params(
            length=5, color="#4E616C", labelcolor="black", labelsize=11
        )
        ax.yaxis.set_tick_params(
            length=5, color="#4E616C", labelcolor="#4E616C", labelsize=10
        )
        st.write("横坐标含义：考察天数内的活跃天数")
        st.pyplot(fig)
