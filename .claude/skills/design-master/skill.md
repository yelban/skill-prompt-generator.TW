---
name: design-master
description: 平面設計主控 - 自動生成平面設計提示詞，支援海報、logo、插畫等多種設計型別
---

# Design Master - 平面設計主控 Skill

**版本**: 1.0
**領域**: 平面設計
**架構**: Master-Subordinate
**資料來源**: Universal Elements Database

## 🎯 核心功能

自動生成高質量的平面設計提示詞，支援：
- 🎨 佈局系統（Bento Grid、對分屏、網格拼貼等）
- ✨ 視覺效果（Glassmorphism、漸變、3D等）
- 🎭 設計風格（現代極簡、復古、科技等）
- 🌈 色彩方案（配色規則、色調控制）
- 📐 構圖技巧（對稱、黃金比例、視覺層次）

---

## 📋 使用方式

### 方式1：元素級生成（靈活組合）

```
生成一個Bento Grid佈局海報
```

或

```
平面設計：現代極簡風格，玻璃態效果
```

**原理**：從80個design元素中智慧選擇並組合

---

### 方式2：模板級生成（完整系統）⭐ 新增

```
生成Apple風格PPT模板
```

或

```
使用現代商務科技典雅風格PPT模板
```

**關鍵詞**：包含"模板"一詞觸發模板查詢

**原理**：從design_templates表查詢完整設計系統

**返回內容**：
- 設計理念說明
- 完整元素列表（12個元素，按結構組織）
- 使用場景和指南
- 組裝好的完整提示詞

---

## 🔄 工作流程

### 元素級流程（預設）

```
使用者輸入（不含"模板"關鍵詞）
  ↓
查詢design領域元素 (80 elements)
  - layout_systems: Bento網格、對分屏等
  - visual_effects: 玻璃態、漸變等
  - color_schemes: 配色方案
  - typography: 字體系統
  - backgrounds: 背景系統
  ↓
智慧選擇元素
  - 根據使用者需求匹配
  - 語義相關性排序
  ↓
組裝Prompt
  1. 佈局系統
  2. 視覺效果
  3. 色彩方案
  4. 技術引數（4K、DPI）
  ↓
輸出完整設計Prompt
```

### 模板級流程（包含"模板"關鍵詞）⭐ 新增

```
使用者輸入（包含"模板"）
  ↓
檢測關鍵詞："模板" | "template"
  ↓
查詢design_templates表
  - 匹配name、chinese_name、style_tags
  - 示例：Apple → "Apple淡藍商務PPT"
  ↓
返回完整模板
  - 設計理念
  - 12個元素（按結構組織）
  - 使用場景
  - 完整提示詞
  ↓
輸出模板詳情 + 提示詞
```

---

## 📊 資料來源

### 元素庫（elements表）

**領域**: `design` domain (80 elements)

**元素類別**:
- `layout_systems` - 佈局系統
- `visual_effects` - 視覺效果
- `color_schemes` - 配色方案
- `typography` - 字體系統
- `backgrounds` - 背景系統

**可用標籤**:
- `bento-grid`, `glassmorphism`, `modern`
- `minimalist`, `grid`, `layout`, `apple`

### 模板庫（design_templates表）⭐ 新增

**當前模板數**: 1個

**已有模板**:
1. **Apple淡藍商務PPT** (template_apple_soft_blue_ppt_v1)
   - 類別: ppt_design
   - 包含: 12個元素
   - 標籤: apple, business, soft_blue, minimal, professional
   - 適用: 商務彙報、產品釋出會、資料分析

**模板分類**:
- `ppt_design` - PPT演示設計
- `ui_system` - UI設計系統
- `brand_vi` - 品牌視覺識別
- `web_design` - 網頁設計系統
- `dashboard` - 儀表板設計

---

## ✅ 輸出示例

### 示例1：元素級生成

**輸入**: `生成Bento Grid玻璃態海報`

**輸出**:
```
Modern Bento grid layout with 8 asymmetric modular cards, frosted glass effect
with 80% translucency and backdrop blur filter, minimalist modern aesthetics,
90% neutral colors with 10% vibrant accent colors, clean typography, 4K
resolution, professional graphic design, UI/UX design system, contemporary
digital poster design
```

### 示例2：模板級生成 ⭐ 新增

**輸入**: `生成Apple風格PPT模板`

**輸出**:
```
📋 找到匹配模板：現代商務科技典雅風格PPT - 淡藍裝飾版

🎯 設計理念：
極簡主義美學融合溫和的科技感。在Apple設計語言基礎上，
加入淡雅的藍色調和細膩的裝飾紋理，營造既專業又不失溫度
的商務氛圍。

📦 完整模板包含（12個元素）：

【背景系統】
• Apple風格淡藍漸變背景
• 四層裝飾背景系統

【佈局系統】
• Apple風格玻璃卡片系統
• 12列8點網格系統

【配色系統】
• Apple商務藍配色系統

【字體系統】
• Apple字型層級系統

【視覺效果】
• macOS視窗三色圓點
• SF Symbols超細線性圖示
• Apple風格柔和藍資料圖表
• 淡藍標籤元件
• Apple圓角層級系統
• 藍色調投影系統

🎨 使用場景：
高階商務彙報、產品釋出會、資料分析報告

✨ 完整模板提示詞：
────────────────────────────────────────
[包含全部12個元素的完整提示詞]
────────────────────────────────────────
```

---

**Skill狀態**: ✅ 已實現（v1.1 - 支援模板系統）
