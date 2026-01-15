# ⚠️ 舊架構 - Builder Module - 提示片語裝模組

> **注意**：這是舊架構模組，屬於prompt-master系統

**功能**: 根據使用者描述智慧組裝完整提示詞
**呼叫方式**: 透過主Skill路由或直接CLI呼叫

---

## 📋 功能概述

Builder模組負責根據使用者的自然語言描述，智慧選擇合適的模組並組裝成完整的提示詞。

---

## 🔧 實現方式

### 方式1: 智慧描述組裝 (`build`命令)

**CLI命令**:
```bash
python3 prompt_tool.py build "使用者描述"
```

**功能**:
- 自動識別關鍵詞（流派、風格）
- 從風格庫中提取五官組合
- 智慧組裝完整提示詞

**示例**:
```bash
python3 prompt_tool.py build "電影級的清純美少女"
```

**輸出**:
```
✓ 識別成功:
  流派: 電影敘事攝影
  風格: 清純少女

📦 五官模組組合:
  性別: 女性
  年齡: 青年（18-25歲）
  人種: 東亞人
  眼型: 大眼杏仁眼
  唇型: 粉嫩光澤唇
  鼻型: 小巧直鼻
  皮膚: 瓷肌無瑕
  表情: 清純溫柔眼神

✨ 組裝後的提示詞:
A beautiful East Asian young woman, large expressive almond eyes, ...
```

### 方式2: 互動式生成 (`generate`命令)

**CLI命令**:
```bash
python3 prompt_tool.py generate
```

**功能**:
- 10步互動式問答
- 使用者自由選擇每個模組
- 即時組裝並顯示結果

**互動流程**:
1. 選擇性別 (2選項)
2. 選擇年齡段 (3選項)
3. 選擇人種 (3選項)
4. 選擇攝影流派 (10選項)
5. 選擇眼型 (4選項)
6. 選擇臉型 (2選項)
7. 選擇唇型 (2選項)
8. 選擇鼻型 (2選項)
9. 選擇皮膚質感 (4選項)
10. 選擇表情 (3選項)

**優勢**:
- 完全自由組合
- 視覺化選項和評分
- 適合新手學習

---

## 📊 組裝邏輯

### 提示詞結構

```
[形容詞] [人種] [性別+年齡], [眼型關鍵詞], [臉型關鍵詞], [唇型關鍵詞], [鼻型關鍵詞], [皮膚關鍵詞], [表情關鍵詞], [技術引數]
```

### 關鍵順序

1. **主體描述** (必須在最前面):
   - 形容詞: "A beautiful" / "A handsome"
   - 人種: "East Asian" / "Caucasian"
   - 性別+年齡: "young woman" / "adult man"

2. **五官細節**:
   - 眼型 → 臉型 → 唇型 → 鼻型 → 皮膚 → 表情

3. **技術引數** (最後):
   - 相機裝置
   - 流派特定關鍵詞
   - 解析度、光照等

---

## 🎯 使用場景

### 場景1: 快速生成 (適合有經驗使用者)

```
使用者: "生成一個性感挑逗風格的提示詞"
→ 呼叫: python3 prompt_tool.py build "性感挑逗"
→ 自動匹配風格並組裝
```

### 場景2: 自由組合 (適合新手或定製需求)

```
使用者: "我想自己選擇每個細節"
→ 呼叫: python3 prompt_tool.py generate
→ 互動式選擇10個模組
```

### 場景3: 部分定製

```
使用者: "電影級美少女，但用白種人"
→ 呼叫: python3 prompt_tool.py build "電影級美少女"
→ 然後手動修改人種為 Caucasian
```

---

## 💡 關鍵詞對映表

### 流派關鍵詞

| 使用者輸入 | 對映到 |
|---------|--------|
| 電影、電影級、cinematic | cinematic_narrative |
| 膠片 | analog_film |
| 人像 | portrait_beauty |
| 商業 | digital_commercial |
| 產品 | studio_product |

### 風格關鍵詞

| 使用者輸入 | 對映到 |
|---------|--------|
| 美少女、少女、清純 | 清純少女 |
| 性感 | 性感挑逗 |
| 優雅、古典 | 古典優雅 |
| cosplay、真人化 | 真人化Cosplay |

---

## 📁 資料依賴

```
facial_features_library.json
├── gender (2分類)
├── age_range (3分類)
├── ethnicity (3分類)
├── eye_types (4分類)
├── face_shapes (2分類)
├── lip_types (2分類)
├── nose_types (2分類)
├── skin_textures (4分類)
├── expressions (3分類)
└── usage_index
    └── by_style_mood (4種風格預設)

module_library.json
├── photography_genres (10流派)
└── camera_equipment_index (裝置庫)
```

---

## ⚠️ 注意事項

1. **人種必須前置**
   - ❌ 錯誤: "A beautiful woman, East Asian features, ..."
   - ✅ 正確: "A beautiful East Asian woman, ..."

2. **避免關鍵詞重複**
   - 使用 `age_based_terms` 避免 "young" 重複

3. **流派與裝置匹配**
   - 電影敘事 → Canon EOS R5
   - 膠片藝術 → Hasselblad + Kodak Portra 400

---

**模組狀態**: ✅ 可用
**CLI命令**: `build`, `generate`
**支援風格**: 4種預設 + 自由組合
