# ⚠️ 舊架構 - Learner Module - 自學習模組

> **注意**：這是舊架構模組，屬於prompt-master系統


**功能**: 從新Prompt中自動學習和提取未定義的特徵模組
**呼叫方式**: 透過主Skill路由或獨立執行

---

## 📋 功能概述

Learner模組負責：
1. **自動識別**新的特徵維度（髮型、髮色、膚色等）
2. **智慧提取**特徵關鍵詞和描述
3. **自動分類**新特徵到合適的類別
4. **生成建議**供人工稽核和新增
5. **增量學習**持續擴充套件分類庫

---

## 🎯 解決的問題

### 當前缺失的模組

| 類別 | 當前狀態 | 缺失的維度 | 重要性 |
|------|---------|-----------|--------|
| **人物基礎** | ✅ 性別、年齡、人種 | ❌ 膚色、身材、身高 | 高 |
| **頭髮** | ❌ 無 | ❌ 髮型、髮色、髮質 | 高 |
| **五官** | ✅ 眼/臉/唇/鼻/膚/情 | ❌ 眉毛、耳朵 | 中 |
| **妝容** | ❌ 無 | ❌ 妝容風格、口紅色號 | 中 |
| **服裝** | ❌ 無 | ❌ 服裝風格、顏色、材質 | 高 |
| **配飾** | ❌ 無 | ❌ 耳環、項鍊、眼鏡 | 低 |
| **姿勢** | ❌ 無 | ❌ 站姿、坐姿、動作 | 中 |
| **視角** | ❌ 無 | ❌ 特寫、全身、側面 | 中 |

---

## 🤖 自學習流程

### Step 1: 掃描新Prompt

**輸入**: 使用者提供的新Prompt文字

**示例**:
```
A beautiful young Asian woman with long flowing black hair, fair skin tone, wearing elegant traditional Chinese qipao dress in red silk, delicate silver earrings, confident pose, full body shot, photographed with Canon EOS R5
```

### Step 2: 分詞和特徵提取

**使用NLP技術**:
1. 分詞（tokenization）
2. 詞性標註（POS tagging）
3. 命名實體識別（NER）
4. 依存關係分析

**提取結果**:
```json
{
  "detected_features": [
    {
      "category": "hair",
      "keywords": ["long flowing black hair"],
      "attributes": {
        "length": "long",
        "style": "flowing",
        "color": "black"
      }
    },
    {
      "category": "skin",
      "keywords": ["fair skin tone"],
      "attributes": {
        "tone": "fair"
      }
    },
    {
      "category": "clothing",
      "keywords": ["traditional Chinese qipao dress", "red silk"],
      "attributes": {
        "style": "traditional Chinese",
        "type": "qipao dress",
        "color": "red",
        "material": "silk"
      }
    },
    {
      "category": "accessories",
      "keywords": ["delicate silver earrings"],
      "attributes": {
        "type": "earrings",
        "material": "silver",
        "style": "delicate"
      }
    },
    {
      "category": "pose",
      "keywords": ["confident pose", "full body shot"],
      "attributes": {
        "posture": "confident",
        "view": "full body"
      }
    }
  ]
}
```

### Step 3: 匹配現有分類

**檢查每個特徵是否已存在**:
```python
def check_existing_category(feature):
    """檢查特徵是否已在庫中"""

    # 讀取現有庫
    facial_lib = load_json("facial_features_library.json")

    category = feature["category"]
    keywords = feature["keywords"]

    # 檢查類別是否存在
    if category not in facial_lib:
        return "NEW_CATEGORY"

    # 檢查關鍵詞是否已存在
    existing_items = facial_lib[category]
    for item_code, item_data in existing_items.items():
        item_keywords = item_data.get("keywords", [])
        # 關鍵詞重疊度檢查
        overlap = calculate_keyword_overlap(keywords, item_keywords)
        if overlap > 0.7:  # 70%以上重疊
            return "EXISTS", item_code

    return "NEW_ITEM"
```

### Step 4: 生成新分類建議

**對於新發現的特徵**:

#### 4.1 新類別（如 hair）

**生成模板**:
```json
{
  "hair_styles": {
    "long_flowing_black": {
      "chinese_name": "長髮飄逸（黑色）",
      "classification_code": "long_flowing_black",
      "visual_features": {
        "length": "long (shoulder length or longer)",
        "style": "flowing, natural movement",
        "color": "black (natural Asian hair color)",
        "texture": "straight, silky"
      },
      "keywords": [
        "long flowing black hair",
        "silky straight hair",
        "natural black hair"
      ],
      "suitable_styles": [
        "古典優雅",
        "現代時尚",
        "真人化Cosplay"
      ],
      "prompts_using_this": [],  // 將被自動填充
      "reusability_score": 0,     // 待評估
      "usage_recommendations": {
        "best_for": "需要展示頭髮細節的人像",
        "pair_with": "搭配柔和光照展現髮質",
        "lighting": "backlight or soft window light"
      },
      "auto_detected": true,       // 標記為自動檢測
      "needs_review": true,         // 需要人工稽核
      "detection_confidence": 0.85  // 檢測置信度
    }
  }
}
```

#### 4.2 新子分類（在現有類別下）

**示例**: 在 skin_textures 下新增 skin_tone

```json
{
  "skin_textures": {
    // ... 現有的4種皮膚質感

    "fair_skin_tone": {
      "chinese_name": "白皙膚色",
      "classification_code": "fair_skin_tone",
      "visual_features": {
        "tone": "fair, light",
        "undertone": "cool or neutral",
        "characteristics": "pale complexion, minimal melanin"
      },
      "keywords": [
        "fair skin",
        "pale skin",
        "light skin tone",
        "porcelain complexion"
      ],
      "suitable_styles": [
        "所有風格"
      ],
      "prompts_using_this": [],
      "reusability_score": 0,
      "auto_detected": true,
      "needs_review": true,
      "detection_confidence": 0.90
    }
  }
}
```

### Step 5: 人工稽核流程

**生成稽核報告**:
```markdown
# 新特徵發現報告

## 掃描來源
- Prompt來源: 使用者輸入 / Prompt #XX
- 掃描時間: 2026-01-01 12:00:00

## 新發現的特徵 (5個)

### 1. 髮型 (hair_styles) - 新類別 ⭐
**關鍵詞**: "long flowing black hair"
**建議分類碼**: long_flowing_black
**置信度**: 85%
**複用性評估**: 高（髮型是人像的重要元素）

**稽核選項**:
- [ ] 批准新增
- [ ] 需要修改（請說明）
- [ ] 拒絕（說明原因）

### 2. 膚色 (skin_tone) - 新子類別
**關鍵詞**: "fair skin tone"
**建議分類碼**: fair_skin_tone
**置信度**: 90%
**建議**: 新增到 skin_textures 類別

**稽核選項**:
- [ ] 批准新增
- [ ] 需要修改
- [ ] 拒絕

### 3. 服裝 (clothing_style) - 新類別 ⭐
**關鍵詞**: "traditional Chinese qipao dress", "red silk"
**建議分類碼**: traditional_chinese_qipao
**置信度**: 92%
**複用性評估**: 中（特定於文化主題）

**稽核選項**:
- [ ] 批准新增
- [ ] 需要修改
- [ ] 拒絕

... (其他特徵)
```

### Step 6: 自動更新分類庫

**稽核通過後**:
1. 自動新增到 `facial_features_library.json`
2. 更新 `library_metadata`
3. 關聯到源Prompt
4. 生成changelog

---

## 🔧 實現技術

### 方案1: 規則基礎（初級版）

**優點**: 簡單、可控、快速實現
**缺點**: 需要手動定義規則

**實現**:
```python
class RuleBasedLearner:
    """基於規則的特徵學習器"""

    def __init__(self):
        self.patterns = {
            "hair": {
                "keywords": ["hair", "hairstyle", "hairdo"],
                "attributes": ["long", "short", "curly", "straight", "black", "blonde"],
                "regex": r"(long|short|curly|straight)\s+(flowing|silky)?\s*(black|blonde|brown|red)?\s+hair"
            },
            "skin_tone": {
                "keywords": ["skin tone", "complexion", "skin color"],
                "attributes": ["fair", "pale", "tan", "olive", "dark"],
                "regex": r"(fair|pale|tan|olive|dark)\s+skin(\s+tone)?"
            },
            "clothing": {
                "keywords": ["dress", "outfit", "wearing", "clothes"],
                "attributes": ["traditional", "modern", "casual", "formal"],
                "regex": r"wearing\s+(elegant|traditional|modern)?\s*(\w+)\s+(dress|outfit)"
            }
        }

    def extract_features(self, prompt_text):
        """提取特徵"""
        detected = []

        for category, pattern_info in self.patterns.items():
            # 正則匹配
            matches = re.findall(pattern_info["regex"], prompt_text, re.IGNORECASE)

            if matches:
                detected.append({
                    "category": category,
                    "raw_text": matches[0],
                    "confidence": 0.8
                })

        return detected
```

### 方案2: AI輔助（高階版）

**優點**: 智慧、靈活、可發現未知維度
**缺點**: 需要LLM API、成本較高

**實現**:
```python
class AIAssistedLearner:
    """AI輔助的特徵學習器"""

    def extract_features(self, prompt_text):
        """使用LLM提取特徵"""

        system_prompt = """
        你是一個提示詞分析專家。請從以下Prompt中提取所有人物特徵，
        並按類別組織。對於每個特徵，提供：
        1. 類別（如 hair, skin_tone, clothing等）
        2. 關鍵詞
        3. 屬性（如長度、顏色、風格等）

        返回JSON格式。
        """

        user_prompt = f"Prompt: {prompt_text}"

        # 呼叫LLM（如Claude、GPT-4）
        response = call_llm_api(system_prompt, user_prompt)

        # 解析返回的JSON
        features = json.loads(response)

        return features
```

### 方案3: 混合模式（推薦）

**結合兩者優勢**:
1. **規則提取**: 快速識別常見特徵
2. **AI驗證**: 檢查提取準確性
3. **AI發現**: 識別未定義的新維度
4. **人工稽核**: 最終確認

**工作流程**:
```python
def hybrid_learning_pipeline(prompt_text):
    """混合學習流程"""

    # Step 1: 規則提取
    rule_learner = RuleBasedLearner()
    rule_features = rule_learner.extract_features(prompt_text)

    # Step 2: AI增強提取
    ai_learner = AIAssistedLearner()
    ai_features = ai_learner.extract_features(prompt_text)

    # Step 3: 合併和去重
    merged_features = merge_features(rule_features, ai_features)

    # Step 4: 匹配現有庫
    new_features = []
    for feature in merged_features:
        status = check_existing_category(feature)
        if status in ["NEW_CATEGORY", "NEW_ITEM"]:
            new_features.append(feature)

    # Step 5: 生成稽核報告
    if new_features:
        report = generate_review_report(new_features)
        save_report(report)

    return new_features
```

---

## 📊 優先順序建議

### 高優先順序（立即新增）

**1. 髮型 (hair_styles)**
```json
{
  "hair_styles": {
    "long_straight_black": "長直黑髮",
    "long_curly_brown": "長卷棕發",
    "short_bob_blonde": "短髮波波頭（金色）",
    "ponytail_high": "高馬尾",
    "twin_tails": "雙馬尾"
  }
}
```

**2. 髮色 (hair_colors)**
```json
{
  "hair_colors": {
    "natural_black": "自然黑色",
    "dark_brown": "深棕色",
    "blonde": "金色",
    "red_auburn": "紅棕色",
    "silver_gray": "銀灰色（染髮）"
  }
}
```

**3. 膚色 (skin_tones)**
```json
{
  "skin_tones": {
    "fair_pale": "白皙",
    "medium_tan": "小麥色",
    "olive": "橄欖色",
    "dark_rich": "深色"
  }
}
```

### 中優先順序（逐步新增）

**4. 身材 (body_types)**
```json
{
  "body_types": {
    "slim_petite": "纖細嬌小",
    "athletic_fit": "運動健美",
    "curvy_voluptuous": "曲線豐滿",
    "average_balanced": "勻稱標準"
  }
}
```

**5. 服裝風格 (clothing_styles)**
```json
{
  "clothing_styles": {
    "traditional_chinese": "中式傳統",
    "modern_casual": "現代休閒",
    "formal_business": "正式商務",
    "cosplay_character": "角色扮演"
  }
}
```

### 低優先順序（按需新增）

**6. 配飾 (accessories)**
**7. 妝容 (makeup_styles)**
**8. 姿勢 (poses)**

---

## 🎯 使用場景

### 場景1: 掃描新Prompt發現特徵

**使用者操作**:
```
"學習這個Prompt的新特徵: A woman with long flowing red hair..."
```

**執行流程**:
1. 呼叫 `learner.md`
2. 提取特徵: 髮型(long flowing), 髮色(red)
3. 檢查庫: 未找到對應分類
4. 生成建議: 新增 hair_styles.long_flowing_red
5. 輸出稽核報告

**輸出**:
```
發現新特徵:
- 髮型: long_flowing_red (長髮飄逸-紅色)
- 置信度: 88%
- 建議: 新增到hair_styles類別

是否批准新增？
```

### 場景2: 批次掃描提升覆蓋率

**使用者操作**:
```
"掃描所有18個Prompts，發現缺失的特徵維度"
```

**執行**:
```python
# 掃描所有Prompts
all_prompts = load_json("extracted_modules.json")
missing_features = {}

for prompt in all_prompts:
    prompt_text = prompt["original_prompt"]
    features = hybrid_learning_pipeline(prompt_text)

    for feature in features:
        category = feature["category"]
        if category not in missing_features:
            missing_features[category] = []
        missing_features[category].append(feature)

# 生成報告
print(f"發現 {len(missing_features)} 個新類別")
for category, items in missing_features.items():
    print(f"  {category}: {len(items)} 個新子分類")
```

**輸出示例**:
```
掃描完成！發現新類別:

1. hair_styles (髮型): 8個新分類
   - long_straight_black (Prompt #5)
   - twin_tails_blue (Prompt #18)
   - short_spiky (Prompt #17)
   ...

2. skin_tones (膚色): 3個新分類
   - fair_pale (Prompt #5, #18)
   - tan_healthy (Prompt #10)
   ...

3. clothing_styles (服裝): 5個新分類
   - traditional_chinese (Prompt #18)
   - punk_street (Prompt #17)
   ...

生成稽核報告: new_features_review_2026-01-01.md
```

---

## 📁 自動生成的檔案

### 1. 稽核報告 (`new_features_review_YYYY-MM-DD.md`)

**內容**:
- 發現的新特徵列表
- 每個特徵的詳細資訊
- 稽核選項（批准/修改/拒絕）
- 關聯的Prompt ID

### 2. 待稽核特徵庫 (`pending_features.json`)

**格式**:
```json
{
  "pending_items": [
    {
      "category": "hair_styles",
      "code": "long_flowing_red",
      "chinese_name": "長髮飄逸（紅色）",
      "keywords": ["long flowing red hair"],
      "source_prompts": [],
      "detection_date": "2026-01-01",
      "confidence": 0.88,
      "status": "pending_review"
    }
  ]
}
```

### 3. 更新日誌 (`feature_library_changelog.md`)

**記錄所有變更**:
```markdown
## 2026-01-01
- 新增類別: hair_styles (5個分類)
- 新增類別: hair_colors (4個分類)
- 新增子類別: skin_tones (在skin_textures下，3個分類)
- 來源: 自動學習 + 人工稽核
```

---

## ⚠️ 注意事項

### 1. 質量控制

**自動檢測的侷限**:
- ❌ 可能誤識別（false positive）
- ❌ 可能遺漏（false negative）
- ❌ 關鍵詞可能不夠準確

**解決方案**:
- ✅ 始終需要人工稽核
- ✅ 設定置信度閾值（>80%才建議）
- ✅ 多次出現的特徵優先順序更高

### 2. 分類一致性

**確保新分類符合現有規範**:
- 命名規範（classification_code）
- 資料結構一致
- 複用性評分標準
- 關鍵詞格式

### 3. 避免過度細分

**不要為每個細微差別建立分類**:
- ✅ 好: long_straight (通用)
- ❌ 差: long_straight_waist_length (過細)

**合併相似分類**:
- long_straight_black + long_straight_brown → long_straight (顏色單獨分類)

---

## 🚀 實施建議

### 階段1: 手動擴充套件（立即開始）

**不等自學習系統，先手動新增常見維度**:
1. 從18個現有Prompts中人工提取髮型、髮色、膚色
2. 建立3個新類別的基礎分類（各3-5個）
3. 更新 facial_features_library.json 至 v1.3

**時間**: 1-2小時

### 階段2: 規則學習（1周內）

**實現規則基礎的learner**:
1. 編寫正則表示式提取器
2. 實現特徵匹配邏輯
3. 生成稽核報告

**時間**: 1-2天

### 階段3: AI增強（2周內）

**整合LLM API**:
1. 使用Claude/GPT-4分析Prompt
2. 自動提取和分類特徵
3. 混合模式（規則+AI）

**時間**: 3-5天

---

**模組狀態**: 🚧 設計完成，待實施
**優先順序**: 高（髮型、髮色、膚色）
**推薦方案**: 混合模式（規則+AI+人工稽核）
**下一步**: 先手動擴充套件，再實現自動學習
