"""
删除同一单元内的重复题目
保留第一个ID，删除后续重复的
"""

import pyodbc

def get_db_connection():
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER=localhost;'
        f'DATABASE=EnglishLearning;'
        f'Trusted_Connection=yes;'
    )
    return pyodbc.connect(conn_str)

def get_duplicates_to_remove(conn):
    """找出需要删除的重复题目ID"""
    cursor = conn.cursor()
    # 找出每个(grade_unit_id, question_stem)分组中除了第一个之外的所有ID
    # SQL Server 需要用窗口函数
    cursor.execute("""
        WITH Ranked AS (
            SELECT
                id,
                grade_unit_id,
                question_stem,
                ROW_NUMBER() OVER (
                    PARTITION BY grade_unit_id, question_stem
                    ORDER BY id
                ) as rn
            FROM tb_question
        )
        SELECT id FROM Ranked WHERE rn > 1
    """)
    ids = [row[0] for row in cursor.fetchall()]
    return ids

def main():
    conn = get_db_connection()

    print("Finding duplicate questions...")
    duplicate_ids = get_duplicates_to_remove(conn)
    print(f"Found {len(duplicate_ids)} duplicate questions to remove.")

    if not duplicate_ids:
        print("No duplicates found. Done.")
        conn.close()
        return

    print("\nRemoving...")
    cursor = conn.cursor()
    removed = 0
    # 逐个删除
    for qid in duplicate_ids:
        try:
            cursor.execute("DELETE FROM tb_question WHERE id = ?", qid)
            conn.commit()
            removed += 1
            if removed % 10 == 0:
                print(f"  Removed {removed}/{len(duplicate_ids)}")
        except Exception as e:
            print(f"  [ERROR] Failed to delete {qid}: {e}")

    print(f"\nDone. Removed {removed} duplicate questions.")

    # 显示最终统计
    cursor.execute("SELECT question_type, COUNT(*) FROM tb_question GROUP BY question_type")
    print("\nFinal statistics:")
    total = 0
    for qtype, cnt in cursor.fetchall():
        print(f"  {qtype}: {cnt}")
        total += cnt
    print(f"\nTotal questions: {total}")

    conn.close()

if __name__ == "__main__":
    main()
