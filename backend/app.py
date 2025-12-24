import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "zomato")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )


@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200


@app.route("/")
def home():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        return jsonify({"message": "Zomato Backend is running", "db": "connected"})
    except Exception as e:
        return jsonify({"message": "Database connection failed", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
