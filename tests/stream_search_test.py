# 차량등록현황
import streamlit as st
from datetime import datetime
import pandas as pd

st.markdown(("국내 차량 브랜드"))
st.header("차량 등록 현황")

# st.page_link("./tests/pages/streamlit_test.py", label="Page 1", icon="1️⃣")


# 임시 데이터 생성
def create_temp_data():
    data = {
        "brand": ["Toyota", "Hyundai", "Kia", "Toyota", "Hyundai", "Kia"],
        "model": ["Camry", "Sonata", "Optima", "Corolla", "Elantra", "Sportage"],
        "region": ["Seoul", "Busan", "Seoul", "Incheon", "Busan", "Incheon"],
        "date": [
            "2023-01-01",
            "2023-01-02",
            "2023-01-03",
            "2023-01-04",
            "2023-01-05",
            "2023-01-06",
        ],
        "registration_count": [100, 150, 200, 250, 300, 350],
    }
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    return df


# 데이터 불러오기
@st.cache_data
def load_data():
    return create_temp_data()


data = load_data()


with st.form(key="my_form"):
    # selcetbox
    brand = st.selectbox("브랜드", data["brand"].unique())
    model = st.selectbox("모델명", data["model"].unique())
    region = st.selectbox("지역", data["region"].unique())

    start_date, end_date = st.select_slider(
        "날짜 범위 설정",
        options = [f"{year}.{str(month).zfill(2)}" for year in range(2023, 2025) for month in range(1, 13) if not (year == 2024 and month > 6)],
        value=("2023.01", "2023.02"),
    )
    submit_button = (st.form_submit_button(label="검색"),)

    st.title("차량 등록현황 검색")
    if filtered_data.empty:
        st.write("해당 조건에 맞는 데이터가 없습니다.")
    else:
        st.write("검색 결과:", filtered_data.shape[0], "건")
        st.dataframe(filtered_data)

    # if submit_button:
    #     sql = """
    #         select

    #     """
    # st.write(
    #     f"브랜드: {brand}, 모델: {model}, 지역: {region}, 기간: {start_date}~{end_date}"
    # )
# sql문에서 where절에 값이 들어간다.

# col1, col2, col3 = st.columns(3)
# with col1:
#     st.metric(label="해당 기간 총 등록 수", value="111330")  # , delta="2.21%")
# with col2:
#     st.metric(label="해당 기간 총 등록 수", value="320대", delta="-100대")
# with col3:
#     st.metric(label="해당 기간 최소 증가율", value="500대", delta="200대")

# df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
# # st.rine(df)
# st.line_chart(df)

# page_link = st.page_link("./pages/test.py", label="Page 1", icon="1️⃣")

# 차량 등록 현황 페이지에서 다른 페이지로 넘어가면서 값을 전송하는 방법..?
