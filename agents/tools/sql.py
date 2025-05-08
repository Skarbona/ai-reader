import sqlite3
from langchain.tools import Tool
from typing import List
from pydantic.v1 import BaseModel

conn = sqlite3.connect('db.sqlite')

def list_tables():
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)

def run_sqlite_query(query):
    c = conn.cursor()
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"Error: {err}"
    finally:
        c.close()

class RunQueryArgsSchema(BaseModel):
    query: str        

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a SQL query on the SQLite database.",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema,
)

def describe_tables(tables_names):
    c = conn.cursor()
    tables = ', '.join("'" + table + "'" for table in tables_names)
    rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({tables});")
    return "\n".join(row[0] for row in rows if row[0] is not None)

class DescribeTablesArgsSchema(BaseModel):
    tables_names: List[str]

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Describe the structure of the tables in the SQLite database.",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema,
)