import re
import sqlite3

from app.config import DATABASE_PATH


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def run_select(query: str):
    """Execute one read-only SELECT query and return rows as dictionaries."""
    sql = query.strip().rstrip(";").strip()

    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    if ";" in sql or "--" in sql or "/*" in sql:
        raise ValueError("Multiple statements and SQL comments are not allowed.")

    if re.search(
        r"\b(insert|update|delete|drop|alter|create|replace|truncate)\b",
        sql,
        re.IGNORECASE,
    ):
        raise ValueError("Write operations are not allowed.")

    database_uri = DATABASE_PATH.resolve().as_uri() + "?mode=ro"
    connection = sqlite3.connect(database_uri, uri=True)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.execute(sql)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()
