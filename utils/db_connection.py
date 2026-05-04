import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# =========================
# ENV CONFIG
# =========================
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "cricbuzz")
DB_PORT = int(os.getenv("DB_PORT", 3307))


# =========================
# CONNECTION
# =========================
def create_connection(database=None):
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=database,
        port=DB_PORT,
        autocommit=True
    )


# =========================
# SCHEMA (USED BY STREAMLIT)
# =========================
def get_mysql_schema(host, user, password):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=DB_PORT
    )

    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in cursor.fetchall()]

    excluded = {"information_schema", "mysql", "performance_schema", "sys"}
    schema = {}

    for db in databases:
        if db in excluded:
            continue

        try:
            cursor.execute(f"SHOW TABLES FROM {db}")
            tables = cursor.fetchall()

            schema[db] = {
                "tables": {t[0]: [] for t in tables}
            }

        except:
            schema[db] = {"tables": {}}

    cursor.close()
    conn.close()
    return schema


# =========================
# TABLE COLUMNS (FIXED FOR CRUD UI)
# =========================
def get_table_columns(host, user, password, database, table):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=DB_PORT
    )

    cur = conn.cursor(dictionary=True)
    cur.execute(f"DESCRIBE `{table}`")
    cols = cur.fetchall()
    conn.close()

    # normalize keys for Streamlit UI
    return [
        {
            "name": c["Field"],
            "type": c["Type"],
            "null": c["Null"],
            "key": c["Key"],
            "default": c["Default"],
            "extra": c["Extra"],
        }
        for c in cols
    ]


# =========================
# FETCH TABLE
# =========================
def fetch_table(host, user, password, database, table, limit=100):
    conn = create_connection(database)

    sql = f"SELECT * FROM `{table}` LIMIT {int(limit)}"
    df = pd.read_sql(sql, conn)
    conn.close()

    return df, sql


# =========================
# SELECT QUERY
# =========================
def run_select(host, user, password, database, query):
    if not query.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    conn = create_connection(database)
    try:
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()


# =========================
# INSERT
# =========================
def insert_row(host, user, password, database, table, data):
    if not data:
        raise ValueError("No data provided")

    conn = create_connection(database)

    cols = ", ".join([f"`{c}`" for c in data.keys()])
    vals = ", ".join(["%s"] * len(data))

    sql = f"INSERT INTO `{table}` ({cols}) VALUES ({vals})"

    cur = conn.cursor()
    cur.execute(sql, list(data.values()))

    affected = cur.rowcount
    conn.close()

    return affected, sql


# =========================
# DELETE
# =========================
def delete_rows(host, user, password, database, table, where):
    if not where.strip():
        raise ValueError("WHERE clause required")

    sql = f"DELETE FROM `{table}` WHERE {where}"

    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute(sql)

    affected = cur.rowcount
    conn.close()

    return affected, sql


# =========================
# UPDATE
# =========================
def execute_update(host, user, password, database, table, set_clause, where_clause):
    if not set_clause.strip():
        raise ValueError("SET clause required")

    if not where_clause.strip():
        raise ValueError("WHERE clause required")

    sql = f"UPDATE `{table}` SET {set_clause} WHERE {where_clause}"

    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute(sql)

    affected = cur.rowcount
    conn.close()

    return affected, sql