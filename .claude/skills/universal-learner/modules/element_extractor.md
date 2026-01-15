# Element Extractor - 元素提取器模組

**功能**: 從Prompt中提取可複用的元素片段

---

## 🎯 提取策略（按領域）

### 1. Product Domain (產品攝影)

**提取類別**:
- `product_types` - 產品型別
- `material_textures` - 材質紋理
- `photography_techniques` - 攝影技術
- `lighting_setups` - 光照佈局
- `composition_styles` - 構圖風格

**示例**:

```
輸入: "A premium collector's edition book with Italian calfskin binding,
       glossy reflective surface, photographed with Phase One 100mm macro lens"

提取:
1. product_types/collector_edition_book
   - template: "premium collector's edition book, luxury binding"
   - keywords: ["collector's edition", "premium book", "luxury"]

2. material_textures/italian_calfskin
   - template: "Italian calfskin leather, premium natural grain"
   - keywords: ["calfskin", "leather", "luxury material"]

3. material_textures/glossy_reflective
   - template: "glossy reflective surface, high-end finish"
   - keywords: ["glossy", "reflective", "shiny"]

4. photography_techniques/macro_100mm
   - template: "Phase One medium format with 100mm macro lens"
   - keywords: ["macro", "100mm", "close-up"]
```

---

### 2. Design Domain (平面設計)

**提取類別**:
- `layout_systems` - 佈局系統
- `visual_effects` - 視覺效果
- `typography_styles` - 字型風格
- `color_schemes` - 色彩方案
- `composition_techniques` - 構圖技巧

**示例**:

```
輸入: "Modern Bento grid layout with glassmorphism effects,
       asymmetric card arrangement, bold sans-serif typography"

提取:
1. layout_systems/bento_grid
   - template: "modern Bento grid layout, modular card-based design"
   - keywords: ["bento grid", "modular", "asymmetric"]

2. visual_effects/glassmorphism
   - template: "frosted glass effect, 80% translucent, backdrop blur"
   - keywords: ["glass", "frosted", "translucent", "blur"]

3. typography_styles/bold_sans_serif
   - template: "bold sans-serif typography, modern clean font"
   - keywords: ["bold", "sans-serif", "clean"]
```

---

### 3. Art Domain (藝術風格)

**提取類別**:
- `art_styles` - 藝術風格
- `special_effects` - 特效
- `narrative_elements` - 敘事元素
- `visual_techniques` - 視覺技巧

**示例**:

```
輸入: "Surrealistic painting with dreamlike atmosphere,
       melting clocks style, vibrant color explosion"

提取:
1. art_styles/surrealism
   - template: "surrealistic composition, dreamlike impossible scene"
   - keywords: ["surreal", "dreamlike", "fantastical"]

2. special_effects/melting_distortion
   - template: "melting distortion effect, fluid transformation"
   - keywords: ["melting", "distortion", "fluid"]

3. special_effects/color_explosion
   - template: "vibrant color explosion, dynamic paint splash"
   - keywords: ["color explosion", "vibrant", "splash"]
```

---

### 4. Portrait Domain (人像攝影)

**提取類別**:
- `facial_features` - 面部特徵
- `makeup_styles` - 妝容風格
- `hair_styles` - 髮型
- `expressions` - 表情
- `poses` - 姿勢
- `clothing_styles` - 服裝風格

**示例**:

```
輸入: "A woman with large almond eyes, porcelain skin,
       wearing elegant red qipao dress"

提取:
1. facial_features/large_almond_eyes
   - template: "large expressive almond eyes, thick natural lashes"
   - keywords: ["large eyes", "almond", "expressive"]

2. skin_tones/porcelain_fair
   - template: "porcelain fair skin tone, flawless complexion"
   - keywords: ["porcelain", "fair", "pale"]

3. clothing_styles/red_qipao
   - template: "elegant red silk qipao dress, traditional Chinese"
   - keywords: ["qipao", "red", "silk", "traditional"]
```

---

### 5. Video Domain (影片生成)

**提取類別**:
- `scene_types` - 場景型別
- `camera_movements` - 相機運動
- `transitions` - 轉場效果
- `motion_effects` - 動態效果

**示例**:

```
輸入: "Cinematic dolly shot moving through forest,
       slow-motion falling leaves, golden hour lighting"

提取:
1. camera_movements/dolly_forward
   - template: "smooth dolly shot moving forward through scene"
   - keywords: ["dolly", "forward", "tracking"]

2. motion_effects/slow_motion_falling
   - template: "slow-motion falling objects, 120fps capture"
   - keywords: ["slow motion", "falling", "floating"]

3. lighting_scenarios/golden_hour
   - template: "golden hour warm sunlight, magic hour glow"
   - keywords: ["golden hour", "warm", "sunset"]
```

---

### 6. Interior Domain (室內設計)

**提取類別**:
- `space_types` - 空間型別
- `furniture_layouts` - 傢俱佈局
- `design_elements` - 設計元素
- `material_combinations` - 材質組合
- `spatial_atmospheres` - 空間氛圍

**示例**:

```
輸入: "Mid-century modern living room with walnut herringbone flooring,
       L-shaped sofa with tapered legs, sputnik chandelier"

提取:
1. space_types/living_room_midcentury
   - template: "mid-century modern living room, retro-modern fusion"
   - keywords: ["mid-century", "living room", "modern"]

2. design_elements/herringbone_flooring
   - template: "walnut herringbone wood flooring, chevron pattern"
   - keywords: ["herringbone", "wood flooring", "walnut"]

3. furniture_layouts/l_shape_sofa_tapered
   - template: "L-shaped sofa with tapered walnut legs, low-profile"
   - keywords: ["L-shaped", "sofa", "tapered legs"]

4. design_elements/sputnik_chandelier
   - template: "brass sputnik chandelier, mid-century iconic lighting"
   - keywords: ["sputnik", "chandelier", "brass"]
```

---

### 7. Common Domain (通用攝影)

**提取類別**:
- `camera_angles` - 相機角度
- `photography_techniques` - 攝影技術
- `lighting_techniques` - 光照技術
- `technical_effects` - 技術效果

**示例**:

```
輸入: "Shot with 24mm wide-angle lens, f/2.8 aperture,
       soft natural window light, 8K resolution"

提取:
1. photography_techniques/wide_angle_24mm
   - template: "24mm wide-angle lens, expansive field of view"
   - keywords: ["24mm", "wide-angle", "FOV"]

2. lighting_techniques/soft_window_light
   - template: "soft natural window light, diffused daylight"
   - keywords: ["window light", "natural", "soft", "diffused"]

3. technical_effects/8k_resolution
   - template: "8K ultra high resolution, extreme detail capture"
   - keywords: ["8K", "high resolution", "ultra HD"]
```

---

## 🔍 提取規則

### 規則1: 獨立性
每個元素應該可以獨立使用
- ✅ "large almond eyes with thick lashes"
- ❌ "her eyes were beautiful" (依賴上下文)

### 規則2: 具體性
避免空洞描述
- ✅ "brass sputnik chandelier with 12 arms"
- ❌ "nice lighting fixture" (太籠統)

### 規則3: 可複用性
可以在不同場景使用
- ✅ "geometric patterned area rug" (可用於多種室內)
- ❌ "the rug in my grandmother's house" (太特定)

### 規則4: 長度適中
模板長度15-50詞
- ✅ "mid-century modern walnut coffee table with organic curved edges and tapered legs"
- ❌ "table" (太短)
- ❌ 200詞的詳細描述 (太長)

---

## 📋 提取流程

```python
def extract_elements(prompt_text: str, primary_domain: str) -> List[Dict]:
    elements = []

    # Step 1: 領域特定提取
    if primary_domain == 'product':
        elements.extend(extract_product_elements(prompt_text))
    elif primary_domain == 'design':
        elements.extend(extract_design_elements(prompt_text))
    elif primary_domain == 'art':
        elements.extend(extract_art_elements(prompt_text))
    # ... 其他領域

    # Step 2: 通用攝影技術提取（所有領域）
    elements.extend(extract_common_elements(prompt_text))

    # Step 3: 質量過濾
    elements = [e for e in elements if is_high_quality(e)]

    return elements

def is_high_quality(element: Dict) -> bool:
    # 檢查獨立性、具體性、長度
    template = element['ai_prompt_template']
    word_count = len(template.split())

    if word_count < 5 or word_count > 100:
        return False

    if has_vague_words(template):  # "nice", "good", "beautiful"
        return False

    if has_context_dependency(template):  # "it", "her", "the previous"
        return False

    return True
```

---

## ✅ 輸出格式

```json
{
  "extracted_elements": [
    {
      "category": "product_types",
      "name": "collector_edition_book",
      "chinese_name": "收藏版書籍",
      "ai_prompt_template": "premium collector's edition book, luxury binding, Italian calfskin cover",
      "keywords": ["collector's edition", "premium book", "luxury binding"],
      "estimated_reusability": 7.5,
      "source_context": "A premium collector's edition book..."
    },
    {
      "category": "material_textures",
      "name": "glossy_reflective",
      "chinese_name": "光澤反射材質",
      "ai_prompt_template": "glossy reflective surface, high-end finish, metallic sheen",
      "keywords": ["glossy", "reflective", "shiny", "polished"],
      "estimated_reusability": 8.5,
      "source_context": "glossy reflective surface"
    }
  ],
  "total_extracted": 2
}
```

---

**狀態**: ✅ 已實現
**目標**: 從18個Prompts提取~440個高質量元素
