from utils.navigation import render_sidebar

import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="GK AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD CSS
# ============================================================

with open("assets/style.css", "r", encoding="utf-8") as f:
    css = f.read()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

render_sidebar()

# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "quiz": None,
    "score": 0,
    "current_question": 0,
    "quiz_finished": False,
    "total_questions_answered": 0,
    "total_correct_answers": 0,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value



# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="hero">

        <div class="hero-badge">
            🧠 AI-POWERED KNOWLEDGE
        </div>

        <h1 class="hero-title">
            Challenge Your Knowledge.
        </h1>

        <p class="hero-subtitle">
            Test yourself, discover new facts,
            and become smarter every day.
        </p>

    </div>
    """
)


# ============================================================
# FEATURE CARDS
# ============================================================

col1, col2, col3 = st.columns(3)


# ============================================================
# QUIZ CARD
# ============================================================

with col1:

    st.html(
        """
        <div class="feature-card">

            <div class="feature-icon">
                🎯
            </div>

            <h3>
                Take a Quiz
            </h3>

            <p>
                Test your knowledge with
                AI-generated questions across
                multiple categories.
            </p>

        </div>
        """
    )

    if st.button(
        "Start Quiz →",
        key="start_quiz",
        type="primary",
        use_container_width=True
    ):
        st.switch_page("pages/quiz.py")


# ============================================================
# ASK GK CARD
# ============================================================

with col2:

    st.html(
        """
        <div class="feature-card">

            <div class="feature-icon">
                💬
            </div>

            <h3>
                Ask GK
            </h3>

            <p>
                Ask any general knowledge
                question and get a clear,
                educational explanation.
            </p>

        </div>
        """
    )

    if st.button(
        "Ask a Question →",
        key="ask_question",
        use_container_width=True
    ):
        st.switch_page("pages/ask_gk.py")


# ============================================================
# DASHBOARD CARD
# ============================================================

with col3:

    st.html(
        """
        <div class="feature-card">

            <div class="feature-icon">
                📊
            </div>

            <h3>
                Your Progress
            </h3>

            <p>
                Track your quiz performance,
                accuracy and learning progress.
            </p>

        </div>
        """
    )

    if st.button(
        "View Dashboard →",
        key="view_dashboard",
        use_container_width=True
    ):
        st.switch_page("pages/dashboard.py")


# ============================================================
# ACTIVITY
# ============================================================

st.divider()

st.html(
    """
    <div class="section-heading">
        YOUR ACTIVITY
    </div>
    """
)


# ============================================================
# CALCULATE STATISTICS
# ============================================================

questions_answered = st.session_state.total_questions_answered

correct_answers = st.session_state.total_correct_answers


if questions_answered > 0:

    accuracy = (
        correct_answers /
        questions_answered
    ) * 100

else:

    accuracy = 0


# ============================================================
# STATISTICS CARDS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.html(
        f"""
        <div class="stat-card">

            <div class="stat-icon">
                📝
            </div>

            <div class="stat-value">
                {questions_answered}
            </div>

            <div class="stat-label">
                Questions Answered
            </div>

        </div>
        """
    )


with col2:

    st.html(
        f"""
        <div class="stat-card">

            <div class="stat-icon">
                ✅
            </div>

            <div class="stat-value">
                {correct_answers}
            </div>

            <div class="stat-label">
                Correct Answers
            </div>

        </div>
        """
    )


with col3:

    st.html(
        f"""
        <div class="stat-card">

            <div class="stat-icon">
                🎯
            </div>

            <div class="stat-value">
                {accuracy:.0f}%
            </div>

            <div class="stat-label">
                Accuracy
            </div>

        </div>
        """
    )


# ============================================================
# MOTIVATION
# ============================================================

st.html(
    """
    <div class="motivation-card">

        <div class="motivation-title">
            🔥 Keep learning. Keep improving.
        </div>

        <div class="motivation-text">
            Every question is an opportunity to learn
            something you didn't know yesterday.
        </div>

    </div>
    """
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "GK AI • Learn something new every day."
)