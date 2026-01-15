# Prompt Extractor - AI繪畫提示詞模組化提取工具

## 快速開始

### 1. 啟用Skill

在Claude Code中呼叫：
```
/skill prompt-extractor
```

或者直接說：
```
使用 prompt-extractor 分析我的提示詞
```

### 2. 輸入方式（二選一）

**方式A：檔案路徑**（適合大批次）

支援三種格式：

**TXT格式** (每行一個提示詞)
```
a portrait of a woman, cinematic lighting, 85mm lens, ultra detailed
cyberpunk city at night, neon lights, rain, photorealistic
```

**CSV格式**
```csv
id,prompt,score
1,"a portrait of a woman, cinematic lighting",8.5
2,"cyberpunk city at night, neon lights",9.2
```

**JSON格式**
```json
[
  {"prompt": "a portrait of a woman, cinematic lighting, 85mm lens"},
  {"prompt": "cyberpunk city at night, neon lights, rain"}
]
```

**方式B：直接貼上**（適合快速分析，推薦！✨）

```
我：幫我分析這些提示詞：

a portrait of a woman, cinematic lighting, 85mm lens, ultra detailed
cyberpunk city at night, neon lights, rain, photorealistic
beautiful landscape, golden hour, dramatic clouds, HDR
```

**無需建立檔案，直接貼上即可！**

詳見：[貼上模式完整指南](PASTE_MODE_GUIDE.md)

### 3. 自動處理

Skill會自動：
1. 識別檔案格式
2. 清洗和去重
3. 聚類分析（如果>100條）
4. 逐條提取模組
5. 生成模組庫和分析報告

## 輸出檔案說明

### extracted_modules.json
完整的提取結果，每條提示詞對應一個JSON物件：

```json
{
  "original_prompt": "a portrait of a young woman, cinematic lighting, 85mm lens f/1.4, ultra detailed, photorealistic",
  "theme": "人像攝影",
  "modules": {
    "subject_variables": {
      "main": "young woman",
      "modifiers": ["portrait"],
      "is_replaceable": true
    },
    "visual_style": {
      "art_style": "photorealistic",
      "reference_artists": [],
      "color_palette": "natural tones"
    },
    "technical_parameters": {
      "camera": "85mm lens f/1.4",
      "lighting": "cinematic lighting",
      "render_engine": null,
      "resolution": "ultra detailed"
    },
    "detail_enhancers": ["ultra detailed", "photorealistic"],
    "mood_atmosphere": "professional, elegant",
    "constraints": {
      "negative_prompt": "",
      "exclusions": []
    }
  },
  "quality_score": {
    "clarity": 9,
    "detail_richness": 8,
    "reusability": 9,
    "comments": "結構清晰，技術引數具體，高度可複用"
  },
  "extracted_patterns": {
    "structure_type": "分層描述：主體 + 技術 + 質量",
    "advantages": ["引數明確", "易於替換主體", "專業攝影標準"],
    "reusable_templates": "{主體}, {光線}, {鏡頭引數}, {質量增強}"
  }
}
```

### module_library.json
去重後的通用模組庫：

```json
{
  "visual_styles": {
    "art_styles": ["photorealistic", "cinematic", "cyberpunk", "anime", "oil painting"],
    "frequency": {"photorealistic": 45, "cinematic": 38}
  },
  "technical_params": {
    "camera_angles": ["85mm lens", "wide angle", "macro", "aerial view"],
    "lighting": ["cinematic lighting", "soft light", "backlight", "golden hour"],
    "render_engines": ["Unreal Engine", "Octane Render", "V-Ray"]
  },
  "detail_enhancers": [
    "ultra detailed", "8k", "hyperrealistic", "intricate details",
    "sharp focus", "professional photography"
  ],
  "templates": [
    {
      "name": "人像攝影模板",
      "structure": "{主體}, {光線}, {鏡頭}, {質量增強}",
      "example": "a portrait of {subject}, cinematic lighting, 85mm lens, ultra detailed",
      "usage_count": 23,
      "avg_quality_score": 8.7
    },
    {
      "name": "場景構圖模板",
      "structure": "{場景}, {氛圍}, {視角}, {風格}, {質量}",
      "example": "{location} at {time}, {mood}, {camera_angle}, {art_style}, {detail_enhancers}",
      "usage_count": 18,
      "avg_quality_score": 8.2
    }
  ],
  "high_value_modules": [
    {
      "module": "cinematic lighting, 85mm lens f/1.4",
      "reusability_score": 9.5,
      "category": "technical_parameters",
      "usage_scenarios": ["人像", "產品", "靜物"]
    }
  ]
}
```

### analysis_report.md
可讀的分析報告：

```markdown
# 提示詞分析報告

## 資料概覽
- 總數：500條
- 清洗後：487條
- 去重：13條
- 主題分佈：
  - 人像攝影：145條 (29.8%)
  - 風景場景：132條 (27.1%)
  - 概念藝術：98條 (20.1%)
  - 其他：112條 (23.0%)

## 高頻模組

### 視覺風格 Top 5
1. photorealistic (92次)
2. cinematic (76次)
3. cyberpunk (54次)
4. anime style (43次)
5. oil painting (38次)

### 技術引數 Top 5
1. cinematic lighting (88次)
2. 85mm lens (67次)
3. ultra detailed (156次)
4. 8k (89次)
5. Unreal Engine (45次)

## 推薦組合

### 組合1：專業人像
**模板：** {人物}, cinematic lighting, 85mm lens f/1.4, ultra detailed, photorealistic
**優勢：** 技術引數明確，成片率高
**適用場景：** 人像、半身像、特寫

### 組合2：賽博朋克城市
**模板：** cyberpunk {場景}, neon lights, rain, night, cinematic, 8k
**優勢：** 氛圍強烈，視覺衝擊力強
**適用場景：** 科幻、城市、未來主義

## 改進建議

1. **增加負面提示**：只有23%的提示詞包含負面提示，建議補充
2. **細化技術引數**：67%的提示缺乏具體鏡頭引數
3. **明確藝術風格**：建議每個提示都指定清晰的風格標籤
```

## 使用場景示例

### 場景1：新手學習優秀提示詞結構

```
使用者：我有一個收藏的500條AI繪畫提示詞，想學習它們的結構
操作：使用 prompt-extractor 分析 favorites.txt
輸出：
  - 發現85%使用"主體+技術+質量"結構
  - 提取10個高複用模板
  - 生成學習手冊
```

### 場景2：構建自己的模組庫

```
使用者：我想從1萬條提示詞中提煉出我的專屬模組庫
操作：分批處理，每次2000條
輸出：
  - 去重後的5000+獨特模組
  - 按主題分類的模板庫
  - 可直接複用的JSON檔案
```

### 場景3：提升提示詞質量

```
使用者：我的提示詞效果不好，想找到高質量模式
操作：上傳失敗案例和成功案例兩個檔案對比
輸出：
  - 識別成功案例的共同模式
  - 指出失敗案例的缺陷（如缺乏技術引數）
  - 提供改進建議
```

## 高階功能

### 1. 增量更新模組庫

```python
# 合併新提示詞到現有庫
python preprocessor.py new_prompts.txt updated_library.json
```

### 2. 主題過濾

在skill中指定：
```
只提取"人像攝影"主題的模組
```

### 3. 自定義評分標準

修改 skill.md 中的評分權重：
```json
"quality_score": {
  "clarity": {"weight": 0.3, "score": 8},
  "detail_richness": {"weight": 0.3, "score": 9},
  "reusability": {"weight": 0.4, "score": 7}
}
```

## 最佳實踐

### 資料準備
1. 先清理明顯無效的提示（如亂碼、測試文字）
2. 如果有評分，保留高分提示優先處理
3. 按主題分檔案更易管理

### 批次處理策略
- **<100條**：一次性處理，精細提取
- **100-500條**：推薦規模，單次skill呼叫
- **>500條**：分批處理，每批300-500條

### 質量保障
1. 首次處理前，手動標註20-50條作為基準
2. 對比AI提取結果，調整meta-prompt
3. 迭代3-5次達到滿意精度

## 故障排除

### 問題1：檔案格式識別失敗
**原因**：編碼問題或格式不標準
**解決**：
```bash
# 轉換編碼為UTF-8
iconv -f GBK -t UTF-8 input.txt > output.txt
```

### 問題2：提取質量差
**原因**：提示詞本身質量低或結構混亂
**解決**：
- 先聚類，只處理主題清晰的簇
- 提高 min_length 閾值過濾短提示
- 人工review前100條，調整提取規則

### 問題3：處理速度慢
**原因**：單次處理量過大
**解決**：
- 減少批次大小（推薦50-100條/批）
- 先聚類後並行處理各簇
- 使用預處理指令碼先過濾

## 技術支援

如需幫助，在Claude Code中問：
```
prompt-extractor 如何處理CSV中的多列資料？
prompt-extractor 如何自定義模組分類？
```

## 更新日誌

**v1.0** (當前版本)
- 支援 txt/csv/json 三種格式
- 自動聚類和主題識別
- 模組化提取和質量評分
- 生成可複用模板庫

**路線圖**
- [ ] 支援多語言提示詞（中文、日文）
- [ ] 視覺化分析dashboard
- [ ] 與Midjourney/SD引數庫對接
- [ ] 線上模組搜尋引擎
