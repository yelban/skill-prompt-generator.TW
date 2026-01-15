---
name: prompt-analyzer
description: 提示詞分析與洞察 - 檢視Prompt詳情、對比差異、推薦相似提示詞、元素庫統計
---

# Prompt Analyzer - 提示詞分析器

## 🎯 核心職責

**專注於已生成Prompt的分析和洞察**，不負責生成新Prompt。

提供以下5大功能：
1. **檢視詳情** - 分析Prompt使用了哪些元素
2. **對比分析** - 對比兩個Prompt的差異
3. **相似推薦** - 推薦相似的Prompt
4. **元素統計** - 查詢元素庫統計資訊
5. **風格推薦** - 按風格推薦最佳元素組合

---

## 📋 功能1：檢視Prompt詳情

### 觸發場景

使用者說：
- "檢視Prompt #5的詳情"
- "分析一下Prompt #5用了哪些元素"
- "顯示Prompt #5的完整資訊"
- "Prompt #5包含什麼？"

### SKILL處理流程

#### 步驟1：識別意圖

從使用者輸入中提取Prompt ID：

```python
# 示例：使用者說 "檢視Prompt #5的詳情"
prompt_id = 5
```

#### 步驟2：呼叫執行層

```python
from prompt_analyzer import analyze_prompt_detail

result = analyze_prompt_detail(prompt_id=5)
```

#### 步驟3：檢查結果

如果Prompt不存在：
```python
if 'error' in result:
    print(f"❌ {result['error']}")
    # 提示使用者：該Prompt不存在，可能還沒生成過任何Prompt
```

#### 步驟4：格式化展示

```markdown
📸 Prompt #5 詳情

**使用者需求**: {result['user_intent']}
**生成時間**: {result['generation_date']}
**質量評分**: {result['quality_score']}/10
**風格標籤**: {result['style_tag']}

**使用的元素** ({len(result['elements'])}個):

1. [{field_name}] {chinese_name} (複用度: {reusability})
   - 類別: {category}
   - 模板: {template}

2. ...

**完整Prompt**:
────────────────────────────────────────────────────────
{result['prompt_text']}
────────────────────────────────────────────────────────
```

---

## 📋 功能2：對比兩個Prompts

### 觸發場景

使用者說：
- "對比Prompt #5和#17"
- "#5和#17有什麼區別？"
- "比較一下Prompt #5和#17"

### SKILL處理流程

#### 步驟1：識別意圖

從使用者輸入中提取兩個Prompt ID：

```python
# 示例：使用者說 "對比Prompt #5和#17"
prompt_id1 = 5
prompt_id2 = 17
```

#### 步驟2：呼叫執行層

```python
from prompt_analyzer import compare_prompts

result = compare_prompts(prompt_id1=5, prompt_id2=17)
```

#### 步驟3：分析差異維度

SKILL分析返回的資料，生成對比表格：

```markdown
⚖️ Prompt對比：#5 vs #17

### 基本資訊對比

| 維度 | Prompt #5 | Prompt #17 |
|------|-----------|-----------|
| 使用者需求 | {p1['user_intent']} | {p2['user_intent']} |
| 風格標籤 | {p1['style_tag']} | {p2['style_tag']} |
| 質量評分 | {p1['quality_score']}/10 | {p2['quality_score']}/10 |
| 元素總數 | {len(p1['elements'])}個 | {len(p2['elements'])}個 |
| 生成時間 | {p1['generation_date']} | {p2['generation_date']} |

### 元素差異分析

**相似度**: {result['similarity_score']*100:.1f}%

**共同元素** ({len(result['common_elements'])}個):
- {common_element['chinese_name']} ({common_element['category']})
- ...

**Prompt #5 獨有** ({len(result['unique_to_p1'])}個):
- {element['chinese_name']} ({element['category']})
  關鍵詞: {element['template'][:50]}...
- ...

**Prompt #17 獨有** ({len(result['unique_to_p2'])}個):
- {element['chinese_name']} ({element['category']})
  關鍵詞: {element['template'][:50]}...
- ...
```

#### 步驟4：分析結論

SKILL根據相似度給出結論：

```python
if result['similarity_score'] > 0.7:
    print("💡 這兩個Prompt非常相似，風格接近")
elif result['similarity_score'] > 0.4:
    print("💡 這兩個Prompt有一定相似性，但風格有明顯差異")
else:
    print("💡 這兩個Prompt完全不同，屬於不同風格")
```

---

## 📋 功能3：推薦相似Prompts

### 觸發場景

使用者說：
- "推薦與#5相似的Prompt"
- "有沒有類似#5的？"
- "找一些相似的提示詞"
- "基於Prompt #5推薦相似的"

### SKILL處理流程

#### 步驟1：識別意圖

```python
# 示例：使用者說 "推薦與#5相似的Prompt"
prompt_id = 5
top_n = 3  # 預設推薦3個
```

#### 步驟2：呼叫執行層

```python
from prompt_analyzer import recommend_similar_prompts

result = recommend_similar_prompts(prompt_id=5, top_n=3)
```

#### 步驟3：分析推薦理由

SKILL解讀相似度原因，為每個推薦Prompt生成理由：

```python
# 分析共同元素，找出相似的原因
def analyze_similarity_reason(common_element_ids, target_prompt, candidate_prompt):
    """
    分析兩個Prompt為什麼相似

    返回：
    - 共同的風格標籤
    - 共同的元素類別
    - 推薦理由列表
    """
    reasons = []

    # 檢查風格標籤
    if target_prompt['style_tag'] == candidate_prompt['style_tag']:
        reasons.append(f"✓ 同為{candidate_prompt['style_tag']}風格")

    # 按類別統計共同元素
    category_count = {}
    for elem_id in common_element_ids:
        # 查詢元素詳情獲取category
        # ... (執行層已返回)
        category = ...
        category_count[category] = category_count.get(category, 0) + 1

    # 列出重要的共同類別
    for category, count in category_count.items():
        if count >= 2:
            reasons.append(f"✓ {count}個共同的{category}元素")

    return reasons
```

#### 步驟4：格式化展示

```markdown
🔍 為Prompt #5推薦相似提示詞

[1] Prompt #{recommendation['prompt_id']} - {recommendation['user_intent']}
    相似度: {recommendation['similarity']*100:.1f}%
    共同元素: {recommendation['common_count']}個
    質量評分: {recommendation['quality_score']}/10

    理由:
    - ✓ 同為{style_tag}風格
    - ✓ 共用3個makeup元素
    - ✓ 共用2個lighting元素

[2] ...

[3] ...
```

---

## 📋 功能4：元素庫統計

### 觸發場景

使用者說：
- "元素庫有哪些類別？"
- "makeup類別有多少個元素？"
- "哪些元素用得最多？"
- "檢視元素庫統計"
- "makeup_styles的詳細資訊"

### SKILL處理流程

#### 步驟1：識別意圖

```python
# 場景A：使用者說 "元素庫有哪些類別？"
category = None  # 查詢整體統計

# 場景B：使用者說 "makeup類別有多少個元素？"
category = 'makeup_styles'  # 查詢特定類別
```

#### 步驟2：呼叫執行層

```python
from prompt_analyzer import get_library_statistics

# 整體統計
result = get_library_statistics()

# 或者特定類別
result = get_library_statistics(category='makeup_styles')
```

#### 步驟3：格式化展示

**場景A：整體統計**

```markdown
📊 元素庫統計

**總計**: {result['total_elements']} 個元素

**按類別分佈**:
- makeup_styles: {count}個
- clothing_styles: {count}個
- hair_styles: {count}個
- lighting_techniques: {count}個
- facial_features: {count}個
- ...

💡 使用 "檢視makeup_styles詳情" 檢視具體元素列表
```

**場景B：類別詳情**

```markdown
📊 元素庫統計 - {category}

**類別**: {result['category_details']['category']}
**總數**: {result['category_details']['total_count']} 個元素

**最常用元素** (Top 10):

| 排名 | 元素名稱 | 複用度 | 使用次數 | 平均質量 |
|------|---------|--------|---------|---------|
| 1 | {chinese_name} | {reusability} | {usage_count}次 | {avg_quality}/10 |
| 2 | ... | ... | ... | ... |
| ... |

**最高質量元素** (Top 5):
[按avg_quality排序]

**從未使用的元素** ({count}個):
[usage_count = 0的元素]
```

---

## 📋 功能5：按風格推薦元素組合

### 觸發場景

使用者說：
- "古裝風格應該用什麼元素？"
- "科幻風格的最佳元素組合是什麼？"
- "推薦西部世界風格的元素"
- "ancient_chinese風格用哪些元素好？"

### SKILL處理流程

#### 步驟1：識別意圖

```python
# 示例：使用者說 "古裝風格應該用什麼元素？"

# 對映使用者描述到style_tag
style_mapping = {
    '古裝': 'ancient_chinese',
    '古裝中式': 'ancient_chinese',
    '仙劍奇俠傳': 'ancient_chinese',
    '科幻': 'modern_sci_fi',
    '西部世界': 'westworld_android',
    '賽博朋克': 'cyberpunk',
    '奇幻': 'fantasy'
}

style = style_mapping.get('古裝', 'ancient_chinese')
```

#### 步驟2：呼叫執行層

```python
from prompt_analyzer import recommend_elements_by_style

result = recommend_elements_by_style(style='ancient_chinese')
```

#### 步驟3：按類別組織推薦

SKILL將返回的元素按類別分組，便於展示：

```python
# 按category分組
elements_by_category = {}
for element in result['recommended_elements']:
    category = element['category']
    if category not in elements_by_category:
        elements_by_category[category] = []
    elements_by_category[category].append(element)

# 按類別的最高使用頻率排序
sorted_categories = sorted(
    elements_by_category.items(),
    key=lambda x: max(e['usage_frequency'] for e in x[1]),
    reverse=True
)
```

#### 步驟4：格式化展示

```markdown
🎨 風格推薦：{result['style']}

**資料來源**: 基於{result['total_prompts']}個歷史Prompt分析

**推薦元素組合** (按類別):

### 1. {category_name}

[{field_name}] {chinese_name}
- 使用頻率: {usage_frequency*100:.0f}% ({usage_count}/{total_prompts}個Prompt使用)
- 複用度: {reusability}/10
- 平均質量: {avg_quality}/10
- 關鍵詞: {template[:80]}...

### 2. {category_name}

...

**使用建議**:
- ✓ 這個組合在{style}風格中最常用，質量穩定
- ✓ 推薦搭配：{推薦的基礎屬性，如"東亞女性"}
- ⚠️ 避免搭配：{衝突的元素}
```

---

## 🔧 執行層函式列表

SKILL呼叫以下執行函式（程式碼層只執行，不決策）：

```python
# 所有函式在 prompt_analyzer.py 中

def analyze_prompt_detail(prompt_id: int) -> dict:
    """查詢Prompt完整資訊"""

def compare_prompts(prompt_id1: int, prompt_id2: int) -> dict:
    """對比兩個Prompt差異"""

def recommend_similar_prompts(prompt_id: int, top_n: int = 3) -> list:
    """推薦相似Prompts"""

def get_library_statistics(category: str = None) -> dict:
    """查詢元素庫統計"""

def recommend_elements_by_style(style: str) -> dict:
    """按風格推薦元素組合"""
```

---

## 📁 資料依賴

```
elements.db
├── elements                 # 元素庫（由universal-learner維護）
├── generated_prompts        # 生成歷史（由intelligent-prompt-generator寫入）
├── prompt_elements          # Prompt-元素關聯
└── element_usage_stats      # 元素使用統計
```

**重要**：prompt-analyzer依賴intelligent-prompt-generator生成的歷史資料。如果資料庫中沒有generated_prompts記錄，分析功能無法工作。

---

## ⚙️ 架構原則

✅ **SKILL = 大腦（決策層）**
- 識別使用者意圖
- 分析返回資料
- 格式化展示結果
- 生成推薦理由

✅ **程式碼 = 手腳（執行層）**
- 查詢資料庫
- 計算相似度
- 返回原始資料

❌ **程式碼不做決策**
- 不判斷"哪個更好"
- 不決定"展示什麼"
- 只負責"取資料"

---

## 使用示例

### 示例1：檢視詳情

**使用者**: "檢視Prompt #1的詳情"

**SKILL處理**:
```python
from prompt_analyzer import analyze_prompt_detail

result = analyze_prompt_detail(prompt_id=1)

# 展示格式化結果
print(f"📸 Prompt #{result['prompt_id']} 詳情\n")
print(f"**使用者需求**: {result['user_intent']}")
print(f"**生成時間**: {result['generation_date']}")
# ...
```

### 示例2：對比Prompts

**使用者**: "對比Prompt #1和#2"

**SKILL處理**:
```python
from prompt_analyzer import compare_prompts

result = compare_prompts(prompt_id1=1, prompt_id2=2)

# 分析相似度
similarity = result['similarity_score']
if similarity > 0.7:
    conclusion = "非常相似"
elif similarity > 0.4:
    conclusion = "有一定相似性"
else:
    conclusion = "完全不同"

# 展示對比表格和結論
# ...
```

### 示例3：推薦相似Prompt

**使用者**: "推薦與#1相似的Prompt"

**SKILL處理**:
```python
from prompt_analyzer import recommend_similar_prompts

recommendations = recommend_similar_prompts(prompt_id=1, top_n=3)

# 為每個推薦分析理由
for rec in recommendations:
    reasons = analyze_similarity_reason(
        rec['common_element_ids'],
        target_prompt_id=1,
        candidate_prompt_id=rec['prompt_id']
    )

    # 展示推薦和理由
    # ...
```

### 示例4：元素庫統計

**使用者**: "檢視makeup_styles類別詳情"

**SKILL處理**:
```python
from prompt_analyzer import get_library_statistics

result = get_library_statistics(category='makeup_styles')

# 展示統計表格
details = result['category_details']
print(f"📊 {details['category']} - {details['total_count']}個元素\n")

# 按使用次數排序展示
# ...
```

### 示例5：風格推薦

**使用者**: "古裝風格應該用什麼元素？"

**SKILL處理**:
```python
from prompt_analyzer import recommend_elements_by_style

result = recommend_elements_by_style(style='ancient_chinese')

# 按類別組織展示
elements_by_category = group_by_category(result['recommended_elements'])

# 展示每個類別的推薦
for category, elements in elements_by_category.items():
    print(f"### {category}")
    for elem in elements:
        print(f"  - {elem['chinese_name']} (使用頻率: {elem['usage_frequency']*100:.0f}%)")
# ...
```

---

## ⚠️ 重要提醒

1. **資料前提**：必須先有生成歷史才能分析
   - 如果使用者說"檢視Prompt #5"，但資料庫中沒有任何Prompt，應提示：
     ```
     ❌ 資料庫中還沒有生成歷史。
     💡 請先使用 intelligent-prompt-generator 生成一些Prompt。
     ```

2. **Prompt ID範圍**：只能查詢已存在的Prompt ID
   - 使用者輸入的ID可能不存在，需要檢查error欄位

3. **風格標籤一致性**：風格推薦依賴style_tag
   - style_tag由intelligent-prompt-generator在儲存時設定
   - 常見標籤：ancient_chinese, modern_sci_fi, cyberpunk, fantasy, westworld_android

4. **元素類別名稱**：查詢統計時使用正確的category名稱
   - makeup_styles (不是makeup)
   - lighting_techniques (不是lighting)
   - clothing_styles, hair_styles, facial_features 等

---

準備好分析提示詞！等待使用者的分析請求。
