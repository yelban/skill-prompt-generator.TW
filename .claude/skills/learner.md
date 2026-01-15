# Learner Skill - 自學習技能

**功能**: 自動學習新Prompt中的未定義特徵，擴充套件特徵庫
**型別**: 獨立Skill
**實現**: 混合學習系統（規則+AI+人工稽核）

---

## 🎯 核心功能

本Skill提供以下能力：

1. **掃描單個Prompt** - 分析新Prompt，識別未定義的特徵
2. **批次掃描** - 掃描所有18個Prompts，發現缺失維度
3. **生成稽核報告** - 自動生成待稽核的新特徵列表
4. **自動更新庫** - 稽核通過後自動更新 facial_features_library.json

---

## 📋 使用方式

### 方式1: 自然語言呼叫（推薦）

直接描述你的需求，系統會自動理解：

```
示例1: "學習這個Prompt的新特徵: A woman with long flowing red hair, fair skin..."
示例2: "掃描所有Prompts，發現缺失的特徵維度"
示例3: "分析這個Prompt有什麼新的髮型或膚色"
```

### 方式2: 直接呼叫CLI

如果需要精確控制，可直接使用命令列：

```bash
# 掃描單個Prompt
python3 learner.py scan "A woman with long red hair, fair skin, wearing qipao"

# 批次掃描所有Prompts
python3 learner.py batch
```

---

## 🔧 工作原理

### 混合學習流程

```
新Prompt輸入
    ↓
規則提取（Rule-Based）
  - 使用正則表示式匹配常見模式
  - 快速識別：髮型、髮色、膚色、服裝、配飾等
    ↓
AI增強（AI-Assisted）
  - 呼叫LLM驗證規則提取的準確性
  - 發現規則未覆蓋的新維度
    ↓
特徵合併與去重
  - 合併兩種方法的結果
  - 計算置信度
    ↓
匹配現有庫
  - 檢查是否已在 facial_features_library.json 中
  - 計算關鍵詞重疊度（>70%視為已存在）
    ↓
生成稽核報告
  - 列出所有新發現的特徵
  - 提供建議分類碼
  - 評估複用性
    ↓
人工稽核
  - 使用者決定：批准/修改/拒絕
    ↓
自動更新庫
  - 批准後自動新增到 facial_features_library.json
  - 更新版本號
  - 生成changelog
```

---

## 🎯 使用場景

### 場景1: 發現新Prompt的特殊特徵

**使用者請求**:
```
"這個Prompt有什麼新特徵？
'A woman with long flowing red hair, fair porcelain skin, wearing elegant red silk qipao dress, delicate silver earrings'"
```

**系統執行**:
1. 呼叫 `python3 learner.py scan "<prompt>"`
2. 規則提取識別到：
   - hair_style: "long flowing" (長髮飄逸)
   - hair_color: "red" (紅色)
   - skin_tone: "fair porcelain" (白皙瓷肌)
   - clothing: "elegant red silk qipao dress" (優雅紅色絲綢旗袍)
   - accessories: "delicate silver earrings" (精緻銀色耳環)
3. 匹配現有庫：發現 hair_style, hair_color, clothing, accessories 都是新類別
4. 生成稽核報告

**輸出**:
```
🔍 掃描Prompt中...
   文字長度: 150 字元

✅ 掃描完成！
   發現特徵: 5 個
   新特徵: 5 個
   已存在: 0 個

📋 新發現的特徵類別:
   - hair_style: 1 個
   - hair_color: 1 個
   - skin_tone: 1 個
   - clothing: 1 個
   - accessories: 1 個

📄 稽核報告已生成: extracted_results/new_features_review_20260101_120000.md
```

---

### 場景2: 批次掃描所有Prompts

**使用者請求**:
```
"掃描所有18個Prompts，發現缺失的特徵維度"
```

**系統執行**:
1. 呼叫 `python3 learner.py batch`
2. 逐個掃描 extracted_modules.json 中的所有Prompts
3. 統計所有新特徵
4. 生成彙總報告

**輸出**:
```
📚 批次掃描模式
   讀取檔案: extracted_results/extracted_modules.json
   共 18 個Prompts

[1/18] 掃描 Prompt #1...
[2/18] 掃描 Prompt #2...
...
[18/18] 掃描 Prompt #18...

============================================================
📊 批次掃描完成！
============================================================

發現新類別:

hair_style: 8 個新分類
   - long straight black (Prompt #5)
   - twin tails blue (Prompt #18)
   - short spiky (Prompt #17)
   ... 還有 5 個

hair_color: 6 個新分類
   - natural black (Prompt #5, #18)
   - vibrant blue (Prompt #18)
   - purple pink gradient (Prompt #17)
   ... 還有 3 個

skin_tone: 3 個新分類
   - fair pale (Prompt #5, #18)
   - porcelain (Prompt #10)
   - medium tan (Prompt #8)

clothing: 5 個新分類
   - traditional chinese qipao (Prompt #18)
   - punk street style (Prompt #17)
   ... 還有 3 個

📄 彙總報告: extracted_results/batch_scan_summary_20260101_120000.md
```

---

### 場景3: 稽核新特徵

生成的稽核報告示例：

```markdown
# 新特徵發現報告

**掃描時間**: 2026-01-01 12:00:00
**掃描來源**: 使用者輸入

## 源Prompt
A woman with long flowing red hair, fair porcelain skin, wearing elegant red silk qipao dress

## 新發現的特徵 (4個)

### 1. hair_style - NEW_CATEGORY
**關鍵詞**: "long flowing red hair"
**置信度**: 80%
**提取方法**: rule-based
**建議分類碼**: `long_flowing_red_hair`
**複用性評估**: 高（這是人像的重要基礎元素）

**稽核選項**:
- [ ] 批准新增
- [ ] 需要修改（請說明）
- [ ] 拒絕（說明原因）

### 2. hair_color - NEW_CATEGORY
**關鍵詞**: "red hair"
**置信度**: 80%
**提取方法**: rule-based
**建議分類碼**: `red_hair`
**複用性評估**: 高（這是人像的重要基礎元素）

**稽核選項**:
- [ ] 批准新增
- [ ] 需要修改（請說明）
- [ ] 拒絕（說明原因）

...
```

---

## 📊 可檢測的特徵維度

### 高優先順序（已實現）

| 維度 | 示例 | 正則表示式 |
|------|------|-----------|
| **hair_style** | long flowing, short curly, twin tails | `(long\|short)?\s*(straight\|curly)?\s*hair` |
| **hair_color** | black, blonde, red, blue | `(black\|blonde\|red)?\s+hair` |
| **skin_tone** | fair, tan, olive, dark | `(fair\|tan\|olive)\s+skin` |
| **body_type** | slim, athletic, curvy | `(slim\|athletic)\s+body` |
| **clothing** | qipao dress, punk outfit | `wearing\s+(elegant)?\s*(qipao\|dress)` |
| **accessories** | silver earrings, necklace | `(silver\|gold)\s+(earrings\|necklace)` |
| **pose** | confident pose, standing | `(confident)?\s+pose` |

### 中優先順序（待擴充套件）

- **makeup**: 妝容風格（自然、濃妝、哥特）
- **facial_hair**: 鬍鬚（對男性人像）
- **tattoos**: 紋身
- **background**: 背景環境

### 低優先順序（未來考慮）

- **lighting_mood**: 光照情緒
- **color_palette**: 色彩基調
- **artistic_style**: 藝術風格

---

## 🔍 意圖識別

本Skill會自動識別以下意圖關鍵詞：

| 關鍵詞 | 意圖 | 執行操作 |
|--------|------|---------|
| 學習、提取、分析、識別 | 掃描單個Prompt | `learner.py scan` |
| 批次、所有、全部、掃描 | 批次掃描 | `learner.py batch` |
| 發現、缺失、新的 | 發現新特徵 | 自動判斷單個/批次 |

**示例**:

```
使用者: "學習這個Prompt的特徵"
→ 識別為：掃描單個
→ 執行：learner.py scan "<prompt>"

使用者: "掃描所有Prompts發現新維度"
→ 識別為：批次掃描
→ 執行：learner.py batch
```

---

## ⚙️ 配置和引數

### 置信度閾值

```python
# learner.py 中的配置
CONFIDENCE_THRESHOLD = 0.7  # 70%以上才建議新增
OVERLAP_THRESHOLD = 0.7     # 關鍵詞重疊度>70%視為已存在
```

### 檔案路徑

```python
# 特徵庫路徑
LIBRARY_PATH = "extracted_results/facial_features_library.json"

# Prompts資料路徑
PROMPTS_PATH = "extracted_results/extracted_modules.json"

# 稽核報告輸出路徑
REPORT_OUTPUT_DIR = "extracted_results/"
```

---

## 📁 輸出檔案

### 1. 單次掃描稽核報告

**檔名**: `new_features_review_YYYYMMDD_HHMMSS.md`

**位置**: `extracted_results/`

**內容**:
- 源Prompt
- 新發現的特徵列表
- 每個特徵的詳細資訊
- 稽核選項（批准/修改/拒絕）

### 2. 批次掃描彙總報告

**檔名**: `batch_scan_summary_YYYYMMDD_HHMMSS.md`

**位置**: `extracted_results/`

**內容**:
- 掃描統計資訊
- 按類別分組的新特徵
- 每個特徵關聯的Prompt ID
- 置信度評分

---

## 🎓 技術實現細節

### 規則提取示例

```python
# hair_style 提取
regex = r"(long|short|medium)?\s*(straight|curly|wavy)?\s*(black|blonde|red)?\s*(hair|ponytail)"

# 匹配示例
"long flowing black hair" → ("long", "flowing", "black", "hair")
"short curly blonde hair" → ("short", "curly", "blonde", "hair")
"twin tails" → ("", "", "", "twin tails")
```

### 關鍵詞重疊度計算

```python
def calculate_overlap(keywords1, keywords2):
    set1 = set([k.lower() for k in keywords1])
    set2 = set([k.lower() for k in keywords2])

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    return intersection / union  # Jaccard相似度
```

**示例**:
```
keywords1 = ["long flowing hair", "black hair"]
keywords2 = ["long straight hair", "black locks"]

重疊詞: "long", "black", "hair" (3個)
總詞彙: 6個
重疊度: 3/6 = 50%
```

---

## ⚠️ 注意事項

### 1. AI輔助功能需要LLM API

當前實現中，AI輔助提取功能返回空列表，需要整合真實的LLM API（Claude、GPT-4等）。

**整合方法**:
```python
# learner.py 中的 AIAssistedLearner.extract_features()
# 需要呼叫實際的LLM API
response = anthropic_client.messages.create(
    model="claude-sonnet-4-5-20250929",
    system=self.system_prompt,
    messages=[{"role": "user", "content": prompt_text}]
)
```

### 2. 人工稽核是必須的

自動檢測可能存在：
- ❌ 誤識別（false positive）
- ❌ 遺漏（false negative）
- ❌ 分類碼不夠準確

**解決方案**:
- ✅ 始終需要人工稽核
- ✅ 只有置信度>70%的才建議
- ✅ 多次出現的特徵優先順序更高

### 3. 避免過度細分

不要為每個細微差別建立分類：

```
✅ 好: long_straight (通用)
❌ 差: long_straight_waist_length_black_shiny (過細)

建議:
- 髮型: long_straight
- 髮色: black (單獨分類)
- 長度: 用描述詞表達，不單獨分類
```

---

## 🚀 未來擴充套件

### 短期（1周內）

1. **整合真實LLM API**
   - 使用Claude API進行智慧提取
   - 提高識別準確度

2. **最佳化正則表示式**
   - 新增更多匹配模式
   - 支援中文關鍵詞

### 中期（1個月）

3. **Web稽核介面**
   - 視覺化稽核流程
   - 一鍵批准/拒絕
   - 批次操作

4. **自動庫更新**
   - 稽核通過後自動更新JSON
   - 生成changelog
   - 版本控制

### 長期（3個月）

5. **智慧推薦**
   - 基於使用頻率推薦
   - 自動組合建議
   - 風格一致性檢查

6. **多語言支援**
   - 中英文混合Prompt
   - 自動翻譯分類名

---

## 📖 使用示例

### 完整工作流程

```
1. 使用者發現新Prompt
   "我有一個新Prompt: A woman with long red hair, fair skin..."

2. 呼叫Learner Skill
   "學習這個Prompt的新特徵"

3. 系統自動執行
   → 規則提取
   → 匹配現有庫
   → 生成稽核報告

4. 使用者檢視報告
   → 開啟 new_features_review_*.md
   → 檢視新發現的特徵

5. 人工稽核
   → 批准: hair_style (long_flowing_red)
   → 批准: hair_color (red)
   → 批准: skin_tone (fair_pale)

6. 手動更新庫
   → 將批准的特徵新增到 facial_features_library.json
   → 更新版本號至 v1.3

7. 驗證
   → 重新執行生成工具
   → 檢查新特徵是否可用
```

---

**Skill狀態**: ✅ 可用
**實現方式**: 混合學習（規則+AI+人工稽核）
**CLI工具**: `learner.py`
**輸出**: Markdown稽核報告
**下一步**: 整合LLM API，建立Web稽核介面
