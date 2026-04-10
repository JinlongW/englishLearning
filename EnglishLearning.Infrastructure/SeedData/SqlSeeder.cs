using Microsoft.Data.SqlClient;

namespace EnglishLearning.Infrastructure.SeedData;

public class SqlSeeder
{
    private readonly string _connectionString;
    private SqlConnection _connection;

    public SqlSeeder(string connectionString)
    {
        _connectionString = connectionString;
        _connection = new SqlConnection(_connectionString);
    }

    public void Run()
    {
        _connection.Open();
        Console.WriteLine("数据库连接成功！");

        Console.WriteLine("正在导入三年级上册 Unit 1 单词...");
        ImportGrade3Unit1Words();

        Console.WriteLine("正在导入三年级上册 Unit 2 单词...");
        ImportGrade3Unit2Words();

        Console.WriteLine("正在导入三年级上册 Unit 3 单词...");
        ImportGrade3Unit3Words();

        Console.WriteLine("正在导入三年级上册 Unit 4 单词...");
        ImportGrade3Unit4Words();

        Console.WriteLine("正在导入三年级上册 Unit 5 单词...");
        ImportGrade3Unit5Words();

        Console.WriteLine("正在导入三年级上册 Unit 6 单词...");
        ImportGrade3Unit6Words();

        Console.WriteLine("正在更新单词音频 URL...");
        UpdateWordAudioUrls();

        Console.WriteLine("导入完成！");
        _connection.Close();
    }

    /// <summary>
    /// 更新现有单词的音频 URL（使用有道词典发音 API）
    /// </summary>
    public void UpdateWordAudioUrls()
    {
        bool wasClosed = _connection.State != System.Data.ConnectionState.Open;
        if (wasClosed)
        {
            _connection.Open();
        }

        try
        {
            // 查询所有单词
            using var cmd = new SqlCommand("SELECT id, word FROM tb_word", _connection);
            using var reader = cmd.ExecuteReader();

            int updatedCount = 0;
            int failedCount = 0;

            while (reader.Read())
            {
                var wordId = reader.GetGuid(0);
                var wordText = reader.GetString(1);

                // 生成有道词典音频 URL（英式发音）
                var encodedWord = System.Web.HttpUtility.UrlEncode(wordText);
                var audioUrl = $"https://dict.youdao.com/dictvoice?audio={encodedWord}&type=1";

                using var updateCmd = new SqlCommand(
                    "UPDATE tb_word SET audio_url = @audioUrl WHERE id = @id",
                    _connection);
                updateCmd.Parameters.AddWithValue("@audioUrl", audioUrl);
                updateCmd.Parameters.AddWithValue("@id", wordId);

                var rows = updateCmd.ExecuteNonQuery();
                if (rows > 0)
                {
                    updatedCount++;
                    Console.WriteLine($"  更新：{wordText}");
                }
                else
                {
                    failedCount++;
                }
            }

            Console.WriteLine($"共更新 {updatedCount} 个单词的音频 URL，失败 {failedCount} 个");
        }
        finally
        {
            if (wasClosed && _connection.State == System.Data.ConnectionState.Open)
            {
                _connection.Close();
            }
        }
    }

    private Guid? GetUnitId(int grade, string semester, int unitNo)
    {
        using var cmd = new SqlCommand(
            "SELECT id FROM tb_grade_unit WHERE grade=@grade AND semester=@semester AND unit_no=@unitNo",
            _connection);
        cmd.Parameters.AddWithValue("@grade", grade);
        cmd.Parameters.AddWithValue("@semester", semester);
        cmd.Parameters.AddWithValue("@unitNo", unitNo);
        var result = cmd.ExecuteScalar();
        return result is Guid g ? g : null;
    }

    private void InsertWord(Guid gradeUnitId, string word, string phoneticUk, string phoneticUs,
        string meaningCn, string partOfSpeech, string exampleEn, string exampleCn, int sortOrder, string? audioUrl = null)
    {
        using var cmd = new SqlCommand(@"
INSERT INTO tb_word (id, grade_unit_id, word, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order, audio_url)
VALUES (NEWID(), @gradeUnitId, @word, @phoneticUk, @phoneticUs, @meaningCn, @partOfSpeech, @exampleEn, @exampleCn, @sortOrder, @audioUrl)",
            _connection);
        cmd.Parameters.AddWithValue("@gradeUnitId", gradeUnitId);
        cmd.Parameters.AddWithValue("@word", word);
        cmd.Parameters.AddWithValue("@phoneticUk", phoneticUk);
        cmd.Parameters.AddWithValue("@phoneticUs", phoneticUs);
        cmd.Parameters.AddWithValue("@meaningCn", meaningCn);
        cmd.Parameters.AddWithValue("@partOfSpeech", partOfSpeech ?? (object)DBNull.Value);
        cmd.Parameters.AddWithValue("@exampleEn", exampleEn ?? (object)DBNull.Value);
        cmd.Parameters.AddWithValue("@exampleCn", exampleCn ?? (object)DBNull.Value);
        cmd.Parameters.AddWithValue("@sortOrder", sortOrder);
        cmd.Parameters.AddWithValue("@audioUrl", audioUrl ?? (object)DBNull.Value);
        cmd.ExecuteNonQuery();
    }

    private void ImportGrade3Unit1Words()
    {
        var unitId = GetUnitId(3, "上", 1);
        if (unitId == null) return;

        InsertWord(unitId.Value, "ruler", "/ˈruːlə/", "/ˈruːlər/", "尺子", "n.", "I have a ruler.", "我有一把尺子。", 1, "https://dict.youdao.com/dictvoice?audio=ruler&type=1");
        InsertWord(unitId.Value, "pencil", "/ˈpensl/", "/ˈpensl/", "铅笔", "n.", "This is my pencil.", "这是我的铅笔。", 2, "https://dict.youdao.com/dictvoice?audio=pencil&type=1");
        InsertWord(unitId.Value, "eraser", "/ɪˈreɪzə/", "/ɪˈreɪsər/", "橡皮", "n.", "Can I use your eraser?", "我可以用你的橡皮吗？", 3, "https://dict.youdao.com/dictvoice?audio=eraser&type=1");
        InsertWord(unitId.Value, "crayon", "/ˈkreɪən/", "/ˈkreɪən/", "蜡笔", "n.", "She has a red crayon.", "她有一支红色的蜡笔。", 4, "https://dict.youdao.com/dictvoice?audio=crayon&type=1");
        InsertWord(unitId.Value, "book", "/bʊk/", "/bʊk/", "书", "n.", "Open your book.", "打开你的书。", 5, "https://dict.youdao.com/dictvoice?audio=book&type=1");
        InsertWord(unitId.Value, "pencil box", "/ˈpensl bɒks/", "/ˈpensl bɑːks/", "铅笔盒", "n.", "My pen is in the pencil box.", "我的钢笔在铅笔盒里。", 6, "https://dict.youdao.com/dictvoice?audio=pencil%20box&type=1");
        InsertWord(unitId.Value, "bag", "/bæɡ/", "/bæɡ/", "书包", "n.", "I put my books in the bag.", "我把书放进书包里。", 7, "https://dict.youdao.com/dictvoice?audio=bag&type=1");
    }

    private void ImportGrade3Unit2Words()
    {
        var unitId = GetUnitId(3, "上", 2);
        if (unitId == null) return;

        InsertWord(unitId.Value, "head", "/hed/", "/hed/", "头", "n.", "Touch your head.", "摸摸你的头。", 1, "https://dict.youdao.com/dictvoice?audio=head&type=1");
        InsertWord(unitId.Value, "face", "/feɪs/", "/feɪs/", "脸", "n.", "She has a round face.", "她有一张圆脸。", 2, "https://dict.youdao.com/dictvoice?audio=face&type=1");
        InsertWord(unitId.Value, "nose", "/nəʊz/", "/noʊz/", "鼻子", "n.", "Point to your nose.", "指着你的鼻子。", 3, "https://dict.youdao.com/dictvoice?audio=nose&type=1");
        InsertWord(unitId.Value, "eye", "/aɪ/", "/aɪ/", "眼睛", "n.", "I have two eyes.", "我有两只眼睛。", 4, "https://dict.youdao.com/dictvoice?audio=eye&type=1");
        InsertWord(unitId.Value, "ear", "/ɪə/", "/ɪr/", "耳朵", "n.", "Cover your ears.", "捂住你的耳朵。", 5, "https://dict.youdao.com/dictvoice?audio=ear&type=1");
        InsertWord(unitId.Value, "mouth", "/maʊθ/", "/maʊθ/", "嘴巴", "n.", "Open your mouth.", "张开你的嘴巴。", 6, "https://dict.youdao.com/dictvoice?audio=mouth&type=1");
        InsertWord(unitId.Value, "arm", "/ɑːm/", "/ɑːrm/", "胳膊", "n.", "Raise your arm.", "举起你的胳膊。", 7, "https://dict.youdao.com/dictvoice?audio=arm&type=1");
        InsertWord(unitId.Value, "hand", "/hænd/", "/hænd/", "手", "n.", "Clap your hands.", "拍拍你的手。", 8, "https://dict.youdao.com/dictvoice?audio=hand&type=1");
        InsertWord(unitId.Value, "leg", "/leɡ/", "/leɡ/", "腿", "n.", "Stamp your foot.", "跺跺你的脚。", 9, "https://dict.youdao.com/dictvoice?audio=leg&type=1");
        InsertWord(unitId.Value, "foot", "/fʊt/", "/fʊt/", "脚", "n.", "My foot hurts.", "我的脚疼。", 10, "https://dict.youdao.com/dictvoice?audio=foot&type=1");
    }

    private void ImportGrade3Unit3Words()
    {
        var unitId = GetUnitId(3, "上", 3);
        if (unitId == null) return;

        InsertWord(unitId.Value, "red", "/red/", "/red/", "红色", "n./adj.", "The apple is red.", "苹果是红色的。", 1, "https://dict.youdao.com/dictvoice?audio=red&type=1");
        InsertWord(unitId.Value, "yellow", "/ˈjeləʊ/", "/ˈjeloʊ/", "黄色", "n./adj.", "The banana is yellow.", "香蕉是黄色的。", 2, "https://dict.youdao.com/dictvoice?audio=yellow&type=1");
        InsertWord(unitId.Value, "green", "/ɡriːn/", "/ɡriːn/", "绿色", "n./adj.", "The grass is green.", "草地是绿色的。", 3, "https://dict.youdao.com/dictvoice?audio=green&type=1");
        InsertWord(unitId.Value, "blue", "/bluː/", "/bluː/", "蓝色", "n./adj.", "The sky is blue.", "天空是蓝色的。", 4, "https://dict.youdao.com/dictvoice?audio=blue&type=1");
        InsertWord(unitId.Value, "black", "/blæk/", "/blæk/", "黑色", "n./adj.", "The cat is black.", "这只猫是黑色的。", 5, "https://dict.youdao.com/dictvoice?audio=black&type=1");
        InsertWord(unitId.Value, "white", "/waɪt/", "/waɪt/", "白色", "n./adj.", "The snow is white.", "雪是白色的。", 6, "https://dict.youdao.com/dictvoice?audio=white&type=1");
        InsertWord(unitId.Value, "orange", "/ˈɒrɪndʒ/", "/ˈɔːrɪndʒ/", "橙色", "n./adj.", "The orange is orange.", "橙子是橙色的。", 7, "https://dict.youdao.com/dictvoice?audio=orange&type=1");
        InsertWord(unitId.Value, "brown", "/braʊn/", "/braʊn/", "棕色", "n./adj.", "The bear is brown.", "熊是棕色的。", 8, "https://dict.youdao.com/dictvoice?audio=brown&type=1");
    }

    private void ImportGrade3Unit4Words()
    {
        var unitId = GetUnitId(3, "上", 4);
        if (unitId == null) return;

        InsertWord(unitId.Value, "pig", "/pɪɡ/", "/pɪɡ/", "猪", "n.", "The pig is fat.", "这头猪很胖。", 1, "https://dict.youdao.com/dictvoice?audio=pig&type=1");
        InsertWord(unitId.Value, "bear", "/beə/", "/ber/", "熊", "n.", "The bear is big.", "熊很大。", 2, "https://dict.youdao.com/dictvoice?audio=bear&type=1");
        InsertWord(unitId.Value, "duck", "/dʌk/", "/dʌk/", "鸭子", "n.", "The duck can swim.", "鸭子会游泳。", 3, "https://dict.youdao.com/dictvoice?audio=duck&type=1");
        InsertWord(unitId.Value, "elephant", "/ˈelɪfənt/", "/ˈelɪfənt/", "大象", "n.", "The elephant has a long nose.", "大象有一个长鼻子。", 4, "https://dict.youdao.com/dictvoice?audio=elephant&type=1");
        InsertWord(unitId.Value, "monkey", "/ˈmʌŋki/", "/ˈmʌŋki/", "猴子", "n.", "The monkey is clever.", "猴子很聪明。", 5, "https://dict.youdao.com/dictvoice?audio=monkey&type=1");
        InsertWord(unitId.Value, "bird", "/bɜːd/", "/bɜːrd/", "鸟", "n.", "The bird can fly.", "鸟会飞。", 6, "https://dict.youdao.com/dictvoice?audio=bird&type=1");
        InsertWord(unitId.Value, "tiger", "/ˈtaɪɡə/", "/ˈtaɪɡər/", "老虎", "n.", "The tiger is strong.", "老虎很强壮。", 7, "https://dict.youdao.com/dictvoice?audio=tiger&type=1");
        InsertWord(unitId.Value, "panda", "/ˈpændə/", "/ˈpændə/", "熊猫", "n.", "The panda is cute.", "熊猫很可爱。", 8, "https://dict.youdao.com/dictvoice?audio=panda&type=1");
        InsertWord(unitId.Value, "zoo", "/zuː/", "/zuː/", "动物园", "n.", "Let's go to the zoo.", "我们去动物园吧。", 9, "https://dict.youdao.com/dictvoice?audio=zoo&type=1");
    }

    private void ImportGrade3Unit5Words()
    {
        var unitId = GetUnitId(3, "上", 5);
        if (unitId == null) return;

        InsertWord(unitId.Value, "bread", "/bred/", "/bred/", "面包", "n.", "I like bread.", "我喜欢面包。", 1, "https://dict.youdao.com/dictvoice?audio=bread&type=1");
        InsertWord(unitId.Value, "juice", "/dʒuːs/", "/dʒuːs/", "果汁", "n.", "Can I have some juice?", "我能喝点果汁吗？", 2, "https://dict.youdao.com/dictvoice?audio=juice&type=1");
        InsertWord(unitId.Value, "egg", "/eɡ/", "/eɡ/", "鸡蛋", "n.", "I eat an egg for breakfast.", "我早餐吃了一个鸡蛋。", 3, "https://dict.youdao.com/dictvoice?audio=egg&type=1");
        InsertWord(unitId.Value, "milk", "/mɪlk/", "/mɪlk/", "牛奶", "n.", "Drink some milk.", "喝点牛奶。", 4, "https://dict.youdao.com/dictvoice?audio=milk&type=1");
        InsertWord(unitId.Value, "water", "/ˈwɔːtə/", "/ˈwɔːtər/", "水", "n.", "I want some water.", "我想喝水。", 5, "https://dict.youdao.com/dictvoice?audio=water&type=1");
        InsertWord(unitId.Value, "fish", "/fɪʃ/", "/fɪʃ/", "鱼", "n.", "The fish is delicious.", "鱼很美味。", 6, "https://dict.youdao.com/dictvoice?audio=fish&type=1");
        InsertWord(unitId.Value, "rice", "/raɪs/", "/raɪs/", "米饭", "n.", "I have rice for lunch.", "我午餐吃了米饭。", 7, "https://dict.youdao.com/dictvoice?audio=rice&type=1");
    }

    private void ImportGrade3Unit6Words()
    {
        var unitId = GetUnitId(3, "上", 6);
        if (unitId == null) return;

        InsertWord(unitId.Value, "one", "/wʌn/", "/wʌn/", "一", "num.", "I have one book.", "我有一本书。", 1, "https://dict.youdao.com/dictvoice?audio=one&type=1");
        InsertWord(unitId.Value, "two", "/tuː/", "/tuː/", "二", "num.", "I see two birds.", "我看到两只鸟。", 2, "https://dict.youdao.com/dictvoice?audio=two&type=1");
        InsertWord(unitId.Value, "three", "/θriː/", "/θriː/", "三", "num.", "There are three apples.", "有三个苹果。", 3, "https://dict.youdao.com/dictvoice?audio=three&type=1");
        InsertWord(unitId.Value, "four", "/fɔː/", "/fɔːr/", "四", "num.", "I have four pencils.", "我有四支铅笔。", 4, "https://dict.youdao.com/dictvoice?audio=four&type=1");
        InsertWord(unitId.Value, "five", "/faɪv/", "/faɪv/", "五", "num.", "She has five fingers.", "她有五个手指。", 5, "https://dict.youdao.com/dictvoice?audio=five&type=1");
        InsertWord(unitId.Value, "six", "/sɪks/", "/sɪks/", "六", "num.", "There are six days in a week.", "一周有六天。", 6, "https://dict.youdao.com/dictvoice?audio=six&type=1");
        InsertWord(unitId.Value, "seven", "/ˈsevn/", "/ˈsevn/", "七", "num.", "I see seven stars.", "我看到七颗星星。", 7, "https://dict.youdao.com/dictvoice?audio=seven&type=1");
        InsertWord(unitId.Value, "eight", "/eɪt/", "/eɪt/", "八", "num.", "There are eight people.", "有八个人。", 8, "https://dict.youdao.com/dictvoice?audio=eight&type=1");
        InsertWord(unitId.Value, "nine", "/naɪn/", "/naɪn/", "九", "num.", "I have nine balls.", "我有九个球。", 9, "https://dict.youdao.com/dictvoice?audio=nine&type=1");
        InsertWord(unitId.Value, "ten", "/ten/", "/ten/", "十", "num.", "There are ten fingers.", "有十个手指。", 10, "https://dict.youdao.com/dictvoice?audio=ten&type=1");
        InsertWord(unitId.Value, "cake", "/keɪk/", "/keɪk/", "蛋糕", "n.", "Happy birthday! Let's eat cake.", "生日快乐！我们吃蛋糕吧。", 11, "https://dict.youdao.com/dictvoice?audio=cake&type=1");
    }
}
