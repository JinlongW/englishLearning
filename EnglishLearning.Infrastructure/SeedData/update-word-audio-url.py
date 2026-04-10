#!/usr/bin/env python3
"""
更新数据库中现有单词的音频 URL
使用有道词典发音 API: https://dict.youdao.com/dictvoice?audio={word}&type=1
"""

import pyodbc
import urllib.parse

# 数据库连接字符串
conn_str = 'Server=localhost;Database=EnglishLearning;Trusted_Connection=True;TrustServerCertificate=True;'

def get_word_audio_url(word):
    """生成有道词典音频 URL（英式发音）"""
    encoded_word = urllib.parse.quote(word)
    return f"https://dict.youdao.com/dictvoice?audio={encoded_word}&type=1"

def update_word_audio_url():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # 查询所有单词
    cursor.execute("SELECT id, word FROM tb_word")
    words = cursor.fetchall()

    updated_count = 0
    for word_row in words:
        word_id = word_row.id
        word_text = word_row.word

        # 生成音频 URL
        audio_url = get_word_audio_url(word_text)

        # 更新数据库
        cursor.execute(
            "UPDATE tb_word SET audio_url = ? WHERE id = ?",
            audio_url, word_id
        )
        updated_count += 1
        print(f"Updated: {word_text} -> {audio_url}")

    conn.commit()
    print(f"\n完成！共更新 {updated_count} 个单词的音频 URL")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    update_word_audio_url()
