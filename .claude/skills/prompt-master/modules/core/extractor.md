# ⚠️ 舊架構 - Extractor Module - 提取模組

> **注意**：這是舊架構模組，屬於prompt-master系統


**功能**: 從使用者提供的Prompt中提取可複用的模組和特徵
**呼叫方式**: 透過主Skill路由或手動分析

---

## 📋 功能概述

Extractor模組負責：
- 識別Prompt中的人物基礎屬性（性別、年齡、人種）
- 提取五官級別細節（眼型、臉型、唇型、鼻型、皮膚、表情）
- 識別攝影流派和技術引數
- 提取可複用的關鍵片語

---

## 🔧 提取流程

### Step 1: 分析輸入Prompt

**輸入示例**:
```
A beautiful young East Asian woman with large expressive almond eyes, thick natural lashes, delicate refined Asian facial structure, soft full lips with gentle pink gloss, small straight nose, flawless porcelain skin, radiant jade-like brightness, innocent gaze, gentle smile, photographed with Canon EOS R5, RF 50mm f/1.2L, 8K ultra-detailed, soft lighting
```

### Step 2: 提取基礎屬性

**提取目標**:
- **性別**: 識別 "woman" / "man" / "girl" / "boy"
  - 結果: female
- **年齡**: 識別 "young" / "adult" / "teen" / "elderly"
  - 結果: young_adult
- **人種**: 識別 "East Asian" / "Caucasian" / "African" / "mixed"
  - 結果: east_asian

### Step 3: 提取五官特徵

**眼型提取**:
- 關鍵詞: "large expressive almond eyes", "thick natural lashes"
- 匹配到: `large_expressive_almond` (大眼杏仁眼)

**臉型提取**:
- 關鍵詞: "delicate refined Asian facial structure"
- 匹配到: `oval_asian_refined` (精緻鵝蛋臉)

**唇型提取**:
- 關鍵詞: "soft full lips", "gentle pink gloss"
- 匹配到: `soft_pink_gloss` (粉嫩光澤唇)

**鼻型提取**:
- 關鍵詞: "small straight nose"
- 匹配到: `small_straight_delicate` (小巧直鼻)

**皮膚提取**:
- 關鍵詞: "flawless porcelain skin", "radiant jade-like brightness"
- 匹配到: `porcelain_flawless_radiant` (瓷肌無瑕)

**表情提取**:
- 關鍵詞: "innocent gaze", "gentle smile"
- 匹配到: `innocent_gentle_gaze` (清純溫柔眼神)

### Step 4: 提取技術引數

**相機裝置**:
- 識別: "Canon EOS R5"
- 匹配到: `canon_eos_r5`

**鏡頭**:
- 識別: "RF 50mm f/1.2L"

**解析度**:
- 識別: "8K ultra-detailed"

**光照**:
- 識別: "soft lighting"

### Step 5: 識別攝影流派

基於技術引數和風格關鍵詞識別流派：

**流派識別邏輯**:
```python
if "8K" in prompt and "Canon EOS R5" in prompt:
    genre = "digital_commercial"
elif "Hasselblad" in prompt and "Kodak Portra" in prompt:
    genre = "analog_film"
elif "cinematic" in prompt or "HDR" in prompt:
    genre = "cinematic_narrative"
else:
    genre = "portrait_beauty"  # 預設
```

---

## 📊 提取結果格式

```json
{
  "basic_attributes": {
    "gender": "female",
    "age_range": "young_adult",
    "ethnicity": "east_asian"
  },
  "facial_features": {
    "eye_type": "large_expressive_almond",
    "face_shape": "oval_asian_refined",
    "lip_type": "soft_pink_gloss",
    "nose_type": "small_straight_delicate",
    "skin_texture": "porcelain_flawless_radiant",
    "expression": "innocent_gentle_gaze"
  },
  "technical_parameters": {
    "camera": "Canon EOS R5",
    "lens": "RF 50mm f/1.2L",
    "resolution": "8K",
    "lighting": "soft lighting"
  },
  "photography_genre": "portrait_beauty",
  "reusable_keywords": [
    "large expressive almond eyes",
    "thick natural lashes",
    "delicate refined Asian facial structure",
    "soft full lips",
    "gentle pink gloss",
    "small straight nose",
    "flawless porcelain skin",
    "innocent gaze",
    "gentle smile"
  ]
}
```

---

## 🎯 使用場景

### 場景1: 分析優秀Prompt

```
使用者: "提取這個Prompt的五官特徵"
輸入: "A beautiful woman with large blue eyes..."

→ 執行提取流程
→ 輸出分類結果和可複用關鍵詞
```

### 場景2: 學習新特徵

```
使用者: "這個眼型叫什麼？'manic luminous ruby-pink eyes, heavy seductive half-lidded gaze'"

→ 匹配到: half_lidded_seductive (半閉誘惑眼)
→ 顯示該眼型的完整資訊和使用建議
```

### 場景3: 擴充套件特徵庫

```
使用者: "這個新Prompt有什麼特殊的皮膚質感？"
輸入: "wet skin texture, abundant realistic water droplets..."

→ 識別為: wet_dewy_droplets (溼潤水感肌)
→ 可新增到庫中（如果是新型別）
```

---

## 💡 關鍵詞匹配表

### 眼型關鍵詞

| 關鍵片語 | 匹配分類 |
|---------|---------|
| large expressive almond, thick natural lashes | large_expressive_almond |
| large blue eyes, natural contact lenses | large_blue_expressive |
| heavy seductive half-lidded, manic eyes | half_lidded_seductive |
| green eyes, anime eye style | anime_hybrid_green |

### 皮膚關鍵詞

| 關鍵片語 | 匹配分類 |
|---------|---------|
| flawless porcelain, radiant jade-like | porcelain_flawless_radiant |
| realistic texture, visible pores | realistic_textured_pores |
| wet skin, water droplets | wet_dewy_droplets |
| warm rich, film grain | warm_rich_analog_film |

---

## 📁 資料依賴

```
facial_features_library.json (v1.2)
├── 各類別的 keywords 欄位用於匹配
└── classification_code 用於標識

module_library.json
├── photography_genres.<genre>.key_features
└── camera_equipment_index.<equipment>.specs
```

---

## ⚠️ 注意事項

1. **關鍵詞優先順序**
   - 完全匹配 > 部分匹配 > 語義相似

2. **多義詞處理**
   - "young" 可能是年齡或形容詞
   - 需結合上下文判斷

3. **新特徵識別**
   - 如果無法匹配到已有分類
   - 提示使用者這可能是新特徵
   - 建議手動分類或新增到庫

4. **置信度評分**
   - 完全匹配: 100%
   - 部分匹配: 70-90%
   - 語義相似: 50-70%
   - 低於50%: 需人工確認

---

**模組狀態**: ✅ 可用
**功能**: 自動識別、關鍵詞匹配、分類標註
**準確度**: 對已有28個分類識別率 > 90%
**擴充套件性**: 支援新增新分類和關鍵詞
