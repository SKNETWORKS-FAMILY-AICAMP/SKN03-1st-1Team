import streamlit as st


def main():
    conn = st.connection("mydb", type="sql", autocommit=True)

    st.markdown("**국내 차량 브랜드**")
    st.markdown("### 통합 FAQ 페이지")

    brand_name = ["기아", "제네시스"]

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
            getting_faq = f"""
            SELECT question, answer
            FROM faq
            INNER JOIN brand
            ON faq.brand_id = brand.brand_id
            WHERE 1=1
                AND brand_name LIKE '%{brand_option}%'
                AND question LIKE '%{search}%'
                ;
            """
            faq = conn.query(getting_faq, ttl=5000)

    if brand_option is not None:
        st.subheader(f"{brand_option} 답변")

        questions = faq["question"].tolist()
        answers = faq["answer"].tolist()
        container = st.container(border=True)
        for question, answer in zip(questions, answers):
            container = st.container()
            container.markdown(f"### Q. {question}")
            container.text(f"A. {answer}")


if __name__ == "__main__":
    main()
