# -*- coding: utf-8 -*-
"""
音标补充工具
日期：2026-04-02
说明：为 115 个缺失音标的单词补充英式和美氏音标
"""

import pyodbc
import json

# ==================== 配置区域 ====================
DB_SERVER = "localhost"
DB_DATABASE = "EnglishLearning"

# ==================== 音标数据 ====================
# 缺失音标的单词/短语音标映射
PHONETIC_DATA = {
    # 三年级相关
    "PE class": ("/'pi: 'klɑ:s/", "/'pi: 'klæs/"),
    "be careful": ("/bi: 'keəfl/", "/bi: 'kerfl/"),
    "play sports": ("/pleɪ spɔ:ts/", "/pleɪ spɔ:rts/"),
    "come on": ("/'kʌm ɒn/", "/'kʌm ɑ:n/"),
    "OK": ("/'əʊ'keɪ/", "/oʊ'keɪ/"),

    # 运动类
    "ping-pong": ("/'pɪŋpɒŋ/", "/'pɪŋpɔ:ŋ/"),
    "went camping": ("/went 'kæmpɪŋ/", "/went 'kæmpɪŋ/"),
    "pen pal": ("/'pen pæl/", "/'pen pæl/"),
    "water bottle": ("/'wɔ:tə 'bɒtl/", "/'wɔ:tər 'bɑ:tl/"),
    "pick apples": ("/pɪk 'æplz/", "/pɪk 'æplz/"),

    # 日常活动
    "do homework": ("/du: 'həʊmwɜ:k/", "/du: 'hoʊmwɜ:rk/"),
    "do kung fu": ("/du: 'kʌŋ fu:/", "/du: 'kʌŋ fu:/"),
    "read books": ("/ri:d bʊks/", "/ri:d bʊks/"),
    "wash clothes": ("/wɒʃ kləʊðz/", "/wɑ:ʃ kloʊðz/"),
    "watch TV": ("/wɒtʃ 'ti:'vi:/", "/wɑ:tʃ 'ti:'vi:/"),

    # 食物类
    "ice cream": ("/'aɪs kri:m/", "/'aɪs kri:m/"),
    "fresh food": ("/freʃ fu:d/", "/freʃ fu:d/"),
    "sweet food": ("/swi:t fu:d/", "/swi:t fu:d/"),
    "hot food": ("/hɒt fu:d/", "/hɑ:t fu:d/"),
    "delicious food": ("/dɪ'lɪʃəs fu:d/", "/dɪ'lɪʃəs fu:d/"),

    # 地点类
    "nature park": ("/'neɪtʃə pɑ:k/", "/'neɪtʃər pɑ:rk/"),
    "forest park": ("/'fɒrɪst pɑ:k/", "/'fɔ:rɪst pɑ:rk/"),
    "theme park": ("/'θi:m pɑ:k/", "/'θi:m pɑ:rk/"),
    "science museum": ("/'saɪəns mju:'zi:əm/", "/'saɪəns mju:'zi:əm/"),
    "post office": ("/pəʊst 'ɒfɪs/", "/poʊst 'ɔ:fɪs/"),
    "bookstore": ("/'bʊkstɔ:/", "/'bʊkstɔ:r/"),
    "cinema": ("/'sɪnəmə/", "/'sɪnəmə/"),
    "hospital": ("/'hɒspɪtl/", "/'hɑ:spɪtl/"),
    "crossing": ("/'krɒsɪŋ/", "/'krɔ:sɪŋ/"),

    # 交通类
    "by plane": ("/baɪ pleɪn/", "/baɪ pleɪn/"),
    "by ship": ("/baɪ ʃɪp/", "/baɪ ʃɪp/"),
    "by subway": ("/baɪ 'sʌbweɪ/", "/baɪ 'sʌbweɪ/"),
    "by train": ("/baɪ treɪn/", "/baɪ treɪn/"),
    "by bus": ("/baɪ bʌs/", "/baɪ bʌs/"),
    "by taxi": ("/baɪ 'tæksi/", "/baɪ 'tæksi/"),
    "on foot": ("/ɒn fʊt/", "/ɑ:n fʊt/"),

    # 时间类
    "this morning": ("/ðɪs 'mɔ:nɪŋ/", "/ðɪs 'mɔ:rnɪŋ/"),
    "this afternoon": ("/ðɪs 'ɑ:ftə'nu:n/", "/ðɪs 'æftər'nu:n/"),
    "this evening": ("/ðɪs 'i:vnɪŋ/", "/ðɪs 'i:vnɪŋ/"),
    "tonight": ("/tə'naɪt/", "/tə'naɪt/"),
    "tomorrow": ("/tə'mɒrəʊ/", "/tə'mɔ:roʊ/"),

    # 动作类
    "take a trip": ("/teɪk ə trɪp/", "/teɪk ə trɪp/"),
    "see a film": ("/si: ə fɪlm/", "/si: ə fɪlm/"),
    "visit grandparents": ("/'vɪzɪt 'grænpərents/", "/'vɪzɪt 'grænpərents/"),
    "go hiking": ("/gəʊ 'haɪkɪŋ/", "/goʊ 'haɪkɪŋ/"),
    "go shopping": ("/gəʊ 'ʃɒpɪŋ/", "/goʊ 'ʃɑ:pɪŋ/"),
    "go swimming": ("/gəʊ 'swɪmɪŋ/", "/goʊ 'swɪmɪŋ/"),
    "go fishing": ("/gəʊ 'fɪʃɪŋ/", "/goʊ 'fɪʃɪŋ/"),

    # 其他短语
    "turn left": ("/tɜ:n left/", "/tɜ:rn left/"),
    "turn right": ("/tɜ:n raɪt/", "/tɜ:rn raɪt/"),
    "go straight": ("/gəʊ streɪt/", "/goʊ streɪt/"),
    "slow down": ("/sləʊ daʊn/", "/sloʊ daʊn/"),
    "stop and wait": ("/stɒp ənd weɪt/", "/stɑ:p ənd weɪt/"),
    "pay attention": ("/peɪ ə'tenʃn/", "/peɪ ə'tenʃn/"),

    # 形容词类
    "far from": ("/fɑ: frɒm/", "/fɑ:r frʌm/"),
    "next to": ("/'nekst tu:/", "/'nekst tu:/"),
    "near to": ("/nɪə tu:/", "/nɪr tu:/"),
    "close to": ("/kləʊs tu:/", "/kloʊs tu:/"),

    # 问候语
    "good morning": ("/gʊd 'mɔ:nɪŋ/", "/gʊd 'mɔ:rnɪŋ/"),
    "good afternoon": ("/gʊd 'ɑ:ftə'nu:n/", "/gʊd 'æftər'nu:n/"),
    "good evening": ("/gʊd 'i:vnɪŋ/", "/gʊd 'i:vnɪŋ/"),
    "good night": ("/gʊd naɪt/", "/gʊd naɪt/"),
    "nice to meet you": ("/naɪs tu mi:t ju:/", "/naɪs tu mi:t ju:/"),
    "glad to meet you": ("/glæd tu mi:t ju:/", "/glæd tu mi:t ju:/"),

    # 常用语
    "thank you": ("/'θæŋk ju:/", "/'θæŋk ju:/"),
    "you're welcome": ("/jɔ: 'welkəm/", "/jʊr 'welkəm/"),
    "excuse me": ("/ɪk'skju:z mi:/", "/ɪk'skju:z mi:/"),
    "I'm sorry": ("/aɪm 'sɒri/", "/aɪm 'sɔ:ri/"),
    "of course": ("/əv kɔ:s/", "/əv kɔ:rs/"),

    # 学校生活
    "art class": ("/ɑ:t klɑ:s/", "/ɑ:rt klæs/"),
    "music class": ("/'mju:zɪk klɑ:s/", "/'mju:zɪk klæs/"),
    "PE class": ("/'pi: 'klɑ:s/", "/'pi: 'klæs/"),
    "English class": ("/'ɪŋglɪʃ klɑ:s/", "/'ɪŋglɪʃ klæs/"),
    "math class": ("/mæθ klɑ:s/", "/mæθ klæs/"),

    # 日常活动 2
    "get up": ("/get ʌp/", "/get ʌp/"),
    "go to bed": ("/gəʊ tu bed/", "/goʊ tu bed/"),
    "go to school": ("/gəʊ tu sku:l/", "/goʊ tu sku:l/"),
    "go home": ("/gəʊ həʊm/", "/goʊ hoʊm/"),
    "have breakfast": ("/hæv 'brekfəst/", "/hæv 'brekfəst/"),
    "have lunch": ("/hæv lʌntʃ/", "/hæv lʌntʃ/"),
    "have dinner": ("/hæv 'dɪnə/", "/hæv 'dɪnər/"),

    # 天气类
    "sunny day": ("/'sʌni deɪ/", "/'sʌni deɪ/"),
    "rainy day": ("/'reɪni deɪ/", "/'reɪni deɪ/"),
    "cloudy day": ("/'klaʊdi deɪ/", "/'klaʊdi deɪ/"),
    "windy day": ("/'wɪndi deɪ/", "/'wɪndi deɪ/"),
    "snowy day": ("/'snəʊi deɪ/", "/'snoʊi deɪ/"),

    # 季节活动
    "make a snowman": ("/meɪk ə 'snəʊmæn/", "/meɪk ə 'snoʊmæn/"),
    "fly kites": ("/flaɪ kaɪts/", "/flaɪ kaɪts/"),
    "plant trees": ("/plɑ:nt tri:z/", "/plænt tri:z/"),
    "swim in summer": ("/swɪm ɪn 'sʌmə/", "/swɪm ɪn 'sʌmər/"),

    # 节日
    "Mid-Autumn Festival": ("/'mɪd 'ɔ:təm 'festɪvl/", "/'mɪd 'ɔ:təm 'festɪvl/"),
    "National Day": ("/'næʃnəl deɪ/", "/'næʃnəl deɪ/"),
    "Children's Day": ("/'tʃɪldrənz deɪ/", "/'tʃɪldrənz deɪ/"),
    "Teachers' Day": ("/'ti:tʃəz deɪ/", "/'ti:tʃərz deɪ/"),
    "New Year's Day": ("/nju: jɪəz deɪ/", "/nu: jɪrz deɪ/"),
    "Spring Festival": ("/sprɪŋ 'festɪvl/", "/sprɪŋ 'festɪvl/"),

    # 其他
    "wait a minute": ("/weɪt ə 'mɪnɪt/", "/weɪt ə 'mɪnɪt/"),
    "good idea": ("/gʊd aɪ'dɪə/", "/gʊd aɪ'di:ə/"),
    "bad luck": ("/bæd lʌk/", "/bæd lʌk/"),
    "good luck": ("/gʊd lʌk/", "/gʊd lʌk/"),
    "well done": ("/wel dʌn/", "/wel dʌn/"),
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

def update_phonetic(conn, word: str, uk: str, us: str) -> bool:
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
        print(f"  [ERROR] 更新 {word} 失败：{e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("     音标补充工具")
    print("=" * 60)

    conn = get_db_connection()
    print("[OK] 数据库连接成功\n")

    # 统计需要更新的单词数
    total = len(PHONETIC_DATA)
    updated = 0
    skipped = 0
    not_found = 0

    print(f"准备更新 {total} 个单词/短语的音标...\n")

    for word, (uk, us) in PHONETIC_DATA.items():
        # 检查单词是否存在于数据库中
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tb_word WHERE word = ?", word)
        if not cursor.fetchone():
            # 尝试查找部分匹配（处理大小写问题）
            cursor.execute("SELECT id FROM tb_word WHERE LOWER(word) = LOWER(?)", word)
            if cursor.fetchone():
                print(f"[SKIP] {word} - 已存在音标，跳过")
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
            print(f"[SKIP] {word} - 巳有音标或更新失败")
            skipped += 1

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
