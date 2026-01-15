# ⚠️ 舊架構 - Recommender Module - 推薦模組

> **注意**：這是舊架構模組，屬於prompt-master系統


**功能**: 推薦相似或相關的提示詞和模組
**呼叫方式**: 透過主Skill路由或直接CLI呼叫

---

## 📋 功能概述

Recommender模組基於相似度演算法推薦：
- 相似的Prompts（基於流派、裝置、主題）
- 相關的五官模組組合
- 適合的攝影流派和裝置

---

## 🔧 CLI命令

### 1. 推薦相似Prompts

**命令**:
```bash
python3 prompt_tool.py recommend <id> [-n <數量>]
```

**示例**:
```bash
python3 prompt_tool.py recommend 5 -n 3
```

**輸出**:
```
🔍 為 Prompt #5 (清純少女古典美) 推薦相關提示詞

[1] #18 Princess Peach真人化
    相似度: 75%
    理由: 同為清純少女風格 + 同用East Asian人種

[2] #10 溫柔少女人像
    相似度: 65%
    理由: 同為人像美容攝影 + 主題相關

[3] #17 性感朋克Jinx
    相似度: 45%
    理由: 同為年輕女性人像（風格差異大）
```

---

## 📊 推薦演算法

### 相似度計算

基於以下維度計算相似度：

| 維度 | 權重 | 說明 |
|------|------|------|
| 攝影流派 | 50% | 流派相同得分最高 |
| 相機裝置 | 30% | 裝置相同說明技術相似 |
| 主題關鍵詞 | 20% | 主題相關性 |

**計算邏輯**:
```python
score = 0.0
reasons = []

# 流派相同 +0.5
if current_genre == candidate_genre:
    score += 0.5
    reasons.append(f"同為{genre_name}")

# 裝置相同 +0.3
if current_camera == candidate_camera:
    score += 0.3
    reasons.append(f"同用{camera_name}")

# 主題相關 +0.2
if theme_keywords_match:
    score += 0.2
    reasons.append("主題相關")

similarity = score * 100  # 轉換為百分比
```

---

## 🎯 使用場景

### 場景1: 尋找相似風格

```
使用者: "推薦與Prompt #5相似的提示詞"
→ 呼叫: python3 prompt_tool.py recommend 5
→ 獲取Top 3相似Prompts
```

### 場景2: 發現新風格

```
使用者: "我喜歡Prompt #17，還有類似的嗎？"
→ 呼叫: python3 prompt_tool.py recommend 17
→ 發現性感、叛逆風格的其他Prompts
```

### 場景3: 學習特定流派

```
使用者: "哪些Prompts屬於電影敘事攝影？"
→ 呼叫: python3 prompt_tool.py search --genre cinematic_narrative
→ 檢視該流派的所有Prompts
```

---

## 💡 推薦策略

### 1. 基於流派推薦

**最準確**: 流派相同的Prompts技術風格最接近
```
電影敘事攝影 → Prompt #18, #11
膠片藝術攝影 → Prompt #17
人像美容攝影 → Prompt #5, #10
```

### 2. 基於裝置推薦

**技術維度**: 裝置相同說明技術引數接近
```
Canon EOS R5 → #5, #18, #11
Hasselblad + Kodak Portra 400 → #17
```

### 3. 基於主題推薦

**內容維度**: 主題關鍵詞重疊
```
清純少女 → #5, #18
性感挑逗 → #17
角色Cosplay → #18, #11
```

---

## 📁 資料依賴

```
extracted_modules.json
├── prompt_id
├── theme
├── modules.visual_style.photography_genre
└── modules.technical_parameters.camera

module_library.json
├── photography_genres.<genre>.prompts
└── camera_equipment_index.<equipment>.prompts
```

---

## ⚠️ 注意事項

1. **相似度閾值**
   - > 70%: 高度相似，強推薦
   - 50-70%: 中度相似，可參考
   - < 50%: 低相似度，僅作參考

2. **多維度平衡**
   - 流派相同但主題不同 → 可學習技術
   - 主題相似但流派不同 → 可嘗試新風格

3. **推薦數量**
   - 預設推薦Top 3
   - 可透過 `-n` 引數調整（最多10個）

---

**模組狀態**: ✅ 可用
**CLI命令**: `recommend`, `search`
**推薦維度**: 流派、裝置、主題
**演算法**: 多維度加權相似度
