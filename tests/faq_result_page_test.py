import streamlit as st


def main():
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
            title = st.text_input(
                "", placeholder="질문을 검색하세요", label_visibility="collapsed"
            )
        with right:
            submit_button = st.form_submit_button(label="검색")

        if submit_button:
            st.write(f"You selected: {brand_option}")

    st.subheader(f"{brand_option} 답변")
    container = st.container(border=True)
    container.text(f"fdsfdsfsdfdsfsdfsd")


if __name__ == "__main__":
    main()
