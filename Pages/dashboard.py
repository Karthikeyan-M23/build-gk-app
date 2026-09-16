import streamlit as st

from utils.navigation import render_sidebar
from utils.database import (
    get_dashboard_stats,
    get_recent_quizzes,
    get_category_performance,
    get_performance_trend,
    get_category_analytics,
    get_difficulty_analytics,
    get_best_score,
    get_wrong_questions,
    get_question_statistics,
    get_question_category_performance
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Dashboard | GK AI",
    page_icon="📊",
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
# HEADER
# ============================================================

st.html(
    """
    <div class="page-header">

        <div class="page-badge">
            YOUR PERFORMANCE
        </div>

        <h1>Knowledge Dashboard</h1>

        <p>
            Track your quiz performance,
            accuracy and learning progress.
        </p>

    </div>
    """
)


# ============================================================
# LOAD DATABASE DATA
# ============================================================

stats = get_dashboard_stats()

recent_quizzes = get_recent_quizzes(
    limit=10
)

category_data = get_category_performance()

performance_data = get_performance_trend()

category_analytics = get_category_analytics()

difficulty_analytics = get_difficulty_analytics()

best_score = get_best_score()

question_stats = get_question_statistics()

wrong_questions = get_wrong_questions(
    limit=20
)

question_category_data = (
    get_question_category_performance()
)

# ============================================================
# TOP STATISTICS
# ============================================================

st.html(
    f"""
    <div class="stats-grid">

        <div class="stat-card">

            <div class="stat-label">
                TOTAL QUIZZES
            </div>

            <div class="stat-value">
                {stats["total_quizzes"]}
            </div>

        </div>


        <div class="stat-card">

            <div class="stat-label">
                QUESTIONS ANSWERED
            </div>

            <div class="stat-value">
                {stats["total_questions"]}
            </div>

        </div>


        <div class="stat-card">

            <div class="stat-label">
                CORRECT ANSWERS
            </div>

            <div class="stat-value">
                {stats["total_correct"]}
            </div>

        </div>


        <div class="stat-card">

            <div class="stat-label">
                OVERALL ACCURACY
            </div>

            <div class="stat-value">
                {stats["accuracy"]:.1f}%
            </div>

        </div>

    </div>
    """
)


# ============================================================
# PERSONAL BEST
# ============================================================

st.html("<br>")

st.html(
    f"""
    <div class="best-score-card">

        <div class="best-score-icon">
            🏆
        </div>

        <div>

            <div class="best-score-label">
                PERSONAL BEST
            </div>

            <div class="best-score-value">
                {best_score:.1f}%
            </div>

        </div>

    </div>
    """
)

# ============================================================
# QUESTION STATISTICS
# ============================================================

st.html("<br>")

st.html(
    """
    <div class="section-title">
        🧠 Question Performance
    </div>
    """
)

st.html(
    f"""
    <div class="question-stats-grid">

        <div class="question-stat-card">

            <div class="question-stat-label">
                TOTAL QUESTIONS
            </div>

            <div class="question-stat-value">
                {question_stats["total_questions"]}
            </div>

        </div>


        <div class="question-stat-card">

            <div class="question-stat-label">
                CORRECT
            </div>

            <div class="question-stat-value">
                {question_stats["correct_questions"]}
            </div>

        </div>


        <div class="question-stat-card">

            <div class="question-stat-label">
                NEEDS REVIEW
            </div>

            <div class="question-stat-value">
                {question_stats["wrong_questions"]}
            </div>

        </div>

    </div>
    """
)

# ============================================================
# QUESTIONS TO REVIEW
# ============================================================

st.html("<br>")

st.html(
    """
    <div class="section-title">
        🔁 Questions to Review
    </div>
    """
)


if not wrong_questions:

    st.success(
        "🎉 No incorrect questions. "
        "You're doing great!"
    )

else:

    for question in wrong_questions:

        with st.expander(
            f"❌ {question['question_text']}"
        ):

            st.markdown(
                f"**Your answer:** "
                f"{question['selected_answer']}"
            )

            st.markdown(
                f"**Correct answer:** "
                f"{question['correct_answer']}"
            )

            st.markdown(
                f"**Explanation:** "
                f"{question['explanation']}"
            )

            st.caption(
                f"{question['category']} "
                f"• "
                f"{question['difficulty']}"
            )

# ============================================================
# QUESTION ACCURACY BY CATEGORY
# ============================================================

st.html("<br>")

st.html(
    """
    <div class="section-title">
        🎯 Question Accuracy by Category
    </div>
    """
)


if question_category_data:

    category_question_chart = {
        "Category": [
            row["category"]
            for row in question_category_data
        ],
        "Accuracy": [
            (
                row["correct_questions"]
                /
                row["total_questions"]
            ) * 100
            for row in question_category_data
        ]
    }

    st.bar_chart(
        category_question_chart,
        x="Category",
        y="Accuracy",
        height=350
    )

else:

    st.info(
        "Complete quizzes to see question-level "
        "category accuracy."
    )


# ============================================================
# PERFORMANCE TREND
# ============================================================

st.html("<br>")

st.html(
    """
    <div class="section-title">
        📈 Performance Trend
    </div>
    """
)


if performance_data:

    trend_data = {
        "Quiz": [
            f"Quiz {index + 1}"
            for index in range(
                len(performance_data)
            )
        ],
        "Score": [
            row["score_percentage"]
            for row in performance_data
        ]
    }

    st.line_chart(
        trend_data,
        x="Quiz",
        y="Score",
        height=350
    )

else:

    st.info(
        "Complete quizzes to build your performance trend."
    )


# ============================================================
# CATEGORY ANALYTICS
# ============================================================

st.html("<br>")

st.html(
    """
    <div class="section-title">
        🎯 Category Analytics
    </div>
    """
)


if category_analytics:

    category_chart_data = {
        "Category": [
            row["category"]
            for row in category_analytics
        ],
        "Average Score": [
            row["average_score"]
            for row in category_analytics
        ]
    }

    st.bar_chart(
        category_chart_data,
        x="Category",
        y="Average Score",
        height=350
    )

else:

    st.info(
        "Complete quizzes to see category analytics."
    )


# ============================================================
# DIFFICULTY ANALYTICS
# ============================================================

st.html("<br>")

st.html(
    """
    <div class="section-title">
        🧠 Difficulty Performance
    </div>
    """
)


if difficulty_analytics:

    difficulty_chart_data = {
        "Difficulty": [
            row["difficulty"]
            for row in difficulty_analytics
        ],
        "Average Score": [
            row["average_score"]
            for row in difficulty_analytics
        ]
    }

    st.bar_chart(
        difficulty_chart_data,
        x="Difficulty",
        y="Average Score",
        height=300
    )

else:

    st.info(
        "Complete quizzes at different difficulties "
        "to compare performance."
    )


# ============================================================
# RECENT QUIZ HISTORY
# ============================================================

st.html("<br>")

st.html(
    """
    <div class="section-title">
        📚 Recent Quiz History
    </div>
    """
)


if not recent_quizzes:

    st.info(
        "You haven't completed any quizzes yet."
    )

else:

    for quiz in recent_quizzes:

        score = quiz["score_percentage"]

        if score >= 80:
            performance = "Excellent"

        elif score >= 60:
            performance = "Good"

        elif score >= 40:
            performance = "Needs Practice"

        else:
            performance = "Keep Learning"


        st.html(
            f"""
            <div class="quiz-history-card">

                <div class="quiz-history-main">

                    <div class="quiz-history-category">
                        {quiz["category"]}
                    </div>

                    <div class="quiz-history-meta">
                        {quiz["difficulty"]}
                        &nbsp; • &nbsp;
                        {quiz["total_questions"]}
                        questions
                    </div>

                </div>


                <div class="quiz-history-score">

                    <div class="quiz-score">
                        {quiz["correct_answers"]}
                        /
                        {quiz["total_questions"]}
                    </div>

                    <div class="quiz-percentage">
                        {score:.0f}%
                    </div>

                    <div class="quiz-performance">
                        {performance}
                    </div>

                </div>

            </div>
            """
        )


# ============================================================
# CATEGORY PERFORMANCE DETAILS
# ============================================================

st.html("<br>")

st.html(
    """
    <div class="section-title">
        📊 Category Details
    </div>
    """
)


if not category_data:

    st.info(
        "Complete more quizzes to see category details."
    )

else:

    for category in category_data:

        average_score = category["average_score"]

        st.html(
            f"""
            <div class="category-performance-card">

                <div class="category-info">

                    <div class="category-name">
                        {category["category"]}
                    </div>

                    <div class="category-meta">
                        {category["quiz_count"]}
                        quizzes
                        &nbsp; • &nbsp;
                        {category["total_questions"]}
                        questions
                    </div>

                </div>


                <div class="category-result">

                    <div class="category-score">
                        {average_score:.1f}%
                    </div>

                    <div class="category-correct">
                        {category["total_correct"]}
                        correct
                    </div>

                </div>

            </div>
            """
        )


# ============================================================
# REFRESH DASHBOARD
# ============================================================

st.html("<br>")

if st.button(
    "🔄 Refresh Dashboard",
    use_container_width=True
):

    st.rerun()