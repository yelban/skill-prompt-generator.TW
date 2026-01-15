# Skill Prompt Generator - 基於Skills的智慧提示詞生成系統

> 🌐 **繁體中文版** | [English Version](https://github.com/huangserva/skill-prompt-generator)
> 📦 **Clone**: `git clone https://github.com/yelban/skill-prompt-generator.TW.git`

> 🎉 **v2.0 已釋出！** 新增跨domain查詢和設計系統整合。[檢視升級指南 →](UPGRADE_GUIDE_v2.0.md)

**一個 Claude Code Skills 專案**，透過12個專業領域Skills，基於Universal Elements Library（1246+元素）生成高質量AI影像提示詞。

### 🖼️ 支援的繪圖平台

| 平台 | 適用場景 | 提示詞格式 |
|------|----------|-----------|
| **Midjourney** | 藝術風格、概念設計 | 簡潔 + `--ar` 參數 |
| **Stable Diffusion** | 精確控制、專業攝影 | 詳細 + `(text:1.3)` 權重 |
| **DALL-E 3** | 快速原型、創意探索 | 自然語言 |
| **Nano Banana Pro** | 高品質寫實、人像攝影 | 自然語言（🆕 新增）|

> 💡 **Nano Banana Pro** 即 Google Gemini 3 Pro Image，支援中英文自然語言描述，無需特殊語法。

## 🆕 v2.0 新特性

- 🔄 **跨Domain查詢** - 資料庫利用率從40.3%提升到79.9%，充分利用所有領域元素
- 🎨 **設計系統整合** - 融合prompt-crafter的配色方案，支援20萬+組合
- 📐 **三種生成模式** - Portrait（人像）/ Cross-Domain（跨域）/ Design（設計）
- 🔧 **變數取樣系統** - 引數化元素，避免重複生成
- ✅ **100%向後相容** - v1.0功能完全保留

**[快速開始 v2.0 →](README_v2.0.md)** | **[完整升級指南 →](UPGRADE_GUIDE_v2.0.md)**

## 🎯 專案定位

**這不是一個普通的Python工具，而是一個完整的Skills系統：**

- 🎨 **Skills優先**：使用者透過呼叫Skills生成提示詞，不直接呼叫Python
- 🧠 **智慧路由**：自動識別領域（人像/藝術/設計/產品/影片），呼叫對應專家
- 📦 **12個專業Skills**：每個領域有獨立的專家Skill
- 💾 **統一資料來源**：所有Skills共享Universal Elements Library（1140+元素）

## ✨ 核心特性

### 🎯 Skills系統（核心）
- **12個專業領域Skills**：intelligent-prompt-generator, art-master, design-master, product-master, video-master, universal-learner等
- **智慧領域路由**：自動識別使用者需求，呼叫對應專家
- **模組化架構**：每個Skill獨立工作，協同配合

### 🆕 v2.0 三種生成模式
- **Portrait（人像）** - 純人像攝影，使用portrait domain（502元素）
- **Cross-Domain（跨域）** - 複雜場景，自動組合多個domains（995元素）
- **Design（設計）** - 海報卡片，SQLite元素 + YAML配色（20萬+組合）

### 🧠 智慧能力
- **語義理解**：區分主體/風格/氛圍
- **常識推理**：自動推斷合理屬性（如人種→眼睛顏色）
- **一致性檢查**：自動檢測並修正邏輯衝突
- **框架驅動**：基於`prompt_framework.yaml`結構化生成
- **🆕 跨域查詢**：自動識別所需domains並智慧組合
- **🆕 變數取樣**：引數化元素，智慧避免重複

### 📦 雙軌制系統
- **元素級生成**：從1246+個元素中智慧選擇組合
- **模板級生成**：完整設計系統模板（如Apple PPT模板）
- **🆕 設計變數庫**：37種配色方案 + 邊框 + 裝飾元素

### 📦 支援領域
- 📷 **portrait** - 人像攝影（502個元素）
- 🎨 **design** - 平面設計（155個元素，含5個完整模板）
- 🏠 **interior** - 室內設計
- 📦 **product** - 產品攝影（77個元素）
- 🎭 **art** - 藝術風格（51個元素）
- 🎬 **video** - 影片生成（49個元素）
- 📸 **common** - 通用攝影技術（205個元素）
- 🆕 **跨domain** - 自動組合多個領域（995個元素）
- 🆕 **設計變數** - 配色+邊框+裝飾（20萬+組合）

## 📦 安裝

### 前置要求

- **Claude Code** - 需要安裝Claude Code CLI
- **Python 3.8+** - 用於執行底層引擎
- **Git** - 用於克隆專案（可選）

### 安裝步驟

#### 方式1：克隆到本地（推薦）

```bash
# 1. 克隆專案
git clone https://github.com/yelban/skill-prompt-generator.TW.git

# 2. 進入專案目錄
cd skill-prompt-generator.TW

# 3. 安裝Python依賴（二選一）
pip install -r requirements.txt

# 或使用 uv（更快）
uv venv && uv pip install -r requirements.txt
```

**重要**：克隆後，`.claude/skills/` 下的12個Skills會自動被Claude Code識別。

#### 方式2：下載ZIP

1. 訪問 https://github.com/yelban/skill-prompt-generator.TW
2. 點選 "Code" → "Download ZIP"
3. 解壓到任意目錄
4. 安裝依賴（二選一）：
   - `pip install -r requirements.txt`
   - `uv venv && uv pip install -r requirements.txt`（更快）

### 驗證安裝

在Claude Code中測試：

```
# 測試人像生成skill
生成電影級的亞洲女性

# 測試設計skill
生成Bento Grid海報
```

如果Claude Code能正確呼叫Skills並生成提示詞，說明安裝成功。

---

## 🚀 快速開始

### 方式1：透過Skills使用（推薦）⭐

**這是主要使用方式** - 在Claude Code中直接呼叫Skills：

```
# 人像攝影（Portrait模式）
生成電影級的亞洲女性，張藝謀電影風格

# 跨domain場景（Cross-Domain模式）🆕
生成龍珠悟空打出龜派氣功的提示詞

# 設計海報（Design模式）🆕
生成溫馨可愛風格的兒童教育海報

# 平面設計
生成Bento Grid玻璃態海報

# 藝術繪畫
生成中國水墨畫山水

# 產品攝影
生成奢華手錶產品攝影
```

Claude Code會自動：
1. 識別領域（人像/設計/藝術/產品）
2. 識別生成模式（Portrait/Cross-Domain/Design）🆕
3. 呼叫對應的專家Skill
4. 返回完美的提示詞

### 方式2：直接呼叫v2.0 Python引擎 🆕

使用新的統一介面：

```python
from core.cross_domain_generator import CrossDomainGenerator

generator = CrossDomainGenerator()

# 自動識別型別（portrait/cross_domain/design）
result = generator.generate("龍珠悟空打出龜派氣功")

print(result['type'])      # cross_domain
print(result['prompt'])    # 完整提示詞
print(result['domains'])   # ['portrait', 'video', 'art', 'common']

generator.close()
```

### 方式3：使用v1.0 引擎（完全相容）

v1.0 API完全保留，無需修改：

```python
from intelligent_generator import IntelligentGenerator

gen = IntelligentGenerator()

# 生成人像提示詞（v1.0方式）
prompt = gen.generate_from_intent({
    'subject': {
        'gender': 'female',
        'ethnicity': 'East_Asian',
        'age_range': 'young_adult'
    },
    'styling': {
        'makeup': 'k_beauty'
    },
    'lighting': {
        'lighting_type': 'natural'
    }
})

print(prompt)
gen.close()
```

**注意**：
- **推薦使用方式1**（Skills）- 最簡單、最智慧
- **方式2**（v2.0）- 適合需要跨domain和設計系統的場景
- **方式3**（v1.0）- 適合只需要人像生成的場景

## 📖 專案結構

```
.
├── .claude/                       # ⭐ Skills系統（核心）
│   ├── CLAUDE.md                  # 專案規則和Skill路由指南
│   └── skills/                    # 12個專業領域Skills
│       ├── intelligent-prompt-generator/  # 人像提示詞專家
│       ├── art-master/            # 藝術風格專家
│       ├── design-master/         # 平面設計專家
│       ├── product-master/        # 產品攝影專家
│       ├── video-master/          # 影片生成專家
│       ├── universal-learner/     # 學習系統
│       ├── prompt-analyzer/       # 提示詞分析
│       ├── prompt-extractor/      # 元素提取
│       ├── prompt-generator/      # 通用生成器
│       ├── prompt-master/         # 主控排程
│       ├── prompt-xray/           # X-Ray分析
│       └── domain-classifier/     # 領域分類
│
├── 🆕 core/                       # v2.0 核心模組
│   ├── cross_domain_generator.py  # 統一生成介面（主入口）
│   ├── cross_domain_query.py      # 跨domain查詢引擎
│   ├── variable_sampler.py        # 變數取樣系統
│   ├── yaml_sampler.py            # YAML變數取樣
│   ├── design_bridge.py           # SQLite+YAML融合
│   └── schema_migration_v1.sql    # 資料庫擴充套件指令碼
│
├── 🆕 variables/                  # 設計變數庫（YAML）
│   ├── colors.yaml                # 37種配色方案
│   ├── borders.yaml               # 邊框樣式
│   └── decorations.yaml           # 裝飾元素
│
├── 🆕 design-logic/               # 設計邏輯系統
│   ├── warm-cute/                 # 溫馨可愛風格
│   └── modern-minimal/            # 現代簡約風格
│
├── intelligent_generator.py       # Python引擎：核心生成
├── framework_loader.py            # Python引擎：框架載入
├── element_db.py                  # Python引擎：資料庫操作
├── prompt_framework.yaml          # 人像框架定義
│
├── extracted_results/
│   └── elements.db                # Universal Elements Library (1246+元素)
│
├── README_v2.0.md                 # 🆕 v2.0快速開始
├── UPGRADE_GUIDE_v2.0.md          # 🆕 v2.0升級指南
├── requirements.txt               # Python依賴
└── README.md                      # 專案文件（本檔案）
```

**架構說明**：
- **使用者層**：透過Claude Code呼叫Skills
- **Skills層**：12個專業領域專家（.claude/skills/）
- **🆕 v2.0引擎層**：core/ 模組（跨domain + 設計系統）
- **v1.0引擎層**：Python引擎支援Skills執行（完全保留）
- **資料層**：Universal Elements Library（1246+元素）+ 設計變數庫

## 🎨 使用示例

### 示例1：人像攝影 - Portrait模式（intelligent-prompt-generator skill）

**使用者請求**：
```
生成電影級的亞洲女性，張藝謀電影風格
```

**Skill自動處理**：
- 識別：人像攝影領域，Portrait模式
- 呼叫：intelligent-prompt-generator skill
- 生成：電影級人像提示詞，包含戲劇性光影

**輸出提示詞**：
```
Cinematic portrait of young East Asian woman, dramatic lighting with rim light
and chiaroscuro effect, Zhang Yimou's signature color palette with rich reds
and golds, 85mm lens, shallow depth of field, film grain texture...
```

### 示例2：跨Domain複雜場景 - Cross-Domain模式 🆕

**使用者請求**：
```
生成龍珠悟空打出龜派氣功的提示詞
```

**Skill自動處理**：
- 識別：跨domain場景（人物+動作+特效）
- 自動組合4個domains: portrait + video + art + common
- 生成：包含人物、動作姿勢、能量特效的完整提示詞

**輸出提示詞**：
```
Son Goku from Dragon Ball, spiky black hair, orange gi martial arts uniform,
Kamehameha pose with hands at waist forming glowing blue energy sphere,
dynamic action shot, energy beam effects, blue energy glow, cinematic lighting...
```

### 示例3：設計海報 - Design模式 🆕

**使用者請求**：
```
生成溫馨可愛風格的兒童教育海報
```

**Skill自動處理**：
- 識別：設計海報，需要專業配色系統
- 呼叫：Design模式（SQLite + YAML融合）
- 生成：完整設計規範（配色+邊框+裝飾+技術引數）

**輸出**：
```
Color scheme: 天空藍色系, primary color 淡紫藍 (#C7CEEA),
Decorative elements: elements, soft natural window light,
Border style: box_shadow, round corners 20px...
```

### 示例4：平面設計（design-master skill）

**使用者請求**：
```
生成Apple風格PPT模板
```

**Skill自動處理**：
- 識別：平面設計領域
- 呼叫：design-master skill
- 查詢：Apple淡藍商務PPT模板（12個元素完整系統）

**輸出**：完整模板系統，包括背景、佈局、配色、字型、視覺效果

### 示例5：藝術繪畫（art-master skill）

**使用者請求**：
```
生成中國水墨畫山水
```

**Skill自動處理**：
- 識別：藝術繪畫領域（無人物）
- 呼叫：art-master skill
- 生成：包含筆觸、留白、潑墨等技法的提示詞

### 示例6：產品攝影（product-master skill）

**使用者請求**：
```
生成奢華手錶產品攝影
```

**Skill自動處理**：
- 識別：產品攝影領域
- 呼叫：product-master skill
- 生成：商業級產品攝影提示詞

## 🛠️ 核心功能

### 1. 元素庫系統
- **1140+個可複用元素**
- 7大領域分類
- 複用性評分（1-10）
- SQLite資料庫儲存

### 2. 模板系統
- 完整設計系統儲存
- 包含設計理念、使用指南
- 元素結構化組織
- 支援PPT、UI、品牌VI等

### 3. 智慧生成
- 框架驅動（`prompt_framework.yaml`）
- 語義匹配和推理
- 一致性檢查
- 自動衝突解決

### 4. 學習系統
- 從新提示詞中提取元素
- 自動領域分類
- 複用性評分
- 持續積累知識

## 📊 資料庫統計

### v2.0 (當前版本)
- **總元素數**: 1246+
- **Portrait領域**: 502個（人像專用）
- **Design領域**: 155個（平面設計，含5個完整模板）
- **Product領域**: 77個（產品攝影）
- **Art領域**: 51個（藝術風格）
- **Video領域**: 49個（影片生成）
- **Common領域**: 205個（通用技術）
- **跨domain可用**: 995個（組合使用）
- **設計變數**: 37種配色 + 邊框 + 裝飾（20萬+組合）
- **完整模板**: 5個（Apple、Material Design、Fluent Design等）

### 效能提升（v1.0 → v2.0）
- 資料庫利用率：40.3% → 79.9% ⬆️ **+98.2%**
- 生成模式：1種 → 3種 ⬆️ **+200%**
- 可用組合：固定 → 20萬+ ⬆️ **100倍+**

## 🔧 配置

### prompt_framework.yaml

定義人像提示詞的完整框架：
- 7大類：subject, facial, styling, expression, lighting, scene, technical
- 欄位到資料庫的對映
- 依賴規則（如era=ancient → makeup=traditional）
- 驗證規則

## 📝 開發指南

### 新增新元素

```python
from element_db import ElementDatabase

db = ElementDatabase()
db.add_element({
    'element_id': 'portrait_expressions_010',
    'domain_id': 'portrait',
    'category_id': 'expressions',
    'name': 'serene_smile',
    'chinese_name': '寧靜微笑',
    'ai_prompt_template': 'serene gentle smile...',
    'keywords': '["serene", "gentle", "peaceful"]',
    'reusability_score': 8.5
})
```

### 建立新模板

```python
template = {
    'template_id': 'template_xxx',
    'name': 'Template Name',
    'chinese_name': '模板中文名',
    'category': 'ppt_design',
    'element_ids': ['elem1', 'elem2', ...],
    'element_structure': {
        'backgrounds': ['elem1'],
        'layouts': ['elem2']
    },
    'design_philosophy': '設計理念...',
    'usage_scenarios': '使用場景...'
}
```

## 🤝 貢獻

歡迎提交Issue和Pull Request！

## 📄 License

MIT License

## 📚 相關文件

- **[README_v2.0.md](README_v2.0.md)** - v2.0快速開始指南
- **[UPGRADE_GUIDE_v2.0.md](UPGRADE_GUIDE_v2.0.md)** - 詳細升級指南和功能說明
- **[prompt_framework.yaml](prompt_framework.yaml)** - 人像框架配置檔案

## 🙏 致謝

- 基於Claude Code Skills系統
- Universal Elements Library架構
- 框架驅動生成理念
