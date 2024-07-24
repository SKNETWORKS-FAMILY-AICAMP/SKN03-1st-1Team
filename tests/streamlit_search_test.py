# 차량등록현황

import streamlit as st
from datetime import datetime
import pandas as pd


st.markdown(("국내 차량 브랜드"))
st.header("차량 등록 현황")

# st.page_link("./tests/pages/streamlit_test.py", label="Page 1", icon="1️⃣")

container = st.container(border=True)

with st.form(key="my_form"):
    # selcetbox
    brand = container.selectbox("브랜드", ("현대", "기아", "삼성"))
    model = container.selectbox("모델명", ("페이지1", "페이지2", "페이지3"))
    region = container.selectbox("지역", ("페이지1", "페이지2", "페이지3"))

    start_date, end_date = container.select_slider(
        "날짜 범위 설정",
        options=[
            "2023.01",
            "2023.02",
            "2023.03",
            "2023.04",
            "2023.05",
            "2023.06",
            "2023.07",
            "2023.08",
            "2023.09",
            "2023.10",
            "2023.11",
            "2023.12",
            "2024.01",
            "2024.02",
            "2024.03",
            "2024.04",
            "2024.05",
            "2024.06",
        ],
        value=("2023.01", "2023.02"),
    )
    submit_button = st.form_submit_button(label="검색")

    if submit_button:
        st.write(
            f"브랜드: {brand}, 모델: {model}, 지역: {region}, 기간: {start_date}~{end_date}"
        )
        st.session_state.runpage = streamlit_test.py
        st.session_state.runpage()
        st.experimental_rerun()


# if btn1:
#     st.session_state.runpage = App1page
#     st.session_state.runpage()
#     st.experimental_rerun()
