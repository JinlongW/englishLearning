# -*- coding: utf-8 -*-
"""
音标补充工具 v3 - 补充剩余 52 个单词
日期：2026-04-02
"""

import pyodbc
import time

DB_SERVER = "localhost"
DB_DATABASE = "EnglishLearning"

# 剩余 52 个缺失音标的单词
PHONETIC_DATA = {
    "English class": ("/'ɪŋglɪʃ klɑ:s/", "/'ɪŋglɪʃ klæs/"),
    "have a look": ("/hæv ə lʊk/", "/hæv ə lʊk/"),
    "have...class": ("/hæv klɑ:s/", "/hæv klæs/"),
    "having...class": ("/'hævɪŋ klɑ:s/", "/'hævɪŋ klæs/"),
    "head teacher": ("/hed 'ti:tʃə/", "/hed 'ti:tʃər/"),
    "help yourself": ("/help jɔ:'self/", "/help jɔ:r'self/"),
    "how about...": ("/haʊ ə'baʊt/", "/haʊ ə'baʊt/"),
    "just a minute": ("/dʒʌst ə 'mɪnɪt/", "/dʒʌst ə 'mɪnɪt/"),
    "keep to the right": ("/ki:p tu ðə raɪt/", "/ki:p tu ðə raɪt/"),
    "keep your desk clean": ("/ki:p jɔ: desk kli:n/", "/ki:p jɔ:r desk kli:n/"),
    "Labour Day": ("/'leɪbə deɪ/", "/'leɪbər deɪ/"),
    "laughed": ("/lɑ:ft/", "/læft/"),
    "listening to music": ("/'lɪsnɪŋ tu 'mju:zɪk/", "/'lɪsnɪŋ tu 'mju:zɪk/"),
    "look for": ("/lʊk fɔ:/", "/lʊk fɔ:r/"),
    "look up": ("/lʊk ʌp/", "/lʊk ʌp/"),
    "lots of": ("/lɒts ɒv/", "/lɑ:ts ɑ:v/"),
    "maths book": ("/mæθs bʊk/", "/mæθs bʊk/"),
    "Ms": ("/mɪz/", "/mɪz/"),
    "music class": ("/'mju:zɪk klɑ:s/", "/'mju:zɪk klæs/"),
    "music room": ("/'mju:zɪk ru:m/", "/'mju:zɪk ru:m/"),
    "New York": ("/nju: 'jɔ:k/", "/nu: 'jɔ:rk/"),
    "no problem": ("/nəʊ 'prɒbləm/", "/noʊ 'prɑ:bləm/"),
    "on foot": ("/ɒn fʊt/", "/ɑ:n fʊt/"),
    "p.m.": ("/'pi:'em/", "/'pi:'em/"),
    "Papa Westray": ("/'pɑ:pə 'westreɪ/", "/'pɑ:pər 'westreɪ/"),
    "pay attention to": ("/peɪ ə'tenʃn tu:/", "/peɪ ə'tenʃn tu:/"),
    "play sports": ("/pleɪ spɔ:ts/", "/pleɪ spɔ:rts/"),
    "play the pipa": ("/pleɪ ðə 'pi:pə/", "/pleɪ ðə 'pi:pə/"),
    "post card": ("/pəʊst kɑ:d/", "/poʊst kɑ:rd/"),
    "reading a book": ("/'ri:dɪŋ ə bʊk/", "/'ri:dɪŋ ə bʊk/"),
    "RSVP": ("/'ɑ:resvi:'pi:/", "/'ɑ:resvi:'pi:/"),
    "second floor": ("/'sekənd flɔ:/", "/'sekənd flɔ:r/"),
    "see a doctor": ("/si: ə 'dɒktə/", "/si: ə 'dɑ:ktər/"),
    "see a film": ("/si: ə fɪlm/", "/si: ə fɪlm/"),
    "sing English songs": ("/sɪŋ 'ɪŋglɪʃ sɒŋz/", "/sɪŋ 'ɪŋglɪʃ sɔ:ŋz/"),
    "so much": ("/səʊ mʌtʃ/", "/soʊ mʌtʃ/"),
    "speak English": ("/spi:k 'ɪŋglɪʃ/", "/spi:k 'ɪŋglɪʃ/"),
    "take a dancing class": ("/teɪk ə 'dɑ:nsɪŋ klɑ:s/", "/teɪk ə 'dænsɪŋ klæs/"),
    "take a deep breath": ("/teɪk ə di:p breθ/", "/teɪk ə di:p breθ/"),
    "take turns": ("/teɪk tɜ:nz/", "/teɪk tɜ:rnz/"),
    "talk quietly": ("/tɔ:k 'kwaɪətli/", "/tɔ:k 'kwaɪətli/"),
    "teacher's desk": ("/'ti:tʃəz desk/", "/'ti:tʃərz desk/"),
    "teacher's office": ("/'ti:tʃəz 'ɒfɪs/", "/'ti:tʃərz 'ɔ:fɪs/"),
    "the Great Wall": ("/ðə greɪt wɔ:l/", "/ðə greɪt wɔ:l/"),
    "traffic lights": ("/'træfɪk laɪts/", "/'træfɪk laɪts/"),
    "try on": ("/traɪ ɒn/", "/traɪ ɑ:n/"),
    "Turpan": ("/'tʊpɑ:n/", "/'tʊrpɑ:n/"),
    "twenty-third": ("/'twenti θɜ:d/", "/'twenti θɜ:rd/"),
    "UK": ("/'ju:'keɪ/", "/'ju:'keɪ/"),
    "USA": ("/'ju:'es'eɪ/", "/'ju:'es'eɪ/"),
    "wash my clothes": ("/wɒʃ maɪ kləʊðz/", "/wɑ:ʃ maɪ kloʊðz/"),
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
            WHERE word = ? AND (phonetic_uk IS NULL OR phonetic_uk = '' OR phonetic_us IS NULL OR phonetic_us = '')
        """, (uk, us, word))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        return False

def main():
    print("=" * 60)
    print("     音标补充工具 v3 - 最后补充")
    print("=" * 60)

    conn = get_db_connection()
    print("[OK] 数据库连接成功\n")

    total = len(PHONETIC_DATA)
    updated = 0
    skipped = 0
    not_found = 0

    for i, (word, (uk, us)) in enumerate(PHONETIC_DATA.items()):
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tb_word WHERE word = ?", word)
        result = cursor.fetchone()

        if not result:
            cursor.execute("SELECT id FROM tb_word WHERE LOWER(word) = LOWER(?)", word)
            if cursor.fetchone():
                print(f"[SKIP] {word} - 已有音标")
                skipped += 1
            else:
                print(f"[NOT FOUND] {word}")
                not_found += 1
            continue

        if update_phonetic(conn, word, uk, us):
            print(f"[OK] {word}")
            updated += 1
        else:
            print(f"[SKIP] {word} - 已有音标")
            skipped += 1

        if (i + 1) % 10 == 0:
            time.sleep(0.5)

    conn.close()

    print("\n" + "=" * 60)
    print("     更新完成!")
    print("=" * 60)
    print(f"  总计：{total} 个")
    print(f"  成功：{updated} 个")
    print(f"  跳过：{skipped} 个")
    print(f"  未找到：{not_found} 个")
    print("=" * 60)

if __name__ == "__main__":
    main()
