# -*- coding: utf-8 -*-
"""
多释义扩展工具 - 最后补充至 200+ 词
日期：2026-04-02
"""

import pyodbc
import json
import time

DB_SERVER = "localhost"
DB_DATABASE = "EnglishLearning"

FINAL_ADDITIONS = {
    "blue": (["蓝色", "蓝色的"], "adj./n."),
    "green": (["绿色", "绿色的"], "adj./n."),
    "yellow": (["黄色", "黄色的"], "adj./n."),
    "black": (["黑色", "黑色的"], "adj./n."),
    "white": (["白色", "白色的"], "adj./n."),
    "red": (["红色", "红色的"], "adj./n."),
    "brown": (["棕色", "棕色的"], "adj./n."),
    "orange": (["橙色", "橙子", "橙色的"], "adj./n."),
    "pink": (["粉色", "粉色的"], "adj./n."),
    "purple": (["紫色", "紫色的"], "adj./n."),
}

def get_db_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

def update_one_word(word, meanings):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, meaning_trans FROM tb_word WHERE word = ?", word)
        result = cursor.fetchone()
        if not result:
            return False, "NOT FOUND"

        if result[1]:
            try:
                existing = json.loads(result[1])
                if len(existing) > 1:
                    return False, "SKIP"
            except Exception:
                pass

        meaning_json = json.dumps(meanings, ensure_ascii=False)
        main_meaning = meanings[0]
        cursor.execute("""
            UPDATE tb_word
            SET meaning_trans = ?, meaning_cn = ?
            WHERE word = ?
        """, (meaning_json, main_meaning, word))
        conn.commit()
        return True, "OK"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def main():
    print("=" * 60)
    print("     多释义扩展工具 - 最后补充至 200+ 词")
    print("=" * 60)

    # 统计当前
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT word, meaning_trans FROM tb_word WHERE meaning_trans IS NOT NULL")
    current = 0
    for word, meaning_trans in cursor.fetchall():
        try:
            arr = json.loads(meaning_trans)
            if len(arr) > 1:
                current += 1
        except:
            pass
    conn.close()

    print(f"当前多释义单词数：{current}")
    print(f"需要补充：{200 - current} 个\n")

    total = len(FINAL_ADDITIONS)
    updated = 0
    skipped = 0
    not_found = 0

    print(f"准备更新 {total} 个单词...\n")

    for word, (meanings, pos) in FINAL_ADDITIONS.items():
        success, msg = update_one_word(word, meanings)
        if success:
            print(f"[OK] {word}: {meanings}")
            updated += 1
        else:
            if msg == "NOT FOUND":
                print(f"[NOT FOUND] {word}")
                not_found += 1
            elif msg == "SKIP":
                print(f"[SKIP] {word} - 已有多释义")
                skipped += 1
            else:
                print(f"[FAIL] {word} - {msg}")

        time.sleep(0.5)

    # 最终统计
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT word, meaning_trans FROM tb_word WHERE meaning_trans IS NOT NULL")
    final = 0
    for word, meaning_trans in cursor.fetchall():
        try:
            arr = json.loads(meaning_trans)
            if len(arr) > 1:
                final += 1
        except:
            pass
    conn.close()

    print("\n" + "=" * 60)
    print("     更新完成!")
    print("=" * 60)
    print(f"  尝试更新：{total} 个")
    print(f"  成功：{updated} 个")
    print(f"  跳过：{skipped} 个")
    print(f"  未找到：{not_found} 个")
    print(f"  当前多释义总数：{final} 个")
    print(f"  目标：200+ → {'完成' if final >= 200 else '需要继续'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
