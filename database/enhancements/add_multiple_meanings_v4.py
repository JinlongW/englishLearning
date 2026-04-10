# -*- coding: utf-8 -*-
"""
多释义扩展工具 v4 - 扩展至 200+ 词
日期：2026-04-02
说明：每个单词单独连接，避免连接过载
"""

import pyodbc
import json
import time

DB_SERVER = "localhost"
DB_DATABASE = "EnglishLearning"

# 只有数据库中实际存在且需要多释义的单词
# 格式：单词：(["释义 1", "释义 2", "释义 3", ...], "词性")
MEANINGS = {
    "big": (["大的", "巨大的", "重要的"], "adj."),
    "by": (["通过", "被", "在...旁"], "prep."),
    "child": (["孩子", "儿童", "小孩"], "n."),
    "down": (["向下", "在下", "下去"], "prep./adv."),
    "eye": (["眼睛", "视力", "眼光"], "n."),
    "friend": (["朋友", "友人", "支持者"], "n."),
    "hand": (["手", "帮助", "指针"], "n."),
    "head": (["头", "首领", "前端"], "n."),
    "house": (["房子", "住宅", "家"], "n."),
    "like": (["喜欢", "像", "如同"], "v./prep."),
    "long": (["长的", "长久的", "长期的"], "adj."),
    "more": (["更多", "再", "更"], "adv."),
    "new": (["新的", "新鲜的", "陌生的"], "adj."),
    "old": (["老的", "旧的", "年老的"], "adj."),
    "play": (["玩", "打 (球)", "演奏", "扮演"], "v."),
    "show": (["展示", "显示", "引导"], "v."),
    "small": (["小的", "少数的", "微不足道的"], "adj."),
    "start": (["开始", "出发", "启动"], "v."),
    "stop": (["停止", "阻止", "车站"], "v./n."),
    "take": (["拿", "取", "花费", "乘坐"], "v."),
    "turn": (["转", "变成", "轮到"], "v./n."),
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
    """更新一个单词的多释义"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # 检查是否存在
        cursor.execute("SELECT id, meaning_trans FROM tb_word WHERE word = ?", word)
        result = cursor.fetchone()
        if not result:
            return False, "NOT FOUND"

        # 已有多释义？
        if result[1]:
            try:
                existing = json.loads(result[1])
                if len(existing) > 1:
                    return False, "SKIP"
            except:
                pass

        # 更新
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
    print("     多释义扩展工具 v4 - 扩展至 200+ 词")
    print("=" * 60)

    # 当前统计
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM tb_word
        WHERE meaning_trans IS NOT NULL
          AND LEN(meaning_trans) > 2
    """)
    current_count = cursor.fetchone()[0]
    conn.close()

    print(f"当前多释义单词数：{current_count}")
    print(f"目标：200+ 词\n")

    total = len(MEANINGS)
    updated = 0
    skipped = 0
    not_found = 0
    failed = 0

    print(f"准备更新 {total} 个单词...\n")

    for i, (word, (meanings, pos)) in enumerate(MEANINGS.items()):
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
                failed += 1

        # 延迟避免过载
        time.sleep(0.8)

    # 最终统计
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM tb_word
        WHERE meaning_trans IS NOT NULL
          AND LEN(meaning_trans) > 2
    """)
    new_total = cursor.fetchone()[0]
    conn.close()

    print("\n" + "=" * 60)
    print("     更新完成!")
    print("=" * 60)
    print(f"  尝试更新：{total} 个")
    print(f"  成功：{updated} 个")
    print(f"  跳过：{skipped} 个")
    print(f"  未找到：{not_found} 个")
    print(f"  失败：{failed} 个")
    print(f"  当前多释义总数：{new_total} 个")
    print(f"  目标完成率：{new_total/200*100:.1f}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
