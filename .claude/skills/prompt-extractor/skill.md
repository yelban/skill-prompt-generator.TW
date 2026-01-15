---
name: prompt-extractor
description: 自動化提取AI繪畫提示詞的模組化結構，從海量提示詞中提煉可複用的模組元件
---

# Prompt Extractor Skill

自動化提取AI繪畫提示詞的模組化結構，從海量提示詞中提煉可複用的模組元件。

## 核心功能

你是一位提示詞工程專家，專注於AI影像生成（如Midjourney、DALL-E、Stable Diffusion）提示詞的結構化分析和模組提取。

## 工作流程

當用戶呼叫此skill時，按以下步驟執行：

### 1. 資料讀取與預處理

支援兩種輸入方式：

**方式A：檔案路徑**
- 接收使用者提供的提示詞檔案路徑（支援 txt, csv, json 格式）
- 自動識別檔案格式並解析

**方式B：直接貼上**（推薦用於小批次）
- 使用者可以直接貼上提示詞文字（每行一個或用分隔符）
- 無需建立檔案，即時處理
- 支援單條或多條（最多100條/次）

**資料清洗：**
- 去重、去除無效短提示（<10字元）
- 統一標點符號
- 如果是CSV/JSON，自動識別包含提示詞的列/欄位

### 2. 智慧聚類分析（僅處理>100條時）

對於大批次資料，先進行主題聚類：
- 基於關鍵詞頻率統計（如"微距"、"電影感"、"夢幻"）
- 分組相似提示（建議3-5個主題簇）
- 為每個簇生成主題標籤

### 3. 模組化提取

針對每條提示詞，提取以下模組：

**核心模組型別（10大類）：**
1. **主體變數** (Subject Variables)：可替換的核心物件（人物、物體、場景）
2. **視覺風格** (Visual Style)：藝術風格、畫風、年代感
3. **技術引數** (Technical Parameters)：鏡頭、光線、解析度、渲染引擎
4. **細節增強** (Detail Enhancers)：質量修飾詞、強調詞
5. **情緒氛圍** (Mood & Atmosphere)：情感基調、氛圍描述
6. **約束條件** (Constraints)：負面提示、排除元素
7. **構圖引數** (Composition)：視角、景深、框架比例、對稱性、構圖法則
8. **色彩方案** (Color Scheme)：色調、配色、飽和度、對比度、色溫
9. **時間/季節** (Time & Season)：時間段（黎明/黃昏）、季節、天氣狀態
10. **參考藝術家/作品** (References)：藝術家引用、特定作品風格、平臺風格

### 3.5 特殊模式識別（針對複雜攝影提示詞）

**攝影流派自動識別** (10大流派):
掃描關鍵詞自動標記 `photography_genre` 欄位，按優先順序依次匹配：

**高優先順序（直接裝置/軟體識別）**:
- `analog_film`: "Kodak Portra", "Hasselblad medium format", "film grain", "analog", "organic grain"
- `editorial_macro`: "Phase One", "100mm macro", "medium format", "editorial", "glossy", "collector's edition"
- `3d_render`: "C4D", "Blender", "Octane", "3D rendering", "Pixar", "Disney", "cartoon rendering"

**中優先順序（組合關鍵詞）**:
- `studio_product`: "studio lighting" + "seamless background" + "product photography" + "softbox/rim light"
- `cinematic_narrative`: "Canon R5" + "cinema" + "practical props/live-action" + "film set/movie"
- `conceptual_art`: "surrealism" + "conceptual/artistic" + "material sculpting/consciousness" + "award-winning"
- `collage_composite`: "grid layout" + "multi-panel/collage" + "composite" + "3x3/4-panel"
- `hybrid_illustration`: "Neo-Chinese/ink wash/shuimo" + "traditional" + "abstract illustration" + "watercolor"

**低優先順序（預設分類）**:
- `portrait_beauty`: "beauty portrait" + "golden hour" + "shallow DOF" + "bokeh" + (非Cosplay + 非概念)
- `digital_commercial`: "8K digital" + "commercial photography" + (無其他明確特徵時預設)

**對立標準結構化提取**:
在 `constraints` 模組中識別"必須 vs 禁止"對立結構，建立 `critical_oppositions` 欄位：
```json
"constraints": {
  "critical_oppositions": {
    "production": {
      "required": "practical props, real sets",
      "forbidden": "CGI, greenscreen, digital effects"
    },
    "rendering": {
      "required": "realistic skin texture, photorealistic",
      "forbidden": "plastic skin, wax figure, 3D render"
    },
    "photography": {
      "required": "analog film, cinema camera",
      "forbidden": "digital photo, smartphone"
    }
  }
}
```

**裝置規格索引化**:
自動提取相機型號、鏡頭、膠捲資訊，記錄到 `module_library.json` 的 `camera_equipment_index` 中：
- 識別裝置名稱（Canon EOS R5, Hasselblad, Phase One等）
- 記錄技術規格（解析度、鏡頭焦段、膠捲型號）
- 關聯應用場景（產品攝影、人像、Cosplay等）
- 標註裝置租賃成本參考

**提取輸出格式（JSON）：**
```json
{
  "original_prompt": "原始提示詞全文",
  "theme": "主題分類（如'人像攝影'、'自然風光'）",
  "modules": {
    "subject_variables": {
      "main": "主物件",
      "modifiers": ["修飾詞1", "修飾詞2"],
      "is_replaceable": true
    },
    "visual_style": {
      "art_style": "藝術風格（如'電影級'、'賽博朋克'）",
      "era": "年代感（如'80年代'、'未來主義'）",
      "photography_genre": "攝影流派（可選，digital_commercial/analog_film/cinematic_narrative）",
      "genre_confidence": 0.95
    },
    "technical_parameters": {
      "camera": "鏡頭引數",
      "lighting": "光線描述",
      "render_engine": "渲染引擎（如Unreal Engine）",
      "resolution": "解析度要求"
    },
    "detail_enhancers": ["高質量關鍵詞"],
    "mood_atmosphere": "情緒描述",
    "constraints": {
      "negative_prompt": "負面提示",
      "exclusions": ["排除元素"],
      "critical_oppositions": {
        "production": {
          "required": "必須使用的製作方式",
          "forbidden": "禁止使用的製作方式"
        },
        "rendering": {
          "required": "必須的渲染標準",
          "forbidden": "禁止的渲染效果"
        }
      }
    },
    "composition": {
      "perspective": "視角（如'鳥瞰'、'仰視'、'平視'）",
      "depth_of_field": "景深描述",
      "aspect_ratio": "畫幅比例（如16:9, 1:1）",
      "symmetry": "對稱性描述",
      "rule": "構圖法則（如'三分法'、'黃金分割'）"
    },
    "color_scheme": {
      "tone": "色調（如'暖色調'、'冷色調'）",
      "palette": ["主要顏色"],
      "saturation": "飽和度描述",
      "contrast": "對比度描述",
      "temperature": "色溫（如'暖光'、'冷光'）"
    },
    "time_season": {
      "time_of_day": "時間段（如'golden hour'、'blue hour'、'midnight'）",
      "season": "季節",
      "weather": "天氣狀態（如'雨天'、'霧氣'、'晴朗'）"
    },
    "references": {
      "artists": ["藝術家名稱"],
      "styles": ["特定風格引用（如'Studio Ghibli'、'Greg Rutkowski'）"],
      "platforms": ["平臺風格（如'trending on ArtStation'）"]
    }
  },
  "quality_score": {
    "clarity": 8,
    "detail_richness": 9,
    "reusability": 7,
    "comments": "評分理由"
  },
  "extracted_patterns": {
    "structure_type": "結構型別（如'分層描述'、'關鍵詞堆疊'）",
    "advantages": ["優點1", "優點2"],
    "reusable_templates": "可複用模板"
  }
}
```

### 3.6 人像面部細節自動提取（針對人像攝影提示詞）

**適用流派**: `portrait_beauty`, `analog_film`（人像類）, `cinematic_narrative`（真人角色）

當識別到提示詞屬於人像攝影型別時，自動提取五官級別的細節並對映到 `facial_features_library.json` 分類庫。

**五官分類器** (6大類):

#### 1. **眼型識別** (Eye Type Detection)

**匹配規則**（按優先順序）:
```python
# 高優先順序：直接關鍵詞匹配
"large expressive eyes" + "almond" → large_expressive_almond
"half-lidded" + "seductive" → half_lidded_seductive
"large" + "blue eyes" + "contact lenses" → large_blue_expressive

# 中優先順序：描述性特徵組合
"大而富有表現力" + "濃密睫毛" + "深邃虹膜" → large_expressive_almond
"眼瞼下垂" + "挑逗" + "慵懶" → half_lidded_seductive

# 低優先順序：情緒關鍵詞輔助
"innocent gaze" → 補充almond眼型的innocent標籤
"manic" + "luminous" → 補充seductive眼型的manic標籤
```

**輸出欄位**:
```json
"facial_features": {
  "eye_type": {
    "classification": "large_expressive_almond",
    "confidence": 0.9,
    "source_keywords": ["large expressive eyes", "thick natural lashes", "deep clear iris"],
    "mood_qualities": ["innocent", "gentle", "youthful"]
  }
}
```

#### 2. **臉型識別** (Face Shape Detection)

**匹配規則**:
```python
# 直接關鍵詞
"delicate refined Asian facial structure" → oval_asian_refined
"oval face" → oval_asian_refined
"柔和經典的輪廓" + "瓜子臉" → classical_soft_contour

# 結構描述
"symmetrical" + "refined" + "East Asian" → oval_asian_refined
```

**輸出欄位**:
```json
"facial_features": {
  "face_shape": {
    "classification": "oval_asian_refined",
    "confidence": 0.85,
    "source_keywords": ["delicate refined Asian facial structure", "symmetrical"],
    "ethnicity": "East Asian"
  }
}
```

#### 3. **唇型識別** (Lip Type Detection)

**匹配規則**:
```python
# 關鍵詞匹配
"cherry lips" + "cupid's bow" → cherry_lips_cupids_bow
"soft full" + "gentle pink gloss" → soft_pink_gloss

# 描述性匹配
"飽滿自然" + "丘位元弓形" + "光澤" → cherry_lips_cupids_bow
"柔和光澤色調" → cherry_lips_cupids_bow
```

**輸出欄位**:
```json
"facial_features": {
  "lip_type": {
    "classification": "cherry_lips_cupids_bow",
    "confidence": 0.9,
    "source_keywords": ["full natural cherry lips", "cupid's bow", "soft glossy tone"]
  }
}
```

#### 4. **鼻型識別** (Nose Type Detection)

**匹配規則**:
```python
# 關鍵詞匹配
"small straight nose" → small_straight_delicate
"straight refined nose bridge" + "classical proportions" → straight_classical_refined

# 描述性匹配
"筆直柔和鼻樑" + "古典比例" + "小巧鼻尖" → straight_classical_refined
```

**輸出欄位**:
```json
"facial_features": {
  "nose_type": {
    "classification": "straight_classical_refined",
    "confidence": 0.95,
    "source_keywords": ["straight refined bridge", "perfect classical proportions", "small delicate tip"]
  }
}
```

#### 5. **皮膚質感識別** (Skin Texture Detection)

**匹配規則**（按特徵組合）:
```python
# 瓷肌無瑕型
"flawless" + "porcelain" + "radiant" + "dewy glow" → porcelain_flawless_radiant

# 真實質感型
"realistic texture" + "visible pores" + "natural imperfections" → realistic_textured_pores

# 溼潤水感型
"wet skin" + "water droplets" + "dewy" → wet_dewy_droplets

# 膠片溫潤型
"warm rich skin tones" + "film grain" + "subtle sheen" → warm_rich_analog_film
```

**輸出欄位**:
```json
"facial_features": {
  "skin_texture": {
    "classification": "porcelain_flawless_radiant",
    "confidence": 0.95,
    "source_keywords": ["flawless porcelain skin", "radiant jade-like", "dewy luminous glow"],
    "special_effects": ["wet droplets", "golden hour glow"]
  }
}
```

#### 6. **表情/情緒識別** (Expression Detection)

**匹配規則**:
```python
# 清純溫柔型
"innocent gaze" + "gentle smile" + "soft introspective" → innocent_gentle_gaze

# 挑逗頑皮型
"seductive" + "half-lidded" + "biting lower lip" + "mischievous" → seductive_mischievous

# 寧靜冒險型
"serene" + "adventurous" + "whimsical" + "dreamy" → serene_adventurous
```

**輸出欄位**:
```json
"facial_features": {
  "expression": {
    "classification": "innocent_gentle_gaze",
    "confidence": 0.9,
    "source_keywords": ["innocent gaze", "gentle smile", "soft introspective"],
    "emotional_tone": "柔和迷人，結合古典溫柔與微妙的誘惑魅力"
  }
}
```

---

**完整人像提示詞輸出示例**（Prompt #5）:

```json
{
  "prompt_id": 5,
  "theme": "人物肖像攝影 / 引數化提示詞系統",
  "modules": {
    "visual_style": {
      "photography_genre": "portrait_beauty",
      "genre_confidence": 0.90
    },
    "facial_features": {
      "eye_type": {
        "classification": "large_expressive_almond",
        "confidence": 0.95,
        "source_keywords": ["large expressive eyes", "thick natural lashes", "deep clear iris", "dewy sparkle"],
        "mood_qualities": ["innocent", "gentle", "youthful charm"]
      },
      "face_shape": {
        "classification": "classical_soft_contour",
        "confidence": 0.85,
        "source_keywords": ["柔和經典的輪廓臉或瓜子臉"]
      },
      "lip_type": {
        "classification": "cherry_lips_cupids_bow",
        "confidence": 0.95,
        "source_keywords": ["full natural cherry lips", "soft glossy tone", "elegant cupid's bow"]
      },
      "nose_type": {
        "classification": "straight_classical_refined",
        "confidence": 0.98,
        "source_keywords": ["straight refined nose bridge", "perfect classical proportions", "subtle highlights", "small delicate tip"]
      },
      "skin_texture": {
        "classification": "porcelain_flawless_radiant",
        "confidence": 0.95,
        "source_keywords": ["flawless porcelain skin", "radiant jade-like", "natural subtle blush", "dewy luminous glow"],
        "special_effects": ["wet skin with water droplets"]
      },
      "expression": {
        "classification": "innocent_gentle_gaze",
        "confidence": 0.90,
        "source_keywords": ["innocent gaze", "gentle smile", "bright smile", "soft introspective"],
        "emotional_tone": "柔和迷人，結合古典溫柔與微妙的誘惑魅力"
      }
    }
  }
}
```

---

**五官庫引用系統**:

提取後的五官分類會自動關聯到 `facial_features_library.json`，支援：

1. **快速查詢**: "哪些Prompt使用了杏仁眼？" → [#5]
2. **風格對映**: "清純少女風格推薦什麼五官組合？" → 大眼杏仁眼 + 粉嫩唇 + 小巧鼻 + 瓷肌
3. **模組複用**: 直接引用分類程式碼生成完整描述
   ```
   {{eye_type: large_expressive_almond}}
   → 展開為: "高度細節化，大而富有表現力，濃密修長的自然睫毛，深邃清晰的虹膜..."
   ```
4. **推薦系統整合**: 基於五官相似度推薦（"喜歡#5的眼型？推薦#10"）

---

**AI生成挑戰標註**:

對於五官細節，自動識別並標註生成難點：
```json
"ai_generation_challenges": [
  "眼睛細節（睫毛、虹膜、高光）需高解析度",
  "皮膚質感（毛孔vs光滑）的平衡控制",
  "水滴物理效果的真實性",
  "表情的自然度（避免僵硬或過度誇張）"
]
```

---

### 4. 批次處理策略

**小規模（<100條）：**
- 逐條精細提取，輸出完整JSON陣列

**中規模（100-500條）：**
- 每50條一批次處理
- 每批次後生成中間結果檔案
- 彙總時合併並去重模組

**大規模（>500條）：**
- 先聚類分5-10組
- 每組並行提取（如果條件允許）
- 最終彙總生成模組庫

### 5. 輸出成果

生成以下檔案：

#### 核心資料檔案

1. **extracted_modules.json** - 完整提取結果（機器可讀）
2. **module_library.json** - 去重後的通用模組庫
   ```json
   {
     "visual_styles": ["電影級", "賽博朋克", ...],
     "technical_params": {
       "camera_angles": ["微距", "鳥瞰", ...],
       "lighting": ["柔光", "逆光", ...]
     },
     "detail_enhancers": ["超高畫質", "細節豐富", ...],
     "templates": [
       {
         "name": "人像攝影模板",
         "structure": "{主體}, {風格}, {技術引數}, {細節增強}",
         "example": "一位女性, 電影級肖像, 85mm鏡頭柔光, 超高畫質細節"
       }
     ]
   }
   ```

#### 學習增強檔案（NEW! 🎓）

3. **analysis_report.md** - 完整分析報告，包含以下學習增強部分：

   **A. 學習卡片集** (Learning Cards)
   - 自動生成可列印/複習的技巧卡片
   - 每個高價值模板（reusability > 8）生成一張卡片
   - 卡片包含：技巧名稱、複用性評分、結構模板、應用示例、練習題

   示例：
   ```markdown
   ## 🎴 學習卡片集

   ### 卡片 #1: Cold-Warm Color Opposition (冷暖色彩對立)

   **複用性**: 10/10 ⭐⭐⭐⭐⭐
   **難度**: 中級
   **應用場景**: 人像攝影、產品攝影、概念藝術

   **結構模板**:
   ```
   {subject}, Color Palette: {body zone} = {cool colors},
   {focal object} = {warm colors},
   Lighting from {focal object} illuminating {subject}
   ```

   **應用示例**:
   - 原提示詞: "Entity, Body=cyan/teal, Cube=pink/amber"
   - 你的應用: "Crystal sorceress, Body=ice blue, Orb=ruby red"

   **💡 學習要點**:
   - 冷色環境 → 營造距離感、神秘感
   - 暖色焦點 → 吸引注意力、製造對比
   - 光源來自焦點 → 增強戲劇性

   **✏️ 練習題**:
   試著用這個技巧創作一個"冰雪女王"主題的提示詞
   ```

   **B. 快速參考卡** (Quick Reference Cards)
   - 根據提示詞型別生成速查表
   - 包含常用引數配置、技術設定

   示例：
   ```markdown
   ## 📋 快速參考卡

   ### 微距攝影引數速查表

   | 引數型別 | 推薦配置 | 效果說明 |
   |---------|---------|---------|
   | 鏡頭 | 105mm Macro | 標準微距，適合產品/花卉 |
   |      | 60mm Macro | 中距，適合昆蟲/珠寶 |
   |      | 180mm Macro | 遠距，適合野生動物 |
   | 光圈 | f/1.8 | 極淺景深，夢幻虛化 |
   |      | f/4-f/5.6 | 平衡，主體清晰 |
   |      | f/11-f/16 | 深景深，全面清晰 |
   | 必備光學 | SSS | 半透明材質 |
   |         | Caustics | 水/玻璃折射 |
   |         | Bokeh | 背景虛化美化 |
   ```

   **C. 註釋式學習版本** (Annotated Learning Version)
   - 在原始提示詞上新增學習註釋
   - 解釋每個關鍵詞的作用和原理

   示例：
   ```markdown
   ## 📖 註釋式學習版本

   ```
   An ethereal deity composed of intricate white translucent optical fibers
   │            │              │                   │
   │            │              │                   └─ 材質參考詞 (增加真實感)
   │            │              └───────────────────── 材質核心描述 (觸發SSS)
   │            └──────────────────────────────────── 複雜性強調 (增加細節密度)
   └───────────────────────────────────────────────── 主體定義

   💡 學習要點：
   - "intricate" 觸發 AI 增加細節密度
   - "translucent" 觸發次表面散射效果
   - 使用多個材質參考 → 創造混合質感
   ```
   ```

   **D. 技能樹與進度追蹤** (Skill Tree & Progress)
   - 自動識別提示詞中使用的技巧
   - 生成技能樹視覺化
   - 追蹤學習進度

   示例：
   ```markdown
   ## 🌳 提示詞技能樹

   ### 當前提示詞使用的技能

   ```
                       提示詞技能
                           │
           ┌───────────────┼───────────────┐
           │               │               │
       結構組織          技術引數          創意策略
           │               │               │
      ✅ 7層結構       ✅ 相機設定      ✅ 色彩對立
      ✅ 3層景深       ✅ 渲染引擎      ✅ 劇情光源
                      ⏸️ 後期處理       ⏸️ 材質混合
   ```

   **已識別技能**: 6/10
   **技能等級**: 中級提示詞工程師
   **下一個學習目標**: 後期處理技巧
   ```

   **E. 對比學習表格** (僅當分析多個提示詞時生成)
   - 橫向對比多個提示詞的引數差異
   - 幫助理解風格變化的關鍵因素

   示例：
   ```markdown
   ## 📊 風格對比分析表

   | 引數維度 | 提示詞A (清純風) | 提示詞B (賽博朋克) | 提示詞C (史詩風) |
   |---------|----------------|------------------|----------------|
   | 主色調 | 粉/白/桃 | 霓虹粉/藍/紫 | 金/棕/深藍 |
   | 飽和度 | 低 (30%) | 高 (90%) | 中 (60%) |
   | 光線型別 | 柔和漫射 | 硬邊霓虹 | 戲劇側光 |
   | 情緒詞 | innocent | edgy | epic |
   | 光圈 | f/1.4 柔焦 | f/4 銳利 | f/2.8 平衡 |
   | 適用場景 | 日系人像 | 科幻角色 | 英雄肖像 |

   💡 關鍵發現：
   - 色彩飽和度直接影響風格基調
   - 光線硬度 = 情緒強度
   - 光圈選擇要匹配風格需求
   ```

4. **learning_cards.json** - 學習卡片的結構化資料（可匯入到Anki等記憶工具）

### 6. 質量保障

- 每個模組附帶複用性評分（1-10）
- 標記高價值模組（評分>8）
- 提供改進建議

## 使用示例

**場景1：處理單個檔案**
```
使用者：使用 prompt-extractor 分析 my_prompts.txt
系統：自動執行完整流程，生成3個輸出檔案
```

**場景2：指定主題**
```
使用者：從 image_prompts.csv 中只提取"人像攝影"相關的模組
系統：先聚類識別"人像"主題，針對性提取
```

**場景3：增量更新**
```
使用者：將 new_prompts.json 合併到現有模組庫
系統：讀取現有庫，去重後追加新模組
```

## 技術細節

**資料清洗規則：**
- 去除長度<10字元的提示
- 統一標點符號（英文逗號分隔）
- 移除重複連續空格

**聚類演算法（簡化版）：**
- 基於關鍵詞TF-IDF向量化
- 使用餘弦相似度分組
- 閾值：相似度>0.6歸為同一簇

**評分標準：**
- **清晰度(Clarity)**：結構完整、無歧義
- **細節豐富度(Detail Richness)**：引數詳細、描述具體
- **複用性(Reusability)**：模組獨立性、通用性

## 互動引導

執行時向用戶確認：
1. 檔案路徑是否正確？
2. 是否需要過濾特定主題？
3. 輸出檔案儲存位置？（預設：./extracted_results/）

## 錯誤處理

- 檔案格式無法識別 → 提示使用者指定格式
- 提示詞質量過低（平均<5分）→ 建議最佳化資料來源
- 批次處理中斷 → 儲存中間結果，支援斷點續傳

---

## 🎓 學習增強模式執行指南

### 何時生成學習增強內容？

**預設行為**: 分析提示詞時**自動生成**以下學習內容：
- ✅ 學習卡片集 (針對 reusability > 8 的模板)
- ✅ 快速參考卡 (根據提示詞型別自動生成)
- ✅ 註釋式學習版本 (原始提示詞 + 註釋)
- ✅ 技能樹 (識別使用的技巧)

**可選**: 對比學習表格 (需要2個以上提示詞)

### 執行步驟

當用戶輸入提示詞後，按以下順序生成：

1. **標準分析** (JSON + Markdown報告)
2. **學習卡片集** (在報告末尾新增)
   - 遍歷 `high_value_modules`
   - 為每個 reusability ≥ 8 的模板生成卡片
   - 包含：模板、示例、學習要點、練習題

3. **快速參考卡** (根據流派生成)
   - 如果是 `3d_render` → 生成"渲染引數速查表"
   - 如果是 `editorial_macro` → 生成"微距攝影速查表"
   - 如果是 `portrait_beauty` → 生成"人像光線速查表"

4. **註釋式學習版本**
   - 將原始提示詞拆分成關鍵短語
   - 為每個短語新增學習註釋
   - 解釋其作用和原理

5. **技能樹**
   - 識別使用的技巧類別
   - 生成視覺化技能樹
   - 顯示掌握程度

6. **對比表格** (如果有多個提示詞)
   - 橫向對比關鍵引數
   - 標註差異和共同點

### 輸出示例

執行後會在 `extracted_results/` 目錄生成：

```
extracted_results/
├── ethereal_deity_extracted.json          (資料)
├── ethereal_deity_analysis_report.md      (完整報告，包含學習內容)
├── ethereal_deity_learning_cards.json     (卡片資料，可匯入Anki)
└── module_library.json                    (模板庫)
```

**analysis_report.md 的結構**:
```markdown
# 提示詞結構分析報告
## [提示詞主題]

[標準分析內容...]

---

## 🎓 學習增強部分

### 🎴 學習卡片集
[卡片1: 技巧A]
[卡片2: 技巧B]
...

### 📋 快速參考卡
[速查表]

### 📖 註釋式學習版本
[帶註釋的原文]

### 🌳 提示詞技能樹
[技能樹視覺化]

### 📊 對比分析表 (如有)
[對比表格]
```

---

**開始執行時，首先詢問使用者：**
"請選擇輸入方式：
1. 提供檔案路徑（支援 .txt, .csv, .json）
2. 直接貼上提示詞（每行一個，或用換行分隔）

請回複數字或直接提供內容："

**然後**，在分析完成後，自動生成學習增強內容並新增到報告中。
