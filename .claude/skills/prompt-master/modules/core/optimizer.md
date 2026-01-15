# ⚠️ 舊架構 - Optimizer Module - 最佳化模組

> **注意**：這是舊架構模組，屬於prompt-master系統


**功能**: 最佳化和增強使用者提供的提示詞
**呼叫方式**: 透過主Skill路由或手動最佳化

---

## 📋 功能概述

Optimizer模組負責：
- 檢測提示詞缺失的關鍵資訊
- 最佳化詞彙順序（人種前置）
- 增強細節描述
- 修正常見錯誤
- 提供改進建議

---

## 🔧 最佳化流程

### Step 1: 診斷問題

**檢查清單**:

| 檢查項 | 問題示例 | 嚴重性 |
|--------|---------|--------|
| 人種缺失 | "A beautiful woman, large eyes..." | ⚠️ 高 |
| 人種位置錯誤 | "A woman, East Asian features..." | ⚠️ 中 |
| 年齡缺失 | "A woman with..." | ⚠️ 中 |
| 五官描述過於簡單 | "large eyes" (缺少細節) | ⚠️ 低 |
| 關鍵詞重複 | "young woman, youthful..." | ⚠️ 低 |
| 技術引數缺失 | 無相機、解析度 | ℹ️ 資訊 |

### Step 2: 應用最佳化規則

#### 規則1: 補充缺失的基礎屬性

**最佳化前**:
```
A beautiful woman, large eyes, soft lips
```

**問題診斷**:
- ❌ 缺少人種
- ❌ 缺少年齡
- ⚠️ 眼型描述過於簡單

**最佳化後**:
```
A beautiful East Asian young woman, large expressive almond eyes, thick natural lashes, deep clear iris, soft full lips with gentle pink gloss
```

**改進說明**:
- ✅ 新增人種 "East Asian"
- ✅ 新增年齡 "young"
- ✅ 增強眼型細節 "expressive almond", "thick natural lashes", "deep clear iris"
- ✅ 增強唇型細節 "soft full", "gentle pink gloss"

#### 規則2: 修正順序錯誤

**最佳化前**:
```
A woman with expressive eyes, East Asian features, young and beautiful
```

**問題診斷**:
- ❌ 人種位置錯誤（應在最前面）
- ❌ 年齡位置錯誤
- ❌ "beautiful" 應在主體描述最前面

**最佳化後**:
```
A beautiful young East Asian woman, large expressive eyes
```

**修正邏輯**:
```
正確順序: [形容詞] [人種] [性別+年齡], [五官細節]
          ↓        ↓      ↓
      A beautiful  East Asian  young woman
```

#### 規則3: 去除重複詞彙

**最佳化前**:
```
A beautiful young East Asian young woman, youthful appearance
```

**問題診斷**:
- ❌ "young" 重複出現

**最佳化後**:
```
A beautiful East Asian young woman, youthful appearance
```

#### 規則4: 增強細節描述

**最佳化前**:
```
A woman with blue eyes
```

**最佳化後**:
```
A beautiful young East Asian woman, large expressive blue eyes (natural contact lenses), photorealistic eye texture, bright blue iris
```

**增強策略**:
- 從特徵庫中提取完整關鍵片語
- 新增技術細節（如 "natural contact lenses" 使藍眼更真實）
- 增加質感描述（如 "photorealistic eye texture"）

#### 規則5: 新增技術引數

**最佳化前**:
```
A beautiful East Asian young woman, large eyes, soft skin
```

**最佳化後**:
```
A beautiful East Asian young woman, large expressive almond eyes, thick natural lashes, flawless porcelain skin, radiant glow, photographed with Canon EOS R5, RF 50mm f/1.2L, 8K ultra-detailed, soft lighting, professional portrait photography
```

**新增內容**:
- ✅ 相機裝置（基於風格推薦）
- ✅ 解析度
- ✅ 光照描述
- ✅ 流派關鍵詞

---

## 📊 最佳化級別

### 級別1: 基礎修正 (必須)

**修正內容**:
- 補充人種（如果缺失）
- 修正人種位置（移到最前面）
- 補充年齡（如果缺失）
- 補充性別（如果缺失）

**適用場景**: 所有不完整的提示詞

### 級別2: 細節增強 (推薦)

**增強內容**:
- 從簡單描述擴充套件到完整關鍵片語
  - "large eyes" → "large expressive almond eyes, thick natural lashes, deep clear iris"
- 新增質感描述
  - "soft skin" → "flawless porcelain skin, radiant jade-like brightness, natural subtle blush"

**適用場景**: 描述過於簡單的提示詞

### 級別3: 技術最佳化 (可選)

**新增內容**:
- 相機裝置
- 解析度
- 光照描述
- 流派關鍵詞

**適用場景**: 需要專業攝影效果的提示詞

---

## 🎯 使用場景

### 場景1: 快速修正錯誤

```
使用者: "最佳化這個提示詞: A woman with eyes"

診斷:
- ❌ 缺少人種、年齡
- ❌ 眼型描述過於簡單

最佳化結果:
A beautiful East Asian young woman, large expressive almond eyes, thick natural lashes, deep clear iris, dewy sparkle
```

### 場景2: 增強細節

```
使用者: "增強這個提示詞的細節: A beautiful young woman, blue eyes, pink lips"

增強結果:
A beautiful East Asian young woman, large expressive blue eyes (natural contact lenses), photorealistic eye texture, bright blue iris, soft full lips with gentle pink gloss, natural lip color, fresh look, flawless porcelain skin, radiant glow
```

### 場景3: 新增技術引數

```
使用者: "為這個提示詞新增專業攝影引數"

新增結果:
... photographed with Canon EOS R5, RF 50mm f/1.2L, 8K ultra-detailed, soft lighting, golden hour, professional portrait photography, high-end retouching
```

---

## 💡 最佳化策略

### 策略1: 保守最佳化

**原則**: 只修正明顯錯誤，不改變原意
- 僅補充缺失的基礎屬性
- 修正順序錯誤
- 去除重複

**適用**: 使用者已有明確意圖，只需小幅調整

### 策略2: 激進增強

**原則**: 大幅擴充套件細節，追求專業效果
- 補充所有模組
- 擴充套件所有描述到完整關鍵片語
- 新增所有技術引數

**適用**: 使用者提供的描述過於簡單，需要專業提示詞

### 策略3: 風格定向最佳化

**原則**: 基於目標風格最佳化
- 識別目標風格（清純/性感/古典/真人化）
- 使用該風格的預設五官組合
- 新增該風格的特定關鍵詞

**適用**: 使用者明確表示想要某種風格

---

## 📁 最佳化模板

### 模板1: 清純少女風格

**基礎結構**:
```
A beautiful East Asian young woman, [眼型:大眼杏仁眼], [唇型:粉嫩光澤唇], [鼻型:小巧直鼻], [皮膚:瓷肌無瑕], [表情:清純溫柔], photographed with Canon EOS R5, soft lighting, 8K ultra-detailed
```

### 模板2: 性感挑逗風格

**基礎結構**:
```
A beautiful East Asian young woman, [眼型:半閉誘惑眼], [皮膚:溫潤膠片肌], [表情:挑逗頑皮], photographed with Hasselblad 503CX, Kodak Portra 400, warm tones, fine grain
```

### 模板3: 電影敘事風格

**基礎結構**:
```
A beautiful East Asian young woman, [眼型:大藍眼真人化], [臉型:精緻鵝蛋臉], [皮膚:真實質感肌], [表情:寧靜冒險], photographed with Canon EOS R5, 35mm f/2.8, 8K HDR, cinematic lighting, photorealistic
```

---

## ⚠️ 最佳化注意事項

1. **尊重原意**
   - 不要改變使用者明確指定的特徵
   - 最佳化應該是"增強"而非"替換"

2. **避免過度最佳化**
   - 提示詞過長可能影響AI理解
   - 建議控制在200-300詞以內

3. **保持一致性**
   - 風格統一（不要混合清純和性感）
   - 技術引數匹配流派

4. **提供解釋**
   - 告知使用者做了哪些最佳化
   - 解釋為什麼這樣最佳化

---

**模組狀態**: ✅ 可用
**功能**: 診斷、修正、增強、建議
**最佳化級別**: 基礎修正、細節增強、技術最佳化
**支援風格**: 4種預設模板 + 自定義
