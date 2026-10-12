from pathlib import Path

from app.database import get_connection
from app.config import KNOWLEDGE_PATH


def import_knowledge():
    KNOWLEDGE_PATH.mkdir(parents=True, exist_ok=True)
    files = sorted(KNOWLEDGE_PATH.glob("*.md"))

    if not files:
        print("No Markdown articles found.")
        return

    with get_connection() as connection:
        for file_path in files:
            content = file_path.read_text(encoding="utf-8-sig", errors="replace")
            lines = content.splitlines()

            title = next(
                (line.removeprefix("# ").strip()
                 for line in lines if line.startswith("# ")),
                file_path.stem
            )

            category = file_path.stem.replace("_", " ").title()

            source_index = next(
                (i for i, line in enumerate(lines)
                 if line.strip() == "## Source"),
                None
            )

            source = None
            if source_index is not None:
                source = next(
                    (line.strip() for line in lines[source_index + 1:]
                     if line.strip().startswith("http")),
                    None
                )

            existing = connection.execute(
                "SELECT id FROM knowledge_articles "
                "WHERE title = ? AND category = ?",
                (title, category)
            ).fetchone()

            if existing:
                connection.execute(
                    "UPDATE knowledge_articles "
                    "SET content = ?, source = ? WHERE id = ?",
                    (content, source, existing["id"])
                )
                print(f"Updated: {title}")
            else:
                connection.execute(
                    "INSERT INTO knowledge_articles "
                    "(title, category, content, source) "
                    "VALUES (?, ?, ?, ?)",
                    (title, category, content, source)
                )
                print(f"Imported: {title}")

    print(f"Finished processing {len(files)} articles.")


if __name__ == "__main__":
    import_knowledge()

