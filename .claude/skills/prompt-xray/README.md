# Prompt Xray - 提示詞X光透視系統

**狀態**: 🚧 開發中
**版本**: 1.0
**靈感**: BerryXia Multi-Agent Architecture

## 快速開始

```bash
# 從專案根目錄執行
python -m claude.skills.prompt_xray.xray_controller
```

## 目錄結構

```
prompt-xray/
├── skill.md          # Skill說明文件
├── xray_controller.py  # 主控制器
├── agents/            # 8個分析Agent
│   ├── color_analyzer.py
│   ├── layout_architect.py
│   └── ...
└── utils/             # 工具函式
```

## 已實現功能

- [x] COLOR_ANALYZER - 配色知識提取
- [x] LAYOUT_ARCHITECT - 佈局知識提取
- [ ] SYMBOL_EXTRACTOR - 符號新增方法
- [ ] TYPOGRAPHY_ANALYST - 排版知識
- [ ] MATERIAL_ENGINEER - 材質知識
- [ ] LIGHT_PHYSICIST - 光影知識
- [ ] KNOWLEDGE_SYNTHESIZER - 知識聚合
