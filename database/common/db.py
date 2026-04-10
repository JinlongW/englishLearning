"""
Database connection utility
Shared database connection configuration and helper functions
"""

import os
import pyodbc
from typing import Optional


def get_db_connection() -> pyodbc.Connection:
    """
    Get database connection using environment variables or default values.
    Uses Windows Integrated Authentication by default.
    """
    server = os.getenv("DB_SERVER", "localhost")
    database = os.getenv("DB_DATABASE", "EnglishLearning")
    username = os.getenv("DB_USERNAME", "")
    password = os.getenv("DB_PASSWORD", "")

    if username and password:
        # SQL Server authentication
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password};'
        )
    else:
        # Windows Integrated Authentication
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'Trusted_Connection=yes;'
        )

    return pyodbc.connect(conn_str)


def get_grade_unit_id(
    conn: pyodbc.Connection,
    grade: int,
    semester: str,
    unit_no: int
) -> Optional[str]:
    """
    Get grade_unit_id by grade, semester and unit number.
    Returns None if not found.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM tb_grade_unit
        WHERE grade = ? AND semester = ? AND unit_no = ?
    """, (grade, semester, unit_no))
    row = cursor.fetchone()
    if row:
        return row[0]
    return None
