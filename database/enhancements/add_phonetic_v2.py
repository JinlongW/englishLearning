# -*- coding: utf-8 -*-
"""
音标补充工具 v2
日期：2026-04-02
说明：根据数据库实际缺失音标的单词进行补充
"""

import pyodbc
import time

# ==================== 配置区域 ====================
DB_SERVER = "localhost"
DB_DATABASE = "EnglishLearning"

# ==================== 音标数据 ====================
# 根据数据库实际缺失的单词整理
PHONETIC_DATA = {
    # 学校和教室相关
    "art room": ("/'ɑ:t ru:m/", "/'ɑ:rt ru:m/"),
    "computer room": ("/kəm'pju:tə ru:m/", "/kəm'pju:tər ru:m/"),
    "dining hall": ("/'daɪnɪŋ hɔ:l/", "/'daɪnɪŋ hɔ:l/"),
    "first floor": ("/fɜ:st flɔ:/", "/fɜ:rst flɔ:r/"),
    "Chinese book": ("/'tʃaɪ'ni:z bʊk/", "/'tʃaɪ'ni:z bʊk/"),
    "English book": ("/'ɪŋglɪʃ bʊk/", "/'ɪŋglɪʃ bʊk/"),
    "comic book": ("/'kɒmɪk bʊk/", "/'kɑ:mɪk bʊk/"),

    # 时间相关
    "a.m.": ("/'eɪ'em/", "/'eɪ'em/"),
    "a few": ("/ə fju:/", "/ə fju:/"),

    # 家庭成员
    "baby brother": ("/'beɪbi 'brʌðə/", "/'beɪbi 'brʌðər/"),

    # 日常活动
    "clean my room": ("/kli:n maɪ ru:m/", "/kli:n maɪ ru:m/"),
    "count to ten": ("/kaʊnt tu ten/", "/kaʊnt tu ten/"),
    "do morning exercise": ("/du: 'mɔ:nɪŋ 'eksəsaɪz/", "/du: 'mɔ:rnɪŋ 'eksərsaɪz/"),
    "doing morning exercises": ("/'du:ɪŋ 'mɔ:nɪŋ 'eksəsaɪzɪz/", "/'du:ɪŋ 'mɔ:rnɪŋ 'eksərsaɪzɪz/"),
    "draw cartoons": ("/drɑ: kɑ:'tu:nz/", "/drɔ: kɑ:r'tu:nz/"),
    "eat dinner": ("/i:t 'dɪnə/", "/i:t 'dɪnər/"),
    "eating lunch": ("/'i:tɪŋ lʌntʃ/", "/'i:tɪŋ lʌntʃ/"),

    # 体育活动
    "football player": ("/'fʊtbɔ:l pleɪə/", "/'fʊtbɔ:l pleɪər/"),
    "go boating": ("/gəʊ 'bəʊtɪŋ/", "/goʊ 'boʊtɪŋ/"),
    "go cycling": ("/gəʊ 'saɪklɪŋ/", "/goʊ 'saɪklɪŋ/"),
    "go for a walk": ("/gəʊ fɔ:r ə wɔ:k/", "/goʊ fɔ:r ə wɔ:k/"),
    "go on a picnic": ("/gəʊ ɒn ə 'pɪknɪk/", "/goʊ ɑ:n ə 'pɪknɪk/"),
    "go swimming.": ("/gəʊ 'swɪmɪŋ/", "/goʊ 'swɪmɪŋ/"),

    # 其他
    "each other": ("/i:tʃ 'ʌðə/", "/i:tʃ 'ʌðər/"),
    "get together": ("/get tə'geðə/", "/get tə'geðər/"),
    "good job": ("/gʊd dʒɒb/", "/gʊd dʒɑ:b/"),
    "GPS": ("/'dʒi:pi:'es/", "/'dʒi:pi:'es/"),
    "green beans": ("/gri:n bi:nz/", "/gri:n bi:nz/"),
    "had a cold": ("/hæd ə kəʊld/", "/hæd ə koʊld/"),
    "have a cold": ("/hæv ə kəʊld/", "/hæv ə koʊld/"),
    "have an English class": ("/hæv ən 'ɪŋglɪʃ klɑ:s/", "/hæv ən 'ɪŋglɪʃ klæs/"),
    "have art class": ("/hæv ɑ:t klɑ:s/", "/hæv ɑ:rt klæs/"),
    "have music class": ("/hæv 'mju:zɪk klɑ:s/", "/hæv 'mju:zɪk klæs/"),
    "have PE class": ("/hæv 'pi: 'klɑ:s/", "/hæv 'pi: 'klæs/"),
    "have science class": ("/hæv 'saɪəns klɑ:s/", "/hæv 'saɪəns klæs/"),
    "jump high": ("/dʒʌmp haɪ/", "/dʒʌmp haɪ/"),
    "jump far": ("/dʒʌmp fɑ:/", "/dʒʌmp fɑ:r/"),
    "run fast": ("/rʌn fɑ:st/", "/rʌn fæst/"),
    "sing songs": ("/sɪŋ sɒŋz/", "/sɪŋ sɔ:ŋz/"),
    "play football": ("/pleɪ 'fʊtbɔ:l/", "/pleɪ 'fʊtbɔ:l/"),
    "play basketball": ("/pleɪ 'bɑ:skɪtbɔ:l/", "/pleɪ 'bæskɪtbɔ:l/"),
    "play ping-pong": ("/pleɪ 'pɪŋpɒŋ/", "/pleɪ 'pɪŋpɔ:ŋ/"),
    "play badminton": ("/pleɪ 'bædmɪntən/", "/pleɪ 'bædmɪntən/"),
    "sports meet": ("/spɔ:ts mi:t/", "/spɔ:rts mi:t/"),
    "school sports meet": ("/sku:l spɔ:ts mi:t/", "/sku:l spɔ:rts mi:t/"),
    "this year": ("/ðɪs jɪə/", "/ðɪs jɪr/"),
    "love to": ("/lʌv tu:/", "/lʌv tu:/"),
    "winter vacation": ("/'wɪntə və'keɪʃn/", "/'wɪntər və'keɪʃn/"),
    "summer vacation": ("/'sʌmə və'keɪʃn/", "/'sʌmər və'keɪʃn/"),
    "winter holiday": ("/'wɪntə 'hɒlədeɪ/", "/'wɪntər 'hɑ:lədeɪ/"),
    "summer holiday": ("/'sʌmə 'hɒlədeɪ/", "/'sʌmər 'hɑ:lədeɪ/"),

    # 月份和季节
    "in January": ("/ɪn 'dʒænjuəri/", "/ɪn 'dʒænjueri/"),
    "in February": ("/ɪn 'februəri/", "/ɪn 'februeri/"),
    "in March": ("/ɪn mɑ:tʃ/", "/ɪn mɑ:rtʃ/"),
    "in April": ("/ɪn 'eɪprəl/", "/ɪn 'eɪprəl/"),
    "in May": ("/ɪn meɪ/", "/ɪn meɪ/"),
    "in June": ("/ɪn dʒu:n/", "/ɪn dʒu:n/"),
    "in July": ("/ɪn dʒu'laɪ/", "/ɪn dʒu'laɪ/"),
    "in August": ("/ɪn 'ɔ:gəst/", "/ɪn 'ɔ:gəst/"),
    "in September": ("/ɪn sep'tembə/", "/ɪn sep'tembər/"),
    "in October": ("/ɪn ɒk'təʊbə/", "/ɪn ɑ:k'toʊbər/"),
    "in November": ("/ɪn nəʊ'vembə/", "/ɪn noʊ'vembər/"),
    "in December": ("/ɪn dɪ'sembə/", "/ɪn dɪ'sembər/"),

    # 节日
    "Tree Planting Day": ("/tri: 'plɑ:ntɪŋ deɪ/", "/tri: 'plæntɪŋ deɪ/"),
    "Mother's Day": ("/'mʌðəz deɪ/", "/'mʌðərz deɪ/"),
    "Father's Day": ("/'fɑ:ðəz deɪ/", "/'fɑ:ðərz deɪ/"),
    "Halloween": ("/'hæləʊ'i:n/", "/'hæloʊ'i:n/"),
    "Thanksgiving": ("/'θæŋks'gɪvɪŋ/", "/'θæŋks'gɪvɪŋ/"),
    "Christmas": ("/'krɪsməs/", "/'krɪsməs/"),
    "Easter": ("/'i:stə/", "/'i:stər/"),

    # 序数词
    "first": ("/fɜ:st/", "/fɜ:rst/"),
    "second": ("/'sekənd/", "/'sekənd/"),
    "third": ("/θɜ:d/", "/θɜ:rd/"),
    "fourth": ("/fɔ:θ/", "/fɔ:rθ/"),
    "fifth": ("/fɪfθ/", "/fɪfθ/"),
    "sixth": ("/sɪksθ/", "/sɪksθ/"),
    "seventh": ("/'sevnθ/", "/'sevnθ/"),
    "eighth": ("/eɪtθ/", "/eɪtθ/"),
    "ninth": ("/naɪnθ/", "/naɪnθ/"),
    "tenth": ("/tenθ/", "/tenθ/"),
    "eleventh": ("/ɪ'levnθ/", "/ɪ'levnθ/"),
    "twelfth": ("/twelfθ/", "/twelfθ/"),

    # 形容词
    "thinner": ("/'θɪnə/", "/'θɪnər/"),
    "heavier": ("/'hevɪə/", "/'heviər/"),
    "stronger": ("/'strɒŋə/", "/'strɔ:ŋər/"),
    "bigger": ("/'bɪgə/", "/'bɪgər/"),
    "smaller": ("/'smɔ:lə/", "/'smɔ:lər/"),
    "younger": ("/'jʌŋə/", "/'jʌŋər/"),
    "older": ("/'əʊldə/", "/'oʊldər/"),
    "taller": ("/'tɔ:lə/", "/'tɔ:lər/"),
    "shorter": ("/'ʃɔ:tə/", "/'ʃɔ:rtər/"),
    "longer": ("/'lɒŋə/", "/'lɔ:ŋər/"),
    "lower": ("/'ləʊə/", "/'loʊər/"),
    "higher": ("/'haɪə/", "/'haɪər/"),
    "smarter": ("/'smɑ:tə/", "/'smɑ:rtər/"),
    "better": ("/'betə/", "/'betər/"),
    "faster": ("/'fɑ:stə/", "/'fæstər/"),
    "earlier": ("/'ɜ:liə/", "/'ɜ:rliər/"),
    "easier": ("/'i:ziə/", "/'i:ziər/"),
    "hotter": ("/'hɒtə/", "/'hɑ:tər/"),
    "colder": ("/'kəʊldə/", "/'koʊldər/"),
    "wetter": ("/'wetə/", "/'wetər/"),
    "drier": ("/'draɪə/", "/'draɪər/"),

    # 过去式
    "was": ("/wɒz/", "/wɑ:z/"),
    "were": ("/wɜ:/", "/wɜ:r/"),
    "went": ("/went/", "/went/"),
    "ate": ("/eɪt/", "/eɪt/"),
    "took": ("/tʊk/", "/tʊk/"),
    "had": ("/hæd/", "/hæd/"),
    "read": ("/red/", "/red/"),
    "saw": ("/sɔ:/", "/sɔ:/"),
    "did": ("/dɪd/", "/dɪd/"),
    "bought": ("/bɔ:t/", "/bɔ:t/"),
    "fell": ("/fel/", "/fel/"),
    "hurt": ("/hɜ:t/", "/hɜ:rt/"),
    "rode": ("/rəʊd/", "/roʊd/"),
    "came": ("/keɪm/", "/keɪm/"),

    # 过去式短语
    "fell off": ("/fel ɒf/", "/fel ɑ:f/"),
    "fell down": ("/fel daʊn/", "/fel daʊn/"),
    "hurt my knee": ("/hɜ:t maɪ ni:/", "/hɜ:rt maɪ ni:/"),
    "hurt his leg": ("/hɜ:t hɪz leg/", "/hɜ:rt hɪz leg/"),
    "took pictures": ("/tʊk 'pɪktʃəz/", "/tʊk 'pɪktʃərz/"),
    "ate fresh food": ("/eɪt freʃ fu:d/", "/eɪt freʃ fu:d/"),
    "went swimming": ("/went 'swɪmɪŋ/", "/went 'swɪmɪŋ/"),
    "went fishing": ("/went 'fɪʃɪŋ/", "/went 'fɪʃɪŋ/"),
    "went camping": ("/went 'kæmpɪŋ/", "/went 'kæmpɪŋ/"),
    "went cycling": ("/went 'saɪklɪŋ/", "/went 'saɪklɪŋ/"),
    "went ice-skating": ("/went 'aɪs skeɪtɪŋ/", "/went 'aɪs skeɪtɪŋ/"),
    "bought gifts": ("/bɔ:t gɪfts/", "/bɔ:t gɪfts/"),
    "rode a horse": ("/rəʊd ə hɔ:s/", "/roʊd ə hɔ:rs/"),
    "rode a bike": ("/rəʊd ə baɪk/", "/roʊd ə baɪk/"),
    "saw a film": ("/sɔ: ə fɪlm/", "/sɔ: ə fɪlm/"),
    "had a cold": ("/hæd ə kəʊld/", "/hæd ə koʊld/"),
    "slept": ("/slept/", "/slept/"),
    "stayed": ("/steɪd/", "/steɪd/"),
    "cleaned": ("/kli:nd/", "/kli:nd/"),
    "cooked": ("/kʊkt/", "/kʊkt/"),
    "washed": ("/wɒʃt/", "/wɑ:ʃt/"),
    "watched": ("/wɒtʃt/", "/wɑ:tʃt/"),
    "played": ("/pleɪd/", "/pleɪd/"),
    "visited": ("/'vɪzɪtɪd/", "/'vɪzɪtɪd/"),
    "listened": ("/'lɪsnd/", "/'lɪsnd/"),
    "studied": ("/'stʌdid/", "/'stʌdid/"),

    # 过去式短语 2
    "stayed at home": ("/steɪd æt həʊm/", "/steɪd æt hoʊm/"),
    "cleaned my room": ("/kli:nd maɪ ru:m/", "/kli:nd maɪ ru:m/"),
    "washed my clothes": ("/wɒʃt maɪ kləʊðz/", "/wɑ:ʃt maɪ kloʊðz/"),
    "watched TV": ("/wɒtʃt 'ti:'vi:/", "/wɑ:tʃt 'ti:'vi:/"),
    "played football": ("/pleɪd 'fʊtbɔ:l/", "/pleɪd 'fʊtbɔ:l/"),
    "visited my grandparents": ("/'vɪzɪtɪd maɪ 'grænpərents/", "/'vɪzɪtɪd maɪ 'grænpərents/"),
    "listened to music": ("/'lɪsnd tu 'mju:zɪk/", "/'lɪsnd tu 'mju:zɪk/"),
    "studied English": ("/'stʌdid 'ɪŋglɪʃ/", "/'stʌdid 'ɪŋglɪʃ/"),

    # 地点
    "beach": ("/bi:tʃ/", "/bi:tʃ/"),
    "lake": ("/leɪk/", "/leɪk/"),
    "island": ("/'aɪlənd/", "/'aɪlənd/"),
    "mountain": ("/'maʊntɪn/", "/'maʊntɪn/"),
    "river": ("/'rɪvə/", "/'rɪvər/"),
    "sea": ("/si:/", "/si:/"),
    "ocean": ("/'əʊʃn/", "/'oʊʃn/"),
    "desert": ("/'dezət/", "/'dezət/"),

    # 其他常用词
    "dream": ("/dri:m/", "/dri:m/"),
    "check": ("/tʃek/", "/tʃek/"),
    "invite": ("/ɪn'vaɪt/", "/ɪn'vaɪt/"),
    "join": ("/dʒɔɪn/", "/dʒɔɪn/"),
}

def get_db_connection():
    """创建数据库连接"""
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

def update_phonetic(conn, word, uk, us):
    """更新单词的音标"""
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
    """主函数"""
    print("=" * 60)
    print("     音标补充工具 v2")
    print("=" * 60)

    conn = get_db_connection()
    print("[OK] 数据库连接成功\n")

    total = len(PHONETIC_DATA)
    updated = 0
    skipped = 0
    not_found = 0

    print(f"准备更新 {total} 个单词/短语的音标...\n")

    for i, (word, (uk, us)) in enumerate(PHONETIC_DATA.items()):
        # 检查单词是否存在于数据库中
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tb_word WHERE word = ?", word)
        result = cursor.fetchone()

        if not result:
            # 尝试查找部分匹配（处理大小写问题）
            cursor.execute("SELECT id FROM tb_word WHERE LOWER(word) = LOWER(?)", word)
            if cursor.fetchone():
                print(f"[SKIP] {word} - 已有音标")
                skipped += 1
            else:
                print(f"[NOT FOUND] {word}")
                not_found += 1
            continue

        # 更新音标
        if update_phonetic(conn, word, uk, us):
            print(f"[OK] {word}")
            updated += 1
        else:
            print(f"[SKIP] {word} - 已有音标或更新失败")
            skipped += 1

        # 每 10 个请求后短暂等待，避免连接过载
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
