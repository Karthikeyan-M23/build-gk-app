import sqlite3
from pathlib import Path


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "gk_ai.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------------------------
    # QUIZZES TABLE
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            total_questions INTEGER NOT NULL,
            correct_answers INTEGER DEFAULT 0,
            score_percentage REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # --------------------------------------------------------
    # QUIZ QUESTIONS TABLE
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            question_number INTEGER NOT NULL,
            question_text TEXT NOT NULL,

            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            option_d TEXT,

            selected_answer TEXT,
            correct_answer TEXT NOT NULL,
            is_correct INTEGER DEFAULT 0,
            explanation TEXT,

            FOREIGN KEY (quiz_id)
                REFERENCES quizzes(id)
        )
        """
    )

    # ========================================================
    # DATABASE MIGRATION
    # ========================================================
    # Your existing database already has quiz_questions.
    # Add the new option columns without deleting old data.
    # ========================================================

    cursor.execute(
        "PRAGMA table_info(quiz_questions)"
    )

    existing_columns = {
        row["name"]
        for row in cursor.fetchall()
    }

    required_columns = {
        "option_a": "TEXT",
        "option_b": "TEXT",
        "option_c": "TEXT",
        "option_d": "TEXT"
    }

    for column_name, column_type in required_columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE quiz_questions
                ADD COLUMN {column_name} {column_type}
                """
            )

    # --------------------------------------------------------
    # INDEX
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_quiz_questions_quiz_id
        ON quiz_questions(quiz_id)
        """
    )

    connection.commit()
    connection.close()


# ============================================================
# SAVE QUIZ RESULT
# ============================================================

def save_quiz_result(
    category,
    difficulty,
    questions
):
    """
    Save a completed quiz and all its questions.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:

        total_questions = len(questions)

        correct_answers = sum(
            1
            for question in questions
            if question.get("selected_answer")
            == question.get("correct_answer")
        )

        if total_questions > 0:

            score_percentage = (
                correct_answers /
                total_questions
            ) * 100

        else:

            score_percentage = 0

        # ----------------------------------------------------
        # SAVE QUIZ
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO quizzes (
                category,
                difficulty,
                total_questions,
                correct_answers,
                score_percentage
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                category,
                difficulty,
                total_questions,
                correct_answers,
                score_percentage
            )
        )

        quiz_id = cursor.lastrowid

        # ----------------------------------------------------
        # SAVE QUESTIONS
        # ----------------------------------------------------

        for index, question in enumerate(
            questions,
            start=1
        ):

            options = question.get(
                "options",
                []
            )

            # Safely get all four options
            option_a = (
                options[0]
                if len(options) > 0
                else None
            )

            option_b = (
                options[1]
                if len(options) > 1
                else None
            )

            option_c = (
                options[2]
                if len(options) > 2
                else None
            )

            option_d = (
                options[3]
                if len(options) > 3
                else None
            )

            selected_answer = question.get(
                "selected_answer"
            )

            correct_answer = question.get(
                "correct_answer"
            )

            is_correct = int(
                selected_answer == correct_answer
            )

            cursor.execute(
                """
                INSERT INTO quiz_questions (
                    quiz_id,
                    question_number,
                    question_text,

                    option_a,
                    option_b,
                    option_c,
                    option_d,

                    selected_answer,
                    correct_answer,
                    is_correct,
                    explanation
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    quiz_id,
                    index,
                    question.get("question"),

                    option_a,
                    option_b,
                    option_c,
                    option_d,

                    selected_answer,
                    correct_answer,
                    is_correct,
                    question.get("explanation")
                )
            )

        connection.commit()

        return quiz_id

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

def get_dashboard_stats():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_quizzes,

            COALESCE(
                SUM(total_questions),
                0
            ) AS total_questions,

            COALESCE(
                SUM(correct_answers),
                0
            ) AS total_correct

        FROM quizzes
        """
    )

    result = cursor.fetchone()

    connection.close()

    total_quizzes = result["total_quizzes"]
    total_questions = result["total_questions"]
    total_correct = result["total_correct"]

    if total_questions > 0:

        accuracy = (
            total_correct /
            total_questions
        ) * 100

    else:

        accuracy = 0

    return {
        "total_quizzes": total_quizzes,
        "total_questions": total_questions,
        "total_correct": total_correct,
        "accuracy": accuracy
    }


# ============================================================
# RECENT QUIZ HISTORY
# ============================================================

def get_recent_quizzes(limit=10):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            category,
            difficulty,
            total_questions,
            correct_answers,
            score_percentage,
            created_at

        FROM quizzes

        ORDER BY id DESC

        LIMIT ?
        """,
        (limit,)
    )

    results = cursor.fetchall()

    connection.close()

    return results


# ============================================================
# CATEGORY PERFORMANCE
# ============================================================

def get_category_performance():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            category,
            COUNT(*) AS quiz_count,
            SUM(total_questions) AS total_questions,
            SUM(correct_answers) AS total_correct,
            AVG(score_percentage) AS average_score

        FROM quizzes

        GROUP BY category

        ORDER BY average_score DESC
        """
    )

    results = cursor.fetchall()

    connection.close()

    return results


# ============================================================
# PERFORMANCE TREND
# ============================================================

def get_performance_trend():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            category,
            difficulty,
            score_percentage,
            created_at

        FROM quizzes

        ORDER BY id ASC
        """
    )

    results = cursor.fetchall()

    connection.close()

    return results


# ============================================================
# CATEGORY ANALYTICS
# ============================================================

def get_category_analytics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            category,
            COUNT(*) AS quiz_count,
            SUM(total_questions) AS total_questions,
            SUM(correct_answers) AS total_correct,
            AVG(score_percentage) AS average_score,
            MAX(score_percentage) AS best_score

        FROM quizzes

        GROUP BY category

        ORDER BY average_score DESC
        """
    )

    results = cursor.fetchall()

    connection.close()

    return results


# ============================================================
# DIFFICULTY ANALYTICS
# ============================================================

def get_difficulty_analytics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            difficulty,
            COUNT(*) AS quiz_count,
            SUM(total_questions) AS total_questions,
            SUM(correct_answers) AS total_correct,
            AVG(score_percentage) AS average_score

        FROM quizzes

        GROUP BY difficulty

        ORDER BY
            CASE difficulty
                WHEN 'Easy' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Hard' THEN 3
                ELSE 4
            END
        """
    )

    results = cursor.fetchall()

    connection.close()

    return results


# ============================================================
# BEST SCORE
# ============================================================

def get_best_score():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            score_percentage

        FROM quizzes

        ORDER BY score_percentage DESC

        LIMIT 1
        """
    )

    result = cursor.fetchone()

    connection.close()

    if result:

        return result["score_percentage"]

    return 0


# ============================================================
# WRONG QUESTIONS
# ============================================================

def get_wrong_questions(limit=20):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            qq.id,
            qq.quiz_id,
            qq.question_number,
            qq.question_text,

            qq.option_a,
            qq.option_b,
            qq.option_c,
            qq.option_d,

            qq.selected_answer,
            qq.correct_answer,
            qq.explanation,

            q.category,
            q.difficulty,
            q.created_at

        FROM quiz_questions qq

        JOIN quizzes q
            ON qq.quiz_id = q.id

        WHERE qq.is_correct = 0

        ORDER BY qq.id DESC

        LIMIT ?
        """,
        (limit,)
    )

    results = cursor.fetchall()

    connection.close()

    return results


# ============================================================
# QUESTION STATISTICS
# ============================================================

def get_question_statistics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_questions,

            SUM(
                CASE
                    WHEN is_correct = 1
                    THEN 1
                    ELSE 0
                END
            ) AS correct_questions,

            SUM(
                CASE
                    WHEN is_correct = 0
                    THEN 1
                    ELSE 0
                END
            ) AS wrong_questions

        FROM quiz_questions
        """
    )

    result = cursor.fetchone()

    connection.close()

    return {
        "total_questions":
            result["total_questions"] or 0,

        "correct_questions":
            result["correct_questions"] or 0,

        "wrong_questions":
            result["wrong_questions"] or 0
    }


# ============================================================
# QUESTION PERFORMANCE BY CATEGORY
# ============================================================

def get_question_category_performance():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            q.category,

            COUNT(qq.id)
                AS total_questions,

            SUM(
                CASE
                    WHEN qq.is_correct = 1
                    THEN 1
                    ELSE 0
                END
            ) AS correct_questions

        FROM quiz_questions qq

        JOIN quizzes q
            ON qq.quiz_id = q.id

        GROUP BY q.category

        ORDER BY
            (
                CAST(
                    SUM(
                        CASE
                            WHEN qq.is_correct = 1
                            THEN 1
                            ELSE 0
                        END
                    ) AS REAL
                )
                /
                COUNT(qq.id)
            ) ASC
        """
    )

    results = cursor.fetchall()

    connection.close()

    return results


# ============================================================
# PRACTICE QUESTIONS
# ============================================================

def get_practice_questions(limit=10):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            qq.id,
            qq.quiz_id,
            qq.question_number,
            qq.question_text,

            qq.option_a,
            qq.option_b,
            qq.option_c,
            qq.option_d,

            qq.selected_answer,
            qq.correct_answer,
            qq.explanation,

            q.category,
            q.difficulty

        FROM quiz_questions qq

        JOIN quizzes q
            ON qq.quiz_id = q.id

        WHERE qq.is_correct = 0

        ORDER BY qq.id DESC

        LIMIT ?
        """,
        (limit,)
    )

    results = cursor.fetchall()

    connection.close()

    return results


# ============================================================
# GET QUESTION BY ID
# ============================================================

def get_question_by_id(question_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            qq.id,
            qq.quiz_id,
            qq.question_number,
            qq.question_text,

            qq.option_a,
            qq.option_b,
            qq.option_c,
            qq.option_d,

            qq.selected_answer,
            qq.correct_answer,
            qq.explanation,

            q.category,
            q.difficulty

        FROM quiz_questions qq

        JOIN quizzes q
            ON qq.quiz_id = q.id

        WHERE qq.id = ?
        """,
        (question_id,)
    )

    result = cursor.fetchone()

    connection.close()

    return result


# ============================================================
# DATABASE TEST
# ============================================================

if __name__ == "__main__":

    initialize_database()

    print(
        "Database initialized successfully."
    )

    print(
        f"Database location: {DATABASE_PATH}"
    )