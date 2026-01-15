---
name: video-master
description: 影片生成主控 - 自動生成影片場景提示詞，支援動態效果、轉場、運鏡等
---

# Video Master - 影片生成主控 Skill

**版本**: 1.0
**領域**: 影片生成
**架構**: Master-Subordinate
**資料來源**: Universal Elements Database

## 🎯 核心功能

自動生成高質量的影片場景提示詞，支援：
- 🎬 場景型別（武俠、科幻、動作、劇情等）
- 📹 相機運動（推進、拉遠、跟蹤、環繞等）
- ⚡ 動作效果（慢動作、快速剪輯、特效）
- 🎭 敘事元素（角色、環境、氛圍）
- 🌅 光照場景（黃昏、黎明、夜晚、室內）

---

## 📋 使用方式

### 快速生成

```
生成一個武俠動作場景影片
```

或

```
影片場景：電影級質感，慢鏡頭，動態相機運動
```

---

## 🔄 工作流程

```
使用者輸入
  ↓
查詢video領域元素 (1 element)
  - scene_types: 武俠等
  - camera_movements: 動態運鏡（待補充）
  - motion_effects: 慢動作等（待補充）
  ↓
組裝Prompt
  1. 場景描述
  2. 相機運動
  3. 動作效果
  4. 技術引數（8K HDR）
  ↓
輸出完整影片Prompt
```

---

## 📊 資料來源

**主要庫**: `video` domain (1 element)

**元素類別**:
- `scene_types` - 場景型別
- `camera_movements` - 相機運動（待補充）
- `motion_effects` - 動態效果（待補充）
- `transitions` - 轉場效果（待補充）

**可用標籤**:
- `cinematic`, `action`, `dramatic`
- `slow-motion`, `tracking-shot`

---

## ✅ 輸出示例

**輸入**: `生成武俠動作場景`

**輸出**:
```
Cinematic Chinese martial arts action scene, dynamic tracking shot following
warrior through bamboo forest, slow-motion combat sequences with sword fighting,
dramatic lighting with volumetric fog effects, 8K HDR quality, film-grade
cinematography, fluid camera movements, epic atmosphere with traditional
Chinese aesthetics, professional action choreography, movie-quality VFX
```

---

**Skill狀態**: ✅ 已實現
**Note**: 影片領域元素較少（1個），建議後續補充更多camera_movements和motion_effects
