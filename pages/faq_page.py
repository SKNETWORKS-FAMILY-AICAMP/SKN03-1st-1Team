import streamlit as st


class DatabaseConnection:
    def __init__(self, connection):
        self.conn = connection

    def query(self, query, ttl=None):
        if ttl:
            return self.conn.query(query, ttl=ttl)
        else:
            return self.conn.query(query)


class FAQData:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_faq(self, brand_option, search):
        query = f"""
            SELECT question, answer
            FROM faq
            INNER JOIN brand
            ON faq.brand_id = brand.brand_id
            WHERE 1=1
                AND brand_name LIKE '%{brand_option}%'
                AND question LIKE '%{search}%'
            GROUP BY 
                question, answer
            ORDER BY 
                question
            ;
        """
        return self.db_conn.query(query, ttl=5000)


class FAQApp:
    def __init__(self):
        self.db_conn = DatabaseConnection(
            st.connection("mydb", type="sql", autocommit=True)
        )
        self.faq_data = FAQData(self.db_conn)
        self.brand_name = ["기아", "제네시스"]

    def run(self):
        st.markdown("**국내 차량 브랜드**")
        st.markdown("### 통합 FAQ 페이지")

        with st.form(key="my_form"):
            left, middle, right = st.columns([2, 4, 1])
            with left:
                brand_option = st.selectbox(
                    "",
                    self.brand_name,
                    index=None,
                    label_visibility="collapsed",
                    placeholder="브랜드명",
                )

            with middle:
                search = st.text_input(
                    "", placeholder="질문을 검색하세요", label_visibility="collapsed"
                )
            with right:
                submit_button = st.form_submit_button(label="검색")

            if submit_button:
                faq = self.faq_data.get_faq(brand_option, search)
                self.display_faq(brand_option, faq)

    def display_faq(self, brand_option, faq):
        if brand_option is not None:
            st.subheader(f"{brand_option} 답변")

            questions = faq["question"].tolist()
            answers = faq["answer"].tolist()
            for question, answer in zip(questions, answers):
                container = st.container(border=True)
                container.markdown(f"### Q. {question}")
                container.write(f"A. {answer}")


if __name__ == "__main__":
    app = FAQApp()
    app.run()
