# 貼上式互動模式使用指南

## 什麼是貼上式互動？

**傳統方式**：需要先建立檔案 → 儲存 → 提供路徑
**貼上模式**：直接複製提示詞 → 貼上給Claude → 立即分析 ✨

**適用場景**：
- 快速分析1-50條提示詞
- 臨時測試新prompt結構
- 從網頁/社交媒體收集的片段
- 不想建立臨時檔案

## 使用方法

### 方式1：完整對話式

**步驟1：啟用Skill**
```
使用者：使用 prompt-extractor
```

**步驟2：選擇貼上模式**
```
Claude：請選擇輸入方式：
       1. 提供檔案路徑
       2. 直接貼上提示詞

使用者：2
```

**步驟3：貼上內容**
```
使用者：
a portrait of a young woman, cinematic lighting, 85mm lens, ultra detailed
cyberpunk city at night, neon lights, rain, photorealistic, 8k
beautiful landscape, golden hour, dramatic clouds, HDR
```

**步驟4：自動處理**
```
Claude：
✓ 已接收3條提示詞
✓ 開始提取模組...
[提取結果展示]
```

---

### 方式2：一句話啟動（推薦）

直接說：
```
幫我分析這些AI繪畫提示詞：

a portrait of a young woman, cinematic lighting, 85mm lens, ultra detailed
cyberpunk city at night, neon lights, rain, photorealistic, 8k
```

Claude會自動：
- 識別你在貼上提示詞
- 啟用 prompt-extractor skill
- 立即開始提取分析

---

### 方式3：混合模式

```
使用者：用 prompt-extractor 分析下面這些：

1. "stunning portrait, soft lighting, dreamy atmosphere"
2. "futuristic cityscape, neon colors, cyberpunk style, 4k"
3. "landscape photography, misty mountains, sunrise, HDR"
```

支援：
- 帶編號的列表
- 帶引號的文字
- 用逗號/換行分隔

---

## 支援的格式

### ✅ 推薦格式

**換行分隔**（最清晰）
```
提示詞1
提示詞2
提示詞3
```

**逗號+換行**
```
提示詞1,
提示詞2,
提示詞3
```

**帶編號**
```
1. 提示詞1
2. 提示詞2
3. 提示詞3
```

**JSON陣列**（適合從程式碼複製）
```json
[
  "提示詞1",
  "提示詞2",
  "提示詞3"
]
```

### ⚠️ 需要注意的格式

**逗號分隔**（可能混淆提示詞內部的逗號）
```
提示詞1, 提示詞2, 提示詞3
# 如果提示詞本身含逗號，會分割錯誤
```

建議改為：
```
提示詞1
---
提示詞2
---
提示詞3
```

---

## 實戰示例

### 示例1：分析收藏的優秀prompt

**場景**：從ArtStation看到5個優秀作品的提示詞

```
我：幫我分析這些優秀提示詞：

portrait of a woman, cinematic studio lighting, 85mm f/1.4, shallow depth of field, soft bokeh, professional photography, ultra detailed, photorealistic

cyberpunk samurai, neon-lit tokyo street, rain reflections, dramatic pose, blade runner aesthetic, purple and cyan color scheme, cinematic composition, 8k, trending on artstation

mystical forest, god rays through mist, ancient trees, magical atmosphere, fantasy art, greg rutkowski style, ethereal lighting, vibrant colors, highly detailed

macro photography of dewdrops on flower petals, golden hour lighting, shallow DOF, natural colors, bokeh background, canon 100mm macro, crystal clear details

futuristic architecture, zaha hadid style, flowing curves, white marble and glass, blue hour photography, symmetrical composition, architectural visualization, unreal engine 5
```

**Claude輸出**：
```json
{
  "總覽": {
    "數量": 5,
    "主題分佈": {
      "人像攝影": 1,
      "場景概念": 2,
      "微距攝影": 1,
      "建築設計": 1
    }
  },
  "提取的核心模組": {
    "高頻技術引數": [
      "cinematic lighting (2次)",
      "8k/ultra detailed (5次)",
      "shallow depth of field (2次)"
    ],
    "高頻視覺風格": [
      "photorealistic (1次)",
      "fantasy art (1次)",
      "cyberpunk (1次)"
    ],
    "高頻構圖": [
      "symmetrical composition (1次)",
      "dramatic pose (1次)"
    ],
    "色彩方案": [
      "purple and cyan (1次)",
      "natural colors (1次)"
    ],
    "參考藝術家": [
      "Greg Rutkowski",
      "Zaha Hadid"
    ]
  },
  "發現的模式": [
    "所有提示都包含質量增強詞（ultra detailed/8k等）",
    "80%指定了具體光線型別",
    "60%引用了專業標準（攝影器材、藝術家）",
    "結構型別：主體 + 技術/風格 + 質量增強"
  ],
  "可複用模板": {
    "人像攝影": "{人物}, cinematic lighting, 85mm f/1.4, shallow DOF, ultra detailed, photorealistic",
    "場景概念": "{場景}, {氛圍}, {色彩方案}, cinematic composition, 8k, trending on artstation",
    "建築視覺化": "{建築風格}, {材質}, {時間}, symmetrical composition, unreal engine 5"
  }
}
```

---

### 示例2：快速測試單個prompt的結構

```
我：分析這個prompt的模組結構：

a mystical elven warrior princess, flowing silver hair, emerald eyes, ornate armor with Celtic patterns, standing in enchanted forest, magical blue fireflies, ethereal mist, dramatic rim lighting, fantasy art, artstation trending, highly detailed, 8k, unreal engine
```

**Claude輸出**：
```json
{
  "original_prompt": "a mystical elven warrior princess...",
  "modules": {
    "subject_variables": {
      "main": "elven warrior princess",
      "modifiers": ["mystical"],
      "attributes": ["flowing silver hair", "emerald eyes"],
      "is_replaceable": true
    },
    "visual_style": {
      "art_style": "fantasy art",
      "era": "mythological"
    },
    "technical_parameters": {
      "lighting": "dramatic rim lighting",
      "render_engine": "unreal engine",
      "resolution": "8k"
    },
    "detail_enhancers": ["highly detailed", "8k"],
    "mood_atmosphere": "mystical, ethereal",
    "composition": {
      "perspective": "standing pose (full body implied)",
      "depth_of_field": "implied foreground subject focus"
    },
    "color_scheme": {
      "palette": ["silver", "emerald", "blue"],
      "tone": "cool tones",
      "specific_colors": "silver hair, emerald eyes, blue fireflies"
    },
    "time_season": {
      "weather": "misty"
    },
    "references": {
      "platforms": ["artstation trending"]
    }
  },
  "quality_score": {
    "clarity": 9,
    "detail_richness": 10,
    "reusability": 8,
    "comments": "結構完整，細節豐富，主體描述具體，易於替換核心元素"
  },
  "提取的模板": "{角色描述}, {外觀細節}, {服飾/道具}, {場景環境}, {氛圍元素}, {光線}, {風格}, {質量增強}"
}
```

**關鍵發現**：
- ✓ 10大模組中使用了8個
- ✓ 主體描述非常詳細（髮色、眼睛、服飾）
- ✓ 環境和氛圍詞豐富（森林、螢火蟲、霧氣）
- ⚠️ 缺少構圖引數（可補充視角）
- ⚠️ 缺少約束條件（可新增負面提示）

**改進建議**：
```
原始：a mystical elven warrior princess, flowing silver hair...
改進：a mystical elven warrior princess, flowing silver hair..., **front view, rule of thirds composition, --no blurry, distorted**
```

---

### 示例3：對比兩個prompt找差異

```
我：對比這兩個提示詞，哪個更好？

A: portrait of a woman, beautiful, detailed
B: portrait of a young woman, cinematic studio lighting, 85mm lens f/1.4, soft bokeh background, natural skin texture, professional photography, ultra high resolution, photorealistic
```

**Claude分析**：
```markdown
## 對比分析

### Prompt A
- 模組數量：2個（主體 + 細節增強）
- 質量評分：4/10
- 問題：
  - 缺乏技術引數（光線、鏡頭）
  - "beautiful"過於主觀
  - "detailed"泛泛而談
  - 無具體風格指引

### Prompt B
- 模組數量：7個（主體、技術、細節、構圖、視覺風格等）
- 質量評分：9/10
- 優勢：
  - 技術引數明確（85mm f/1.4）
  - 光線指定（cinematic studio lighting）
  - 細節具體（natural skin texture）
  - 質量標準清晰（photorealistic, ultra high resolution）
  - 構圖暗示（soft bokeh background → 淺景深）

### 結論
**B 明顯優於 A**

差距原因：
1. 技術引數的缺失vs完整
2. 主觀形容詞vs客觀描述
3. 模糊指引vs精確指令

### 學習要點
從B中提取的可複用模式：
- ✓ 永遠指定光線型別
- ✓ 鏡頭引數提升專業度
- ✓ 用技術詞替代主觀詞（"photorealistic" > "beautiful"）
- ✓ 細節具體化（"natural skin texture" > "detailed"）
```

---

## 高階技巧

### 技巧1：批次貼上變體測試

```
我：分析這3個漸進版本的差異：

v1: girl, pink hair, cute
v2: anime girl, pink hair, cute expression, colorful
v3: anime girl, vibrant pink hair, cute expression with sparkles in eyes, colorful outfit, studio ghibli style, soft lighting, pastel colors, highly detailed, 4k
```

Claude會自動：
- 對比3個版本的模組覆蓋度
- 展示漸進最佳化路徑
- 給出繼續改進建議

---

### 技巧2：從Midjourney/SD匯出直接貼上

**Midjourney匯出格式**：
```
我：分析我的MJ歷史記錄：

/imagine prompt: cyberpunk city, neon lights --ar 16:9 --v 5
/imagine prompt: portrait, cinematic --ar 2:3 --stylize 750
/imagine prompt: landscape, epic --q 2
```

Claude會：
- 自動剔除MJ命令語法
- 只提取核心prompt部分
- 識別引數（--ar, --v等）並歸類到"約束條件"

---

### 技巧3：混合檔案+貼上

```
我：先分析 my_library.json，然後對比這個新prompt：

stunning landscape, misty mountains at sunrise, golden light, dramatic clouds
```

Claude會：
- 載入現有庫
- 分析新prompt
- 對比找出庫中已有/缺失的模組
- 建議如何融合

---

## 限制與最佳實踐

### 數量限制

| 模式 | 推薦數量 | 最大數量 | 處理時間 |
|------|---------|---------|---------|
| 單條分析 | 1 | 1 | <10秒 |
| 小批次 | 5-10 | 50 | 1-3分鐘 |
| 中批次 | - | 100 | 5-10分鐘 |
| 大批次 | 用檔案 | - | - |

**建議**：
- 1-10條 → 貼上模式
- 10-50條 → 貼上模式（分批）
- >50條 → 檔案模式

---

### 格式建議

**✅ 推薦**：
```
# 每行一個，清晰明確
提示詞1
提示詞2
提示詞3
```

**⚠️ 小心**：
```
# 逗號分隔（提示詞內部也有逗號時易混淆）
girl, pink hair, cute, boy, blue shirt, cool
# ↑ 會被錯誤分為6條而非2條
```

**解決方案**：
```
# 用換行或明確分隔符
girl, pink hair, cute
---
boy, blue shirt, cool
```

---

## 常見問題

### Q1: 貼上長文字後沒反應？
**A**: 可能超過了上下文限制。建議：
- 分批貼上（每批20-30條）
- 或儲存為檔案使用檔案模式

### Q2: 提示詞被錯誤分割怎麼辦？
**A**: 使用更明確的分隔符：
```
===提示詞1===
a portrait of woman, detailed

===提示詞2===
landscape, mountains
```

### Q3: 能貼上中文提示詞嗎？
**A**: 完全支援！
```
我：分析這些中文提示詞：

一位年輕女性的肖像，電影級光線，85mm鏡頭，超高畫質細節
賽博朋克城市夜景，霓虹燈，雨水反射，8k超高畫質
```

### Q4: 能從Excel複製貼上嗎？
**A**: 可以！複製Excel的一列：
```
[從Excel複製]
portrait, lighting, 8k
landscape, sunset, HDR
cityscape, neon, 4k

[貼上到Claude]
我：分析這些從表格複製的提示詞：
portrait, lighting, 8k
landscape, sunset, HDR
cityscape, neon, 4k
```

---

## 實用工作流

### 工作流1：日常收集與分析

```mermaid
瀏覽網頁/社交媒體
  ↓
看到好提示詞 → 複製
  ↓
貼上給Claude Code
  ↓
立即獲得結構分析
  ↓
積累到個人模組庫
```

### 工作流2：提示詞最佳化迭代

```
1. 貼上初稿提示詞
2. 獲得結構分析 + 缺失模組提示
3. 根據建議補充模組
4. 再次貼上新版本
5. 對比改進效果
6. 重複直到滿意
```

### 工作流3：學習大師作品

```
1. 從頂級作品提取提示詞
2. 批次貼上給Claude
3. 分析共同模式
4. 提取複用模板
5. 應用到自己創作
```

---

**開始嘗試貼上模式吧！** 🚀

隨時在Claude Code中貼上你的提示詞，無需建立檔案，立即開始分析！
