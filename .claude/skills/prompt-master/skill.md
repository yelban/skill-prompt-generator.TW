---
name: prompt-master
description: 提示詞主控 - 智慧選擇合適的領域skill並生成提示詞，支援自動領域分類和排程
---

# ⚠️ 舊架構 - Prompt Master - 提示詞主控 Skill

> **注意**：這是舊架構系統，使用JSON檔案（facial_features_library.json）作為資料來源。
>
> **新架構**請使用：`intelligent-prompt-generator`（使用elements.db資料庫）

**版本**: 1.0
**建立日期**: 2026-01-01
**架構**: Master-Subordinate (主從結構)

---

## 📋 系統概述

這是一個智慧提示詞管理系統的主控 Skill，負責：
1. 理解使用者的自然語言意圖
2. 路由到對應的子模組
3. 整合子模組輸出並返回結果

---

## 🎯 核心功能

### 1. 意圖識別 (Intent Recognition)

自動識別使用者請求的5種意圖型別：

| 意圖型別 | 關鍵詞 | 示例請求 | 路由到 |
|---------|--------|----------|--------|
| **提取** (Extract) | 提取、分析、分類、識別 | "提取這個Prompt中的五官特徵" | extractor.md |
| **組裝** (Build) | 生成、組裝、建立、製作 | "生成一個電影級美少女的提示詞" | builder.md |
| **最佳化** (Optimize) | 最佳化、改進、增強、調整 | "最佳化這個提示詞" | optimizer.md |
| **推薦** (Recommend) | 推薦、建議、相似、匹配 | "推薦類似的提示詞" | recommender.md |
| **分析** (Analyze) | 分析、對比、評估、查詢 | "分析這兩個提示詞的區別" | analyzer.md |

### 2. 資料來源

系統使用以下JSON資料檔案：
- `facial_features_library.json` (v1.2) - 人像面部特徵庫（28個分類）
- `module_library.json` - 攝影流派與裝置索引
- `extracted_modules.json` - 18個源Prompts的提取結果

---

## 🤖 執行流程

### Step 1: 意圖識別

分析使用者輸入，識別意圖型別：

```python
# 虛擬碼示例
user_input = "生成一個電影級美少女的提示詞"

if any(keyword in user_input for keyword in ["生成", "組裝", "建立", "製作"]):
    intent = "build"
elif any(keyword in user_input for keyword in ["提取", "分析Prompt", "識別"]):
    intent = "extract"
elif any(keyword in user_input for keyword in ["最佳化", "改進", "增強"]):
    intent = "optimize"
elif any(keyword in user_input for keyword in ["推薦", "建議", "相似"]):
    intent = "recommend"
elif any(keyword in user_input for keyword in ["分析", "對比", "查詢"]):
    intent = "analyze"
else:
    # 預設：build（最常用）
    intent = "build"
```

### Step 2: 路由到子模組

根據意圖呼叫對應模組：

```python
# 虛擬碼示例
if intent == "build":
    # 呼叫 builder.md
    result = call_builder_module(user_input)
elif intent == "extract":
    # 呼叫 extractor.md
    result = call_extractor_module(user_input)
# ... 其他模組
```

### Step 3: 返回結果

整合子模組輸出，格式化返回給使用者。

---

## 📦 子模組說明

### 1. extractor.md - 提取模組
**功能**: 從使用者提供的Prompt中提取可複用的模組
**輸入**: 原始Prompt文字
**輸出**: 提取的模組分類（眼型、臉型、唇型等）

**示例**:
```
使用者: "提取這個Prompt的五官特徵: A beautiful young woman with large blue eyes..."
輸出:
  - 眼型: large blue expressive
  - 性別: female
  - 年齡: young_adult
```

### 2. builder.md - 組裝模組
**功能**: 根據使用者描述智慧組裝提示詞
**輸入**: 使用者的自然語言描述
**輸出**: 完整的提示詞

**示例**:
```
使用者: "生成一個電影級美少女的提示詞"
輸出: A beautiful East Asian young woman, large expressive almond eyes, ...
```

### 3. optimizer.md - 最佳化模組
**功能**: 最佳化使用者提供的提示詞
**輸入**: 原始提示詞
**輸出**: 最佳化後的提示詞 + 最佳化建議

**示例**:
```
使用者: "最佳化這個提示詞: A woman with eyes"
輸出: A beautiful young East Asian woman, large expressive almond eyes, ...
建議: 添加了年齡、人種、眼型細節
```

### 4. recommender.md - 推薦模組
**功能**: 推薦相似或相關的提示詞/模組
**輸入**: Prompt ID 或 描述
**輸出**: 推薦列表（帶相似度評分）

**示例**:
```
使用者: "推薦與Prompt #5相似的提示詞"
輸出:
  1. Prompt #18 (相似度: 85%) - 同為清純少女風格
  2. Prompt #10 (相似度: 75%) - 同為East Asian人像
```

### 5. analyzer.md - 分析模組
**功能**: 分析提示詞、對比、查詢資訊
**輸入**: Prompt ID 或 查詢條件
**輸出**: 詳細分析結果

**示例**:
```
使用者: "對比Prompt #5和#17的區別"
輸出:
  - Prompt #5: 清純少女，古典優雅
  - Prompt #17: 性感挑逗，叛逆風格
  差異: 表情、眼型、皮膚質感完全不同
```

---

## 🔧 實際執行邏輯

當你作為 Prompt Master Skill 被呼叫時，請按以下步驟執行：

### 1. 接收使用者輸入

從使用者訊息中提取關鍵資訊：
- 意圖型別（提取/組裝/最佳化/推薦/分析）
- 具體引數（Prompt ID、描述、查詢條件等）

### 2. 意圖識別

使用關鍵詞匹配識別使用者意圖：

**提取意圖**:
- 關鍵詞: "提取", "分析Prompt中的", "識別", "這個Prompt的"
- 示例: "提取Prompt #18的眼型"

**組裝意圖**:
- 關鍵詞: "生成", "建立", "組裝", "製作", "我想要"
- 示例: "生成一個清純少女的提示詞"

**最佳化意圖**:
- 關鍵詞: "最佳化", "改進", "增強", "調整", "修正"
- 示例: "最佳化這個提示詞"

**推薦意圖**:
- 關鍵詞: "推薦", "建議", "相似", "類似", "相關"
- 示例: "推薦相似的提示詞"

**分析意圖**:
- 關鍵詞: "分析", "對比", "查詢", "檢視", "詳細資訊"
- 示例: "分析Prompt #5的特點"

### 3. 呼叫子模組

**重要**: 你不能直接執行子模組的邏輯。你需要：

#### 選項A: 呼叫CLI工具（推薦）
使用 `prompt_tool.py` CLI工具：
```bash
# 組裝功能
python3 prompt_tool.py build "電影級美少女"
python3 prompt_tool.py generate  # 互動式生成

# 查詢功能
python3 prompt_tool.py show 5
python3 prompt_tool.py recommend 5
python3 prompt_tool.py compare 5 17

# 五官查詢
python3 prompt_tool.py facial --list-types
python3 prompt_tool.py facial --style "清純少女"
```

#### 選項B: 直接讀取JSON資料
當CLI工具無法滿足需求時，直接操作JSON資料：
```python
# 讀取資料檔案
facial_lib = load_json("extracted_results/facial_features_library.json")
module_lib = load_json("extracted_results/module_library.json")
prompts_data = load_json("extracted_results/extracted_modules.json")

# 根據意圖處理資料
# ...
```

### 4. 格式化輸出

將結果以清晰易讀的格式返回給使用者：
- 使用Markdown格式化
- 突出關鍵資訊
- 提供可操作的建議

---

## 📊 使用示例

### 示例1: 組裝提示詞

**使用者輸入**:
```
"我想生成一個電影級的清純美少女的提示詞"
```

**執行流程**:
1. 識別意圖: build（組裝）
2. 提取關鍵詞: "電影級" → cinematic_narrative, "清純美少女" → 清純少女
3. 呼叫CLI: `python3 prompt_tool.py build "電影級的清純美少女"`
4. 返回生成的完整提示詞

**輸出**:
```
✨ 已生成提示詞:

A beautiful East Asian young woman, large expressive almond eyes, thick natural lashes, deep clear iris, dewy sparkle, soft highlights, oval face, delicate refined Asian facial structure, soft full lips, gentle pink gloss, small straight delicate nose, flawless porcelain skin, radiant jade-like brightness, natural subtle blush, dewy luminous glow, innocent gaze, gentle smile, soft introspective, photographed with canon_eos_r5, 35mm f/2.8, 8K HDR, cinematic lighting, photorealistic, ultra-detailed

📋 組合詳情:
- 流派: 電影敘事攝影
- 風格: 清純少女
- 人種: 東亞人
- 年齡: 青年（18-25歲）
- 性別: 女性
```

### 示例2: 推薦相似提示詞

**使用者輸入**:
```
"推薦與Prompt #5相似的提示詞"
```

**執行流程**:
1. 識別意圖: recommend（推薦）
2. 提取Prompt ID: 5
3. 呼叫CLI: `python3 prompt_tool.py recommend 5`
4. 返回推薦列表

**輸出**:
```
🔍 為 Prompt #5 (清純少女古典美) 推薦相關提示詞

[1] #18 清純公主Cosplay
    相似度: 75%
    理由: 同為清純少女風格 + 同用東亞人種

[2] #10 溫柔少女人像
    相似度: 65%
    理由: 同為人像美容攝影 + 主題相關

[3] #17 性感朋克少女
    相似度: 45%
    理由: 同為年輕女性人像（風格差異大）
```

### 示例3: 查詢五官組合

**使用者輸入**:
```
"清純少女風格應該用什麼五官組合？"
```

**執行流程**:
1. 識別意圖: analyze（分析/查詢）
2. 識別風格: "清純少女"
3. 呼叫CLI: `python3 prompt_tool.py facial --style "清純少女"`
4. 返回五官組合推薦

**輸出**:
```
🎨 風格: 清純少女

推薦五官組合:

性別: 女性 (female)
年齡: 青年（18-25歲） (young_adult)
人種: 東亞人 (east_asian)
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

---

## 🎯 最佳實踐

### 1. 優先使用CLI工具
- ✅ CLI工具已經過測試，穩定可靠
- ✅ 輸出格式統一，易於理解
- ✅ 包含彩色輸出，體驗更好

### 2. 清晰的輸出格式
- 使用Markdown格式化
- 使用emoji增強可讀性
- 突出顯示關鍵資訊

### 3. 智慧路由
- 當用戶意圖不明確時，提供選項讓使用者選擇
- 對於複雜請求，可能需要呼叫多個子模組

### 4. 錯誤處理
- 當JSON檔案不存在時，提示使用者
- 當Prompt ID不存在時，列出可用ID
- 當關鍵詞無法匹配時，提供建議

---

## 📚 資料檔案路徑

```
/Users/huangzongning/prompt_gen_image/
├── extracted_results/
│   ├── facial_features_library.json (v1.2, 28分類)
│   ├── module_library.json (10攝影流派)
│   └── extracted_modules.json (18 Prompts)
├── prompt_tool.py (CLI工具)
└── demo_generate.py (演示指令碼)
```

---

## 🔍 執行指令

當用戶呼叫這個Skill時，請：

1. **分析使用者意圖**
   - 仔細閱讀使用者輸入
   - 識別關鍵詞和引數

2. **選擇執行方式**
   - 優先使用CLI工具（Bash呼叫 prompt_tool.py）
   - 必要時直接讀取JSON資料（Read tool）

3. **執行並返回**
   - 格式化輸出結果
   - 提供可操作的後續建議

4. **主動最佳化**
   - 如果使用者提供的資訊不完整，主動最佳化或詢問
   - 提供改進建議

---

**Skill狀態**: ✅ 可用
**支援的操作**: 提取、組裝、最佳化、推薦、分析
**資料版本**: facial_features_library v1.2
**總分類數**: 28個（9大類）
