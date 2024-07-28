import numpy as np
import pandas as pd
import streamlit as st

conn = st.connection("mydb", type="sql", autocommit=True)


# 브랜드 목록
def load_brand_name():
    getting_model_name = f"""
        SELECT DISTINCT 
            brand_name
        FROM 
            model
        INNER JOIN brand
        ON model.brand_id = brand.brand_id
        ORDER BY 
            (
                CASE WHEN ASCII(SUBSTRING(brand_name,1)) < 123 THEN 2 ELSE 1 END
            ), brand_name;    
    """
    car = conn.query(getting_model_name, ttl=5000)
    return car["brand_name"].tolist()


# 브랜드에 따른 모델 목록
def load_brand_models(brand):
    getting_model_name = f"""
        SELECT DISTINCT 
            model_name
        FROM 
            model
        INNER JOIN brand
        ON model.brand_id = brand.brand_id
        WHERE 1=1
            AND brand_name = '{brand}'
        ORDER BY 
            (
                CASE WHEN ASCII(SUBSTRING(model_name,1)) < 123 THEN 2 ELSE 1 END
            ), model_name;
    """
    car = conn.query(getting_model_name, ttl=5000)
    return car["model_name"].tolist()


# 지역 목록
def load_region():
    getting_model_name = f"""
        SELECT DISTINCT 
            region
        FROM 
            model
        ORDER BY 
            region;
    """
    car = conn.query(getting_model_name, ttl=5000)
    return car["region"].tolist()


def main():

    st.markdown(("국내 차량 브랜드"))
    st.header("차량 등록 현황")

    if "brand" not in st.session_state:
        st.session_state["brand"] = ""
    elif "region" not in st.session_state:
        st.session_state["region"] = ""
    elif "model" not in st.session_state:
        st.session_state["model"] = ""
    elif "start_date" not in st.session_state:
        st.session_state["start_date"] = ""
    elif "end_date" not in st.session_state:
        st.session_state["end_date"] = ""
    data = {
        "brand": load_brand_name(),
        "region": load_region(),
    }
    brand = st.selectbox("브랜드", data["brand"], index=0, placeholder="브랜드명")

    model = load_brand_models(brand)
    # 브랜드 선택 시 모델 선택박스 업데이트
    model = st.selectbox("모델", model, index=None, placeholder="모델명")

    region = st.selectbox("지역", data["region"])

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
    if region:
        st.session_state["model"] = region
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
                CONCAT(year, '.', LPAD(month, 2, '0')) AS '날짜',
                region AS '지역',
                SUM(car_cnt) AS '차량 등록 수'
            FROM 
                model
            INNER JOIN brand
            ON model.brand_id = brand.brand_id
            WHERE 1=1
                AND brand_name = '{brand}'
                AND region = '{region}'
                AND model_name LIKE '{model}'
                AND (year > {start_year} OR (year = {start_year} AND month >= {start_month}))
                AND (year < {end_year} OR (year = {end_year} AND month <= {end_month}))
            GROUP BY 
                year, month
            ORDER BY 
                year, month;
        """
        car = conn.query(getting_car_cnt, ttl=5000)
        container.subheader(f"{region}지역 {brand} {model}차량 등록 현황 차트")

        # 데이터프레임 생성
        chart_df = car.set_index("날짜")
        container.dataframe(chart_df)
        container.line_chart(chart_df["차량 등록 수"])


if __name__ == "__main__":
    main()
