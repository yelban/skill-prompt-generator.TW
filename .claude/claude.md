# Claude Code 專案規則

## ⚠️ SKILL呼叫規則（最高優先順序）

### 當用戶請求生成提示詞時

---

### 📊 架構原理（重要！）

**統一資料來源，分層訪問**：

所有學習成果都儲存在 `elements.db`（1103元素，12領域），但每個skill訪問不同的領域：

| Skill | 訪問Domain | 元素數 | 框架/方法 | 專長 |
|-------|-----------|--------|----------|------|
| intelligent-prompt-generator | portrait | 491 | 人像框架(7大類) | 五官、妝容、表情、人像光影 |
| art-master | art | 51 | 直接查詢 | 藝術技法、筆觸、留白 |
| design-master | design | 59 | 直接查詢 | Bento Grid、玻璃態、佈局 |
| product-master | product | 77 | 直接查詢 | 商業攝影、產品布光 |
| video-master | video | 49 | 直接查詢 | 鏡頭運動、轉場、特效 |
| **prompt-crafter** ⭐ | design (變數庫) | 20萬+組合 | 專業設計系統 | 配色方案、裝飾元素、風格推薦 |

**關鍵**：
- intelligent-prompt-generator 使用 `prompt_framework.yaml`（人像專用框架）
- 框架包含：subject（主體）、facial（面部）、styling（造型）、expression（表情）、lighting（光影）、scene（場景）、technical（技術）
- **所有欄位都是人像專用**：eyes, nose, lips, makeup, hairstyle, pose 等
- 風景畫、產品、海報不需要這些欄位 → 必須用domain expert skills

---

### ⚡ 快速決策樹

```
使用者請求
    ↓
【有人物嗎？】
    ↓
  YES ────────────→ intelligent-prompt-generator
    │               （portrait domain, 491元素）
    │               除非強調藝術技法術語
    │
  NO
    ↓
【主體是什麼？】
    ↓
    ├─ 風景/靜物/藝術繪畫 → art-master (art domain, 51元素)
    ├─ 產品/商品 → product-master (product domain, 77元素)
    ├─ 海報/UI/佈局（需要設計術語） → design-master (design domain, 59元素)
    ├─ 海報/卡片（需要配色+風格系統） → prompt-crafter ⭐ (20萬+組合)
    └─ 影片/鏡頭運動 → video-master (video domain, 49元素)
```

---

**STEP 1: 判斷主體（最重要）**

首先判斷：**請求中是否包含人物？**

**YES - 有人物**：
- 預設傾向 → `intelligent-prompt-generator`（人像專家）
- 除非使用者明確強調藝術技法/設計佈局

**NO - 無人物**：
- 根據主體型別選擇專家（見下方）

---

**STEP 2: 根據主體型別選擇專家**

**🎨 藝術作品（無人物）** → `art-master`
- 關鍵詞：水墨畫山水、油畫風景、抽象藝術、靜物繪畫
- 示例："生成中國水墨畫山水" "油畫風格的靜物"

**🎯 平面設計（無人物）** → 兩種選擇：

**A. design-master** - 設計術語和佈局描述
- 關鍵詞：Bento Grid、玻璃態、UI、排版技術術語
- 示例："生成Bento Grid海報" "玻璃態UI設計"
- 輸出：設計術語描述

**B. prompt-crafter** ⭐ - 專業設計規範和配色系統
- 關鍵詞：溫馨可愛、現代簡約、配色方案、兒童教育、卡片設計
- 示例："生成溫馨可愛的兒童海報" "現代簡約科技宣傳圖"
- 輸出：完整設計規範（配色+圓角+陰影+裝飾+技術引數）

**如何選擇**：
- 需要設計術語 → design-master
- 需要完整設計系統（配色+裝飾+風格） → prompt-crafter

**📦 產品攝影（無人物）** → `product-master`
- 關鍵詞：產品、商品、商業攝影、包裝、靜物
- 示例："生成奢華手錶產品攝影" "書籍產品展示"

**🎬 影片場景（無人物）** → `video-master`
- 關鍵詞：影片、鏡頭運動、運鏡、轉場、動態場景
- 示例："生成武俠場景運鏡" "風景延時攝影"

**👤 人像攝影（有人物）** → `intelligent-prompt-generator`
- 關鍵詞：人物、肖像、面部、五官、表情、姿勢、妝容
- 示例："生成電影級亞洲女性" "美少女肖像"

---

**STEP 3: 衝突場景處理**

**當請求同時涉及人物 + 特殊風格時**（如："水墨畫風格的人物"）

**預設策略**（80%的情況適用）：
- 有人物 → 優先 `intelligent-prompt-generator`
- 原因：人像框架能處理人物屬性（五官、表情、妝容），風格透過 art_style 引數實現

**何時使用 art-master**（20%的情況）：
使用者明確強調藝術技法專業術語時：
- "水墨畫的**筆觸和留白技法**"
- "油畫的**厚塗和筆觸肌理**"
- "超現實主義的**藝術手法**"
- 關鍵詞：筆觸、留白、潑墨、厚塗、肌理、技法

**何時詢問使用者**：
當同時強調人物細節和藝術技法時：
```
我注意到你的請求涉及：
- 人物肖像（intelligent-prompt-generator 專長：深度五官理解）
- 水墨畫技法（art-master 專長：筆觸、留白、潑墨）

你更關注：
A. 人物細節（五官、表情、妝容）
B. 藝術技法（筆觸、留白、潑墨）

請選擇？
```

---

### 📝 示例對比表

**典型場景路由示例**：

| 使用者請求 | 有人物？ | 路由選擇 | 理由 |
|---------|---------|---------|------|
| "生成電影級亞洲女性" | ✅ | intelligent-prompt-generator | 人物肖像，需要五官妝容 |
| "生成水墨畫風格的女性" | ✅ | intelligent-prompt-generator | 主體是人物，水墨畫作為art_style |
| "生成中國水墨畫山水" | ❌ | art-master | 無人物，純藝術風格 |
| "生成Bento Grid海報" | ❌ | design-master | 無人物，設計佈局術語 |
| "生成溫馨可愛的兒童海報" | ❌ | **prompt-crafter** ⭐ | 需要配色+裝飾+風格系統 |
| "生成現代簡約科技宣傳圖" | ❌ | **prompt-crafter** ⭐ | 需要專業設計規範 |
| "生成奢華手錶產品攝影" | ❌ | product-master | 產品攝影 |
| "生成武俠場景運鏡" | ❌ | video-master | 鏡頭運動 |
| "生成女性肖像，要求水墨畫的筆觸留白" | ✅ | 詢問使用者 | 同時強調人物和藝術技法 |
| "生成Bento Grid海報，包含人物頭像" | ❌ | design-master | 主體是海報，人物只是元素 |

**邊界案例示例**：

| 使用者請求 | 分析 | 路由選擇 |
|---------|------|---------|
| "梵高風格的女性肖像" | 主體：女性肖像 / 風格：梵高 | intelligent-prompt-generator (art_style='van_gogh') |
| "油畫技法的厚塗肌理效果" | 無人物，強調技法 | art-master |
| "女模特展示香水瓶" | 焦點不明確（人物 vs 產品） | 詢問使用者焦點 |
| "武俠人物飛身躍起" | 人物動作 vs 鏡頭運動 | intelligent-prompt-generator (pose欄位) |

---

**STEP 4: 呼叫對應的專家 Skill**

使用 `Skill` tool 呼叫選定的專家：
- `Skill(command="art-master")`
- `Skill(command="design-master")`
- `Skill(command="product-master")`
- `Skill(command="video-master")`
- `Skill(command="intelligent-prompt-generator")`
- `Skill(command="prompt-crafter")` ⭐ **新增**

**你絕對不能**：
- ❌ 在conversation裡直接用Bash呼叫Python
- ❌ 在conversation裡直接生成提示詞
- ❌ 繞過skill自己做所有事情
- ❌ 所有請求都預設呼叫 intelligent-prompt-generator（要先識別領域）

### 為什麼要智慧路由？

**我們的目標**：讓每個領域專家發揮專長，不是把所有任務都扔給一個skill

**每個專家的獨特價值**：
- art-master: 藝術流派專業術語（筆觸、留白、潑墨）
- design-master: 現代設計系統（Bento Grid、Glassmorphism）
- product-master: 商業攝影器材（Phase One相機、softbox）
- video-master: 鏡頭語言（運鏡、轉場、特效）
- intelligent-prompt-generator: 深度人像理解（五官、人種推理）
- **prompt-crafter** ⭐: 專業設計規範（配色方案、裝飾元素、風格系統、20萬+組合）

---

## 🎯 其他Skill呼叫規則

### 當用戶請求專業設計提示詞時 ⭐ **新增**

**使用者說**：
- "生成溫馨可愛/現代簡約的海報"
- "我要做兒童教育/科技宣傳的設計"
- "需要配色方案"
- "幫我設計XX風格的卡片"

**你必須**：
✅ 呼叫 `prompt-crafter` skill

**prompt-crafter 的特點**：
- 從20萬+變數組合中取樣
- 輸出完整設計規範（配色+圓角+陰影+裝飾+技術引數）
- 支援風格：溫馨可愛、現代簡約
- 適用場景：兒童教育、科技商務、海報卡片設計

### 當用戶請求NotebookLM相關功能時

**使用者說**：
- "查詢NotebookLM"
- "生成播客/影片/思維導圖"
- NotebookLM相關任務

**你必須**：
✅ 呼叫 `notebooklm` skill

### 當用戶請求推特寫作時

**使用者說**：
- "生成推特內容"
- "基於知識庫寫推文"

**你必須**：
✅ 呼叫 `twitter-writer` skill

### 當用戶請求健身計劃時

**使用者說**：
- "制定健身計劃"
- "規劃運動安排"

**你必須**：
✅ 呼叫 `workout-planner` skill

### 當用戶請求寫作規劃時

**使用者說**：
- "幫我規劃文章"
- "構思部落格結構"

**你必須**：
✅ 呼叫 `writing-planner` skill

---

## 🤔 如果不確定

**當你不確定應該呼叫哪個skill時**：

1. ✅ **提問使用者**
2. ❌ **不要自己猜**
3. ❌ **不要在conversation裡直接做**

**問法示例**：
```
我注意到你的請求可能涉及XXX。

我應該：
A. 呼叫 XXX skill
B. 呼叫 YYY skill
C. 直接在這裡處理

請選擇？
```

---

## 📋 專案架構

### 核心系統：智慧提示詞生成

**入口**：`.claude/skills/intelligent-prompt-generator/skill.md`

**引擎**：`intelligent_generator.py`

**資料**：`extracted_results/elements.db`（1100+ 元素，持續增長）

**特性**：
- 語義理解（區分主體/風格/氛圍）
- 常識推理（人種→典型特徵）
- 一致性檢查（檢測邏輯衝突）
- 智慧修正（自動解決問題）

### 工作流程

```
使用者："生成XXX提示詞"
    ↓
Claude Code: 呼叫 intelligent-prompt-generator skill
    ↓
Skill: 解析意圖 + 呼叫Python + 生成提示詞
    ↓
返回完美提示詞
```

---

## 🚫 禁止行為

1. **繞過skill系統**
   - ❌ 直接在conversation呼叫Python
   - ❌ 自己實現skill應該做的事情

2. **不問就猜**
   - ❌ 不確定時自己決定
   - ✅ 應該提問使用者

3. **把skill當文件**
   - ❌ 只讀skill.md但不呼叫skill
   - ✅ 應該實際呼叫skill執行任務

---

## ✅ 正確示例

### 示例1：生成提示詞

**使用者**："生成電影級的亞洲女性，張藝謀電影風格"

**正確做法**：
```
立即呼叫 intelligent-prompt-generator skill
```

**錯誤做法**：
```
❌ 讓我用Bash呼叫Python生成...
❌ 讓我直接在這裡生成...
```

### 示例2：不確定場景

**使用者**："幫我最佳化這段程式碼"

**正確做法**：
```
這個任務不涉及現有的skill。
我應該直接在conversation處理，還是你希望建立新的skill？
```

**錯誤做法**：
```
❌ 直接開始最佳化（應該先確認）
```

---

## 🎯 核心原則

1. **Skill優先** - 能用skill的必須用skill
2. **提問為先** - 不確定時問使用者，不要猜
3. **系統完整性** - 證明skill系統可以工作，不是擺設

---

## 💡 設計原則（重要！）

### 原則1：解決根本問題，不是當前問題

**❌ 錯誤思維**：
- "提取率31.4%太低，補充提取邏輯"
- "新領域無法識別，新增更多關鍵詞"
- "準確率不夠，調整閾值"
- 頭痛醫頭，腳痛醫腳

**✅ 正確思維**：
- "為什麼要用關鍵詞匹配？我們有AI能力"
- "為什麼要硬編碼？應該AI驅動"
- "架構是否合理？是否可擴充套件？"
- 從根本上重新設計

**教訓**：
- 我們是 **Skill 系統**，有 Claude AI 能力
- 不要用 2010 年的方法（關鍵詞匹配、硬編碼規則）
- 應該用 2024 年的方法（AI 理解、智慧提取）
- **臨時補丁只會積累技術債，永遠解決不了根本問題**

### 原則2：說到做到，不要畫大餅

**❌ 常見錯誤**：
- 承諾"95%準確率"但沒驗證
- 說要"配置化"但繼續硬編碼
- 提議"AI驅動"但又建議臨時方案
- 說一套，做另一套

**✅ 正確做法**：
- 只承諾已驗證的效果
- 只提供真正打算實施的方案
- 誠實承認"不知道"
- 先做小規模測試，再下結論

### 原則3：架構優先於功能

**設計系統時要問**：
1. 這個設計是否可擴充套件？
2. 新需求來了是否要改程式碼？
3. 是否充分利用了 AI 能力？
4. 是否方便維護和測試？

**不要問**：
1. 能不能快速修復當前問題？
2. 能不能少改點程式碼？
3. 能不能不重構？

---

**記住**：
- 我們在建立 skill 系統，不是展示 Claude Code 有多強！
- **解決根本問題，不是當前問題**
- **說到做到，不要畫大餅**
