from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


@app.route("/")
def home():
    return jsonify({
        "message": "Kubernetes CI/CD application is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/db")
def database():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT version();")
        version = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            "database": "connected",
            "version": version[0]
        })

    except Exception as e:
        return jsonify({
            "database": "connection failed",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)