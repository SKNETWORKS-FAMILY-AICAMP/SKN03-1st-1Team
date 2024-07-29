import streamlit as st


class DatabaseConnection:
    def __init__(self, connection):
        self.conn = connection

    def query(self, query, ttl=None):
        if ttl:
            return self.conn.query(query, ttl=ttl)
        else:
            return self.conn.query(query)


class CarData:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def load_brand_name(self):
        query = """
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
        result = self.db_conn.query(query, ttl=5000)
        return result["brand_name"].tolist()

    def load_brand_models(self, brand):
        query = f"""
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
        result = self.db_conn.query(query, ttl=5000)
        return result["model_name"].tolist()

    def load_region(self):
        query = """
            SELECT DISTINCT 
                region
            FROM 
                model
            ORDER BY 
                region;
        """
        result = self.db_conn.query(query, ttl=5000)
        return result["region"].tolist()

    def get_car_count(
        self, brand, region, model, start_year, start_month, end_year, end_month
    ):
        query = f"""
            SELECT 
                CONCAT(year, '.', LPAD(month, 2, '0')) AS '날짜',
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
        return self.db_conn.query(query, ttl=5000)


class CarApp:
    def __init__(self):
        connection = st.connection("mydb", type="sql", autocommit=True)
        self.db_conn = DatabaseConnection(connection)
        self.car_data = CarData(self.db_conn)

    def run(self):
        self.setup_session_state()
        st.markdown("국내 차량 브랜드")
        st.header("차량 등록 현황")

        brand = st.selectbox(
            "브랜드", self.car_data.load_brand_name(), index=0, placeholder="브랜드명"
        )
        model = st.selectbox(
            "모델",
            self.car_data.load_brand_models(brand),
            index=None,
            placeholder="모델명",
        )
        region = st.selectbox("지역", self.car_data.load_region())
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

        self.update_session_state(brand, model, region, start_date, end_date)

        submit_button = st.button(label="Submit")
        if submit_button:
            self.display_chart(brand, model, region, start_date, end_date)

    def setup_session_state(self):
        if "brand" not in st.session_state:
            st.session_state["brand"] = ""
        if "region" not in st.session_state:
            st.session_state["region"] = ""
        if "model" not in st.session_state:
            st.session_state["model"] = ""
        if "start_date" not in st.session_state:
            st.session_state["start_date"] = ""
        if "end_date" not in st.session_state:
            st.session_state["end_date"] = ""

    def update_session_state(self, brand, model, region, start_date, end_date):
        st.session_state["brand"] = brand
        st.session_state["model"] = model
        st.session_state["region"] = region
        st.session_state["start_date"] = start_date
        st.session_state["end_date"] = end_date

    def display_chart(self, brand, model, region, start_date, end_date):
        container = st.container()
        start_year, start_month = map(int, start_date.split("."))
        end_year, end_month = map(int, end_date.split("."))
        car_data = self.car_data.get_car_count(
            brand, region, model, start_year, start_month, end_year, end_month
        )

        container.subheader(f"{region}지역 {brand} {model}차량 등록 현황 차트")
        chart_df = car_data.set_index("날짜")
        container.dataframe(chart_df)
        container.line_chart(chart_df["차량 등록 수"])


if __name__ == "__main__":
    app = CarApp()
    app.run()
