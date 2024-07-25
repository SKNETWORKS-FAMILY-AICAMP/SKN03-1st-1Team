import streamlit as st


def main():
    conn = st.connection("mydb", type="sql", autocommit=True)

    st.markdown("**국내 차량 브랜드**")
    st.markdown("### 통합 FAQ 페이지")

    brand_name = ["기아", "제네시스", "현대"]

    with st.form(key="my_form"):

        left, middle, right = st.columns([2, 4, 1])
        with left:
            brand_option = st.selectbox(
                "",
                brand_name,
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
            getting_question = f"""
            SELECT answer
            FROM faq
            INNER JOIN brand
            ON faq.brand_id = brand.brand_id
            WHERE 1=1
                  AND brand_name LIKE '%제네시스%'
                  AND question LIKE '%법%'
                  ;
            """
            question = conn.query(question, ttl=3600)

            getting_answer = f"""
            SELECT answer
            FROM faq
            INNER JOIN brand
            ON faq.brand_id = brand.brand_id
            WHERE 1=1
                  AND brand_name LIKE '%제네시스%'
                  AND question LIKE '%법%'
                  ;
            """
            answer = conn.query(question, ttl=3600)

    if brand_option is not None:
        st.subheader(f"{brand_option} 답변")
        container = st.container(border=True)
        container.text(f"Q. {question}")
        container.text(f"A. {answer}")


if __name__ == "__main__":
    main()
