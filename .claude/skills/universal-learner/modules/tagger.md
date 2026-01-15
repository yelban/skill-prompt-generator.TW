# Tagger - 標籤生成器模組

**功能**: 為提取的元素自動生成高質量標籤

---

## 🎯 標籤型別

### 1. 領域標籤 (Domain Tags)
每個元素至少有一個領域標籤

| 領域 | 標籤 |
|------|------|
| portrait | `portrait` |
| product | `product` |
| design | `design` |
| art | `art` |
| video | `video` |
| interior | `interior` |
| common | `photography` |

### 2. 類別標籤 (Category Tags)
基於元素所屬類別

- `facial-features`, `makeup-styles`, `hair-styles`
- `product-types`, `material-textures`
- `layout-systems`, `visual-effects`
- `furniture-layouts`, `design-elements`
- etc.

### 3. 特徵標籤 (Feature Tags)
基於元素的關鍵特徵

- 材質：`glass`, `wood`, `metal`, `fabric`
- 風格：`modern`, `vintage`, `luxury`, `minimal`
- 顏色：`red`, `gold`, `neutral`, `vibrant`
- 效果：`glossy`, `matte`, `reflective`, `translucent`

### 4. 跨領域標籤 (Cross-Domain Tags)
可用於多個領域的通用標籤

| 標籤 | 適用領域 | 含義 |
|------|----------|------|
| `luxury` | product, interior, portrait | 高階奢華 |
| `glass` | design, art, product | 玻璃/透明效果 |
| `geometric` | design, interior, art | 幾何圖案 |
| `dynamic` | art, video, design | 動態/運動感 |
| `soft` | lighting, texture, makeup | 柔和效果 |
| `bold` | typography, color, makeup | 大膽/強烈 |

---

## 📋 標籤生成流程

### Step 1: 從關鍵詞提取

```python
def extract_tags_from_keywords(keywords: List[str]) -> List[str]:
    tags = []

    for kw in keywords:
        # 轉換為標籤格式
        tag = kw.lower()
        tag = tag.replace(' ', '-')
        tag = tag.replace('_', '-')

        # 過濾
        if is_valid_tag(tag):
            tags.append(tag)

    return tags

def is_valid_tag(tag: str) -> bool:
    # 長度檢查
    if len(tag) < 2 or len(tag) > 30:
        return False

    # 避免無意義標籤
    stopwords = ['the', 'a', 'an', 'with', 'and', 'or', 'of']
    if tag in stopwords:
        return False

    return True
```

### Step 2: 新增領域和類別標籤

```python
def add_domain_category_tags(
    element: Dict,
    domain_id: str,
    category_id: str
) -> List[str]:
    tags = []

    # 領域標籤
    domain_tag_map = {
        'portrait': 'portrait',
        'product': 'product',
        'design': 'design',
        'art': 'art',
        'video': 'video',
        'interior': 'interior',
        'common': 'photography'
    }
    tags.append(domain_tag_map[domain_id])

    # 類別標籤
    category_tag = category_id.replace('_', '-')
    tags.append(category_tag)

    return tags
```

### Step 3: 智慧特徵標籤識別

```python
def identify_feature_tags(element: Dict) -> List[str]:
    tags = []
    template = element['ai_prompt_template'].lower()

    # 材質特徵
    material_patterns = {
        'wood': ['wood', 'wooden', 'walnut', 'oak', 'teak'],
        'metal': ['metal', 'brass', 'gold', 'copper', 'steel'],
        'glass': ['glass', 'translucent', 'transparent'],
        'fabric': ['fabric', 'linen', 'cotton', 'silk'],
        'leather': ['leather', 'calfskin', 'suede']
    }

    for tag, patterns in material_patterns.items():
        if any(p in template for p in patterns):
            tags.append(tag)

    # 風格特徵
    style_patterns = {
        'modern': ['modern', 'contemporary', 'minimalist'],
        'vintage': ['vintage', 'retro', 'mid-century', 'classic'],
        'luxury': ['luxury', 'premium', 'high-end', 'upscale'],
        'geometric': ['geometric', 'angular', 'linear', 'grid']
    }

    for tag, patterns in style_patterns.items():
        if any(p in template for p in patterns):
            tags.append(tag)

    # 效果特徵
    effect_patterns = {
        'glossy': ['glossy', 'shiny', 'reflective', 'polished'],
        'matte': ['matte', 'flat', 'non-reflective'],
        'soft': ['soft', 'gentle', 'subtle', 'diffused'],
        'bold': ['bold', 'strong', 'vibrant', 'dramatic']
    }

    for tag, patterns in effect_patterns.items():
        if any(p in template for p in patterns):
            tags.append(tag)

    return tags
```

### Step 4: 跨領域標籤對映

```python
def identify_cross_domain_tags(element: Dict, domain_id: str) -> List[str]:
    tags = []
    template = element['ai_prompt_template'].lower()
    keywords = element.get('keywords', [])

    cross_domain_keywords = {
        'luxury': [
            'luxury', 'premium', 'high-end', 'upscale',
            'exclusive', 'collector', 'elite'
        ],
        'minimalist': [
            'minimal', 'clean', 'simple', 'streamlined'
        ],
        'dynamic': [
            'dynamic', 'motion', 'movement', 'flowing', 'energy'
        ],
        'organic': [
            'organic', 'natural', 'curved', 'flowing'
        ]
    }

    for tag, patterns in cross_domain_keywords.items():
        if any(p in template or p in ' '.join(keywords).lower()
               for p in patterns):
            tags.append(tag)

    return tags
```

---

## 📊 標籤生成示例

### 示例1: Product Element

**輸入元素**:
```json
{
  "category": "product_types",
  "name": "collector_edition_book",
  "ai_prompt_template": "premium collector's edition book, luxury binding, Italian calfskin cover",
  "keywords": ["collector's edition", "premium book", "luxury binding"]
}
```

**標籤生成過程**:
1. 從keywords: `["collectors-edition", "premium-book", "luxury-binding"]`
2. 領域+類別: `["product", "product-types"]`
3. 智慧特徵: `["luxury", "leather"]` (從"calfskin"識別)
4. 跨領域: `["collectible", "book"]`

**最終標籤**:
```json
[
  "product",
  "product-types",
  "collectors-edition",
  "premium-book",
  "luxury-binding",
  "luxury",
  "leather",
  "collectible",
  "book"
]
```

---

### 示例2: Design Element

**輸入元素**:
```json
{
  "category": "visual_effects",
  "name": "glassmorphism",
  "ai_prompt_template": "frosted glass effect, 80% translucent, backdrop-filter blur",
  "keywords": ["glassmorphism", "frosted glass", "translucent"]
}
```

**標籤生成過程**:
1. 從keywords: `["glassmorphism", "frosted-glass", "translucent"]`
2. 領域+類別: `["design", "visual-effects"]`
3. 智慧特徵: `["glass", "modern"]` (玻璃態是現代設計)
4. 跨領域: `["ui", "effect"]`

**最終標籤**:
```json
[
  "design",
  "visual-effects",
  "glassmorphism",
  "frosted-glass",
  "translucent",
  "glass",
  "modern",
  "ui",
  "effect"
]
```

---

### 示例3: Interior Element

**輸入元素**:
```json
{
  "category": "design_elements",
  "name": "sputnik_chandelier",
  "ai_prompt_template": "brass sputnik chandelier, mid-century iconic lighting",
  "keywords": ["sputnik", "chandelier", "brass", "mid-century"]
}
```

**標籤生成過程**:
1. 從keywords: `["sputnik", "chandelier", "brass", "mid-century"]`
2. 領域+類別: `["interior", "design-elements"]`
3. 智慧特徵: `["metal", "vintage", "lighting"]`
4. 跨領域: `["statement-piece", "iconic"]`

**最終標籤**:
```json
[
  "interior",
  "design-elements",
  "sputnik",
  "chandelier",
  "brass",
  "mid-century",
  "metal",
  "vintage",
  "lighting",
  "statement-piece",
  "iconic"
]
```

---

## 🎯 標籤質量標準

### 優秀標籤
- ✅ 描述性強：`geometric-pattern`, `soft-lighting`
- ✅ 適度具體：`mid-century`, `luxury`
- ✅ 可搜尋：`glass`, `wood`, `modern`
- ✅ 跨領域複用：`luxury` (product/interior/portrait)

### 避免的標籤
- ❌ 太泛泛：`good`, `nice`, `thing`
- ❌ 太具體：`my-grandmothers-rug`
- ❌ 無意義：`the`, `a`, `and`
- ❌ 過長：`mid-century-modern-walnut-tapered-leg-furniture`

---

## 🔍 標籤去重和最佳化

```python
def optimize_tags(tags: List[str]) -> List[str]:
    # 1. 去重
    tags = list(set(tags))

    # 2. 移除冗餘
    # 如果有"mid-century-modern"，移除"mid-century"
    if 'mid-century-modern' in tags and 'mid-century' in tags:
        tags.remove('mid-century')

    # 3. 長度限制（最多15個標籤）
    if len(tags) > 15:
        # 優先保留：領域標籤、類別標籤、高頻標籤
        tags = prioritize_tags(tags)[:15]

    # 4. 排序（領域 > 類別 > 特徵 > 其他）
    tags = sort_tags(tags)

    return tags
```

---

## ✅ 輸出格式

```json
{
  "tags": [
    "product",
    "product-types",
    "collectors-edition",
    "premium-book",
    "luxury-binding",
    "luxury",
    "leather",
    "collectible",
    "book"
  ],
  "tag_count": 9,
  "cross_domain_tags": ["luxury", "collectible"],
  "primary_tags": ["product", "product-types"]
}
```

---

**狀態**: ✅ 已實現
**目標**: 每個元素 5-15 個高質量標籤
