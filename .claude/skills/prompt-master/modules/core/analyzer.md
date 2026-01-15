# ⚠️ 舊架構 - Analyzer Module - 分析查詢模組

> **注意**：這是舊架構模組，屬於prompt-master系統


**功能**: 分析、查詢、對比提示詞和模組資訊
**呼叫方式**: 透過主Skill路由或直接CLI呼叫

---

## 📋 功能概述

Analyzer模組提供以下分析功能：
- 檢視Prompt詳細資訊
- 對比兩個Prompts的差異
- 查詢五官模組資訊
- 查詢流派和裝置資訊

---

## 🔧 CLI命令

### 1. 檢視Prompt詳細資訊

**命令**:
```bash
python3 prompt_tool.py show <id>
```

**示例**:
```bash
python3 prompt_tool.py show 5
```

**輸出**:
```
📸 Prompt #5: 清純少女古典美

基本資訊:
  主題: 清純少女 / 古典優雅 / 自然光人像
  長度: 892 字元
  評分: 10.0/10

攝影流派:
  人像美容攝影 (置信度: 95%)

技術引數:
  相機: Canon EOS R5
  鏡頭: RF 50mm f/1.2L
  解析度: 8K

對立標準:
  aesthetic:
    ✓ 必須: flawless porcelain skin, soft classical contour
    ✗ 禁止: modern edgy makeup, harsh contours
```

### 2. 對比兩個Prompts

**命令**:
```bash
python3 prompt_tool.py compare <id1> <id2>
```

**示例**:
```bash
python3 prompt_tool.py compare 5 17
```

**輸出**:
```
⚖️  對比: #5 vs #17

屬性         Prompt #5                  Prompt #17
=======================================================
標題         清純少女古典美             性感朋克Jinx
評分         10.0/10                    9.8/10
流派         人像美容攝影               膠片藝術攝影
相機         Canon EOS R5               Hasselblad 503CX
解析度       8K                         medium format
```

### 3. 查詢五官型別列表

**命令**:
```bash
python3 prompt_tool.py facial --list-types
```

**輸出**:
```
📊 五官特徵分類庫

眼型 (4種):
  large_expressive_almond    大眼杏仁眼      (9.8/10) Prompts: [5]
  large_blue_expressive      大藍眼（真人化）(8.5/10) Prompts: [18]
  half_lidded_seductive      半閉誘惑眼      (8.0/10) Prompts: [17]
  anime_hybrid_green         動漫混合綠眼    (8.5/10) Prompts: [11]

臉型 (2種):
  oval_asian_refined         精緻鵝蛋臉（亞洲）(10.0/10) Prompts: [17, 18]
  classical_soft_contour     柔和古典臉型      (9.5/10)  Prompts: [5]

... (其他類別)
```

### 4. 查詢特定五官型別

**命令**:
```bash
python3 prompt_tool.py facial --eye-type <型別>
python3 prompt_tool.py facial --skin-texture <型別>
python3 prompt_tool.py facial --expression <型別>
```

**示例**:
```bash
python3 prompt_tool.py facial --eye-type almond
```

**輸出**:
```
🔍 五官特徵: 大眼杏仁眼

視覺特徵:
  • size: 大而富有表現力 (large and expressive)
  • shape: 杏仁形 (almond-shaped)
  • eyelashes: 濃密修長的自然睫毛 (thick long natural lashes)

提示詞關鍵詞:
  • large expressive eyes
  • almond eyes
  • thick natural lashes
  • deep clear iris
  • dewy sparkle

適合風格:
  • 清純少女
  • 鄰家小妹
  • 古典溫柔
  • 現代商業人像

使用該特徵的Prompts (1個):
  #5   清純少女古典美                      10.0/10

使用建議:
  • best_for: 萬能眼型，適合清純、優雅、古典風格
  • pair_with: 搭配 'innocent', 'gentle', 'youthful' 強化純淨感
  • lighting: 黃金時刻柔和光 (golden hour soft light) 最佳
```

### 5. 按風格推薦五官組合

**命令**:
```bash
python3 prompt_tool.py facial --style <風格>
```

**示例**:
```bash
python3 prompt_tool.py facial --style "清純少女"
```

**輸出**:
```
🎨 風格: 清純少女

推薦五官組合:

性別: 女性 (female)
年齡: 青年（18-25歲） (young_adult) [10.0/10]
人種: 東亞人 (east_asian) [10.0/10]
  關鍵詞: East Asian, Asian features

眼型: 大眼杏仁眼 (large_expressive_almond) [9.8/10]
  關鍵詞: large expressive eyes, almond eyes, thick natural lashes

唇型: 粉嫩光澤唇 (soft_pink_gloss) [9.0/10]
  關鍵詞: soft full lips, gentle pink gloss, natural lip color

鼻型: 小巧直鼻 (small_straight_delicate) [9.0/10]
  關鍵詞: small straight nose, delicate nose

皮膚: 瓷肌無瑕（發光質感） (porcelain_flawless_radiant) [9.5/10]
  關鍵詞: flawless porcelain skin, radiant jade-like brightness

表情: 清純溫柔眼神 (innocent_gentle_gaze) [9.5/10]
  關鍵詞: innocent gaze, gentle smile, soft introspective
```

### 6. 按流派搜尋

**命令**:
```bash
python3 prompt_tool.py search --genre <流派>
```

**示例**:
```bash
python3 prompt_tool.py search --genre cinematic_narrative
```

**輸出**:
```
🔍 流派: 電影敘事攝影

流派特徵:
  • 8K HDR超高畫質數碼攝影
  • 電影級實景拍攝
  • 自然敘事性光照
  • 真人化角色演繹

典型裝置:
  • Canon EOS R5
  • RF 35mm f/2.8 macro IS STM

應用場景:
  • 真人化角色攝影
  • 電影級概念藝術
  • 遊戲IP真人化

相關提示詞 (2個):
  #18  Princess Peach真人化                    9.8/10
  #11  Saber真人化                             9.5/10
```

### 7. 按裝置搜尋

**命令**:
```bash
python3 prompt_tool.py search --equipment <裝置>
```

**示例**:
```bash
python3 prompt_tool.py search --equipment R5
```

---

## 🎯 使用場景

### 場景1: 學習優秀Prompt

```
使用者: "我想學習Prompt #5的細節"
→ 呼叫: python3 prompt_tool.py show 5
→ 檢視完整技術引數、對立標準、獨特特徵
```

### 場景2: 對比兩種風格

```
使用者: "清純和性感風格有什麼區別？"
→ 呼叫: python3 prompt_tool.py compare 5 17
→ 對比表格一目瞭然
```

### 場景3: 查詢五官庫

```
使用者: "有哪些眼型可選？"
→ 呼叫: python3 prompt_tool.py facial --list-types
→ 檢視所有6大類五官分類
```

### 場景4: 學習風格搭配

```
使用者: "古典優雅風格應該用什麼五官？"
→ 呼叫: python3 prompt_tool.py facial --style "古典優雅"
→ 獲取完整五官組合推薦
```

---

## 📁 資料依賴

```
facial_features_library.json (v1.2)
├── 9大類別、28個分類
└── usage_index.by_style_mood (4種風格)

module_library.json
├── photography_genres (10流派)
└── camera_equipment_index (裝置庫)

extracted_modules.json
└── 18個源Prompts的完整資料
```

---

**模組狀態**: ✅ 可用
**CLI命令**: `show`, `compare`, `search`, `facial`
**支援查詢**: Prompt、流派、裝置、五官、風格
