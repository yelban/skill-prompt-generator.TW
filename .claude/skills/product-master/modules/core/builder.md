# Product Builder - 產品Prompt組裝器

**功能**: 從Universal Elements Database查詢元素並組裝產品攝影Prompt

---

## 🎯 組裝策略

### 基礎結構

```
產品攝影Prompt =
  產品描述 (20%) +
  材質紋理 (15%) +
  攝影技術 (25%) +
  光照設定 (20%) +
  技術引數 (10%) +
  質量增強 (10%)
```

---

## 📋 組裝流程

### Step 1: 查詢產品元素

```python
from element_db import ElementDB

db = ElementDB('extracted_results/elements.db')

# 查詢產品型別
product_elements = db.search_by_domain(
    'product',
    category_id='product_types',
    min_reusability=6.0
)

# 如果使用者指定了標籤（如"luxury"）
if user_tags:
    product_elements = db.search_by_tags(
        user_tags + ['product'],
        require_all=False
    )
```

### Step 2: 查詢材質紋理

```python
# 查詢材質
materials = db.search_by_domain(
    'product',
    category_id='material_textures',
    min_reusability=7.0,
    limit=2
)

# 或按標籤查詢
materials = db.search_by_tags(['glossy', 'leather', 'metal'])
```

### Step 3: 查詢攝影技術

```python
# 查詢專業攝影技術
photo_tech = db.search_by_domain(
    'common',
    category_id='photography_techniques',
    min_reusability=8.0
)

# 產品攝影常用：macro, Phase One, editorial
macro_tech = [e for e in photo_tech if 'macro' in e['name'].lower()]
```

### Step 4: 查詢光照技術

```python
# 查詢光照
lighting = db.search_by_domain(
    'common',
    category_id='lighting_techniques',
    min_reusability=8.0
)

# 產品攝影常用：softbox, rim lighting, studio lighting
product_lighting = [e for e in lighting if any(kw in e['ai_prompt_template'].lower()
                    for kw in ['softbox', 'rim', 'studio'])]
```

### Step 5: 查詢技術效果

```python
# 查詢解析度等技術引數
tech_effects = db.search_by_domain(
    'common',
    category_id='technical_effects',
    min_reusability=9.0
)

# 4K/8K resolution
resolution = [e for e in tech_effects if '4k' in e['name'].lower() or '8k' in e['name'].lower()]
```

---

## 🔧 組裝演算法

```python
def build_product_prompt(
    product_type: str = "premium product",
    style: str = "luxury",
    user_tags: list = None
) -> str:
    """
    組裝產品攝影Prompt

    Args:
        product_type: 產品型別（如"book", "watch", "electronics"）
        style: 風格（如"luxury", "minimalist", "tech"）
        user_tags: 使用者指定的標籤

    Returns:
        完整的產品攝影Prompt
    """

    db = ElementDB('extracted_results/elements.db')
    prompt_parts = []

    # 1. 產品主體
    if product_type != "premium product":
        # 搜尋特定產品
        products = db.search_by_tags([product_type, 'product'])
    else:
        # 使用通用產品描述
        products = db.search_by_domain('product', limit=1)

    if products:
        prompt_parts.append(products[0]['ai_prompt_template'])
    else:
        prompt_parts.append(f"premium {product_type}")

    # 2. 攝影技術（核心）
    photo_tech = db.search_by_domain('common', category_id='photography_techniques', limit=1)
    if photo_tech:
        prompt_parts.append(photo_tech[0]['ai_prompt_template'])

    # 3. 光照設定
    lighting = db.search_by_domain('product', category_id='lighting_techniques', limit=1)
    if lighting:
        prompt_parts.append(lighting[0]['ai_prompt_template'])

    # 4. 材質紋理（如果有style要求）
    if style and style.lower() in ['luxury', 'premium', 'high-end']:
        materials = db.search_by_tags(['luxury'], require_all=False)
        if materials:
            prompt_parts.append(materials[0]['ai_prompt_template'])

    # 5. 技術引數
    tech = db.search_by_tags(['4k', 'resolution'])
    if tech:
        prompt_parts.append(tech[0]['ai_prompt_template'])

    # 6. 質量增強詞
    quality_enhancers = [
        "photorealistic",
        "ultra-detailed",
        "professional commercial photography",
        "editorial magazine quality",
        "pristine studio environment",
        "perfectly controlled lighting"
    ]

    prompt_parts.extend(quality_enhancers)

    # 組裝
    prompt = ', '.join(prompt_parts)

    db.close()
    return prompt
```

---

## 📊 輸出示例

### 示例1: 奢華書籍

**輸入**:
```python
build_product_prompt(
    product_type="collector edition book",
    style="luxury"
)
```

**輸出**:
```
Premium collector's edition book, luxury binding, Italian calfskin cover,
Phase One medium format camera with 100mm macro lens, sophisticated softbox
rim lighting, 4K resolution, photorealistic, ultra-detailed, professional
commercial photography, editorial magazine quality, pristine studio environment,
perfectly controlled lighting
```

---

### 示例2: 科技產品

**輸入**:
```python
build_product_prompt(
    product_type="smartphone",
    style="tech",
    user_tags=["glass", "modern"]
)
```

**輸出**:
```
Premium smartphone with glossy glass surface, modern sleek design, Phase One
camera with macro lens capturing screen details, soft studio lighting creating
elegant reflections, 4K ultra high resolution, photorealistic render,
professional tech product photography, minimal background, clean aesthetic
```

---

## ✅ 質量保證

### 必備元素檢查

每個產品Prompt應包含：
- ✅ 產品描述
- ✅ 攝影技術（相機/鏡頭）
- ✅ 光照設定
- ✅ 解析度/質量引數

### 長度控制

- 目標: 150-250詞
- 最小: 100詞
- 最大: 300詞

---

**模組狀態**: ✅ 已實現
**查詢效率**: O(log n) 索引查詢
