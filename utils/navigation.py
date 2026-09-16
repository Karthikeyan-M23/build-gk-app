import streamlit as st


def render_sidebar():

    with st.sidebar:

        # ====================================================
        # BRAND
        # ====================================================

        st.markdown(
            """
# 🧠 GK AI

**Knowledge. Challenge. Learn.**
            """
        )

        st.divider()

        # ====================================================
        # NAVIGATION
        # ====================================================

        st.markdown("### Navigation")

        # Home
        if st.button(
            "🏠  Home",
            use_container_width=True,
            key="nav_home"
        ):
            st.switch_page("app.py")

        # Quiz
        if st.button(
            "🎯  Quiz",
            use_container_width=True,
            key="nav_quiz"
        ):
            st.switch_page("pages/quiz.py")

        #practice
        if st.button(
            "🔁  Practice",
                use_container_width=True,
                key="nav_practice"
            ):
                st.switch_page(
                    "pages/practice.py"
                )

        # Ask GK
        if st.button(
            "💬  Ask GK",
            use_container_width=True,
            key="nav_ask_gk"
        ):
            st.switch_page("pages/ask_gk.py")

        # Dashboard
        if st.button(
            "📊  Dashboard",
            use_container_width=True,
            key="nav_dashboard"
        ):
            st.switch_page("pages/dashboard.py")

        st.divider()

        st.caption("Powered by OpenAI")