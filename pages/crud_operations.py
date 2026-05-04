import streamlit as st
from utils.db_connection import (
    get_mysql_schema,
    fetch_table,
    run_select,
    insert_row,
    delete_rows,
    execute_update,
    get_table_columns,
)

def show_crud_operations():
    st.title("🛠️ CRUD Operations")
    st.caption("Create, Read, Update, Delete Records (MySQL + Streamlit)")

    st.divider()

    # ===============================
    # CONNECTION
    # ===============================
    st.header("🔌 MySQL Connection")

    host = st.text_input("Host", "127.0.0.1")
    user = st.text_input("User", "root")
    passwd = st.text_input("Password", type="password")

    if st.button("Connect & Load Schema"):
        try:
            schema = get_mysql_schema(host, user, passwd)
            st.session_state["schema"] = schema
            st.success(f"Connected! {len(schema)} databases loaded.")
        except Exception as e:
            st.error(f"Connection failed: {e}")

    schema = st.session_state.get("schema")

    if not schema:
        st.info("👉 Please connect to MySQL first")
        return

    st.divider()

    # ===============================
    # DATABASE + TABLE
    # ===============================
    st.header("📂 Explorer")

    dbs = sorted(schema.keys())
    database = st.selectbox("Database", dbs)

    tables = sorted(schema[database]["tables"].keys())

    if not tables:
        st.warning("No tables found")
        return

    table = st.selectbox("Table", tables)

    st.divider()

    # ===============================
    # READ DATA
    # ===============================
    st.header("📖 View Data")

    limit = st.number_input("Rows limit", 1, 10000, 100)

    if st.button("Load Table"):
        try:
            df, sql = fetch_table(host, user, passwd, database, table, limit)
            st.code(sql, language="sql")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

    st.divider()

    # ===============================
    # SELECT QUERY
    # ===============================
    st.header("🔍 Custom Query")

    query = st.text_area("SELECT query")

    if st.button("Run Query"):
        if not query.strip().lower().startswith("select"):
            st.error("Only SELECT allowed")
        else:
            try:
                df = run_select(host, user, passwd, database, query)
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Query error: {e}")

    st.divider()

    # ===============================
    # INSERT
    # ===============================
    st.header("➕ Insert Row")

    try:
        cols_meta = get_table_columns(host, user, passwd, database, table)
    except Exception as e:
        st.error(f"Column fetch error: {e}")
        return

    if cols_meta:
        with st.form("insert_form"):
            data = {}

            for col in cols_meta:
                name = col["name"]
                dtype = col["type"].lower()
                extra = (col["extra"] or "").lower()

                if "auto_increment" in extra:
                    continue

                if "int" in dtype:
                    data[name] = st.number_input(name, step=1)
                elif "float" in dtype or "double" in dtype:
                    data[name] = st.number_input(name)
                else:
                    data[name] = st.text_input(name)

            if st.form_submit_button("Insert"):
                try:
                    affected, sql = insert_row(host, user, passwd, database, table, data)
                    st.code(sql, language="sql")
                    st.success(f"Inserted {affected} row(s)")
                    st.rerun()
                except Exception as e:
                    st.error(f"Insert failed: {e}")

    st.divider()

    # ===============================
    # DELETE
    # ===============================
    st.header("🗑️ Delete Rows")

    with st.form("delete_form"):
        where = st.text_input("WHERE condition (e.g. id=1)")
        confirm = st.checkbox("Confirm delete")

        if st.form_submit_button("Delete"):
            if not confirm:
                st.warning("Confirm delete first")
            else:
                try:
                    affected, sql = delete_rows(host, user, passwd, database, table, where)
                    st.code(sql, language="sql")
                    st.success(f"Deleted {affected} row(s)")
                    st.rerun()
                except Exception as e:
                    st.error(f"Delete failed: {e}")

    st.divider()

    # ===============================
    # UPDATE
    # ===============================
    st.header("✏️ Update Rows")

    with st.form("update_form"):
        set_clause = st.text_input("SET clause (e.g. runs=50)")
        where_clause = st.text_input("WHERE clause (e.g. id=1)")

        if st.form_submit_button("Update"):
            if not set_clause or "=" not in set_clause:
                st.error("Invalid SET clause")
            elif not where_clause:
                st.error("WHERE required")
            else:
                try:
                    affected, sql = execute_update(
                        host, user, passwd, database, table,
                        set_clause, where_clause
                    )
                    st.code(sql, language="sql")
                    st.success(f"Updated {affected} row(s)")
                    st.rerun()
                except Exception as e:
                    st.error(f"Update failed: {e}")