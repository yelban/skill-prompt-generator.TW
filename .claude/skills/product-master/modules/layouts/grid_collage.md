# Grid Collage 佈局模板

**版本**: 1.0
**用途**: 多角度產品展示的網格拼貼布局
**參考**: 基於專業時尚攝影的9宮格框架

---

## 📐 支援的佈局型別

### 3×3 Grid (9宮格) - 推薦

**適用場景**：
- 全方位產品展示
- 高階電商詳情頁
- 社交媒體輪播圖
- 產品宣傳海報

**特點**：
- 8格可見 + 1格中間遮擋 = 9格總數
- 中間3D產品巨大突出
- 最佳視覺衝擊力

### 2×2 Grid (4宮格)

**適用場景**：
- 簡潔對比展示
- 移動端最佳化
- 快速產品預覽

**特點**：
- 4格全部可見或3格可見+1格遮擋
- 適合簡約風格

### 4×1 Carousel (輪播條)

**適用場景**：
- 移動端橫向滑動
- 產品細節展示
- 故事化敘事

**特點**：
- 橫向4格排列
- 適合移動裝置

---

## 🎨 3×3 Grid 完整框架（專業模板）

以下是用於生成9宮格產品攝影的完整提示詞框架：

### 基礎結構

```
Create a 2:3 portrait luxury product poster featuring THE SAME [PRODUCT] shown in 9 different product photography styles with 3D pop-out effect:
```

---

### PRODUCT CONSISTENCY (產品一致性規則)

**CRITICAL - HIGHEST PRIORITY**

THE SAME [產品型別] appears in ALL 9 positions:
- Same product model, same design, same brand
- [產品具體描述：材質、顏色、特徵]
- [關鍵細節1]
- [關鍵細節2]
- [關鍵細節3]
- Its identity NEVER changes across all 9 appearances

**示例（手錶）**：
```
THE SAME luxury timepiece appears in ALL 9 positions:
- Same watch model, same design, same brand
- Premium Swiss automatic watch with blue dial
- Stainless steel case with polished and brushed finish
- Blue sunburst dial with applied silver hour markers
- Date window at 3 o'clock position
- Steel bracelet with three-link design
- Sapphire crystal with anti-reflective coating
- Its identity NEVER changes across all 9 appearances
```

---

### BACKGROUND LAYER (Z=0) - 8格背景攝影

**Grid Structure & Occlusion:**
- Standard 3×3 layout = 9 product photography shots
- **8 visible cells** (center cell [2,2] COMPLETELY OCCLUDED by 3D product)
- Cells separated by DISTINCT THICK WHITE LINES (3-4px) for clear separation

**8個不同攝影角度定義**：

```
[1,1] Top View - [產品頂視角]:
- Same product, face-up/top-down perspective
- Style: Macro close-up of top details
- Lighting: Soft top light, minimal shadows
- Sharp focus, clear details

[1,2] [關鍵細節1] Detail:
- Same product, [具體角度]
- Style: Macro detail of [特定部位]
- Lighting: Rim light highlighting [材質]
- Sharp focus, clear details

[1,3] [關鍵細節2] Detail:
- Same product, [具體角度]
- Style: [拍攝風格]
- Lighting: Controlled reflection on [材質]
- Sharp focus, clear details

[2,1] 45-Degree Hero Angle:
- Same product, classic product photography angle
- Style: Editorial magazine presentation
- Lighting: Three-point lighting, elegant shadows
- Sharp focus, clear details

[2,3] [特殊角度] View:
- Same product, [具體描述]
- Style: [技術/藝術特點]
- Lighting: [光照方式]
- Sharp focus, clear details

[3,1] Lifestyle/Context Shot:
- Same product, in use or lifestyle context
- Style: [場景描述]
- Lighting: Natural elegant ambient light
- Sharp focus, clear details

[3,2] [材質/紋理] Detail:
- Same product, texture close-up
- Style: Macro focus on [材質細節]
- Lighting: Gradient light revealing texture
- Sharp focus, clear details

[3,3] Packaging/Presentation:
- Same product, in premium display/packaging
- Style: Unboxing luxury experience
- Lighting: Soft diffused light on presentation
- Sharp focus, clear details
```

**手錶示例**：
- [1,1] Top View - Dial Detail（錶盤俯視）
- [1,2] Crown & Case Side Detail（錶冠側面）
- [1,3] Clasp Mechanism Detail（表扣細節）
- [2,1] 45-Degree Hero Angle（經典45度角）
- [2,3] Case Back Exhibition（底蓋/機芯）
- [3,1] On-Wrist Lifestyle Shot（上手效果）
- [3,2] Bracelet Link Detail（錶帶鏈節）
- [3,3] Packaging & Presentation（包裝盒）

---

### CRITICAL TECHNICAL SPECS (背景網格技術規範)

- Deep depth of field (f/16) - ALL products sharp and clear
- NO bokeh, NO blur, NO out-of-focus areas
- Even bright studio lighting across all cells
- High resolution details in every cell
- Thick white grid lines clearly visible between cells
- Background color: Bright minimalist studio white/grey gradient

---

### FOREGROUND LAYER (Z=5-10cm forward) - 3D突出產品

**THE SAME [PRODUCT] (Center Dominant Presentation):**

- Massive hyper-realistic 3D rendered product dominating the center
- Positioned at EXACT CENTER, completely occluding center cell [2,2]
- **Product top touches very top edge of canvas**
- **Product bottom touches very bottom edge of canvas**
- Occupies MAXIMUM vertical space for strong 3D illusion

**Presentation Style:**
- Dynamic floating perspective with slight rotation
- [具體角度，如：30-degree tilt showing both front and side]
- Suspended in space, [無背景干擾]
- Direct frontal presentation, commanding presence
- Full product visible from top to bottom

**Technical Execution:**
- Product extends 5-10cm forward from background plane
- Hyper-realistic 3D render (Blender/Cinema 4D quality)
- Substance 3D material: [材質列表：polished metal, glass, leather等]
- +20% saturation compared to background for "pop forward" effect
- Slightly sharper focus than background (but background still sharp)
- Photorealistic reflections and refractions
- Visible [產品特徵] clearly rendered

---

### OCCLUSION MECHANICS (遮擋機制)

**9格 - 1格遮擋 = 8格可見**

**Complete Occlusion:**
- Product body COMPLETELY covers center cell [2,2] (100% invisible)
- Center shot is fully hidden behind 3D product

**Partial Occlusion (Natural Edge Overlap):**
- Top [1,2]: [產品頂部] overlaps 10-15% into top detail shot
- Left [2,1]: [產品左側] overlaps 15-20% into hero angle shot
- Right [2,3]: [產品右側] overlaps 15-20% into right view shot
- Bottom [3,2]: [產品底部] overlaps 10-15% into bottom detail shot
- Overlaps break the white grid boundaries naturally

**Edge Treatment:**
- Soft organic transitions, NO hard cutout edges
- Product appears to physically exist in front of the grid
- Like a 3D display stand showcasing product above poster

---

### DEPTH EFFECTS (深度效果)

**Shadows:**
- Drop shadow from 3D product onto grid background
  * Blur: 12px
  * Color: rgba(0,0,0,0.25)
  * Offset: X=6px, Y=10px
- Contact shadow where product "hovers" on background
  * Blur: 8px
  * Color: rgba(0,0,0,0.35)
  * Creates floating suspension effect

**Lighting:**
- Background grid: Even bright studio lighting (no dramatic shadows)
- Foreground 3D product:
  * Key light upper left 45°
  * Fill light reducing harsh shadows
  * Rim light on edges for separation
  * Spotlight on key features for emphasis
- Consistent lighting direction across all elements

**Separation Techniques:**
- Slight brightness difference (foreground +10% brighter)
- Slight saturation boost (foreground +20% more saturated)
- Subtle sharpening halo around product edges
- Clear Z-axis spatial hierarchy

---

### CONSISTENCY RULES (一致性規則)

**Same Product Verification:**
- Same product model in all 9 positions
- Same [特徵1] with identical [細節]
- Same [特徵2] with same [細節]
- Same [特徵3]
- Same [關鍵元素] position
- Same brand logo placement

**What Changes:**
- ✅ Photography style (macro, lifestyle, technical, editorial)
- ✅ Camera angle and perspective
- ✅ Lighting setup and mood
- ✅ Focal point (different details in each cell)

**What NEVER Changes:**
- ❌ The product model or brand
- ❌ The [核心特徵1]
- ❌ The [核心特徵2]
- ❌ Any product specifications

---

### TECHNICAL SPECIFICATIONS (技術規格)

**Image Composition:**
- Aspect ratio: 2:3 portrait (or 9:16 vertical)
- Resolution: 2000×3000 pixels (or higher)
- Color mode: RGB, sRGB color space
- Quality: Professional commercial product photography

**Camera & Focus:**
- **Deep depth of field (f/16 or higher)**
- **NO selective focus, NO bokeh, NO blur**
- **ALL products in background grid MUST be sharp and clear**
- Foreground product slightly sharper for hierarchy
- Both layers fully illuminated and visible

**Environment:**
- Bright minimalist indoor studio
- Pure white or soft grey gradient background
- Clean, uncluttered aesthetic
- Premium luxury brand presentation
- Museum-quality display mood

**Layout:**
- Background: Clear 3×3 grid with THICK WHITE LINES visible
- Foreground: Massive full-product 3D render breaking grid boundaries
- Surreal creative product collage composition
- Editorial luxury advertising feel

**Material Rendering (3D Product):**
[根據產品型別定製材質列表]
- [材質1]: [具體效果描述]
- [材質2]: [具體效果描述]
- [材質3]: [具體效果描述]

---

### FORBIDDEN ELEMENTS (嚴格禁止)

**Product:**
- ❌ Different product models in different cells
- ❌ Changing colors or designs
- ❌ Different brands or styles
- ❌ Inconsistent product details

**Technical:**
- ❌ Blurred background or bokeh effect
- ❌ Out of focus products in grid
- ❌ Shallow depth of field
- ❌ Missing or unclear grid lines
- ❌ Dark shadows obscuring details
- ❌ Low resolution or pixelation
- ❌ Deformed product shapes
- ❌ Messy composition

**Structure:**
- ❌ 4×4 or other grid sizes (must be 3×3)
- ❌ All 9 cells visible (center must be occluded)
- ❌ Flat composition (must have clear 3D depth)
- ❌ Hard cutout edges on foreground product

---

### QUALITY CHECKLIST (質量檢查清單)

**Before Generation:**
- [ ] Same product model in all 9 positions?
- [ ] Each cell shows different photography style?
- [ ] Center cell [2,2] completely hidden?
- [ ] 8 visible background cells clearly defined?
- [ ] Thick white grid lines visible?
- [ ] ALL background products sharp and clear (no blur)?
- [ ] Foreground product full-size, top-to-bottom?
- [ ] Product extends maximum vertical space?
- [ ] Clear 3D pop-out effect with shadows?
- [ ] Natural edge overlaps into adjacent cells?
- [ ] Hyper-realistic 3D render quality?
- [ ] Deep depth of field maintained (f/16)?
- [ ] Material reflections realistic?
- [ ] Transparency/translucency visible (if applicable)?

---

### MIDJOURNEY COMMAND FORMAT

```
/imagine prompt: A surreal 3x3 luxury [product type] grid collage with THICK WHITE LINES separating cells. Background shows THE SAME [product description] in 8 different professional product photography styles ([列出8個角度]) - various angles but identical product. CENTER CELL HIDDEN. OVERLAID by a massive hyper-realistic 3D rendered floating version of THE SAME PRODUCT, top touching top edge, bottom touching bottom edge, [angle description]. ALL products in background sharp and in focus, deep depth of field f/16, no blur anywhere, bright studio lighting, clear white grid lines visible, strong 3D pop-out effect with drop shadows, professional commercial product photography, same product 9 times, photorealistic Substance 3D materials, [material list], 8k resolution --ar 2:3 --v 6.1 --style raw --quality 2
```

---

### MATHEMATICAL LOGIC (數學邏輯)

```
Same product × 9 different photography styles arranged in 3×3 grid.

Center style completely occluded by 3D foreground version =
8 visible background shots + 1 foreground 3D render =
9 total appearances of ONE PRODUCT with NINE photographic interpretations.
```

---

## 🎯 產品型別適配

### 手錶 (Luxury Watch)

**8個角度**：
1. 錶盤俯視 (Top View - Dial Detail)
2. 錶冠側面 (Crown & Case Side Detail)
3. 表扣細節 (Clasp Mechanism Detail)
4. 經典45度角 (45-Degree Hero Angle)
5. 底蓋/機芯 (Case Back Exhibition)
6. 上手效果 (On-Wrist Lifestyle Shot)
7. 錶帶鏈節 (Bracelet Link Detail)
8. 包裝盒 (Packaging & Presentation)

**材質渲染**：
- Polished stainless steel: mirror reflections
- Brushed steel: subtle linear grain
- Sapphire crystal: transparent with refraction
- Leather strap: realistic texture and stitching

### 香水 (Perfume Bottle)

**8個角度**：
1. 瓶蓋俯視 (Cap Top View)
2. 瓶身側面 (Bottle Side Profile)
3. 品牌Logo特寫 (Brand Logo Detail)
4. 經典45度角 (45-Degree Hero Angle)
5. 瓶底設計 (Base Design Detail)
6. 使用場景 (Lifestyle Context Shot)
7. 液體/漸變 (Liquid Gradient Detail)
8. 包裝盒 (Luxury Box Presentation)

**材質渲染**：
- Glass bottle: transparency, light refraction
- Gold cap: metallic sheen
- Liquid: color gradient, translucency
- Embossed logo: subtle depth

### 電子產品 (Electronics)

**8個角度**：
1. 正面螢幕 (Front Screen View)
2. 側面埠 (Side Ports Detail)
3. 背面Logo (Back Logo & Design)
4. 經典45度角 (45-Degree Hero Angle)
5. 內部結構 (Internal Structure/Components)
6. 使用場景 (In-Use Lifestyle Shot)
7. 材質紋理 (Material Texture Close-up)
8. 包裝全家福 (Unboxing All Contents)

**材質渲染**：
- Aluminum body: brushed metal finish
- Glass screen: anti-glare coating
- Plastic: matte or glossy finish
- LED indicators: subtle glow

---

## 💡 使用建議

1. **選擇合適的產品角度**：根據產品特點選擇最能展示特徵的8個角度
2. **保持一致性**：所有9個位置必須是同一產品
3. **材質真實性**：3D渲染的材質要與實物照片一致
4. **光照統一**：背景8格用均勻光照，前景3D用戲劇性光照
5. **深景深必須**：f/16確保所有格子都清晰，避免bokeh

---

**最後更新**: 2026-01-04
**維護者**: Product Master Skill System
