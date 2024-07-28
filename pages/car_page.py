import pandas as pd
import streamlit as st
import numpy as np

st.markdown(("국내 차량 브랜드"))
st.header("차량 등록 현황")


# 브랜드에 따른 모델 목록
def load_brand_models(brand):
    if brand == "기아":
        return [
            "쏘렌토",
            "카니발",
            "스포티지",
            "셀토스",
            "레이",
            "K8",
            "K5",
            "모닝",
            "니로",
            "EV6",
            "K3",
            "EV9",
            "모하비",
            "K9",
            "스팅어",
        ]
    elif brand == "현대":
        return [
            "그랜저",
            "아반떼",
            "싼타페",
            "투싼",
            "캐스퍼",
            "쏘나타",
            "팰리세이드",
            "코나",
            "아이오닉 5",
            "아이오닉 6",
            "베뉴",
            "넥쏘",
        ]
    elif brand == "제네시스":
        return ["G80", "GV80", "GV70", "G90", "G70", "GV60"]
    elif brand == "KGM":
        return ["토레스", "렉스턴 스포츠", "티볼리", "렉스턴", "코란도"]
    elif brand == "쉐보래":
        return [
            "트랙스",
            "트레일블레이저",
            "콜로라도",
            "트래버스",
            "볼트 EUV",
            "스파크",
            "이쿼녹스",
            "타호",
            "볼트 EV",
            "말리부",
        ]
    elif brand == "르노코리아":
        return ["QM6", "XM3", "SM6", "아르카나"]
    return []


def main():
    conn = st.connection("mydb", type="sql", autocommit=True)

    if "brand" not in st.session_state:
        st.session_state["brand"] = ""
    # elif "region" not in st.session_state:
    #     st.session_state["region"] = ""
    elif "model" not in st.session_state:
        st.session_state["model"] = ""
    elif "start_date" not in st.session_state:
        st.session_state["start_date"] = ""
    elif "end_date" not in st.session_state:
        st.session_state["end_date"] = ""
    data = {
        "brand": ["기아", "현대", "제네시스", "KGM", "쉐보래", "르노코리아"],
        "region": [
            "강원도",
            "경기도",
            "경상남도",
            "경상북도",
            "광주시",
            "대구시",
            "대전시",
            "부산시",
            "서울시",
            "세종시",
            "울산시",
            "인천시",
            "전라남도",
            "전라북도",
            "제주도",
            "충청남도",
            "충청북도",
        ],
    }

    brand = st.selectbox("브랜드", data["brand"], index=0, placeholder="브랜드명")

    # 브랜드 선택 시 모델 선택박스 업데이트
    models_for_brand = load_brand_models(brand)
    model = st.selectbox("모델", models_for_brand, index=None, placeholder="모델명")

    # region = st.selectbox("지역", data["region"])

    start_date, end_date = st.select_slider(
        "날짜 범위 설정",
        options=[
            f"{year}.{str(month).zfill(2)}"
            for year in range(2023, 2025)
            for month in range(1, 13)
            if not (year == 2024 and month > 6)
        ],
        value=("2023.06", "2024.01"),
    )
    if brand:
        st.session_state["brand"] = brand
    if model:
        st.session_state["region"] = model
    # if region:
    #     st.session_state["model"] = region
    if start_date:
        st.session_state["start_date"] = start_date
    if end_date:
        st.session_state["end_date"] = end_date

    submit_button = st.button(label="Submit")
    if submit_button:
        container = st.container(border=True)
        # 날짜 포맷 변환
        start_year, start_month = map(int, start_date.split("."))
        end_year, end_month = map(int, end_date.split("."))

        getting_car_cnt = f"""
            SELECT 
                CONCAT(year, '.', LPAD(month, 2, '0')) AS date,
                SUM(car_cnt) AS car_cnt
            FROM 
                model
            INNER JOIN brand
            ON model.brand_id = brand.brand_id
            WHERE 
                brand_name = '{brand}'
                AND model_name LIKE '{model}'
                AND (year > {start_year} OR (year = {start_year} AND month >= {start_month}))
                AND (year < {end_year} OR (year = {end_year} AND month <= {end_month}))
            GROUP BY 
                year, month
            ORDER BY 
                year, month;
        """
        car = conn.query(getting_car_cnt, ttl=5000)
        container.subheader(f"{brand} {model}차량 등록 현황 차트")

        # 데이터프레임 생성

        df1 = car.set_index("date")
        container.line_chart(df1)


if __name__ == "__main__":
    main()
