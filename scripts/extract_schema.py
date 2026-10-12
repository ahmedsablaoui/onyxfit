import json
import sqlite3

from app.config import DATABASE_PATH, SCHEMA_PATH


def main():
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
        """)
        tables = [row[0] for row in cursor.fetchall()]

        schema = {}

        for table in tables:
            cursor.execute(f'PRAGMA table_info("{table}")')
            columns = cursor.fetchall()
            table_schema = []

            for column in columns:
                name, data_type = column[1], column[2]
                entry = {"column": name, "type": data_type}

                if "TEXT" in data_type.upper() or "CHAR" in data_type.upper():
                    cursor.execute(
                        f'SELECT DISTINCT "{name}" FROM "{table}" '
                        f'WHERE "{name}" IS NOT NULL LIMIT 5'
                    )
                    entry["sample_values"] = [
                        row[0] for row in cursor.fetchall()
                    ]

                table_schema.append(entry)

            schema[table] = table_schema

    SCHEMA_PATH.write_text(
        json.dumps(schema, indent=2),
        encoding="utf-8"
    )

    print(f"Schema written to {SCHEMA_PATH}")
    print(json.dumps(schema, indent=2))


if __name__ == "__main__":
    main()
