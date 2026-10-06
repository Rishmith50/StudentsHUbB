import csv
import datetime
from functools import wraps
import io

from flask import Flask, Response, flash, redirect, render_template, request, session, url_for
import mysql.connector
from werkzeug.security import check_password_hash
from database import get_db_connection

app = Flask(__name__)
app.secret_key = "studenthub-session-reset-key-v3"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to access this page.", "error")
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Please provide both username and password.", "error")
            return render_template("login.html", username=username)

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s LIMIT 1", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and check_password_hash(user["password_hash"], password):
            session.permanent = False
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user.get("role", "admin")
            flash(f"Welcome back, {user['username']}!", "success")
            next_url = request.args.get("next")
            if next_url and next_url.startswith("/"):
                return redirect(next_url)
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password. Please try again.", "error")
            return render_template("login.html", username=username)

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out successfully.", "success")
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM students")
    total_students = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM students WHERE status = 'Active'")
    active_students = cursor.fetchone()["total"]

    inactive_students = total_students - active_students

    cursor.execute("SELECT COUNT(*) AS total FROM courses")
    total_courses = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT
            students.id,
            students.name,
            courses.name AS course,
            students.status
        FROM students
        INNER JOIN courses
            ON students.course_id = courses.id
        ORDER BY students.id DESC
        LIMIT 5
        """
    )
    recent_students = cursor.fetchall()

    # --- Chart data: students per course ---
    cursor.execute(
        """
        SELECT courses.name AS course_name, COUNT(students.id) AS count
        FROM courses
        LEFT JOIN students ON students.course_id = courses.id
        GROUP BY courses.id, courses.name
        ORDER BY count DESC
        """
    )
    course_distribution = cursor.fetchall()
    course_labels = [r["course_name"] for r in course_distribution]
    course_counts = [int(r["count"]) for r in course_distribution]

    # --- Chart data: gender distribution ---
    cursor.execute(
        """
        SELECT gender, COUNT(*) AS count
        FROM students
        GROUP BY gender
        ORDER BY gender
        """
    )
    gender_rows = cursor.fetchall()
    gender_labels = [r["gender"] for r in gender_rows]
    gender_counts = [int(r["count"]) for r in gender_rows]

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        total_students=total_students,
        active_students=active_students,
        inactive_students=inactive_students,
        total_courses=total_courses,
        recent_students=recent_students,
        course_labels=course_labels,
        course_counts=course_counts,
        gender_labels=gender_labels,
        gender_counts=gender_counts,
    )


@app.route("/students")
@login_required
def students():
    search = request.args.get("search", "").strip()
    course_id = request.args.get("course_id", "")
    status = request.args.get("status", "")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            students.id,
            students.name,
            students.email,
            students.phone,
            students.gender,
            students.status,
            courses.name AS course
        FROM students
        INNER JOIN courses
            ON students.course_id = courses.id
        WHERE 1 = 1
    """
    parameters = []

    if search:
        query += """
            AND (
                students.name LIKE %s
                OR students.email LIKE %s
                OR students.phone LIKE %s
            )
        """
        search_value = f"%{search}%"
        parameters.extend([search_value, search_value, search_value])

    if course_id:
        query += " AND students.course_id = %s"
        parameters.append(course_id)

    if status:
        query += " AND students.status = %s"
        parameters.append(status)

    query += " ORDER BY students.id"

    cursor.execute(query, parameters)
    students_list = cursor.fetchall()

    cursor.execute("SELECT id, name FROM courses ORDER BY name")
    courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "students.html",
        students=students_list,
        courses=courses,
        search=search,
        selected_course=course_id,
        selected_status=status,
    )


@app.route("/add_students", methods=["GET", "POST"])
@login_required
def add_students():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id, name FROM courses ORDER BY name")
    courses = cursor.fetchall()

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        gender = request.form["gender"]
        course_id = request.form["course_id"]
        date_of_birth = request.form["date_of_birth"] or None
        status = request.form["status"]

        if not name or not email or not course_id:
            cursor.close()
            connection.close()
            flash("Name, email and course are required.", "error")
            return render_template(
                "add_students.html",
                student=request.form,
                courses=courses,
                form_title="Add Student",
            )

        try:
            cursor.execute(
                """
                INSERT INTO students
                    (name, email, phone, gender, course_id, date_of_birth, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (name, email, phone, gender, course_id, date_of_birth, status),
            )
            connection.commit()
            cursor.close()
            connection.close()

            flash("Student added successfully.", "success")
            return redirect(url_for("students"))

        except mysql.connector.Error as error:
            connection.rollback()
            cursor.close()
            connection.close()

            if error.errno == 1062:
                flash("A student with this email already exists.", "error")
            else:
                flash("Unable to add student. Check the information.", "error")

            return render_template(
                "add_students.html",
                student=request.form,
                courses=courses,
                form_title="Add Student",
            )

    cursor.close()
    connection.close()

    return render_template(
        "add_students.html",
        student=None,
        courses=courses,
        form_title="Add Student",
    )

@app.route("/attendance", methods=["GET", "POST"])
@login_required
def attendance():
    today = datetime.date.today().isoformat()
    selected_date = request.args.get("date") or request.form.get("date") or today

    # Validate date format (YYYY-MM-DD)
    try:
        datetime.date.fromisoformat(selected_date)
    except ValueError:
        selected_date = today

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        # Check active students to save attendance for
        cursor.execute("SELECT id FROM students WHERE status = 'Active'")
        active_students = cursor.fetchall()

        try:
            for s in active_students:
                student_id = s["id"]
                # Default status to Present if not marked Absent
                status_val = request.form.get(f"status_{student_id}", "Present")
                if status_val not in ("Present", "Absent"):
                    status_val = "Present"

                cursor.execute(
                    """
                    INSERT INTO attendance (student_id, attendance_date, status)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE status = %s
                    """,
                    (student_id, selected_date, status_val, status_val),
                )

            connection.commit()
            flash("Attendance saved successfully.", "success")
        except mysql.connector.Error as err:
            connection.rollback()
            flash(f"Error saving attendance: {err}", "error")

        cursor.close()
        connection.close()
        return redirect(url_for("attendance", date=selected_date))

    # GET Request:
    # 1. Check if attendance already marked for selected_date
    cursor.execute(
        "SELECT COUNT(*) AS cnt FROM attendance WHERE attendance_date = %s",
        (selected_date,),
    )
    already_marked = cursor.fetchone()["cnt"] > 0

    # 2. Fetch active students roster with their attendance status for selected_date
    cursor.execute(
        """
        SELECT
            students.id,
            students.name,
            courses.name AS course,
            attendance.status AS marked_status
        FROM students
        INNER JOIN courses
            ON students.course_id = courses.id
        LEFT JOIN attendance
            ON students.id = attendance.student_id
            AND attendance.attendance_date = %s
        WHERE students.status = 'Active'
        ORDER BY students.id
        """,
        (selected_date,),
    )
    roster = cursor.fetchall()

    # 3. Fetch attendance summary for all students
    cursor.execute(
        """
        SELECT
            students.id,
            students.name,
            courses.name AS course,
            COUNT(attendance.id) AS total_days,
            SUM(CASE WHEN attendance.status = 'Present' THEN 1 ELSE 0 END) AS present_days,
            SUM(CASE WHEN attendance.status = 'Absent' THEN 1 ELSE 0 END) AS absent_days
        FROM students
        INNER JOIN courses
            ON students.course_id = courses.id
        LEFT JOIN attendance
            ON students.id = attendance.student_id
        GROUP BY students.id, students.name, courses.name
        ORDER BY students.id
        """
    )
    summary_rows = cursor.fetchall()

    summary = []
    for row in summary_rows:
        total = int(row["total_days"] or 0)
        present = int(row["present_days"] or 0)
        absent = int(row["absent_days"] or 0)
        pct = round((present / total) * 100, 1) if total > 0 else None
        summary.append(
            {
                "id": row["id"],
                "name": row["name"],
                "course": row["course"],
                "total_days": total,
                "present_days": present,
                "absent_days": absent,
                "percentage": pct,
            }
        )

    cursor.close()
    connection.close()

    return render_template(
        "attendance.html",
        roster=roster,
        summary=summary,
        selected_date=selected_date,
        already_marked=already_marked,
        today=today,
    )


@app.route("/export/attendance.csv")
@login_required
def export_attendance_csv():
    date_filter = request.args.get("date")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            attendance.attendance_date,
            students.id AS student_id,
            students.name AS student_name,
            courses.name AS course,
            attendance.status
        FROM attendance
        INNER JOIN students
            ON attendance.student_id = students.id
        INNER JOIN courses
            ON students.course_id = courses.id
    """
    params = []
    if date_filter:
        query += " WHERE attendance.attendance_date = %s"
        params.append(date_filter)

    query += " ORDER BY attendance.attendance_date DESC, students.id ASC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Student ID", "Student Name", "Course", "Status"])
    for r in rows:
        writer.writerow(
            [
                r["attendance_date"].isoformat() if hasattr(r["attendance_date"], "isoformat") else r["attendance_date"],
                r["student_id"],
                r["student_name"],
                r["course"],
                r["status"],
            ]
        )

    filename = f"attendance_{date_filter}.csv" if date_filter else "attendance_all.csv"
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.route("/export/attendance_summary.csv")
@login_required
def export_attendance_summary_csv():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            students.id,
            students.name,
            courses.name AS course,
            COUNT(attendance.id) AS total_days,
            SUM(CASE WHEN attendance.status = 'Present' THEN 1 ELSE 0 END) AS present_days,
            SUM(CASE WHEN attendance.status = 'Absent' THEN 1 ELSE 0 END) AS absent_days
        FROM students
        INNER JOIN courses
            ON students.course_id = courses.id
        LEFT JOIN attendance
            ON students.id = attendance.student_id
        GROUP BY students.id, students.name, courses.name
        ORDER BY students.id
        """
    )
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Student ID", "Student Name", "Course", "Present Days", "Absent Days", "Total Days", "Attendance %"])
    for r in rows:
        total = int(r["total_days"] or 0)
        present = int(r["present_days"] or 0)
        absent = int(r["absent_days"] or 0)
        pct_str = f"{(present / total * 100):.1f}%" if total > 0 else "N/A"
        writer.writerow([r["id"], r["name"], r["course"], present, absent, total, pct_str])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=attendance_summary.csv"},
    )


@app.route("/fees")
@login_required
def fees():
    selected_status = request.args.get("status", "").strip()

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            students.id,
            students.name,
            courses.name AS course,
            COALESCE(fees.total_fee, 50000.00) AS total_fee,
            COALESCE(fees.amount_paid, 0.00) AS amount_paid,
            fees.last_payment_date
        FROM students
        INNER JOIN courses
            ON students.course_id = courses.id
        LEFT JOIN fees
            ON students.id = fees.student_id
        ORDER BY students.id
        """
    )
    raw_rows = cursor.fetchall()

    cursor.close()
    connection.close()

    total_fees = 0.0
    collected = 0.0
    pending = 0.0
    rows = []

    for r in raw_rows:
        tf = float(r["total_fee"] or 0)
        pd = float(r["amount_paid"] or 0)
        pnd = max(0.0, tf - pd)

        if tf == 0:
            status = "Pending"
        elif pd >= tf:
            status = "Paid"
        elif pd > 0:
            status = "Partial"
        else:
            status = "Pending"

        total_fees += tf
        collected += pd
        pending += pnd

        if not selected_status or status.lower() == selected_status.lower():
            rows.append(
                {
                    "id": r["id"],
                    "name": r["name"],
                    "course": r["course"],
                    "total_fee": tf,
                    "amount_paid": pd,
                    "pending": pnd,
                    "fee_status": status,
                    "last_payment_date": r["last_payment_date"],
                }
            )

    paid_count = sum(1 for r in rows if r["fee_status"] == "Paid")
    partial_count = sum(1 for r in rows if r["fee_status"] == "Partial")
    pending_count = sum(1 for r in rows if r["fee_status"] == "Pending")

    return render_template(
        "fees.html",
        rows=rows,
        total_fees=total_fees,
        collected=collected,
        pending=pending,
        paid_count=paid_count,
        partial_count=partial_count,
        pending_count=pending_count,
        selected_status=selected_status,
    )


@app.route("/fees/pay/<int:student_id>", methods=["POST"])
@login_required
def pay_fee(student_id):
    try:
        amount = float(request.form.get("amount", 0))
    except (ValueError, TypeError):
        flash("Invalid payment amount. Please enter a valid number.", "error")
        return redirect(url_for("fees"))

    if amount <= 0:
        flash("Payment amount must be greater than zero.", "error")
        return redirect(url_for("fees"))

    today = datetime.date.today().isoformat()
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM fees WHERE student_id = %s", (student_id,))
        fee_record = cursor.fetchone()

        if fee_record:
            total_fee = float(fee_record["total_fee"])
            amount_paid = float(fee_record["amount_paid"])
            remaining = max(0.0, total_fee - amount_paid)
            if amount > remaining:
                flash(f"Amount exceeds remaining pending fee of ₹{remaining:,.0f}.", "error")
                return redirect(url_for("fees"))

            cursor.execute(
                """
                UPDATE fees
                SET amount_paid = amount_paid + %s,
                    last_payment_date = %s
                WHERE student_id = %s
                """,
                (amount, today, student_id),
            )
        else:
            if amount > 50000.00:
                flash("Amount exceeds total fee of ₹50,000.", "error")
                return redirect(url_for("fees"))

            cursor.execute(
                """
                INSERT INTO fees (student_id, total_fee, amount_paid, last_payment_date)
                VALUES (%s, 50000.00, %s, %s)
                """,
                (student_id, amount, today),
            )

        connection.commit()
        flash("Payment recorded successfully.", "success")
    except mysql.connector.Error as err:
        connection.rollback()
        flash(f"Error recording payment: {err}", "error")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("fees"))


@app.route("/export/fees.csv")
@login_required
def export_fees_csv():
    selected_status = request.args.get("status", "").strip()

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            students.id,
            students.name,
            courses.name AS course,
            COALESCE(fees.total_fee, 50000.00) AS total_fee,
            COALESCE(fees.amount_paid, 0.00) AS amount_paid,
            fees.last_payment_date
        FROM students
        INNER JOIN courses
            ON students.course_id = courses.id
        LEFT JOIN fees
            ON students.id = fees.student_id
        ORDER BY students.id
        """
    )
    raw_rows = cursor.fetchall()
    cursor.close()
    connection.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Student ID", "Name", "Course", "Total Fee", "Amount Paid", "Pending", "Status", "Last Payment Date"])

    for r in raw_rows:
        tf = float(r["total_fee"] or 0)
        pd = float(r["amount_paid"] or 0)
        pnd = max(0.0, tf - pd)

        if tf == 0:
            status = "Pending"
        elif pd >= tf:
            status = "Paid"
        elif pd > 0:
            status = "Partial"
        else:
            status = "Pending"

        if not selected_status or status.lower() == selected_status.lower():
            writer.writerow(
                [
                    r["id"],
                    r["name"],
                    r["course"],
                    tf,
                    pd,
                    pnd,
                    status,
                    r["last_payment_date"].isoformat() if r["last_payment_date"] else "—",
                ]
            )

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=fees.csv"},
    )


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)