import streamlit as st
from sql_agent import generate_sql, run_sql, explain_sql
from utils.validator import validate_sql

st.set_page_config(page_title="Text-to-SQL AI", layout="wide")

st.title(" AI Text-to-SQL Generator ")

question = st.text_area("Ask anything about your database:")

if st.button("Generate SQL") and question:

    sql = generate_sql(question)

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    # validation
    ok, msg = validate_sql(sql)

    if not ok:
        st.error(msg)
        st.stop()

    st.success(msg)

    # run query
    st.subheader("Results")

    result = run_sql(sql)
    st.dataframe(result)

    # explanation
    st.subheader("Explanation")
    st.write(explain_sql(sql))


# ---------------- EXAMPLES ----------------
st.sidebar.title("💡 Try Examples")

examples = [
    "show all employees",
    "highest salary employee",
    "average salary",
    "employees in IT department",
    "count employees by department",
    "employees joined after 2022"
]

for ex in examples:
    if st.sidebar.button(ex):
        st.session_state["question"] = ex