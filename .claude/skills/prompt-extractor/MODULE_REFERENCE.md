# 10大模組分類完整參考手冊

## 模組體系概覽

```
AI繪畫提示詞 = 10大模組的組合
├── 1. 主體變數 (Subject Variables)
├── 2. 視覺風格 (Visual Style)
├── 3. 技術引數 (Technical Parameters)
├── 4. 細節增強 (Detail Enhancers)
├── 5. 情緒氛圍 (Mood & Atmosphere)
├── 6. 約束條件 (Constraints)
├── 7. 構圖引數 (Composition) ← 新增
├── 8. 色彩方案 (Color Scheme) ← 新增
├── 9. 時間/季節 (Time & Season) ← 新增
└── 10. 參考藝術家/作品 (References) ← 新增
```

---

## 1. 主體變數 (Subject Variables)

**定義**：提示詞的核心物件，可替換性最強的部分。

### 子模組
- **main**: 主物件（人物、物體、場景）
- **modifiers**: 修飾詞
- **attributes**: 具體屬性
- **is_replaceable**: 是否可替換（布林值）

### 示例

| 提示詞 | 主物件 | 修飾詞 | 屬性 |
|--------|--------|--------|------|
| "a young woman" | woman | young | - |
| "cyberpunk city" | city | cyberpunk | - |
| "red sports car" | sports car | - | red |
| "elven warrior, silver hair" | elven warrior | - | silver hair |

### 提取技巧
- 通常在提示詞開頭
- 名詞或名詞短語
- 去掉後提示詞失去主題的部分

### 複用價值
⭐⭐⭐⭐⭐ (最高)
- 替換主體可生成同風格不同主題的作品
- 模板複用的核心

---

## 2. 視覺風格 (Visual Style)

**定義**：整體藝術風格、畫風、年代感。

### 子模組
- **art_style**: 藝術風格
- **era**: 年代感/時代

### 常見風格分類

**寫實類**：
- photorealistic, hyperrealistic, photo-real
- cinematic, filmic
- documentary style

**藝術類**：
- oil painting, watercolor, ink drawing
- digital art, concept art
- pixel art, low poly

**風格流派**：
- impressionism, surrealism, abstract
- anime style, manga style
- art deco, art nouveau

**特定世界觀**：
- cyberpunk, steampunk, dieselpunk
- fantasy, sci-fi, post-apocalyptic
- retro, vintage, futuristic

### 示例

```
photorealistic → 照片級真實
anime style → 動漫風格
oil painting, renaissance style → 文藝復興油畫
cyberpunk aesthetic → 賽博朋克美學
minimalist design → 極簡主義設計
```

### 複用價值
⭐⭐⭐⭐⭐
- 定義整體視覺基調
- 風格一致性的關鍵

---

## 3. 技術引數 (Technical Parameters)

**定義**：攝影/渲染的技術規格。

### 子模組
- **camera**: 鏡頭引數
- **lighting**: 光線描述
- **render_engine**: 渲染引擎
- **resolution**: 解析度/質量

### 鏡頭引數詳解

**焦距**：
- 14mm, 24mm → 超廣角
- 35mm, 50mm → 標準鏡頭
- 85mm, 105mm → 人像鏡頭
- 200mm+ → 長焦/野生動物

**光圈**：
- f/1.4, f/1.8 → 大光圈，淺景深
- f/8, f/11 → 小光圈，大景深

### 光線型別

**自然光**：
- natural lighting, sunlight
- window light, diffused light
- golden hour, blue hour

**人工光**：
- studio lighting, softbox
- ring light, key light
- neon lights, LED

**特殊光效**：
- rim lighting (輪廓光)
- backlighting (逆光)
- volumetric lighting (體積光)
- god rays (丁達爾效應)

### 渲染引擎

```
Unreal Engine 5 → 遊戲級即時渲染
Octane Render → 高質量離線渲染
V-Ray → 建築視覺化
Blender Cycles → 開源渲染器
```

### 示例

```
85mm lens f/1.4 → 人像標準配置
wide angle 24mm → 風光/建築
macro 100mm lens → 微距攝影
cinematic lighting, rim light → 電影級光效
rendered in Unreal Engine 5 → UE5渲染
```

### 複用價值
⭐⭐⭐⭐
- 直接影響成片質量
- 專業感的體現

---

## 4. 細節增強 (Detail Enhancers)

**定義**：提升質量、細節的修飾詞。

### 分類

**解析度/清晰度**：
- 8k, 4k, ultra high resolution
- sharp focus, crystal clear
- highly detailed, intricate details

**質量標準**：
- professional photography
- award-winning
- masterpiece, best quality

**平臺/競賽**：
- trending on artstation
- featured on behance
- contest winner

### 常見組合

```
ultra detailed, 8k, sharp focus
highly detailed, intricate, professional
hyperrealistic, photorealistic, 8k uhd
masterpiece, best quality, award-winning
```

### 示例

| 提示詞 | 效果 |
|--------|------|
| 8k | 暗示極高解析度 |
| sharp focus | 強調清晰度 |
| intricate details | 複雜細節 |
| professional photography | 專業攝影水準 |

### 複用價值
⭐⭐⭐⭐
- 幾乎所有提示詞都需要
- 顯著提升生成質量

---

## 5. 情緒氛圍 (Mood & Atmosphere)

**定義**：情感基調、氛圍感受。

### 情緒型別

**正面情緒**：
- joyful, cheerful, uplifting
- peaceful, serene, calm
- epic, majestic, grand

**負面情緒**：
- melancholic, sad, somber
- tense, anxious, ominous
- dark, gloomy, moody

**中性/複雜**：
- mysterious, enigmatic
- nostalgic, wistful
- ethereal, dreamlike

### 氛圍描述

**空間氛圍**：
- cozy, intimate
- vast, expansive
- claustrophobic, confined

**時間氛圍**：
- timeless, eternal
- fleeting, transient
- suspended in time

### 示例

```
peaceful morning atmosphere
dark and mysterious mood
epic and dramatic feeling
nostalgic 80s vibe
ethereal dreamlike quality
```

### 複用價值
⭐⭐⭐
- 傳遞情感資訊
- 提升藝術表現力

---

## 6. 約束條件 (Constraints)

**定義**：負面提示、排除元素、技術約束。

### 子模組
- **negative_prompt**: 負面提示
- **exclusions**: 排除元素

### 常見負面提示

**質量相關**：
- no blur, not blurry
- no distortion, no artifacts
- no noise, no grain (除非刻意要膠片感)

**內容相關**：
- no text, no watermark
- no extra limbs, no deformed
- no low quality, no bad anatomy

**Stable Diffusion專用**：
```
Negative: ugly, tiling, poorly drawn hands, poorly drawn feet,
poorly drawn face, out of frame, extra limbs, disfigured,
deformed, body out of frame, blurry, bad anatomy, blurred,
watermark, grainy, signature, cut off, draft
```

**Midjourney專用**：
```
--no text, watermark, signature
--no blur, distortion
```

### 示例

```
portrait of a woman, beautiful, detailed
Negative: ugly, deformed, blurry, low quality

landscape, mountains, epic
--no people, buildings, text
```

### 複用價值
⭐⭐⭐⭐
- 避免常見問題
- 提高成片率

---

## 7. 構圖引數 (Composition) ✨ 新增

**定義**：畫面構圖、視角、景深等視覺組織方式。

### 子模組
- **perspective**: 視角
- **depth_of_field**: 景深
- **aspect_ratio**: 畫幅比例
- **symmetry**: 對稱性
- **rule**: 構圖法則

### 視角型別

**高度視角**：
- bird's eye view (鳥瞰)
- high angle (俯視)
- eye level (平視)
- low angle (仰視)
- worm's eye view (蟲視)

**距離視角**：
- extreme close-up (大特寫)
- close-up (特寫)
- medium shot (中景)
- full body (全身)
- wide shot (遠景)

**特殊視角**：
- first person POV (第一人稱)
- over the shoulder (過肩)
- dutch angle (荷蘭角/傾斜)

### 景深描述

```
shallow depth of field (淺景深) → 背景虛化
deep depth of field (大景深) → 全景清晰
bokeh background (焦外散景)
f/1.4, soft bokeh → 柔美散景
```

### 畫幅比例

| 比例 | 用途 | 示例 |
|------|------|------|
| 1:1 | 社交媒體 | Instagram |
| 16:9 | 電影/橫屏 | YouTube |
| 9:16 | 豎屏影片 | TikTok |
| 4:3 | 傳統攝影 | 經典照片 |
| 21:9 | 超寬電影 | 影院 |

### 構圖法則

**經典法則**：
- rule of thirds (三分法)
- golden ratio (黃金分割)
- leading lines (引導線)
- frame within frame (框中框)

**對稱構圖**：
- symmetrical composition
- centered composition
- radial symmetry

### 示例

```
portrait, close-up, shallow DOF, f/1.4
landscape, wide shot, deep focus, rule of thirds
architectural photo, symmetrical composition, centered
bird's eye view, urban cityscape, dramatic perspective
```

### 複用價值
⭐⭐⭐⭐⭐
- 專業攝影必備
- 顯著提升構圖質量

---

## 8. 色彩方案 (Color Scheme) ✨ 新增

**定義**：色調、配色、飽和度等色彩相關描述。

### 子模組
- **tone**: 色調（暖/冷）
- **palette**: 調色盤/主要顏色
- **saturation**: 飽和度
- **contrast**: 對比度
- **temperature**: 色溫

### 色調分類

**溫度色調**：
- warm tones (暖色調) → 紅橙黃
- cool tones (冷色調) → 藍綠紫
- neutral tones (中性色調) → 灰白黑

**明度色調**：
- bright colors (明亮色)
- pastel colors (粉彩色)
- dark colors (深色)
- muted colors (柔和色)

### 配色方案

**單色系**：
- monochromatic (單色)
- black and white (黑白)
- sepia tones (棕褐色)

**互補色**：
- blue and orange
- purple and yellow
- red and cyan

**類似色**：
- analogous colors (鄰近色)
- earth tones (大地色)
- jewel tones (寶石色)

**特定配色**：
- cyberpunk colors (賽博朋克) → 紫、青、粉
- vaporwave aesthetic → 粉、青、紫漸變
- autumn colors → 橙、黃、棕
- nordic palette → 灰、白、藍

### 飽和度描述

```
highly saturated, vibrant colors → 高飽和鮮豔
desaturated, washed out → 低飽和褪色
oversaturated, neon colors → 過飽和霓虹
natural colors, true to life → 自然真實色彩
```

### 對比度

```
high contrast → 強對比
low contrast, soft → 低對比柔和
dramatic contrast → 戲劇性對比
subtle contrast → 微妙對比
```

### 示例

```
warm color palette, golden tones → 暖色系金色調
cool blue and purple tones, high contrast
cyberpunk colors, neon pink and cyan, vibrant
pastel colors, soft and dreamy, low saturation
monochromatic blue, various shades of blue
```

### 複用價值
⭐⭐⭐⭐⭐
- 定義視覺情緒
- 風格一致性關鍵

---

## 9. 時間/季節 (Time & Season) ✨ 新增

**定義**：時間段、季節、天氣狀態。

### 子模組
- **time_of_day**: 時間段
- **season**: 季節
- **weather**: 天氣狀態

### 時間段

**黃金時刻**：
- golden hour (日出日落前後1小時)
- blue hour (民用曙暮光時段)
- magic hour (魔法時刻)

**一天時段**：
- dawn, sunrise (黎明、日出)
- morning, noon (早晨、正午)
- afternoon (下午)
- dusk, sunset (黃昏、日落)
- twilight (暮光)
- night, midnight (夜晚、午夜)

### 季節特徵

| 季節 | 視覺特徵 | 關鍵詞 |
|------|---------|--------|
| 春 Spring | 新綠、花朵 | cherry blossoms, fresh green |
| 夏 Summer | 明亮、陽光 | bright sunlight, lush |
| 秋 Autumn | 金黃、落葉 | golden leaves, harvest |
| 冬 Winter | 雪、冷色 | snow, frost, cold |

### 天氣狀態

**晴朗**：
- clear sky, sunny
- cloudless, bright

**雲霧**：
- cloudy, overcast
- misty, foggy
- hazy

**降水**：
- rainy, rain drops
- snowy, snowfall
- stormy

**特殊天氣**：
- dramatic clouds
- storm clouds, lightning
- rainbow after rain

### 光線與時間的關係

```
golden hour → 溫暖金色光線，長陰影
blue hour → 冷藍色調，柔和光線
noon → 強烈頂光，短陰影
overcast → 柔和漫射光，無明顯陰影
```

### 示例

```
golden hour lighting, warm sunset glow
misty morning, soft diffused light
winter scene, snow falling, cold blue tones
stormy sky, dramatic clouds, moody atmosphere
cherry blossom season, spring, soft pink petals
```

### 複用價值
⭐⭐⭐⭐
- 自然光效的關鍵
- 氛圍營造重要元素

---

## 10. 參考藝術家/作品 (References) ✨ 新增

**定義**：引用特定藝術家、作品風格、平臺風格。

### 子模組
- **artists**: 藝術家名稱列表
- **styles**: 特定風格引用
- **platforms**: 平臺風格

### 熱門藝術家

**數字藝術**：
- Greg Rutkowski (奇幻、史詩)
- Artgerm (人物、插畫)
- Sakimichan (動漫風)
- Loish (色彩、角色)

**傳統大師**：
- Rembrandt (光影大師)
- Monet (印象派)
- Van Gogh (後印象派)
- Caravaggio (巴洛克)

**概念藝術**：
- Syd Mead (未來主義)
- H.R. Giger (生物機械)
- Moebius (科幻漫畫)

**攝影師**：
- Annie Leibovitz (人像)
- Ansel Adams (風光)
- Steve McCurry (紀實)

### 工作室/品牌風格

```
Studio Ghibli style → 吉卜力動畫風格
Pixar style → 皮克斯3D動畫
Disney animation → 迪士尼風格
Wes Anderson aesthetic → 韋斯·安德森電影美學
```

### 平臺引用

**藝術社群**：
- trending on ArtStation
- featured on Behance
- DeviantArt popular

**攝影平臺**：
- 500px, Flickr
- National Geographic style
- Vogue magazine style

### 使用技巧

**單一引用**：
```
portrait by Annie Leibovitz → 清晰風格指向
```

**混合引用**：
```
Greg Rutkowski and Alphonse Mucha style → 融合兩種風格
in the style of Studio Ghibli meets Moebius → 風格碰撞
```

**時代引用**：
```
renaissance painting style → 文藝復興風格
80s retro aesthetic → 80年代復古
```

### 示例

```
fantasy landscape, Greg Rutkowski style, dramatic lighting
portrait, Annie Leibovitz style, fashion photography
cyberpunk city, Syd Mead inspired, futuristic
anime character, Studio Ghibli style, watercolor
trending on ArtStation, award-winning digital art
```

### 複用價值
⭐⭐⭐⭐⭐
- 快速傳達風格期望
- 專業圈層認可度高

---

## 模組使用策略

### 必備模組（每個提示詞都應包含）

1. ✅ **主體變數** - 核心物件
2. ✅ **細節增強** - 質量保障
3. ✅ **視覺風格** 或 **參考藝術家** - 風格定義

### 高價值模組（顯著提升質量）

4. ⭐ **技術引數** - 專業感
5. ⭐ **構圖引數** - 專業攝影感
6. ⭐ **色彩方案** - 視覺一致性

### 氛圍模組（增強表現力）

7. **情緒氛圍** - 情感傳遞
8. **時間/季節** - 自然光效

### 輔助模組（按需使用）

9. **約束條件** - 避免常見問題
10. 其他專項模組

---

## 模組組合模板

### 人像攝影模板

```
{主體} + {技術引數} + {光線} + {構圖} + {細節增強}

示例：
portrait of a young woman, 85mm lens f/1.4, soft studio lighting,
shallow depth of field, rule of thirds composition,
ultra detailed, photorealistic, 8k
```

使用模組：1, 3, 4, 7, 5

---

### 風景攝影模板

```
{場景} + {時間/季節} + {色彩} + {構圖} + {氛圍} + {細節}

示例：
mountain landscape, golden hour sunset, warm orange and purple tones,
wide angle shot, dramatic atmosphere, highly detailed, 8k, HDR
```

使用模組：1, 9, 8, 7, 5, 4

---

### 概念藝術模板

```
{主體} + {風格} + {參考} + {色彩} + {氛圍} + {細節}

示例：
futuristic city, cyberpunk aesthetic, Syd Mead inspired,
neon purple and cyan colors, moody atmosphere,
highly detailed, trending on ArtStation, 8k
```

使用模組：1, 2, 10, 8, 5, 4

---

### 角色設計模板

```
{角色} + {外觀} + {風格} + {參考} + {細節}

示例：
elven warrior princess, silver armor with celtic patterns,
fantasy art, Greg Rutkowski style, intricate details,
highly detailed, 8k, masterpiece
```

使用模組：1, 2, 10, 4

---

## 模組權重建議

不同AI工具對模組的敏感度不同：

| 模組 | Midjourney | Stable Diffusion | DALL-E 3 |
|------|------------|------------------|----------|
| 主體變數 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 視覺風格 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 技術引數 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 細節增強 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 參考藝術家 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 構圖引數 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 色彩方案 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 時間/季節 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 約束條件 | ⭐⭐⭐ (--no) | ⭐⭐⭐⭐⭐ | ⭐⭐ |

---

## 快速參考卡片

**最小可用提示詞**（3模組）：
```
{主體} + {風格} + {質量}
girl + anime style + detailed
```

**標準提示詞**（5-6模組）：
```
{主體} + {風格} + {技術} + {構圖} + {色彩} + {質量}
portrait + cinematic + 85mm f/1.4 + close-up + warm tones + 8k
```

**專業提示詞**（8-10模組全覆蓋）：
```
所有模組精細配置，300+ tokens
```

---

**使用這個參考手冊**可以：
- 快速查詢模組定義
- 理解每個模組的作用
- 學習專業術語
- 構建自己的提示詞模板