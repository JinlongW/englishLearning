# -*- coding: utf-8 -*-
"""
音标补充工具 v4 - 最后补充剩余 12 个短语
日期：2026-04-02
"""

import pyodbc

DB_SERVER = "localhost"
DB_DATABASE = "EnglishLearning"

# 剩余缺失音标的短语
PHONETIC_DATA = {
    "play sports": ("/pleɪ spɔ:ts/", "/pleɪ spɔ:rts/"),
    "on foot": ("/ɒn fʊt/", "/ɑ:n fʊt/"),
    "English class": ("/'ɪŋglɪʃ klɑ:s/", "/'ɪŋglɪʃ klæs/"),
    "music class": ("/'mju:zɪk klɑ:s/", "/'mju:zɪk klæs/"),
    "see a film": ("/si: ə fɪlm/", "/si: ə fɪlm/"),
    "have an English class": ("/hæv ən 'ɪŋglɪʃ klɑ:s/", "/hæv ən 'ɪŋglɪʃ klæs/"),
    "have art class": ("/hæv ɑ:t klɑ:s/", "/hæv ɑ:rt klæs/"),
    "have music class": ("/hæv 'mju:zɪk klɑ:s/", "/hæv 'mju:zɪk klæs/"),
    "have PE class": ("/hæv 'pi: 'klɑ:s/", "/hæv 'pi: 'klæs/"),
    "have science class": ("/hæv 'saɪəns klɑ:s/", "/hæv 'saɪəns klæs/"),
    "go swimming.": ("/gəʊ 'swɪmɪŋ/", "/goʊ 'swɪmɪŋ/"),
    "doing morning exercises": ("/'du:ɪŋ 'mɔ:nɪŋ 'eksəsaɪzɪz/", "/'du:ɪŋ 'mɔ:rnɪŋ 'eksərsaɪzɪz/"),
}

def get_db_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

def update_phonetic(conn, word, uk, us):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE tb_word
            SET phonetic_uk = ?, phonetic_us = ?
            WHERE word = ?
        """, (uk, us, word))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

def main():
    print("=" * 60)
    print("     音标补充工具 v4 - 最后补充")
    print("=" * 60)

    conn = get_db_connection()
    print("[OK] 数据库连接成功\n")

    total = len(PHONETIC_DATA)
    updated = 0
    not_found = 0

    print(f"准备更新 {total} 个短语的音标...\n")

    for word, (uk, us) in PHONETIC_DATA.items():
        if update_phonetic(conn, word, uk, us):
            print(f"[OK] {word}")
            updated += 1
        else:
            print(f"[NOT FOUND] {word}")
            not_found += 1

    conn.close()

    print("\n" + "=" * 60)
    print("     更新完成!")
    print("=" * 60)
    print(f"  总计：{total} 个")
    print(f"  成功：{updated} 个")
    print(f"  未找到：{not_found} 个")
    print("=" * 60)

if __name__ == "__main__":
    main()
