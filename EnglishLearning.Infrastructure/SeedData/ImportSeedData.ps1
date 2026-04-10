# 人教版小学英语题库数据导入脚本
# 使用 UTF-8 编码

$connectionString = "Server=localhost;Database=EnglishLearning;Trusted_Connection=True;TrustServerCertificate=True;"
$connection = New-Object System.Data.SqlClient.SqlConnection
$connection.ConnectionString = $connectionString
$connection.Open()

$command = $connection.CreateCommand()

Write-Host "========================================"
Write-Host "人教版小学英语题库数据导入"
Write-Host "========================================"
Write-Host ""

# 获取单元 ID 的辅助函数
function Get-UnitId($grade, $semester, $unitNo) {
    $command.CommandText = "SELECT id FROM tb_grade_unit WHERE grade=$grade AND semester='$semester' AND unit_no=$unitNo"
    $result = $command.ExecuteScalar()
    return $result
}

# 插入单词的辅助函数
function Insert-Word($unitId, $wordText, $phoneticUk, $phoneticUs, $meaningCn, $partOfSpeech, $exampleEn, $exampleCn, $sortOrder) {
    $command.CommandText = @"
INSERT INTO tb_word (id, grade_unit_id, word_text, phonetic_uk, phonetic_us, meaning_cn, part_of_speech, example_en, example_cn, sort_order, created_at)
VALUES (NEWID(), @unitId, @wordText, @phoneticUk, @phoneticUs, @meaningCn, @partOfSpeech, @exampleEn, @exampleCn, @sortOrder, GETDATE())
"@
    $command.Parameters.Clear()
    $command.Parameters.AddWithValue("@unitId", $unitId) | Out-Null
    $command.Parameters.AddWithValue("@wordText", $wordText) | Out-Null
    $command.Parameters.AddWithValue("@phoneticUk", $phoneticUk) | Out-Null
    $command.Parameters.AddWithValue("@phoneticUs", $phoneticUs) | Out-Null
    $command.Parameters.AddWithValue("@meaningCn", $meaningCn) | Out-Null
    $command.Parameters.AddWithValue("@partOfSpeech", $partOfSpeech) | Out-Null
    $command.Parameters.AddWithValue("@exampleEn", $exampleEn) | Out-Null
    $command.Parameters.AddWithValue("@exampleCn", $exampleCn) | Out-Null
    $command.Parameters.AddWithValue("@sortOrder", $sortOrder) | Out-Null
    $command.ExecuteNonQuery() | Out-Null
}

# 插入语法的辅助函数
function Insert-Grammar($unitId, $title, $contentJson, $sortOrder) {
    $command.CommandText = @"
INSERT INTO tb_grammar (id, grade_unit_id, title, content_type, content_json, sort_order, passing_score, created_at)
VALUES (NEWID(), @unitId, @title, 'lesson', @contentJson, @sortOrder, 60, GETDATE())
"@
    $command.Parameters.Clear()
    $command.Parameters.AddWithValue("@unitId", $unitId) | Out-Null
    $command.Parameters.AddWithValue("@title", $title) | Out-Null
    $command.Parameters.AddWithValue("@contentJson", $contentJson) | Out-Null
    $command.Parameters.AddWithValue("@sortOrder", $sortOrder) | Out-Null
    $command.ExecuteNonQuery() | Out-Null
}

# 插入题目的辅助函数
function Insert-Question($unitId, $questionType, $difficulty, $questionStem, $correctAnswer, $answerAnalysis, $knowledgePoint, $tags) {
    $command.CommandText = @"
INSERT INTO tb_question (id, grade_unit_id, question_type, difficulty, question_stem, correct_answer, answer_analysis, knowledge_point, tags, is_active, created_at, updated_at)
VALUES (NEWID(), @unitId, @questionType, @difficulty, @questionStem, @correctAnswer, @answerAnalysis, @knowledgePoint, @tags, 1, GETDATE(), GETDATE())
SELECT CAST(SCOPE_IDENTITY() AS UNIQUEIDENTIFIER)
"@
    $command.Parameters.Clear()
    $command.Parameters.AddWithValue("@unitId", $unitId) | Out-Null
    $command.Parameters.AddWithValue("@questionType", $questionType) | Out-Null
    $command.Parameters.AddWithValue("@difficulty", $difficulty) | Out-Null
    $command.Parameters.AddWithValue("@questionStem", $questionStem) | Out-Null
    $command.Parameters.AddWithValue("@correctAnswer", $correctAnswer) | Out-Null
    $command.Parameters.AddWithValue("@answerAnalysis", $answerAnalysis) | Out-Null
    $command.Parameters.AddWithValue("@knowledgePoint", $knowledgePoint) | Out-Null
    $command.Parameters.AddWithValue("@tags", $tags) | Out-Null
    $result = $command.ExecuteScalar()
    return $result
}

# 插入选项的辅助函数
function Insert-QuestionOption($questionId, $optionKey, $optionContent, $sortOrder) {
    $command.CommandText = @"
INSERT INTO tb_question_option (id, question_id, option_key, option_content, sort_order)
VALUES (NEWID(), @questionId, @optionKey, @optionContent, @sortOrder)
"@
    $command.Parameters.Clear()
    $command.Parameters.AddWithValue("@questionId", $questionId) | Out-Null
    $command.Parameters.AddWithValue("@optionKey", $optionKey) | Out-Null
    $command.Parameters.AddWithValue("@optionContent", $optionContent) | Out-Null
    $command.Parameters.AddWithValue("@sortOrder", $sortOrder) | Out-Null
    $command.ExecuteNonQuery() | Out-Null
}

# =====================
# 三年级上册 Unit 1 Hello!
# =====================
Write-Host "正在导入三年级上册 Unit 1 数据..."

$unit3_1 = Get-UnitId 3 "上" 1

Insert-Word $unit3_1 "ruler" "/ˈruːlə/" "/ˈruːlər/" "尺子" "n." "I have a ruler." "我有一把尺子。" 1
Insert-Word $unit3_1 "pencil" "/ˈpensl/" "/ˈpensl/" "铅笔" "n." "This is my pencil." "这是我的铅笔。" 2
Insert-Word $unit3_1 "eraser" "/ɪˈreɪzə/" "/ɪˈreɪsər/" "橡皮" "n." "Can I use your eraser?" "我可以用你的橡皮吗？" 3
Insert-Word $unit3_1 "crayon" "/ˈkreɪən/" "/ˈkreɪən/" "蜡笔" "n." "She has a red crayon." "她有一支红色的蜡笔。" 4
Insert-Word $unit3_1 "book" "/bʊk/" "/bʊk/" "书" "n." "Open your book." "打开你的书。" 5
Insert-Word $unit3_1 "pencil box" "/ˈpensl bɒks/" "/ˈpensl bɑːks/" "铅笔盒" "n." "My pen is in the pencil box." "我的钢笔在铅笔盒里。" 6
Insert-Word $unit3_1 "bag" "/bæɡ/" "/bæɡ/" "书包" "n." "I put my books in the bag." "我把书放进书包里。" 7

Insert-Grammar $unit3_1 "问候语 Hello/Hi" '{"introduction":"Hello 和 Hi 是最常用的英语问候语，用于见面时打招呼。","examples":[{"en":"Hello! I am Mike.","cn":"你好！我是迈克。"},{"en":"Hi! I am Sarah.","cn":"嗨！我是莎拉。"}],"notes":"Hello 比较正式，Hi 比较随意，两者可以互换使用。"}' 1
Insert-Grammar $unit3_1 "自我介绍 I am..." '{"introduction":"用 I am 或 Im 来介绍自己的名字。","examples":[{"en":"I am Mike.","cn":"我是迈克。"},{"en":"Im Sarah.","cn":"我是莎拉。"}],"notes":"I am 可以缩写为 Im。"}' 2

$q1 = Insert-Question $unit3_1 "single_choice" 1 "当你想和别人打招呼时，你应该说：" "A" "Hello 和 Hi 都是常用的问候语，意思是你好。" "问候语" "greeting,basic"
Insert-QuestionOption $q1 "A" "Hello!" 1
Insert-QuestionOption $q1 "B" "Goodbye!" 2
Insert-QuestionOption $q1 "C" "Thank you!" 3

$q2 = Insert-Question $unit3_1 "fill_blank" 1 "Hello! I ____ Mike." "am" "介绍自己时用 I am 或 Im" "be 动词" "grammar,be-verb"

Write-Host "三年级上册 Unit 1 导入完成！"

# =====================
# 三年级上册 Unit 2 Look at Me
# =====================
Write-Host "正在导入三年级上册 Unit 2 数据..."

$unit3_2 = Get-UnitId 3 "上" 2

Insert-Word $unit3_2 "head" "/hed/" "/hed/" "头" "n." "Touch your head." "摸摸你的头。" 1
Insert-Word $unit3_2 "face" "/feɪs/" "/feɪs/" "脸" "n." "She has a round face." "她有一张圆脸。" 2
Insert-Word $unit3_2 "nose" "/nəʊz/" "/noʊz/" "鼻子" "n." "Point to your nose." "指着你的鼻子。" 3
Insert-Word $unit3_2 "eye" "/aɪ/" "/aɪ/" "眼睛" "n." "I have two eyes." "我有两只眼睛。" 4
Insert-Word $unit3_2 "ear" "/ɪə/" "/ɪr/" "耳朵" "n." "Cover your ears." "捂住你的耳朵。" 5
Insert-Word $unit3_2 "mouth" "/maʊθ/" "/maʊθ/" "嘴巴" "n." "Open your mouth." "张开你的嘴巴。" 6
Insert-Word $unit3_2 "arm" "/ɑːm/" "/ɑːrm/" "胳膊" "n." "Raise your arm." "举起你的胳膊。" 7
Insert-Word $unit3_2 "hand" "/hænd/" "/hænd/" "手" "n." "Clap your hands." "拍拍你的手。" 8
Insert-Word $unit3_2 "leg" "/leɡ/" "/leɡ/" "腿" "n." "Stamp your foot." "跺跺你的脚。" 9
Insert-Word $unit3_2 "foot" "/fʊt/" "/fʊt/" "脚" "n." "My foot hurts." "我的脚疼。" 10

Insert-Grammar $unit3_2 "指令句 Touch your..." '{"introduction":"用 Touch your... 来发出触摸身体部位的指令。","examples":[{"en":"Touch your head.","cn":"摸摸你的头。"},{"en":"Touch your nose.","cn":"摸摸你的鼻子。"}],"notes":"这是祈使句，动词原形开头。"}' 1

$q3 = Insert-Question $unit3_2 "single_choice" 1 "Touch your head. 的意思是：" "A" "Touch your head 意思是摸摸你的头" "指令理解" "listening,comprehension"
Insert-QuestionOption $q3 "A" "摸摸你的头" 1
Insert-QuestionOption $q3 "B" "拍拍你的手" 2
Insert-QuestionOption $q3 "C" "跺跺你的脚" 3

Write-Host "三年级上册 Unit 2 导入完成！"

# =====================
# 三年级上册 Unit 3 Let's Paint
# =====================
Write-Host "正在导入三年级上册 Unit 3 数据..."

$unit3_3 = Get-UnitId 3 "上" 3

Insert-Word $unit3_3 "red" "/red/" "/red/" "红色" "n./adj." "The apple is red." "苹果是红色的。" 1
Insert-Word $unit3_3 "yellow" "/ˈjeləʊ/" "/ˈjeloʊ/" "黄色" "n./adj." "The banana is yellow." "香蕉是黄色的。" 2
Insert-Word $unit3_3 "green" "/ɡriːn/" "/ɡriːn/" "绿色" "n./adj." "The grass is green." "草地是绿色的。" 3
Insert-Word $unit3_3 "blue" "/bluː/" "/bluː/" "蓝色" "n./adj." "The sky is blue." "天空是蓝色的。" 4
Insert-Word $unit3_3 "black" "/blæk/" "/blæk/" "黑色" "n./adj." "The cat is black." "这只猫是黑色的。" 5
Insert-Word $unit3_3 "white" "/waɪt/" "/waɪt/" "白色" "n./adj." "The snow is white." "雪是白色的。" 6
Insert-Word $unit3_3 "orange" "/ˈɒrɪndʒ/" "/ˈɔːrɪndʒ/" "橙色" "n./adj." "The orange is orange." "橙子是橙色的。" 7
Insert-Word $unit3_3 "brown" "/braʊn/" "/braʊn/" "棕色" "n./adj." "The bear is brown." "熊是棕色的。" 8

$q4 = Insert-Question $unit3_3 "single_choice" 1 "天空 (sky) 是什么颜色的？" "B" "天空通常是蓝色的 (blue)" "颜色词汇" "vocabulary,colors"
Insert-QuestionOption $q4 "A" "红色 (red)" 1
Insert-QuestionOption $q4 "B" "蓝色 (blue)" 2
Insert-QuestionOption $q4 "C" "绿色 (green)" 3

Write-Host "三年级上册 Unit 3 导入完成！"

# =====================
# 三年级上册 Unit 4 We Love Animals
# =====================
Write-Host "正在导入三年级上册 Unit 4 数据..."

$unit3_4 = Get-UnitId 3 "上" 4

Insert-Word $unit3_4 "pig" "/pɪɡ/" "/pɪɡ/" "猪" "n." "The pig is fat." "这头猪很胖。" 1
Insert-Word $unit3_4 "bear" "/beə/" "/ber/" "熊" "n." "The bear is big." "熊很大。" 2
Insert-Word $unit3_4 "duck" "/dʌk/" "/dʌk/" "鸭子" "n." "The duck can swim." "鸭子会游泳。" 3
Insert-Word $unit3_4 "elephant" "/ˈelɪfənt/" "/ˈelɪfənt/" "大象" "n." "The elephant has a long nose." "大象有一个长鼻子。" 4
Insert-Word $unit3_4 "monkey" "/ˈmʌŋki/" "/ˈmʌŋki/" "猴子" "n." "The monkey is clever." "猴子很聪明。" 5
Insert-Word $unit3_4 "bird" "/bɜːd/" "/bɜːrd/" "鸟" "n." "The bird can fly." "鸟会飞。" 6
Insert-Word $unit3_4 "tiger" "/ˈtaɪɡə/" "/ˈtaɪɡər/" "老虎" "n." "The tiger is strong." "老虎很强壮。" 7
Insert-Word $unit3_4 "panda" "/ˈpændə/" "/ˈpændə/" "熊猫" "n." "The panda is cute." "熊猫很可爱。" 8
Insert-Word $unit3_4 "zoo" "/zuː/" "/zuː/" "动物园" "n." "Lets go to the zoo." "我们去动物园吧。" 9

$q5 = Insert-Question $unit3_4 "single_choice" 1 "哪个动物会飞 (can fly)？" "B" "鸟 (bird) 会飞" "动物特征" "vocabulary,animals"
Insert-QuestionOption $q5 "A" "大象 (elephant)" 1
Insert-QuestionOption $q5 "B" "鸟 (bird)" 2
Insert-QuestionOption $q5 "C" "猪 (pig)" 3

Write-Host "三年级上册 Unit 4 导入完成！"

# =====================
# 三年级上册 Unit 5 Let's Eat
# =====================
Write-Host "正在导入三年级上册 Unit 5 数据..."

$unit3_5 = Get-UnitId 3 "上" 5

Insert-Word $unit3_5 "bread" "/bred/" "/bred/" "面包" "n." "I like bread." "我喜欢面包。" 1
Insert-Word $unit3_5 "juice" "/dʒuːs/" "/dʒuːs/" "果汁" "n." "Can I have some juice?" "我能喝点果汁吗？" 2
Insert-Word $unit3_5 "egg" "/eɡ/" "/eɡ/" "鸡蛋" "n." "I eat an egg for breakfast." "我早餐吃了一个鸡蛋。" 3
Insert-Word $unit3_5 "milk" "/mɪlk/" "/mɪlk/" "牛奶" "n." "Drink some milk." "喝点牛奶。" 4
Insert-Word $unit3_5 "water" "/ˈwɔːtə/" "/ˈwɔːtər/" "水" "n." "I want some water." "我想喝水。" 5
Insert-Word $unit3_5 "fish" "/fɪʃ/" "/fɪʃ/" "鱼" "n." "The fish is delicious." "鱼很美味。" 6
Insert-Word $unit3_5 "rice" "/raɪs/" "/raɪs/" "米饭" "n." "I have rice for lunch." "我午餐吃了米饭。" 7

$q6 = Insert-Question $unit3_5 "single_choice" 1 "你想喝点果汁，应该说：" "A" "Can I have some juice 是请求喝果汁的礼貌用语" "请求用语" "speaking,food"
Insert-QuestionOption $q6 "A" "Can I have some juice?" 1
Insert-QuestionOption $q6 "B" "I like bread." 2
Insert-QuestionOption $q6 "C" "Drink some milk." 3

Write-Host "三年级上册 Unit 5 导入完成！"

# =====================
# 三年级上册 Unit 6 Happy Birthday
# =====================
Write-Host "正在导入三年级上册 Unit 6 数据..."

$unit3_6 = Get-UnitId 3 "上" 6

Insert-Word $unit3_6 "one" "/wʌn/" "/wʌn/" "一" "num." "I have one book." "我有一本书。" 1
Insert-Word $unit3_6 "two" "/tuː/" "/tuː/" "二" "num." "I see two birds." "我看到两只鸟。" 2
Insert-Word $unit3_6 "three" "/θriː/" "/θriː/" "三" "num." "There are three apples." "有三个苹果。" 3
Insert-Word $unit3_6 "four" "/fɔː/" "/fɔːr/" "四" "num." "I have four pencils." "我有四支铅笔。" 4
Insert-Word $unit3_6 "five" "/faɪv/" "/faɪv/" "五" "num." "She has five fingers." "她有五个手指。" 5
Insert-Word $unit3_6 "six" "/sɪks/" "/sɪks/" "六" "num." "There are six days in a week." "一周有六天。" 6
Insert-Word $unit3_6 "seven" "/ˈsevn/" "/ˈsevn/" "七" "num." "I see seven stars." "我看到七颗星星。" 7
Insert-Word $unit3_6 "eight" "/eɪt/" "/eɪt/" "八" "num." "There are eight people." "有八个人。" 8
Insert-Word $unit3_6 "nine" "/naɪn/" "/naɪn/" "九" "num." "I have nine balls." "我有九个球。" 9
Insert-Word $unit3_6 "ten" "/ten/" "/ten/" "十" "num." "There are ten fingers." "有十个手指。" 10
Insert-Word $unit3_6 "cake" "/keɪk/" "/keɪk/" "蛋糕" "n." "Happy birthday! Lets eat cake." "生日快乐！我们吃蛋糕吧。" 11

$q7 = Insert-Question $unit3_6 "single_choice" 1 "3 + 4 = ? (用英语回答)" "C" "3 + 4 = 7，7 的英语是 seven" "数字计算" "numbers,math"
Insert-QuestionOption $q7 "A" "five" 1
Insert-QuestionOption $q7 "B" "six" 2
Insert-QuestionOption $q7 "C" "seven" 3

Write-Host "三年级上册 Unit 6 导入完成！"
Write-Host ""
Write-Host "========================================"
Write-Host "数据导入完成！"
Write-Host "========================================"

$connection.Close()
