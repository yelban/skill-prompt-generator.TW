#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xray Helper - 簡單的資料讀取和儲存工具
僅負責檔案IO，不做任何分析決策
"""

import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime


def load_prompts(pattern: str = "*_extracted.json",
                 base_dir: str = "extracted_results") -> List[Dict]:
    """
    讀取已分析的提示詞JSON檔案

    Args:
        pattern: 檔名模式（如：moss_terrarium*）
        base_dir: JSON檔案所在目錄

    Returns:
        List of prompt data
    """
    base_path = Path(base_dir)
    prompts = []

    if not base_path.exists():
        print(f"❌ 目錄不存在: {base_path}")
        return []

    for json_file in base_path.glob(pattern):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # 處理單個提示詞或提示詞陣列
                if isinstance(data, list):
                    prompts.extend(data)
                else:
                    prompts.append(data)

                print(f"✅ 已載入: {json_file.name}")
        except Exception as e:
            print(f"❌ 載入失敗 {json_file.name}: {e}")

    print(f"\n📊 總計載入: {len(prompts)} 個提示詞")
    return prompts


def save_knowledge_card(dimension: str,
                       content: str,
                       metadata: Dict = None,
                       output_dir: str = "knowledge_base") -> str:
    """
    儲存知識卡片到Markdown檔案

    Args:
        dimension: 維度名稱（color/layout/symbols等）
        content: Markdown內容
        metadata: 可選的元資料
        output_dir: 輸出目錄

    Returns:
        儲存的檔案路徑
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # 生成檔名
    filename = f"how_to_control_{dimension}.md"
    filepath = output_path / filename

    # 儲存檔案
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"💾 已儲存: {filepath}")

    # 如果有元資料，也儲存JSON版本
    if metadata:
        json_filename = f"how_to_control_{dimension}.json"
        json_filepath = output_path / json_filename

        output_data = {
            'dimension': dimension,
            'creation_time': datetime.now().isoformat(),
            'metadata': metadata,
            'markdown_content': content
        }

        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"💾 已儲存元資料: {json_filepath}")

    return str(filepath)


def list_available_prompts(base_dir: str = "extracted_results") -> List[str]:
    """
    列出所有可用的提示詞檔案

    Args:
        base_dir: JSON檔案所在目錄

    Returns:
        檔名列表
    """
    base_path = Path(base_dir)

    if not base_path.exists():
        print(f"❌ 目錄不存在: {base_path}")
        return []

    files = sorted([f.name for f in base_path.glob("*_extracted.json")])

    print(f"\n📁 可用的提示詞檔案 ({len(files)}個):")
    for f in files:
        print(f"  - {f}")

    return files


if __name__ == '__main__':
    """測試函式"""
    print("=" * 60)
    print("  🔬 Xray Helper - 工具測試")
    print("=" * 60)

    # 測試：列出可用檔案
    list_available_prompts()

    # 測試：載入提示詞
    print("\n" + "=" * 60)
    prompts = load_prompts()

    if prompts:
        print(f"\n📋 第一個提示詞示例:")
        print(f"  ID: {prompts[0].get('prompt_id', 'unknown')}")
        print(f"  主題: {prompts[0].get('theme', 'unknown')}")

    # 測試：儲存知識卡片
    print("\n" + "=" * 60)
    test_content = """# 測試知識卡片

這是一個測試。
"""

    save_knowledge_card(
        dimension="test",
        content=test_content,
        metadata={'test': True, 'samples': 2}
    )

    print("\n" + "=" * 60)
    print("✅ 測試完成！")
