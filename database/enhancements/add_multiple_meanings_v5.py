# -*- coding: utf-8 -*-
"""
多释义扩展工具 v5 - 补充至 200+ 词
日期：2026-04-02
"""

import pyodbc
import json
import time

DB_SERVER = "localhost"
DB_DATABASE = "EnglishLearning"

# 继续补充 40 个单词
MORE_MEANINGS = {
    "over": (["在...上方", "超过", "结束"], "prep."),
    "under": (["在...下面", "低于", "少于"], "prep."),
    "after": (["在...之后", "跟随", "后来"], "prep."),
    "before": (["在...之前", "先前", "早于"], "prep."),
    "behind": (["在...后面", "落后", "支持"], "prep."),
    "front": (["前面", "前部", "前线"], "n./adj."),
    "back": (["后面", "背部", "回来"], "n./adv."),
    "left": (["左边", "左边的", "剩下"], "adj./n."),
    "right": (["右边", "正确的", "权利"], "adj./n."),
    "middle": (["中间", "中部", "中等"], "n./adj."),
    "center": (["中心", "中央", "核心"], "n."),
    "side": (["边", "侧面", "方面"], "n."),
    "top": (["顶部", "顶端", "最高的"], "n./adj."),
    "bottom": (["底部", "底端", "最后"], "n."),
    "open": (["打开", "开放的", "公开的"], "v./adj."),
    "close": (["关闭", "靠近", "结束"], "v./adv."),
    "fast": (["快的", "快速地", "牢固的"], "adj./adv."),
    "slow": (["慢的", "放慢"], "adj./v."),
    "hard": (["硬的", "困难的", "努力地"], "adj./adv."),
    "soft": (["软的", "柔软的", "温和的"], "adj."),
    "easy": (["容易的", "轻松的", "舒适的"], "adj."),
    "hard": (["硬的", "困难的", "努力地"], "adj./adv."),
    "cheap": (["便宜的", "廉价的"], "adj."),
    "expensive": (["贵的", "昂贵的"], "adj."),
    "dirty": (["脏的", "弄脏"], "adj."),
    "clean": (["干净的", "打扫"], "adj./v."),
    "dry": (["干的", "使干燥"], "adj./v."),
    "wet": (["湿的", "弄湿"], "adj./v."),
    "cold": (["冷的", "寒冷", "感冒"], "adj./n."),
    "hot": (["热的", "烫的", "辣的"], "adj."),
    "warm": (["温暖的", "暖和", "热情"], "adj."),
    "cool": (["凉爽的", "酷的", "冷静"], "adj."),
    "bad": (["坏的", "不好的", "严重的"], "adj."),
    "happy": (["开心的", "快乐的", "幸福的"], "adj."),
    "sad": (["伤心的", "悲伤的"], "adj."),
    "angry": (["生气的", "愤怒的"], "adj."),
    "tired": (["累的", "疲劳的"], "adj."),
    "busy": (["忙的", "繁忙的"], "adj."),
    "free": (["免费的", "自由的", "空闲"], "adj."),
    "full": (["满的", "充满的", "吃饱"], "adj."),
    "empty": (["空的", "空洞的", "清空"], "adj./v."),
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
            except:
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
    print("     多释义扩展工具 v5 - 补充至 200+ 词")
    print("=" * 60)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM tb_word
        WHERE meaning_trans IS NOT NULL
    ''')
    current_has = cursor.fetchone()[0]
    conn.close()

    # 统计当前多释义
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT word, meaning_trans FROM tb_word WHERE meaning_trans IS NOT NULL")
    multi_count = 0
    for word, meaning_trans in cursor.fetchall():
        try:
            arr = json.loads(meaning_trans)
            if len(arr) > 1:
                multi_count += 1
        except:
            pass
    conn.close()

    print(f"当前多释义单词数：{multi_count}")
    print(f"需要补充：{200 - multi_count} 个\n")

    total = len(MORE_MEANINGS)
    updated = 0
    skipped = 0
    not_found = 0

    print(f"准备更新 {total} 个单词...\n")

    for i, (word, (meanings, pos)) in enumerate(MORE_MEANINGS.items()):
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

        time.sleep(0.6)

    # 最终统计
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT word, meaning_trans FROM tb_word WHERE meaning_trans is not null")
    final_multi = 0
    for word, meaning_trans in cursor.fetchall():
        try:
            arr = json.loads(meaning_trans)
            if len(arr) > 1:
                final_multi += 1
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
    print(f"  当前多释义总数：{final_multi} 个")
    print(f"  目标：200+ → {'完成' if final_multi >= 200 else '需要继续'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
