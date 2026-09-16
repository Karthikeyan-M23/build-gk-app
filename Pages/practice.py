import streamlit as st

from utils.navigation import render_sidebar
from utils.database import get_practice_questions


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Practice | GK AI",
    page_icon="🔁",
    layout="wide"
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
    "practice_questions": [],
    "practice_index": 0,
    "practice_answers": [],
    "practice_finished": False,
    "practice_submitted": False,
    "practice_selected_answer": None
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HEADER
# ============================================================

st.html(
    """
    <div class="page-header">

        <div class="page-badge">
            WEAK AREA PRACTICE
        </div>

        <h1>
            Practice Mistakes
        </h1>

        <p>
            Revisit questions you previously got wrong
            and strengthen your knowledge.
        </p>

    </div>
    """
)


# ============================================================
# LOAD PRACTICE QUESTIONS
# ============================================================

if not st.session_state.practice_questions:

    practice_questions = get_practice_questions(
        limit=10
    )

    st.session_state.practice_questions = [
        dict(question)
        for question in practice_questions
    ]


questions = st.session_state.practice_questions


# ============================================================
# NO QUESTIONS
# ============================================================

if not questions:

    st.success(
        "🎉 You currently have no questions to practice."
    )

    st.info(
        "Complete a quiz and answer some questions "
        "incorrectly. They will appear here."
    )

    st.stop()


# ============================================================
# PRACTICE COMPLETE
# ============================================================

if st.session_state.practice_finished:

    total = len(questions)

    correct = sum(
        1
        for answer in st.session_state.practice_answers
        if answer["is_correct"]
    )

    percentage = (
        correct / total
    ) * 100 if total else 0


    st.html(
        f"""
        <div class="quiz-complete-card">

            <div class="quiz-complete-icon">
                🧠
            </div>

            <div class="quiz-complete-title">
                Practice Complete
            </div>

            <div class="quiz-complete-score">
                {correct} / {total}
            </div>

            <div class="quiz-complete-percentage">
                {percentage:.0f}%
            </div>

            <div class="quiz-complete-message">
                Keep practicing your weak areas
                and turn mistakes into strengths.
            </div>

        </div>
        """
    )


    st.write("")


    # --------------------------------------------------------
    # PRACTICE AGAIN
    # --------------------------------------------------------

    if st.button(
        "🔁 Practice Again",
        type="primary",
        use_container_width=True
    ):

        st.session_state.practice_questions = []

        st.session_state.practice_index = 0

        st.session_state.practice_answers = []

        st.session_state.practice_finished = False

        st.session_state.practice_submitted = False

        st.session_state.practice_selected_answer = None

        st.rerun()


    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    if st.button(
        "📊 Go to Dashboard",
        use_container_width=True
    ):

        st.switch_page(
            "pages/dashboard.py"
        )

    st.stop()


# ============================================================
# CURRENT QUESTION
# ============================================================

current_index = (
    st.session_state.practice_index
)

current_question = questions[current_index]

total_questions = len(questions)


# ============================================================
# PROGRESS
# ============================================================

progress = (
    (current_index + 1)
    / total_questions
)

st.progress(progress)

st.caption(
    f"Practice Question "
    f"{current_index + 1} of {total_questions}"
)


# ============================================================
# QUESTION CARD
# ============================================================

st.html(
    f"""
    <div class="quiz-question-card">

        <div class="quiz-question-number">
            QUESTION {current_index + 1}
        </div>

        <div class="quiz-question-text">
            {current_question["question_text"]}
        </div>

    </div>
    """
)


st.caption(
    f"{current_question['category']} "
    f"• "
    f"{current_question['difficulty']}"
)


# ============================================================
# ORIGINAL FOUR OPTIONS
# ============================================================

options = [
    current_question.get("option_a"),
    current_question.get("option_b"),
    current_question.get("option_c"),
    current_question.get("option_d")
]


# Remove empty values
options = [
    option
    for option in options
    if option
]


# ------------------------------------------------------------
# OLD DATABASE FALLBACK
# ------------------------------------------------------------
# This protects old questions created before the option
# columns existed.
# ------------------------------------------------------------

if len(options) < 4:

    fallback_options = [
        current_question.get(
            "correct_answer"
        ),
        current_question.get(
            "selected_answer"
        )
    ]

    for option in fallback_options:

        if option and option not in options:

            options.append(option)


# ============================================================
# ANSWER SELECTION
# ============================================================

selected_answer = st.radio(
    "Select your answer",

    options,

    key=f"practice_answer_{current_index}",

    disabled=st.session_state.practice_submitted
)


# ============================================================
# SUBMIT ANSWER
# ============================================================

if not st.session_state.practice_submitted:

    if st.button(
        "✓  Submit Answer",
        type="primary",
        use_container_width=True
    ):

        st.session_state.practice_selected_answer = (
            selected_answer
        )

        is_correct = (
            selected_answer
            == current_question["correct_answer"]
        )

        st.session_state.practice_answers.append(
            {
                "question_id":
                    current_question["id"],

                "selected_answer":
                    selected_answer,

                "correct_answer":
                    current_question["correct_answer"],

                "is_correct":
                    is_correct
            }
        )

        st.session_state.practice_submitted = True

        st.rerun()


# ============================================================
# FEEDBACK
# ============================================================

if st.session_state.practice_submitted:

    selected = (
        st.session_state.practice_selected_answer
    )

    correct_answer = (
        current_question["correct_answer"]
    )


    # --------------------------------------------------------
    # CORRECT
    # --------------------------------------------------------

    if selected == correct_answer:

        st.success(
            "✅ Correct! You remembered it."
        )


    # --------------------------------------------------------
    # INCORRECT
    # --------------------------------------------------------

    else:

        st.error(
            "❌ Not quite."
        )

        st.info(
            f"Correct answer: "
            f"**{correct_answer}**"
        )


    # --------------------------------------------------------
    # EXPLANATION
    # --------------------------------------------------------

    explanation = (
        current_question["explanation"]
    )

    st.html(
        f"""
        <div class="explanation-card">

            <div class="explanation-title">
                💡 Explanation
            </div>

            <div class="explanation-text">
                {explanation}
            </div>

        </div>
        """
    )


    st.write("")


    # ========================================================
    # NEXT QUESTION
    # ========================================================

    if current_index < total_questions - 1:

        if st.button(
            "Next Question →",
            type="primary",
            use_container_width=True,
            key="practice_next_question"
        ):

            st.session_state.practice_index += 1

            st.session_state.practice_submitted = False

            st.session_state.practice_selected_answer = None

            st.rerun()


    # ========================================================
    # FINISH PRACTICE
    # ========================================================

    else:

        if st.button(
            "🏁 Finish Practice",
            type="primary",
            use_container_width=True,
            key="practice_finish"
        ):

            st.session_state.practice_finished = True

            st.session_state.practice_submitted = False

            st.rerun()