# -*- coding: utf-8 -*-
"""
多释义扩展工具 v3 - 扩展至 200+ 词
日期：2026-04-02
说明：只处理数据库中实际存在且需要多释义的单词
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

def update_meaning(conn, word, meanings, pos):
    cursor = conn.cursor()
    max_retries = 3
    for retry in range(max_retries):
        try:
            meaning_json = json.dumps(meanings, ensure_ascii=False)
            main_meaning = meanings[0] if meanings else ""

            cursor.execute("""
                UPDATE tb_word
                SET meaning_trans = ?, meaning_cn = ?
                WHERE word = ?
            """, (meaning_json, main_meaning, word))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if retry < max_retries - 1:
                time.sleep(0.5)
            else:
                print(f"  [ERROR] {e}")
                return False
    return False

def main():
    print("=" * 60)
    print("     多释义扩展工具 v3 - 扩展至 200+ 词")
    print("=" * 60)

    conn = get_db_connection()
    print("[OK] 数据库连接成功\n")

    # 当前统计
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM tb_word
        WHERE meaning_trans IS NOT NULL
          AND LEN(meaning_trans) > 2
    """)
    current_count = cursor.fetchone()[0]
    print(f"当前多释义单词数：{current_count}")
    print(f"目标：200+ 词\n")

    total = len(MEANINGS)
    updated = 0
    skipped = 0

    print(f"准备更新 {total} 个单词的多释义...\n")

    for i, (word, (meanings, pos)) in enumerate(MEANINGS.items()):
        # 检查单词是否存在以及是否已有多释义
        cursor.execute("SELECT id, meaning_trans FROM tb_word WHERE word = ?", word)
        result = cursor.fetchone()

        if not result:
            print(f"[NOT FOUND] {word}")
            continue

        # 已有多释义？跳过
        if result[1]:
            try:
                existing = json.loads(result[1])
                if len(existing) > 1:
                    print(f"[SKIP] {word} - 已有多释义")
                    skipped += 1
                    continue
            except:
                pass

        # 更新
        if update_meaning(conn, word, meanings, pos):
            print(f"[OK] {word}: {meanings}")
            updated += 1
        else:
            print(f"[FAIL] {word} - 更新失败")

        # 每 5 个后延迟
        if (i + 1) % 5 == 0:
            time.sleep(0.3)

    conn.close()

    new_total = current_count + updated
    print("\n" + "=" * 60)
    print("     更新完成!")
    print("=" * 60)
    print(f"  尝试更新：{total} 个")
    print(f"  成功：{updated} 个")
    print(f"  跳过：{skipped} 个")
    print(f"  当前多释义总数：{new}text")
    print(f"  当前多释义总数：{new_total} 个")
    print(f"  目标完成率：{new_total/200*100:.1f}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
