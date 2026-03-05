from mcp.server.fastmcp import FastMCP
import json
import sqlite3
from typing import Dict, List, Any
import re
from sqlite_helper import create_db, load_csv_to_table

mcp = FastMCP("data-query-builder")

conn = create_db()

query_history: List[str] = []

FORBIDDEN_SQL = [
    "DROP",
    "DELETE",
    "ALTER",
    "INSERT",
    "UPDATE",
    "CREATE",
    "REPLACE",
    "TRUNCATE",
    "ATTACH",
    "DETACH",
    "PRAGMA",
]


def is_safe(query: str) -> bool:
    """
    Validate that the SQL query is read-only.
    Only SELECT statements are allowed.
    """

    q = query.strip().upper()

    # must start with SELECT
    if not q.startswith("SELECT"):
        return False

    # prevent multi-statements
    if ";" in q[:-1]:
        return False

    # block dangerous keywords
    for word in FORBIDDEN_SQL:
        if re.search(rf"\b{word}\b", q):
            return False

    return True


# ---------------- TOOLS ----------------


@mcp.tool()
def load_csv(file_path: str, table_name: str) -> Dict:
    """
    Load a CSV file into a SQLite table with automatic type detection.
    """
    try:
        return load_csv_to_table(conn, file_path, table_name)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def list_tables() -> List[Dict]:
    """
    List all tables and their row counts.
    """

    try:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()

        result = []

        for t in tables:
            name = t["name"]

            count = conn.execute(f'SELECT COUNT(*) as c FROM "{name}"').fetchone()["c"]

            result.append({"table": name, "rows": count})

        return result

    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
def describe_schema() -> Dict:
    """
    Return the schema of all tables and columns.
    """

    schema = {}

    try:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()

        for t in tables:
            name = t["name"]

            cols = conn.execute(f'PRAGMA table_info("{name}")').fetchall()

            schema[name] = [{"column": c["name"], "type": c["type"]} for c in cols]

        return schema

    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def run_query(query: str) -> Dict[str, Any]:
    """
    Execute a read-only SQL query (SELECT only).
    Destructive queries are rejected for security reasons.
    """

    try:

        if not is_safe(query):
            return {
                "error": "Query rejected. Only single SELECT statements are allowed."
            }

        cur = conn.execute(query)
        MAX_ROWS = 1000
        rows = [dict(r) for r in cur.fetchall()[:MAX_ROWS]]

        query_history.append(query)

        return {
            "columns": [c[0] for c in cur.description],
            "rows": rows,
        }

    except Exception as e:
        return {"error": str(e)}


# ---------------- RESOURCES ----------------


@mcp.resource("db://schema")
def schema_resource() -> str:
    return json.dumps(describe_schema(), indent=2)


@mcp.resource("db://query-history")
def history_resource() -> str:
    return json.dumps(query_history, indent=2)


@mcp.resource("info:/server")
def server_info() -> str:
    return json.dumps(
        {
            "name": "data-query-builder",
            "version": "1.0",
            "tools": ["load_csv", "list_tables", "describe_schema", "run_query"],
        }
    )


# ---------------- START ----------------

if __name__ == "__main__":
    mcp.run()
