import streamlit as st


def __main__():
    st.markdown("**국내 차량 브랜드**")
    st.markdown("### 통합 FAQ 페이지")

    brand_name = ["기아", "제네시스", "현대"]

    with st.form(key="my_form"):

        left, middle, right = st.columns([2, 4, 1])
        with left:
            option = st.selectbox(
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
            st.write(f"You selected: {option}")

    st.subheader("자주 묻는 질문 TOP 5")
    container = st.container(border=True)

    # List of text items
    text_items = [
        f"<h2 style='color: white;'>현대</h2><pre style='color: white; line-height: 2; font-size: 16px'>1.{1}\n2.{1}\n3.{1}\n4.{1}\n5.{1}</pre>",
        f"<h2 style='color: white;'>기아</h2><pre style='color: white; line-height: 2; font-size: 16px'>1.{2}\n2.{2}\n3.{2}\n4.{2}\n5.{2}</pre>",
        f"<h2 style='color: white;'>삼성</h2><pre style='color: white; line-height: 2; font-size: 16px'>1.{3}\n2.{3}\n3.{3}\n4.{3}\n5.{3}</pre>",
    ]

    # HTML and JavaScript code for the text slider
    slider_html = f"""
    <div class="slider">
      <div class="slides">
        {''.join([f'<div class="slide">{text}</div>' for text in text_items])}
      </div>
    </div>
    <style>
      .slider {{
        width: 100%;
        position: relative;
        overflow: hidden;
      }}
      .slides {{
        display: flex;
        transition: transform 0.5s ease-in-out;
      }}
      .slide {{
        min-width: 100%;
        box-sizing: border-box;
        background-color: transparent; /* 배경을 투명으로 설정 */
        text-align: center; /* 텍스트 중앙 정렬 */
      }}
      h2 {{
        margin: 0; /* 제목의 기본 마진 제거 */
      }}
    </style>
    <script>
      let currentSlide = 0;
      const slides = document.querySelector('.slides');
      const totalSlides = {len(text_items)};
      
      setInterval(() => {{
        currentSlide = (currentSlide + 1) % totalSlides;
        slides.style.transform = 'translateX(' + (-currentSlide * 100) + '%)';
      }}, 4000); // 4000 밀리초마다 슬라이드 전환
    </script>
    """

    container.components.v1.html(slider_html, height=300)


if __name__ == "__main__":
    __main__()
