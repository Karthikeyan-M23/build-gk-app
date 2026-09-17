import streamlit as st

from utils.navigation import render_sidebar
from utils.quiz_engine import generate_quiz
from utils.database import initialize_database


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="GK Quiz",
    page_icon="🎯",
    layout="wide"
)

# ============================================================
# DATABASE
# ============================================================

initialize_database()


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
    "answered": False,
    "selected_answer": None,
    "quiz_finished": False,
    "quiz_total_questions": 0,
    "quiz_correct_answers": 0,
    "quiz_questions_answered": 0,
    "quiz_category": None,
    "quiz_difficulty": None,
    "quiz_answers": [],
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# QUIZ SETUP
# ============================================================

if st.session_state.quiz is None:

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.html(
        """
        <div class="quiz-header">

            <div class="hero-badge">
                🎯 KNOWLEDGE CHALLENGE
            </div>

            <h1 class="quiz-title">
                Test Your Knowledge
            </h1>

            <p class="quiz-subtitle">
                Choose your challenge and see how much you know.
            </p>

        </div>
        """
    )

    st.write("")

    # --------------------------------------------------------
    # SETTINGS CARD
    # --------------------------------------------------------

    st.html(
        """
        <div class="settings-card">

            <div class="settings-title">
                Quiz Settings
            </div>

        </div>
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        category = st.selectbox(
            "Category",
            [
                "Mixed",
                "Science",
                "History",
                "Geography",
                "Technology",
                "Sports",
                "Space",
                "Biology",
                "Literature",
                "Economics",
                "India GK",
                "Java"
            ]
        )

    with col2:

        difficulty = st.selectbox(
            "Difficulty",
            [
                "Easy",
                "Medium",
                "Hard"
            ]
        )

    with col3:

        number_of_questions = st.selectbox(
            "Questions",
            [5, 10, 15, 20]
        )

    st.write("")

    # --------------------------------------------------------
    # START QUIZ
    # --------------------------------------------------------

    if st.button(
        "🚀 Start Quiz",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Creating your personalized quiz..."
        ):

            try:

                quiz_data = generate_quiz(
                    category,
                    difficulty,
                    number_of_questions
                )
                st.session_state.quiz_category = category

                st.session_state.quiz_difficulty = difficulty

                st.session_state.quiz = quiz_data

                st.session_state.score = 0

                st.session_state.current_question = 0

                st.session_state.answered = False

                st.session_state.selected_answer = None

                st.session_state.quiz_finished = False

                st.session_state.quiz_total_questions = len(
                    quiz_data["questions"]
                )

                st.session_state.quiz_correct_answers = 0

                st.session_state.quiz_questions_answered = 0

                st.rerun()

            except Exception as e:

                st.error(
                    f"Unable to generate quiz: {e}"
                )


# ============================================================
# ACTIVE QUIZ
# ============================================================

else:

    questions = st.session_state.quiz["questions"]

    total_questions = len(questions)

    current_index = st.session_state.current_question


    # ========================================================
    # QUIZ COMPLETE
    # ========================================================

    if st.session_state.quiz_finished:

        score = st.session_state.score

        accuracy = (
            score / total_questions
        ) * 100


        # ----------------------------------------------------
        # COMPLETE HEADER
        # ----------------------------------------------------

        st.html(
            """
            <div class="quiz-complete">

                <div class="complete-icon">
                    🎉
                </div>

                <h1 class="complete-title">
                    Quiz Complete!
                </h1>

                <p class="complete-subtitle">
                    Great work. Here's your result.
                </p>

            </div>
            """
        )
        if "last_saved_quiz_id" in st.session_state:

            st.success(
                         "💾 Your quiz result has been saved."
                 )     

        st.write("")


        # ----------------------------------------------------
        # RESULT METRICS
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Score",
                f"{score} / {total_questions}"
            )

        with col2:

            st.metric(
                "Accuracy",
                f"{accuracy:.0f}%"
            )

        with col3:

            st.metric(
                "Questions",
                total_questions
            )


        st.write("")


        # ----------------------------------------------------
        # PERFORMANCE MESSAGE
        # ----------------------------------------------------

        if accuracy == 100:

            st.success(
                "🏆 Perfect score! Outstanding!"
            )

        elif accuracy >= 80:

            st.success(
                "🔥 Excellent performance!"
            )

        elif accuracy >= 60:

            st.info(
                "👍 Good job! Keep practicing."
            )

        else:

            st.warning(
                "💪 Keep learning and try again."
            )


        st.write("")


        # ----------------------------------------------------
        # PLAY AGAIN
        # ----------------------------------------------------

        if st.button(
            "🔄 Play Again",
            type="primary",
            use_container_width=True
        ):

            st.session_state.quiz = None

            st.session_state.score = 0

            st.session_state.current_question = 0

            st.session_state.answered = False

            st.session_state.selected_answer = None

            st.session_state.quiz_finished = False

            st.session_state.quiz_category = None

            st.session_state.quiz_difficulty = None     

            st.rerun()


    # ========================================================
    # CURRENT QUESTION
    # ========================================================

    else:

        question = questions[current_index]

        question_number = current_index + 1


        # ----------------------------------------------------
        # TOP BAR
        # ----------------------------------------------------

        col1, col2 = st.columns([3, 1])


        with col1:

            st.html(
                f"""
                <div class="question-counter">

                    QUESTION {question_number}
                    <span>OF {total_questions}</span>

                </div>
                """
            )


        with col2:

            st.html(
                f"""
                <div class="score-display">

                    🎯 Score: {st.session_state.score}

                </div>
                """
            )


        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        st.progress(
            question_number / total_questions
        )

        st.write("")


        # ----------------------------------------------------
        # QUESTION CARD
        # ----------------------------------------------------

        question_text = question["question"]

        st.html(
            f"""
            <div class="question-card">

                <div class="question-text">
                    {question_text}
                </div>

            </div>
            """
        )


        st.write("")


        # ----------------------------------------------------
        # ANSWER OPTIONS
        # ----------------------------------------------------

        selected_answer = st.radio(
            "Select your answer",
            question["options"],
            key=f"answer_{current_index}",
            disabled=st.session_state.answered
        )


        st.write("")


        # ----------------------------------------------------
        # SUBMIT ANSWER
        # ----------------------------------------------------

        if not st.session_state.answered:

            if st.button(
                "✓  Submit Answer",
                type="primary",
                use_container_width=True
            ):

                st.session_state.selected_answer = (
                    selected_answer
                )

                question["selected_answer"] = selected_answer

                st.session_state.answered = True

                st.session_state.quiz_questions_answered += 1

                st.session_state.total_questions_answered += 1


                # --------------------------------------------
                # CORRECT
                # --------------------------------------------

                if (
                    selected_answer
                    == question["correct_answer"]
                ):

                    st.session_state.score += 1

                    st.session_state.quiz_correct_answers += 1

                    st.session_state.total_correct_answers += 1


                st.rerun()


        # ====================================================
        # FEEDBACK
        # ====================================================

        else:

            # ------------------------------------------------
            # CORRECT
            # ------------------------------------------------

            if (
                st.session_state.selected_answer
                == question["correct_answer"]
            ):

                st.success(
                    "✅ Correct!"
                )

            # ------------------------------------------------
            # INCORRECT
            # ------------------------------------------------

            else:

                st.error(
                    f"❌ Incorrect — "
                    f"Correct answer: "
                    f"**{question['correct_answer']}**"
                )


            # ------------------------------------------------
            # EXPLANATION
            # ------------------------------------------------

            explanation = question["explanation"]

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


            # ------------------------------------------------
            # NEXT QUESTION
            # ------------------------------------------------

            if current_index < total_questions - 1:

                if st.button(
                    "Next Question →",
                    type="primary",
                    use_container_width=True
                ):

                    st.session_state.current_question += 1

                    st.session_state.answered = False

                    st.session_state.selected_answer = None

                    st.rerun()


            # ------------------------------------------------
            # FINISH QUIZ
            # ------------------------------------------------

            else:

               if st.button(
                        "🏁 Finish Quiz",
                        type="primary",
                        use_container_width=True
                    ):

                        from utils.database import save_quiz_result

                        try:

                            quiz_id = save_quiz_result(
                                category=st.session_state.quiz_category,
                                difficulty=st.session_state.quiz_difficulty,
                                questions=questions
                            )

                            st.session_state.last_saved_quiz_id = quiz_id

                            st.session_state.quiz_finished = True

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Unable to save quiz result: {e}"
                            )