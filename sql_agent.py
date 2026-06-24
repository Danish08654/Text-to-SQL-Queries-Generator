import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from langchain_groq import ChatGroq

load_dotenv()

DB_PATH = "database/sample.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

# ---------------- LLM (FREE GROQ) ----------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# ---------------- SCHEMA ----------------
def get_schema():
    inspector = inspect(engine)
    schema = {}

    for table in inspector.get_table_names():
        cols = inspector.get_columns(table)
        schema[table] = [c["name"] for c in cols]

    return schema


# ---------------- PROMPT ----------------
def load_prompt():
    with open("prompts/sql_prompt.txt", "r") as f:
        return f.read()


# ---------------- SQL GENERATION ----------------
def generate_sql(question: str):
    schema = get_schema()

    prompt = load_prompt().format(
        schema=schema,
        question=question
    )

    response = llm.invoke(prompt)

    sql = response.content.strip()

    # cleanup
    sql = sql.replace("```sql", "").replace("```", "")

    return sql


# ---------------- EXECUTE SQL ----------------
def run_sql(query: str):
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})


# ---------------- EXPLAIN SQL ----------------
def explain_sql(query: str):
    prompt = f"""
Explain this SQL in simple words:

{query}
"""
    return llm.invoke(prompt).content