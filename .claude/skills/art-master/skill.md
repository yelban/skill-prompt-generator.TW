---
name: art-master
description: 藝術風格主控 - 自動生成藝術風格提示詞，支援水墨畫、油畫、超現實、插畫等多種藝術風格
---

# Art Master - 藝術風格主控 Skill

**版本**: 1.0
**領域**: 藝術風格
**架構**: Master-Subordinate
**資料來源**: Universal Elements Database

## 🎯 核心功能

自動生成高質量的藝術風格提示詞，支援：
- 🎨 藝術風格（水墨畫、油畫、超現實、插畫等）
- ✨ 特殊效果（玻璃碎片、光影、粒子效果等）
- 🖌️ 繪畫技法（筆觸、質感、構圖等）
- 🌈 色彩運用（冷暖色調、對比、和諧）
- 📜 文化風格（中式、日式、西方古典等）

---

## 📋 使用方式

### 快速生成

```
生成一箇中國水墨畫風格
```

或

```
藝術風格：超現實主義，夢境氛圍
```

---

## 🔄 工作流程

```
使用者輸入
  ↓
查詢art領域元素 (1 element)
  - art_styles: 中國水墨畫等
  - special_effects: 玻璃碎片等（需補充）
  ↓
組裝Prompt
  1. 藝術風格描述
  2. 特殊效果
  3. 繪畫技法
  4. 色彩運用
  ↓
輸出完整藝術Prompt
```

---

## 📊 資料來源

**主要庫**: `art` domain (1 element)

**元素類別**:
- `art_styles` - 藝術風格
- `special_effects` - 特殊效果（待補充）

**可用標籤**:
- `chinese-ink`, `painting`, `traditional`
- `surreal`, `dreamlike`, `artistic`

---

## ✅ 輸出示例

**輸入**: `生成中國水墨畫`

**輸出**:
```
Traditional Chinese ink painting style, flowing brush strokes with varying
ink density, minimalist composition emphasizing negative space, monochromatic
black ink with subtle grey washes, artistic interpretation of natural subjects,
poetic atmosphere with calligraphic elements, traditional Eastern aesthetics,
masterful brushwork technique, contemplative mood
```

---

**Skill狀態**: ✅ 已實現
**Note**: 藝術領域元素較少（1個），建議後續補充更多art_styles和special_effects
