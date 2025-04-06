from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector
from mysql.connector import pooling

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Connection Pool
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "jctrucking_company"
}

connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **DB_CONFIG)

def get_db_connection():
    try:
        conn = connection_pool.get_connection()
        if conn.is_connected():
            print("Database connected successfully!")
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection failed: {e}")
        return None

# Home Route
@app.route("/")
def home():
    return render_template("index.html")

# Register Route
@app.route("/register", methods=["POST"])
def register():
    try:
        conn = get_db_connection()
        if conn is None:
            flash("Database connection failed!", "danger")
            return redirect(url_for("home"))
        cursor = conn.cursor()

        # Get user input
        username = request.form["username"].strip()
        full_name = request.form["full_name"].strip()
        password = request.form["password"].strip()
        role = request.form.get("role", "user").strip()
        email = request.form["email"].strip()
        contact_no = request.form["contact_no"].strip()
        age = request.form["age"].strip()
        address = request.form["address"].strip()

        # Validate input
        if not all([username, full_name, password, email, contact_no, age, address]):
            flash("All fields are required!", "danger")
            return redirect(url_for("home"))

        if role == "admin":
            flash("You cannot register as an admin!", "danger")
            return redirect(url_for("home"))

        # Check if username already exists
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            flash("Username already taken! Choose a different one.", "danger")
            return redirect(url_for("home"))

        # Insert new user into the database
        cursor.execute("""
            INSERT INTO users (username, full_name, password, email, contact_no, age, address, role) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, full_name, password, email, contact_no, age, address, role))

        conn.commit()
        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("home"))

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

    return redirect(url_for("home"))

# User Login
@app.route("/login", methods=["POST"])
def login():
    try:
        conn = get_db_connection()
        if conn is None:
            flash("Database connection failed!", "danger")
            return redirect(url_for("home"))
        cursor = conn.cursor()

        username = request.form["username"].strip()
        password = request.form["password"].strip()

        cursor.execute("SELECT username, password, role FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and user[1] == password:
            session["username"] = user[0]
            session["role"] = user[2]

            if user[2] == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

    return redirect(url_for("home"))

# User Dashboard Route (Uses usersdashboard.html)
@app.route("/dashboard")
def dashboard():
    if "username" in session and session.get("role") == "user":
        return render_template("usersdashboard.html", username=session["username"])
    flash("Unauthorized access!", "danger")
    return redirect(url_for("home"))

# Admin Dashboard Route
@app.route("/admin_dashboard")
def admin_dashboard():
    if "username" in session and session.get("role") == "admin":
        return render_template("admindashboard.html", username=session["username"])
    flash("Unauthorized access!", "danger")
    return redirect(url_for("home"))

# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
