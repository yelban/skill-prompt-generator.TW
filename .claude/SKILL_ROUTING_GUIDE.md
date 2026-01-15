# 提示詞生成 Skill 路由使用指南

本指南詳細說明如何根據使用者請求自動路由到正確的 Skill，包含每個步驟的詳細解釋和實際示例。

---

## 📚 目錄

1. [架構概覽](#架構概覽)
2. [路由流程 4 步驟](#路由流程-4-步驟)
3. [每個 Skill 的詳細示例](#每個-skill-的詳細示例)
4. [常見問題處理](#常見問題處理)

---

## 架構概覽

### 資料儲存結構

```
elements.db (統一資料庫)
    ├─ portrait domain (491 元素) → intelligent-prompt-generator
    ├─ art domain (51 元素) → art-master
    ├─ design domain (59 元素) → design-master
    ├─ product domain (77 元素) → product-master
    ├─ video domain (49 元素) → video-master
    └─ 其他 7 個 domain (common, interior, creative 等)
```

### 為什麼需要不同的 Skill？

雖然所有資料在同一個資料庫，但訪問方式不同：

- **intelligent-prompt-generator**: 使用 `prompt_framework.yaml`（人像專用框架），包含 eyes, nose, lips, makeup, hairstyle, pose 等人像專用欄位
- **domain expert skills**: 直接查詢對應領域，無需人像框架

**關鍵**：風景畫、產品、海報不需要 "眼睛"、"妝容"、"姿勢" 這些欄位 → 必須用專門的 domain expert skills

---

## 路由流程 4 步驟

### STEP 1: 判斷主體（最重要）

**問題**：請求中是否包含人物？

#### 判斷方法

**有人物** 的關鍵詞：
- 明確的人物：女性、男性、女孩、男孩、人物、角色、肖像
- 職業/身份：模特、女演員、武俠人物、商務人士
- 人體部位：面部、五官、表情、姿勢、妝容

**無人物** 的關鍵詞：
- 風景：山水、風景、自然、樹林、海洋
- 靜物：花卉、靜物、桌面
- 抽象：抽象藝術、幾何圖形
- 產品：手錶、香水、書籍、商品
- 介面：海報、UI、佈局、網頁

#### 示例

| 使用者請求 | 有人物？ | 下一步 |
|---------|---------|--------|
| "生成電影級亞洲女性" | ✅ YES | 預設 → intelligent-prompt-generator |
| "生成中國水墨畫山水" | ❌ NO | 繼續 STEP 2 |
| "生成武俠人物飛身躍起" | ✅ YES | 預設 → intelligent-prompt-generator |
| "生成奢華手錶產品攝影" | ❌ NO | 繼續 STEP 2 |

---

### STEP 2: 根據主體型別選擇專家

**前提**：STEP 1 判斷為 "無人物"

#### 分類規則

**🎨 藝術作品** → `art-master`
- 關鍵詞：水墨畫、油畫、水彩畫、抽象藝術、插畫、繪畫
- 特徵：藝術風格、繪畫技法、藝術流派
- Domain: art (51 元素)
- 專長：筆觸、留白、潑墨、厚塗、肌理

**🎯 平面設計** → `design-master`
- 關鍵詞：海報、UI、佈局、Bento Grid、玻璃態、排版
- 特徵：設計佈局、視覺效果、現代設計系統
- Domain: design (59 元素)
- 專長：Bento Grid、Glassmorphism、網格系統

**📦 產品攝影** → `product-master`
- 關鍵詞：產品、商品、商業攝影、包裝、展示
- 特徵：產品、商品、靜物拍攝
- Domain: product (77 元素)
- 專長：Phase One 相機、商業布光、產品構圖

**🎬 影片場景** → `video-master`
- 關鍵詞：影片、鏡頭運動、運鏡、轉場、動態場景、延時攝影
- 特徵：動態、鏡頭語言、影片效果
- Domain: video (49 元素)
- 專長：推拉搖移、轉場、特效、鏡頭運動

**👤 人像攝影** → `intelligent-prompt-generator`
- 關鍵詞：人物、肖像、面部、五官、表情、姿勢、妝容
- 特徵：人物屬性、面部特徵
- Domain: portrait (491 元素)
- 專長：五官、妝容、表情、人種推理、一致性檢查

#### 示例

| 使用者請求 | 主體型別 | 路由選擇 |
|---------|---------|---------|
| "生成中國水墨畫山水，飛白技法" | 藝術作品 | art-master |
| "生成 Bento Grid 佈局海報" | 平面設計 | design-master |
| "生成奢華手錶產品攝影，柔光箱布光" | 產品攝影 | product-master |
| "生成武俠場景推鏡頭運動" | 影片場景 | video-master |

---

### STEP 3: 衝突場景處理

**場景**：請求同時涉及 **人物 + 特殊風格**

#### 預設策略（80% 情況）

**規則**：有人物 → 優先 `intelligent-prompt-generator`

**原因**：
- 人像框架能處理人物屬性（五官、表情、妝容）
- 風格透過 `art_style` 引數實現（如 art_style='watercolor'）

#### 例外情況（20% 情況）

**規則**：使用者明確強調藝術技法專業術語 → 使用 `art-master`

**藝術技法關鍵詞**：
- 筆觸、留白、潑墨（水墨畫）
- 厚塗、肌理、筆觸（油畫）
- 乾溼濃淡、飛白（國畫）
- 暈染、漸變（水彩）

#### 詢問使用者場景

**規則**：同時強調人物細節和藝術技法 → 詢問使用者偏好

#### 示例

| 使用者請求 | 分析 | 路由選擇 | 理由 |
|---------|------|---------|------|
| "生成水墨畫風格的女性" | 人物 + 風格 | intelligent-prompt-generator | 預設策略，水墨畫作為 art_style |
| "生成梵高風格的女性肖像" | 人物 + 風格 | intelligent-prompt-generator | 預設策略，梵高風格作為 art_style |
| "生成女性肖像，要求水墨畫的筆觸和留白技法" | 人物 + 藝術技法術語 | 詢問使用者 | 同時強調人物和技法 |
| "生成油畫效果，要求厚塗和肌理" | 無人物 + 藝術技法 | art-master | 強調藝術技法 |

---

### STEP 4: 呼叫對應的 Skill

根據 STEP 1-3 的判斷結果，呼叫相應的 Skill：

```python
# 呼叫示例
Skill(command="intelligent-prompt-generator")  # 人像
Skill(command="art-master")                    # 藝術
Skill(command="design-master")                 # 設計
Skill(command="product-master")                # 產品
Skill(command="video-master")                  # 影片
```

---

## 每個 Skill 的詳細示例

### 1. intelligent-prompt-generator（人像專家）

**適用場景**：所有包含人物的請求

#### 示例 1: 電影級亞洲女性

**使用者請求**：
```
生成電影級的亞洲女性，張藝謀電影風格
```

**路由流程**：
1. **STEP 1**: 包含 "亞洲女性" → 有人物 ✅
2. **結論**: intelligent-prompt-generator
3. **呼叫**: `Skill(command="intelligent-prompt-generator")`

**Skill 工作**：
- 解析 intent:
  ```json
  {
    "subject": {"gender": "female", "ethnicity": "East_Asian"},
    "lighting": "zhang_yimou",
    "visual_style": {"art_style": "cinematic"}
  }
  ```
- 查詢 portrait domain (491 元素)
- 應用人像框架（facial, styling, expression 等欄位）
- 生成包含戲劇性光影的完整人像提示詞

#### 示例 2: 水墨畫風格的女性

**使用者請求**：
```
生成水墨畫風格的女性
```

**路由流程**：
1. **STEP 1**: 包含 "女性" → 有人物 ✅
2. **STEP 3**: 人物 + 風格，但未強調技法術語 → 預設策略
3. **結論**: intelligent-prompt-generator
4. **呼叫**: `Skill(command="intelligent-prompt-generator")`

**Skill 工作**：
- 解析 intent:
  ```json
  {
    "subject": {"gender": "female", "ethnicity": "East_Asian"},
    "visual_style": {"art_style": "watercolor"}
  }
  ```
- 透過 art_style 引數實現水墨畫風格
- 人像框架處理五官、表情、妝容

#### 示例 3: 古裝女子

**使用者請求**：
```
生成仙劍奇俠傳真人電影風格的年輕古裝女子
```

**路由流程**：
1. **STEP 1**: 包含 "古裝女子" → 有人物 ✅
2. **結論**: intelligent-prompt-generator
3. **呼叫**: `Skill(command="intelligent-prompt-generator")`

**Skill 工作**：
- 解析 intent:
  ```json
  {
    "subject": {"gender": "female", "age_range": "young_adult"},
    "styling": {
      "clothing": "traditional_chinese",
      "makeup": "traditional_chinese",
      "hairstyle": "ancient_chinese"
    },
    "lighting": {"lighting_type": "cinematic"},
    "scene": {"era": "ancient", "atmosphere": "fantasy"}
  }
  ```
- 框架自動推導：era=ancient → makeup/clothing/hairstyle 自動匹配

---

### 2. art-master（藝術專家）

**適用場景**：無人物的藝術作品，或強調藝術技法術語

#### 示例 1: 中國水墨畫山水

**使用者請求**：
```
生成中國水墨畫山水
```

**路由流程**：
1. **STEP 1**: 山水 → 無人物 ❌
2. **STEP 2**: 主體是藝術作品（水墨畫） → art-master
3. **呼叫**: `Skill(command="art-master")`

**Skill 工作**：
- 查詢 art domain (51 元素)
- 選擇中國水墨畫相關元素：
  - 藝術風格：Traditional Chinese ink painting
  - 技法：flowing brush strokes, varying ink density
  - 構圖：minimalist composition, negative space
  - 特徵：monochromatic, grey washes, calligraphic elements
- 生成包含專業藝術術語的提示詞

#### 示例 2: 油畫技法的厚塗效果

**使用者請求**：
```
生成油畫效果，強調厚塗和筆觸肌理
```

**路由流程**：
1. **STEP 1**: 無人物明確提及 → 無人物 ❌
2. **STEP 2**: 強調藝術技法（厚塗、肌理） → art-master
3. **呼叫**: `Skill(command="art-master")`

**Skill 工作**：
- 查詢 art domain
- 選擇油畫技法元素：
  - 技法：impasto technique, thick paint application
  - 筆觸：visible brush strokes, textured surface
  - 效果：palette knife marks, layered paint
- 生成強調技法的藝術提示詞

#### 示例 3: 超現實主義風格

**使用者請求**：
```
生成超現實主義藝術作品，夢境氛圍
```

**路由流程**：
1. **STEP 1**: 無人物 ❌
2. **STEP 2**: 主體是藝術作品（超現實主義） → art-master
3. **呼叫**: `Skill(command="art-master")`

**Skill 工作**：
- 查詢 art domain
- 選擇超現實主義元素：
  - 藝術風格：surrealism, dreamlike atmosphere
  - 特徵：impossible scenarios, symbolic imagery
  - 效果：ethereal, mysterious, subconscious themes
- 生成超現實主義風格提示詞

---

### 3. design-master（設計專家）

**適用場景**：無人物的平面設計、UI、海報、佈局

#### 示例 1: Bento Grid 海報

**使用者請求**：
```
生成 Bento Grid 佈局海報
```

**路由流程**：
1. **STEP 1**: 海報 → 無人物 ❌
2. **STEP 2**: 主體是平面設計（Bento Grid） → design-master
3. **呼叫**: `Skill(command="design-master")`

**Skill 工作**：
- 查詢 design domain (59 元素)
- 選擇 Bento Grid 相關元素：
  - 佈局系統：Bento grid layout, 8 asymmetric modular cards
  - 視覺效果：modern minimalist aesthetics
  - 技術引數：4K resolution, clean typography
- 生成包含專業設計術語的提示詞

#### 示例 2: 玻璃態 UI 設計

**使用者請求**：
```
生成玻璃態 UI 設計，現代極簡風格
```

**路由流程**：
1. **STEP 1**: UI → 無人物 ❌
2. **STEP 2**: 主體是平面設計（玻璃態） → design-master
3. **呼叫**: `Skill(command="design-master")`

**Skill 工作**：
- 查詢 design domain
- 選擇玻璃態元素：
  - 視覺效果：Glassmorphism, frosted glass effect
  - 技術：80% translucency, backdrop blur filter
  - 風格：minimalist, modern aesthetics
  - 色彩：90% neutral colors with 10% vibrant accents
- 生成現代設計系統提示詞

#### 示例 3: 包含人物頭像的海報

**使用者請求**：
```
生成 Bento Grid 海報，包含人物頭像
```

**路由流程**：
1. **STEP 1**: 雖然提到"人物頭像"，但主體是"海報" → 無人物 ❌
2. **STEP 2**: 主體是平面設計 → design-master
3. **呼叫**: `Skill(command="design-master")`

**解釋**：人物頭像只是海報的一個元素，不是主體

---

### 4. product-master（產品專家）

**適用場景**：無人物的產品攝影、商品展示

#### 示例 1: 奢華手錶產品攝影

**使用者請求**：
```
生成奢華手錶產品攝影
```

**路由流程**：
1. **STEP 1**: 手錶 → 無人物 ❌
2. **STEP 2**: 主體是產品 → product-master
3. **呼叫**: `Skill(command="product-master")`

**Skill 工作**：
- 查詢 product domain (77 元素)
- 選擇奢華產品攝影元素：
  - 相機：Phase One camera, macro lens
  - 燈光：softbox lighting, rim light
  - 構圖：luxury product composition
  - 背景：premium backdrop
- 生成商業攝影級提示詞

#### 示例 2: 香水瓶柔光布光

**使用者請求**：
```
生成香水瓶產品攝影，柔光箱布光
```

**路由流程**：
1. **STEP 1**: 香水瓶 → 無人物 ❌
2. **STEP 2**: 主體是產品 → product-master
3. **呼叫**: `Skill(command="product-master")`

**Skill 工作**：
- 查詢 product domain
- 選擇柔光布光元素：
  - 燈光：softbox lighting, diffused light
  - 相機：DSLR, shallow depth of field
  - 效果：elegant, premium, glass reflections
- 生成包含專業攝影術語的提示詞

#### 示例 3: 女模特展示香水（邊界案例）

**使用者請求**：
```
女模特展示香水瓶
```

**路由流程**：
1. **STEP 1**: 有 "女模特" → 有人物 ✅
2. **STEP 3**: 焦點不明確（人物 vs 產品）
3. **詢問使用者**:
   ```
   我注意到你的請求涉及：
   - 女模特（intelligent-prompt-generator）
   - 香水瓶產品（product-master）

   你的焦點是：
   A. 女模特（人物為主，香水為道具）
   B. 香水瓶（產品為主，模特為陪襯）

   請選擇？
   ```

#### 示例 4: 9宮格產品攝影（Grid Collage 模式）

**使用者請求**：
```
生成9宮格奢華手錶產品攝影，中間3D突出
```

**路由流程**：
1. **STEP 1**: 手錶 → 無人物 ❌
2. **STEP 2**: 主體是產品 → product-master
3. **呼叫**: `Skill(command="product-master")`

**Skill 工作**：
- 識別關鍵詞："9宮格" → 自動切換到 **Grid Collage 模式**
- 載入專業模板：`modules/layouts/grid_collage.md`
- 查詢 product domain (77 元素)
- 生成包含以下特性的專業提示詞：
  - **3×3嚴格等分網格** + THICK WHITE LINES 分隔
  - **8個不同角度產品攝影**（背景層，全部清晰）
    - [1,1] 錶盤俯視
    - [1,2] 錶冠側面
    - [1,3] 表扣細節
    - [2,1] 經典45度角
    - [2,3] 底蓋機芯
    - [3,1] 上手效果
    - [3,2] 錶帶鏈節
    - [3,3] 包裝盒
  - **1個超大3D渲染手錶**（前景層）
    - 錶冠觸頂邊，錶帶觸底邊
    - 佔據最大垂直空間
    - 完全遮擋中間格子[2,2]
    - 部分遮擋周圍4格（10-20%）
  - **深景深f/16** - 所有格子都清晰
  - **專業深度效果**：
    - Drop shadow (12px blur)
    - Contact shadow (8px blur)
    - 前景+10%亮度，+20%飽和度
  - **完整質量檢查清單**
  - **一致性規則**（9個位置同一產品）

**輸出效果**：
- 超現實拼貼藝術風格
- 適合電商詳情頁、社交媒體、產品宣傳海報
- 同時展示多個角度 + 3D立體突出

**觸發關鍵詞**：
- "9宮格"、"3×3佈局"、"grid"
- "多角度展示"、"多視角"
- "中間3D突出"、"3D pop-out"

---

### 5. video-master（影片專家）

**適用場景**：無人物的影片場景、鏡頭運動、動態效果

#### 示例 1: 武俠場景運鏡

**使用者請求**：
```
生成武俠場景推鏡頭運動
```

**路由流程**：
1. **STEP 1**: 場景 + 推鏡頭 → 無人物 ❌
2. **STEP 2**: 主體是影片（鏡頭運動） → video-master
3. **呼叫**: `Skill(command="video-master")`

**Skill 工作**：
- 查詢 video domain (49 元素)
- 選擇鏡頭運動元素：
  - 運鏡：dolly in (推鏡頭), slow camera movement
  - 場景：wuxia atmosphere, ancient Chinese architecture
  - 效果：cinematic movement, dramatic reveal
- 生成包含鏡頭語言的提示詞

#### 示例 2: 風景延時攝影

**使用者請求**：
```
生成風景延時攝影，雲霧流動效果
```

**路由流程**：
1. **STEP 1**: 風景 → 無人物 ❌
2. **STEP 2**: 主體是影片（延時攝影） → video-master
3. **呼叫**: `Skill(command="video-master")`

**Skill 工作**：
- 查詢 video domain
- 選擇延時攝影元素：
  - 技術：time-lapse photography
  - 效果：flowing clouds, dynamic motion
  - 運鏡：static camera, long exposure effect
- 生成延時攝影提示詞

#### 示例 3: 武俠人物飛身躍起（邊界案例）

**使用者請求**：
```
武俠人物飛身躍起的動態鏡頭
```

**路由流程**：
1. **STEP 1**: 包含 "武俠人物" → 有人物 ✅
2. **分析**: 主體是人物動作 vs 鏡頭運動？
3. **預設策略**: 主體是人物 → intelligent-prompt-generator
4. **呼叫**: `Skill(command="intelligent-prompt-generator")`

**解釋**：
- 人物動作透過 `expression.pose` 欄位處理（人像框架支援）
- 如果使用者明確強調鏡頭運動（"跟隨鏡頭"、"運鏡"），則詢問使用者

---

## 常見問題處理

### Q1: 如何判斷是 "人物肖像" 還是 "人物在場景中"？

**答案**：看主體是什麼

| 描述 | 主體 | 路由 |
|------|------|------|
| "女性肖像" | 人物 | intelligent-prompt-generator |
| "女性在花園裡" | 人物 | intelligent-prompt-generator |
| "花園場景，遠處有人" | 場景 | 根據場景型別路由 |
| "Bento Grid 海報，包含人物頭像" | 海報 | design-master |

### Q2: 使用者說 "水墨畫風格的人物"，為什麼不用 art-master？

**答案**：預設策略

- 主體是 "人物" → 需要人像框架（facial, styling, expression）
- "水墨畫風格" 作為 `art_style` 引數實現
- art-master 專注於藝術技法術語（筆觸、留白、潑墨）
- 除非使用者明確說 "水墨畫的筆觸和留白技法"

### Q3: 什麼時候需要詢問使用者？

**答案**：兩種情況

1. **焦點不明確**：
   - "女模特展示香水瓶" → 人物 vs 產品？
   - "產品海報設計" → 產品 vs 設計？

2. **同時強調人物和技法**：
   - "女性肖像，要求水墨畫的筆觸留白技法" → 人物細節 vs 藝術技法？

### Q4: 如果使用者請求不屬於任何 domain 怎麼辦？

**答案**：詢問使用者或直接處理

示例：
```
使用者："幫我最佳化這段程式碼"
→ 不涉及提示詞生成
→ 直接在 conversation 處理，不呼叫 skill
```

### Q5: 多個 domain 的組合請求怎麼處理？

**答案**：確定主 domain

| 請求 | 主 domain | 路由 |
|------|----------|------|
| "產品海報設計" | 設計（海報） | design-master |
| "產品攝影布光" | 產品（攝影） | product-master |
| "人物產品廣告" | 詢問焦點 | 詢問使用者 |

---

## 總結

### 路由決策樹（完整版）

```
使用者請求
    ↓
【STEP 1: 有人物嗎？】
    ↓
  YES ─────────┐
    │         ↓
    │    【STEP 3: 有藝術技法術語嗎？】
    │         ↓
    │       NO ──→ intelligent-prompt-generator (預設)
    │         ↓
    │      YES ──→ 詢問使用者偏好
    │
  NO
    ↓
【STEP 2: 主體是什麼？】
    ↓
    ├─ 藝術作品 → art-master
    ├─ 平面設計 → design-master
    ├─ 產品 → product-master
    ├─ 影片 → video-master
    └─ 人物 → intelligent-prompt-generator
```

### 核心原則

1. **人物優先**：有人物 → 優先 intelligent-prompt-generator
2. **技法例外**：明確藝術技法術語 → art-master
3. **主體判斷**：無人物 → 根據主體型別路由
4. **焦點詢問**：焦點不明確 → 詢問使用者

---

**最後更新**: 2026-01-04
**版本**: 1.0
