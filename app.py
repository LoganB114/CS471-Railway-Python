import os
import random
import string
import psycopg2

from flask import Flask, request

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


# =========================
# DATABASE CONNECTION
# =========================
def get_connection():
    return psycopg2.connect(DATABASE_URL)


# =========================
# RANDOM STRING GENERATOR
# =========================
def generate_random_string():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))


# =========================
# HOME PAGE
# =========================
@app.route("/")
def index():
    return "<h1>Python Railway App</h1>"


# =========================
# INPUT FORM
# =========================
@app.route("/dbinput", methods=["GET"])
def dbinput():

    return """
    <html>
    <body>

        <h1>Enter a String</h1>

        <form action="/dbinput" method="POST">
            <input type="text" name="userInput" required>
            <button type="submit">Submit</button>
        </form>

        <br>
        <a href="/database">View Database</a>

    </body>
    </html>
    """


# =========================
# HANDLE FORM SUBMISSION
# =========================
@app.route("/dbinput", methods=["POST"])
def submit_input():

    user_input = request.form["userInput"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS table_timestamp_and_random_string (
            tick timestamp,
            random_string varchar(50)
        )
    """)

    cur.execute(
        "INSERT INTO table_timestamp_and_random_string VALUES (NOW(), %s)",
        (user_input,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return """
    <html>
    <body>

        <h1>String Added Successfully</h1>

        <a href="/database">View Database</a>

    </body>
    </html>
    """


# =========================
# DATABASE PAGE
# =========================
@app.route("/database")
def database():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS table_timestamp_and_random_string (
            tick timestamp,
            random_string varchar(50)
        )
    """)

    # Insert random string each visit
    random_string = generate_random_string()

    cur.execute(
        "INSERT INTO table_timestamp_and_random_string VALUES (NOW(), %s)",
        (random_string,)
    )

    conn.commit()

    cur.execute(
        "SELECT tick, random_string FROM table_timestamp_and_random_string"
    )

    rows = cur.fetchall()

    output = """
    <html>
    <body>

        <h1>Database Records</h1>

        <ul>
    """

    for row in rows:
        output += f"<li>{row[0]} : {row[1]}</li>"

    output += """
        </ul>

        <a href="/dbinput">Add Another String</a>

    </body>
    </html>
    """

    cur.close()
    conn.close()

    return output