---
name: prompt-xray
description: 提示詞X光透視 - 從優秀提示詞中逆向提取"如何做X"的知識，讓黑盒變透明
---

# Prompt Xray - 提示詞逆向工程系統

**設計哲學**: 拆解黑盒，讓模糊變清晰
**核心能力**: 回答"如何做X"的問題

---

## 🎯 解決的問題

**問題**: 提示詞是黑盒 → 不知道：
- 如何控制顏色？
- 如何控制空間佈局？
- 如何新增標誌性符號？
- 如何調整排版？
- 如何控制材質？
- 如何控制光影？

**解決**: 從N個優秀提示詞中提取規律 → 生成知識庫

---

## 📋 使用方式

### 方式1：提取單一維度知識

```
從已分析的提示詞中，提取"如何控制顏色"的知識
```

### 方式2：提取所有維度知識

```
從已分析的提示詞中，構建完整知識庫
```

### 方式3：指定範圍

```
分析moss_terrarium系列，提取配色知識
```

---

## 🔄 執行流程

當用戶請求提取知識時，你需要：

### Step 1: 讀取資料
使用工具讀取 `extracted_results/` 下的所有 `*_extracted.json` 檔案：
```python
from xray_helper import load_prompts
prompts = load_prompts(pattern="*_extracted.json")
```

### Step 2: 按維度分析
根據使用者請求的維度，分析對應模組：

#### 如果使用者要"顏色"知識：
- 提取所有 `color_scheme` 模組
- 分析配色公式、關鍵詞、技巧
- 按下面的模板生成Markdown

#### 如果使用者要"佈局"知識：
- 提取所有 `composition` 模組
- 分析視角、構圖規則、定位方法
- 按模板生成Markdown

#### 如果使用者要"符號"知識：
- 提取 `constraints` 和 `detail_enhancers` 模組
- 分析文字語法、Logo新增方法
- 按模板生成Markdown

#### 如果使用者要"材質"知識：
- 提取 `detail_enhancers` 和相關描述
- 分析表面特徵、物理屬性、質感關鍵詞
- 按模板生成Markdown

#### 如果使用者要"光影"知識：
- 提取 `technical_parameters.lighting` 和 `mood_atmosphere`
- 分析光源型別、布光方案、氛圍效果
- 按模板生成Markdown

#### 如果使用者要"排版"知識（設計類）：
- 提取 `composition` 和 `visual_style`
- 分析柵格系統、視覺層級、對齊規則
- 按模板生成Markdown

### Step 3: 生成知識卡片
使用工具儲存結果：
```python
from xray_helper import save_knowledge_card
save_knowledge_card(dimension="color", content=markdown_content)
```

---

## 📝 輸出模板

### 模板1: 如何控制顏色？

```markdown
# 如何控制顏色？

**分析時間**: {當前時間}
**樣本數量**: {分析了多少個提示詞}
**資料來源**: {哪些提示詞}

---

## 🎨 配色公式

### 公式1: 冷暖對立（7:3黃金比例）
- **公式**: `70% cool base + 30% warm accent`
- **來源**: moss_terrarium_001
- **效果**: 自然和諧 + 視覺層次

### 公式2: ...

---

## 📚 顏色關鍵詞庫

### 冷色系
- `rich forest greens`
- `deep ocean blues`
- `ice whites`

### 暖色系
- `warm amber wood tones`
- `sunset orange`
- `golden hour light`

### 中性色
- `grayscale`
- `pristine whites`

---

## 🛠️ 配色技巧

1. **溫度對比** - 冷色環境 + 暖色焦點 = 視覺層次
2. **7:3比例** - 主色70%，焦點色30%
3. **單色調+焦點色** - 極簡風格

---

## 💡 應用案例

### 案例1: moss_terrarium_001
**配色方案**: rich forest greens (70%) + warm amber wood (30%)
**效果**: Natural harmony, clear focal point
**適用場景**: 自然場景、植物攝影

### 案例2: ...

```

### 模板2: 如何控制空間佈局？

```markdown
# 如何控制空間佈局？

**分析時間**: {當前時間}
**樣本數量**: {分析了多少個提示詞}

---

## 🎥 視角選擇

### `slight top-down angle`
**適用場景**: 微縮場景、產品攝影、生態瓶
**關鍵詞**: `top-down view`, `bird's eye view`, `overhead angle`
**案例**: moss_terrarium_001, moss_terrarium_002
**效果**: 展示全貌，適合平鋪佈局

### `isometric view`
**適用場景**: 3D產品、遊戲場景、建築
**關鍵詞**: `isometric`, `45-degree angle`
**效果**: 保持平行線，無透視變形

---

## 📐 構圖規則

### Golden Ratio（黃金比例）
**關鍵詞**: `golden ratio composition`, `phi grid`
**效果**: 經典和諧比例，視覺平衡
**使用頻率**: 3次

### Rule of Thirds（三分法）
**關鍵詞**: `rule of thirds`, `thirds grid`
**效果**: 動態平衡，引導視線

### Centered Symmetry（中心對稱）
**關鍵詞**: `centered`, `perfectly symmetrical`
**效果**: 穩定、莊重感

---

## 🎯 定位方法

### 相對位置描述
- `iPhone placed next to notebook`
- `floating in 3D space`
- `bottom-left quadrant`

### 精確座標（高階）
- `Subject A [X: 20-40, Y: 60-100] (Bottom-Left)`
- `Subject B [X: 60-80, Y: 0-40] (Top-Right)`

---

## 💡 應用案例

### 案例1: moss_terrarium_001
**視角**: slight top-down angle
**構圖**: centered in frame, golden ratio
**定位**: terrarium centered, cottage as focal point

```

### 模板3: 如何新增標誌性符號？

```markdown
# 如何新增標誌性符號？

---

## ✍️ 文字新增語法

### 基礎語法
```
text "HELLO" in bold serif
large bold sans-serif text "SALE" in red
neon red cursive script "OPEN"
```

### 位置控制
- `lower left corner`
- `centered at top`
- `floating in 3D space`

---

## 🏷️ Logo/水印新增

### 正確示例
```
small square watermark in lower left corner
simple logo in top-right, 10% opacity
brand symbol integrated into design
```

### ❌ 反面案例（避免）
- `exactly 10x10 pixels` → AI無法保證畫素精度
- `Gothic font AND Arial font` → 矛盾指令
- `mandatory mandatory mandatory` → 重複無效

---

## 🎨 符號風格

### 材質效果
- `neon` - 霓虹燈效果
- `embossed` - 浮雕效果
- `metallic sheen` - 金屬光澤
- `glowing` - 發光效果

### 字型風格
- `bold serif` - 粗體襯線
- `sans-serif` - 無襯線
- `cursive script` - 草書
- `calligraphy` - 書法體

```

### 模板4: 如何控制材質？

```markdown
# 如何控制材質？

---

## 🔍 表面特徵

### 金屬材質
- `brushed titanium` - 拉絲鈦金屬
- `polished chrome` - 拋光鍍鉻
- `metallic sheen` - 金屬光澤

### 有機材質
- `living green textures` - 生機勃勃的綠色質感
- `natural wood grain` - 天然木紋
- `rough bark` - 粗糙樹皮

### 玻璃/透明
- `under glass` - 玻璃下
- `translucent` - 半透明
- `crystal clear` - 晶瑩剔透

---

## ⚙️ 物理屬性

- `glossy` / `matte` - 光澤/啞光
- `reflective` / `absorptive` - 反射/吸收
- `weathered` / `pristine` - 風化/原始
- `soft` / `rigid` - 柔軟/堅硬

---

## ✨ 光學效果

- `morning dew droplets` - 晨露水珠
- `soft sunlight reflections on glass` - 玻璃上的柔和陽光反射
- `condensation` - 冷凝水汽
- `refraction` - 折射

```

### 模板5: 如何控制光影？

```markdown
# 如何控制光影？

---

## 💡 光源型別

### 自然光
- `soft diffused daylight` - 柔和漫射日光
- `golden hour light` - 黃金時段光線
- `morning sunlight` - 晨光
- `harsh noon sun` - 正午強光

### 人工光
- `studio lighting` - 影棚燈光
- `neon lights` - 霓虹燈
- `rim light` - 輪廓光
- `softbox overhead` - 頭頂柔光箱

---

## 🎬 布光方案

### Rembrandt Lighting（倫勃朗布光）
**效果**: 戲劇性，適合人像
**關鍵詞**: `Rembrandt light`, `triangle highlight`, `dramatic shadows`

### Soft Diffused Light（柔和漫射光）
**效果**: 自然、清新、無硬影
**關鍵詞**: `soft diffused`, `natural ambient`, `no harsh shadows`

### Rim Light（輪廓光）
**效果**: 勾勒邊緣，分離主體和背景
**關鍵詞**: `rim lighting`, `backlight`, `edge highlight`

---

## 🌤️ 光線+氛圍公式

### 清新寧靜
```
soft diffused daylight + morning dew = fresh, peaceful atmosphere
```

### 戲劇張力
```
Rembrandt light + rim light = dramatic portrait with depth
```

### 科技未來
```
neon accent lights + volumetric fog = cyberpunk atmosphere
```

---

## 🌫️ 大氣效果

- `volumetric fog` - 體積霧
- `misty` - 霧濛濛
- `hazy` - 朦朧
- `clear crisp air` - 清澈空氣

```

---

## 🛠️ 工具函式

你需要使用 `xray_helper.py` 中的工具函式：

### 讀取提示詞
```python
from xray_helper import load_prompts

# 載入所有提示詞
all_prompts = load_prompts()

# 載入特定範圍
moss_prompts = load_prompts(pattern="moss_terrarium*")
```

### 儲存知識卡片
```python
from xray_helper import save_knowledge_card

save_knowledge_card(
    dimension="color",
    content=markdown_content,
    metadata={
        'samples': 10,
        'source': 'moss_terrarium + ethereal_deity'
    }
)
```

---

## 💡 關鍵原則

### 1. 尋找規律，不是羅列
❌ 錯誤：只列出所有顏色關鍵詞
✅ 正確：發現配色公式（如：70% cool + 30% warm）

### 2. 提取技巧，不是描述
❌ 錯誤："這個提示詞用了森林綠"
✅ 正確："冷色環境 + 暖色焦點 = 視覺層次"

### 3. 給出案例，可直接複用
❌ 錯誤：模糊描述"使用對比色"
✅ 正確：具體案例 `rich forest greens + warm amber wood`

### 4. 學習優秀，也學習錯誤
- 從A級提示詞學習最佳實踐
- 從D級提示詞（如pencil_sketch_idol）學習反面案例

---

## 📊 分析步驟（詳細）

### 當用戶說："提取如何控制顏色的知識"

**Step 1**: 載入資料
```python
prompts = load_prompts()
```

**Step 2**: 遍歷所有提示詞，提取 color_scheme 模組
```python
color_data = []
for prompt in prompts:
    if 'color_scheme' in prompt['modules']:
        color_data.append({
            'id': prompt['prompt_id'],
            'scheme': prompt['modules']['color_scheme']
        })
```

**Step 3**: 分析配色公式
- 查詢 `primary_palette` 欄位
- 檢查 `temperature` 描述（如："balanced - cool greens + warm wood"）
- 識別比例關係（70%/30%）
- 提取 `concept`（如："Cold Shell, Warm Heart"）

**Step 4**: 分類關鍵詞
- 遍歷所有顏色描述
- 分為冷色/暖色/中性色
- 去重，排序

**Step 5**: 提取技巧
- 溫度對比？
- 高對比/低對比？
- 單色調+焦點色？

**Step 6**: 建立案例
- 選擇最佳3-5個案例
- 包含：配色方案、效果、適用場景

**Step 7**: 生成Markdown
- 按模板填充內容
- 使用 `save_knowledge_card()` 儲存

---

## 🎯 輸出位置

所有知識卡片儲存到：
```
knowledge_base/
├── how_to_control_color.md
├── how_to_control_layout.md
├── how_to_add_symbols.md
├── how_to_control_materials.md
├── how_to_control_lighting.md
└── how_to_control_typography.md (針對設計類)
```

---

## ✅ 驗收標準

生成的知識卡片應該：
1. ✅ 回答"如何做X"的問題
2. ✅ 包含具體的關鍵詞和公式
3. ✅ 有3+個真實案例
4. ✅ 可以直接複用到新提示詞中
5. ✅ 既有正面案例，也有反面教訓

---

**Skill狀態**: ✅ 設計完成
**最後更新**: 2026-01-04
**使用工具**: xray_helper.py
