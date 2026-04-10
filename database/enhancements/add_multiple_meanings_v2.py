# -*- coding: utf-8 -*-
"""
多释义扩展工具 v2 - 扩展至 200+ 词
日期：2026-04-02
"""

import pyodbc
import json
import time

DB_SERVER = "localhost"
DB_DATABASE = "EnglishLearning"

# 额外多释义数据 - 100+ 新词
# 格式：单词：(["释义 1", "释义 2", "释义 3"], "词性")
# 只包含数据库中实际存在的单词
EXTRA_MEANINGS = {
    # 基础动词 (补充)
    "play": (["玩", "打 (球)", "演奏", "扮演"], "v."),
    "help": (["帮助", "有助于", "招待"], "v./n."),
    "like": (["喜欢", "像", "如同"], "v./prep."),
    "want": (["想要", "需要"], "v."),
    "take": (["拿", "取", "花费", "乘坐"], "v."),
    "bring": (["带来", "拿来", "引起"], "v."),
    "show": (["展示", "显示", "引导"], "v."),
    "turn": (["转", "变成", "轮到"], "v./n."),
    "start": (["开始", "出发", "启动"], "v."),
    "stop": (["停止", "阻止", "车站"], "v./n."),
    "keep": (["保持", "保存", "继续"], "v."),
    "find": (["找到", "发现", "觉得"], "v."),
    "tell": (["告诉", "讲述", "吩咐"], "v."),
    "ask": (["问", "请求", "邀请"], "v."),
    "need": (["需要", "必要"], "v."),

    # 名词 (补充)
    "time": (["时间", "时候", "次", "倍"], "n."),
    "day": (["天", "日子", "白天"], "n."),
    "way": (["方法", "道路", "方式"], "n."),
    "thing": (["事情", "东西", "事物"], "n."),
    "people": (["人", "人们", "人民"], "n."),
    "child": (["孩子", "儿童", "小孩"], "n."),
    "world": (["世界", "领域", "界"], "n."),
    "hand": (["手", "帮助", "指针"], "n."),
    "eye": (["眼睛", "视力", "眼光"], "n."),
    "head": (["头", "首领", "前端"], "n."),
    "room": (["房间", "空间", "室"], "n."),
    "door": (["门", "门口", "入口"], "n."),
    "house": (["房子", "住宅", "家"], "n."),
    "friend": (["朋友", "友人", "支持者"], "n."),
    "week": (["周", "星期", "一周"], "n."),
    "work": (["工作", "作品", "工厂"], "n."),
    "school": (["学校", "学业", "学派"], "n."),

    # 形容词 (补充)
    "new": (["新的", "新鲜的", "陌生的"], "adj."),
    "old": (["老的", "旧的", "年老的"], "adj."),
    "good": (["好的", "良好的", "有益的"], "adj."),
    "great": (["伟大的", "重大的", "很好的"], "adj."),
    "high": (["高的", "高度的", "高级的"], "adj."),
    "small": (["小的", "少数的", "微不足道的"], "adj."),
    "big": (["大的", "巨大的", "重要的"], "adj."),
    "long": (["长的", "长久的", "长期的"], "adj."),
    "little": (["小的", "很少的", "一点儿"], "adj."),
    "own": (["自己的", "拥有的", "特有的"], "adj."),
    "other": (["其他的", "另外的", "其余的"], "adj."),
    "different": (["不同的", "差异的", "各种的"], "adj."),
    "same": (["相同的", "同样的"], "adj."),
    "important": (["重要的", "重大的", "有地位的"], "adj."),
    "early": (["早的", "早期的", "及早的"], "adj."),
    "late": (["晚的", "迟的", "已故的"], "adj."),
    "near": (["近的", "亲近的", "接近的"], "adj."),
    "far": (["远的", "久远的", "疏远的"], "adj."),
    "whole": (["全部的", "完整的", "整个的"], "adj."),
    "clear": (["清楚的", "明确的", "清澈的"], "adj."),

    # 副词 (补充)
    "very": (["非常", "很", "极其"], "adv."),
    "well": (["好", "健康地", "充分地"], "adv."),
    "just": (["刚刚", "只是", "正好"], "adv."),
    "now": (["现在", "立刻", "目前"], "adv."),
    "here": (["这里", "此时", "这点上"], "adv."),
    "there": (["那里", "那边", "在那时"], "adv."),
    "then": (["然后", "那么", "当时"], "adv."),
    "more": (["更多", "再", "更"], "adv."),
    "only": (["只", "仅仅", "唯一的"], "adv."),
    "about": (["大约", "关于", "到处"], "adv./prep."),

    # 介词 (补充)
    "in": (["在...里面", "在...期间", "穿着"], "prep."),
    "on": (["在...上面", "关于", "在...时"], "prep."),
    "at": (["在", "向", "处于"], "prep."),
    "for": (["为了", "对于", "因为"], "prep."),
    "with": (["和", "用", "带有"], "prep."),
    "from": (["从", "来自", "由于"], "prep."),
    "by": (["通过", "被", "在...旁"], "prep."),
    "up": (["向上", "在上", "起来"], "prep./adv."),
    "down": (["向下", "在下", "下去"], "prep./adv."),
    "out": (["向外", "在外", "出来"], "prep./adv."),

    # 连词 (补充)
    "and": (["和", "与", "并且"], "conj."),
    "but": (["但是", "可是", "然而"], "conj."),
    "or": (["或者", "还是", "否则"], "conj."),
    "if": (["如果", "是否", "假如"], "conj."),
    "because": (["因为", "由于"], "conj."),
    "when": (["什么时候", "当...时", "何时"], "adv./conj."),

    # 其他常用词
    "life": (["生活", "生命", "人生"], "n."),
    "parent": (["父亲", "母亲", "家长"], "n."),
    "place": (["地方", "地点", "位置"], "n."),
    "look": (["看", "看起来", "注意"], "v."),
    "let": (["让", "允许"], "v."),
    "put": (["放", "安置", "表达"], "v."),
    "give": (["给", "给予", "授予"], "v."),
    "call": (["打电话", "呼叫", "称呼"], "v."),
    "where": (["在哪里", "到哪里", "何处"], "adv."),
    "what": (["什么", "多么", "多少"], "pron."),
    "how": (["怎样", "如何", "多么"], "adv."),
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
                return False
    return False

def main():
    print("=" * 60)
    print("     多释义扩展工具 v2 - 扩展至 200+ 词")
    print("=" * 60)

    conn = get_db_connection()
    print("[OK] 数据库连接成功\n")

    # 统计当前多释义数量
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM tb_word
        WHERE meaning_trans IS NOT NULL
          AND LEN(meaning_trans) > 2
    """)
    current_count = cursor.fetchone()[0]
    print(f"当前多释义单词数：{current_count}")
    print(f"目标：200+ 词\n")

    total = len(EXTRA_MEANINGS)
    updated = 0
    not_found = 0
    skipped = 0

    print(f"准备更新 {total} 个单词的多释义...\n")

    for i, (word, (meanings, pos)) in enumerate(EXTRA_MEANINGS.items()):
        # 检查单词是否存在
        cursor = conn.cursor()
        cursor.execute("SELECT id, meaning_trans FROM tb_word WHERE word = ?", word)
        result = cursor.fetchone()

        if not result:
            print(f"[NOT FOUND] {word}")
            not_found += 1
            continue

        # 检查是否已有多释义
        if result.meaning_trans:
            try:
                existing = json.loads(result.meaning_trans)
                if len(existing) > 1:
                    print(f"[SKIP] {word} - 已有多释义")
                    skipped += 1
                    continue
            except:
                pass

        # 更新多释义
        if update_meaning(conn, word, meanings, pos):
            print(f"[OK] {word}: {meanings}")
            updated += 1
        else:
            print(f"[ERROR] {word} - 更新失败")

        # 每 5 个请求后短暂延迟，避免连接过载
        if (i + 1) % 5 == 0:
            time.sleep(0.3)

    conn.close()

    new_total = current_count + updated
    print("\n" + "=" * 60)
    print("     更新完成!")
    print("=" * 60)
    print(f"  尝试更新：{total} 个")
    print(f"  成功：{updated} 个")
    print(f"  跳过 (已有多释义)：{skipped} 个")
    print(f"  未找到：{not_found} 个")
    print(f"  当前多释义总数：{new_total} 个")
    print(f"  目标完成率：{new_total/200*100:.1f}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
