---
name: product-master
description: 產品攝影主控 - 自動生成產品攝影提示詞，支援商業拍攝、電商圖片等場景
---

# Product Master - 產品攝影主控 Skill

**版本**: 1.0
**領域**: 產品攝影
**架構**: Master-Subordinate
**資料來源**: Universal Elements Database

## 🎯 核心功能

自動生成高質量的產品攝影提示詞，支援：
- 📦 多種產品型別（書籍、電子產品、食品、時尚等）
- 📸 專業攝影技術（Phase One相機、微距、光照設定）
- 🎨 材質紋理（皮革、金屬、玻璃、木材等）
- 💡 光照佈局（柔光箱、環形光、自然光等）
- 🏆 高階質感（奢華、簡約、科技、復古等）

---

## 📋 使用方式

### 方式1：快速生成

```
生成一個高階書籍產品攝影
```

或

```
產品攝影：收藏版遊戲周邊
```

### 方式2：詳細定製

```
生成一個產品攝影：
- 產品：奢華手錶
- 風格：極簡高階
- 材質：金屬+皮革
- 光照：柔和反光
```

### 方式3：參考風格

```
生成類似Prompt #1的產品攝影（收藏版書籍風格）
```

### 方式4：網格拼貼布局（Grid Collage）

**適用場景**：
- 多角度產品展示
- 電商詳情頁
- 社交媒體內容
- 產品對比展示

**觸發關鍵詞**：
- "9宮格"、"3×3佈局"、"grid"
- "多角度展示"、"多視角"
- "中間3D突出"、"3D pop-out"
- "4宮格"、"2×2佈局"

**示例**：
```
生成9宮格手錶產品攝影，中間3D突出
```

**Skill會自動：**
1. 識別這是Grid Collage模式
2. 載入專業框架模板（參考 `modules/layouts/grid_collage.md`）
3. 生成包含以下特性的完整提示詞：
   - 嚴格的網格等分佈局（3×3、2×2等）
   - THICK WHITE LINES 清晰分隔
   - 中間格子被3D產品完全遮擋
   - 深景深（f/16）確保所有格子清晰
   - 專業深度效果（投影、層次、飽和度提升）
   - 完整的一致性檢查清單

**輸出特點**：
- 8個不同角度的產品攝影（背景層）
- 1個超大3D渲染產品（前景層，從頂到底佔滿畫布）
- 遮擋機制：中間格子100%遮擋，周圍4格部分遮擋
- 超現實拼貼藝術效果

---

## 🔄 工作流程

```
使用者輸入
  ↓
【識別需求】
  - 產品型別
  - 風格偏好
  - 材質要求
  ↓
【查詢資料庫】builder.md
  - 從elements.db搜尋product領域元素
  - 按標籤篩選（luxury, premium, glass...）
  - 按複用性排序
  ↓
【組裝Prompt】
  1. 產品主體描述 (product_types)
  2. 材質紋理 (material_textures)
  3. 攝影技術 (photography_techniques)
  4. 光照設定 (lighting_techniques)
  5. 技術引數 (technical_effects)
  6. 質量增強詞
  ↓
【輸出完整Prompt】
```

---

## 📊 資料來源

**主要庫**:
- `product` domain (4 elements)
- `common` domain (31 elements)

**元素類別**:
- `product_types` - 產品型別
- `material_textures` - 材質紋理
- `photography_techniques` - 攝影技術
- `lighting_techniques` - 光照技術
- `technical_effects` - 技術效果

**可用標籤**:
- `luxury`, `premium`, `high-end`
- `glossy`, `matte`, `reflective`
- `leather`, `metal`, `glass`, `wood`
- `macro`, `editorial`, `commercial`

---

## 🎨 支援的風格

- **Luxury Editorial** - 奢華編輯風格（雜誌級）
- **Minimalist Modern** - 極簡現代風格
- **Tech Premium** - 科技高階風格
- **Vintage Classic** - 復古經典風格
- **Artisanal Craft** - 手工藝品風格

---

## ✅ 輸出示例

**輸入**:
```
生成一個奢華書籍產品攝影
```

**輸出**:
```
Premium collector's edition book photographed with Phase One medium format
camera with 100mm macro lens, sophisticated softbox rim lighting creating
elegant highlights on Italian calfskin leather binding, glossy reflective
surface with high-end finish, metallic gold-embossed details, 4K ultra high
resolution, shallow depth of field isolating the subject, editorial magazine
quality photography, razor-sharp macro focus capturing every texture detail,
photorealistic render, professional commercial product shot, luxury brand
aesthetic, pristine studio environment with controlled lighting
```

---

## 🔧 模組說明

| 模組 | 檔案 | 功能 |
|------|------|------|
| 主控 | `skill.md` | 意圖識別和路由 |
| 組裝器 | `modules/core/builder.md` | 查詢資料庫並組裝Prompt |

---

**Skill狀態**: ✅ 已實現
**最後更新**: 2026-01-01
**維護者**: Universal Library System
