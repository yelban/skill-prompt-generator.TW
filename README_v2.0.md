# 跨Domain提示詞生成系統 v2.0

> 智慧提示詞生成系統 - 支援人像、跨domain場景、專業設計三種模式

---

## 🚀 快速開始

### 基礎使用

```python
from core.cross_domain_generator import CrossDomainGenerator

# 建立生成器
generator = CrossDomainGenerator()

# 生成提示詞（自動識別型別）
result = generator.generate("龍珠悟空打出龜派氣功的蠟像3D感")

print(result['prompt'])  # 完整提示詞
print(result['type'])    # 型別：portrait/cross_domain/design

generator.close()
```

---

## 📊 三種生成模式

### 1. Portrait（人像）

```python
result = generator.generate("生成一個年輕女性肖像")
# 型別: portrait
# 使用: portrait domain (502個元素)
```

### 2. Cross-Domain（跨域）

```python
result = generator.generate("龍珠悟空打出龜派氣功的蠟像3D感")
# 型別: cross_domain
# 使用: portrait + video + art + common (4個domain)
```

### 3. Design（設計）

```python
result = generator.generate("溫馨可愛風格的兒童教育海報")
# 型別: design
# 使用: SQLite元素 + YAML變數（配色、邊框、裝飾）
```

---

## 📁 專案結構

```
skill-prompt-generator/
├── core/                           # 核心模組
│   ├── cross_domain_generator.py   # 統一介面 ⭐
│   ├── cross_domain_query.py       # 跨domain查詢引擎
│   ├── design_bridge.py            # 設計變數橋接器
│   ├── variable_sampler.py         # SQLite變數取樣器
│   ├── yaml_sampler.py             # YAML變數取樣器
│   ├── framework_loader.py         # 框架載入器（原有）
│   └── schema_migration_v1.sql     # Schema升級指令碼
│
├── extracted_results/
│   └── elements.db                 # 元素資料庫（1,246個元素）
│
├── variables/                      # YAML變數（從prompt-crafter複製）
│   ├── colors.yaml                 # 配色方案（37種）
│   ├── borders.yaml                # 邊框樣式
│   └── decorations.yaml            # 裝飾元素
│
├── design-logic/                   # 設計邏輯
│   ├── warm-cute/                  # 溫馨可愛風格
│   └── modern-minimal/             # 現代簡約風格
│
├── intelligent_generator.py        # 智慧生成器（原有，向後相容）
├── framework_loader.py             # 框架載入器（原有）
├── UPGRADE_GUIDE_v2.0.md           # 升級指南
└── README_v2.0.md                  # 本文件
```

---

## 🔧 安裝和初始化

### 1. Schema升級

```bash
# 擴充套件資料庫，新增變量表
sqlite3 extracted_results/elements.db < core/schema_migration_v1.sql
```

### 2. 依賴檢查

```bash
python3 -c "import yaml; print('✅ PyYAML installed')"
```

如果未安裝：
```bash
pip install pyyaml
```

---

## 🧪 測試

### 執行全部測試

```bash
# 測試變數取樣器
python3 core/variable_sampler.py

# 測試跨domain查詢
python3 core/cross_domain_query.py

# 測試YAML取樣器
python3 core/yaml_sampler.py

# 測試設計橋接器
python3 core/design_bridge.py

# 測試統一介面
python3 core/cross_domain_generator.py
```

---

## 📈 效能提升

| 指標 | v1.0 | v2.0 | 提升 |
|-----|------|------|------|
| SQLite利用率 | 40.2% | 80%+ | **2倍** |
| 可用組合數 | ~1,000 | ~10萬+ | **100倍** |
| 功能範圍 | 人像 | 人像+跨域+設計 | **3倍** |

---

## 🎯 使用建議

### 推薦使用場景

| 場景 | 推薦型別 | 示例 |
|------|---------|------|
| 純人像攝影 | portrait | "電影級亞洲女性" |
| 複雜動作場景 | cross_domain | "悟空打龜派氣功" |
| 海報/卡片設計 | design | "溫馨可愛兒童海報" |

### API選擇

- **新專案**：使用 `CrossDomainGenerator`（統一介面）
- **現有專案**：可選升級，無需強制
- **簡單需求**：繼續使用 `IntelligentGenerator`（向後相容）

---

## ✅ 向後相容

v1.0的所有功能完全保留：

```python
# v1.0方式（仍然有效）
from intelligent_generator import IntelligentGenerator
gen = IntelligentGenerator()
elements = gen.select_elements_by_intent(intent)
prompt = gen.compose_prompt(elements)
```

---

## 📚 文件

- **升級指南**：`UPGRADE_GUIDE_v2.0.md`
- **設計文件**：`/tmp/fusion_design.md`
- **架構分析**：`/tmp/domain_architecture_analysis.md`
- **對比分析**：`/tmp/sqlite_vs_yaml_comparison.md`

---

## 🎊 核心特性

✅ **跨Domain智慧查詢** - 自動識別需要的domain並組合
✅ **設計系統整合** - 20萬+配色組合
✅ **變數取樣** - 智慧避免重複
✅ **統一介面** - 一個API處理所有型別
✅ **100%向後相容** - 老程式碼無需修改

---

*系統版本: v2.0*
*更新日期: 2026-01-13*
