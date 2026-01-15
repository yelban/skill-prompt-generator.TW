#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設計變數橋接器 - 連線SQLite元素和YAML設計變數
智慧融合兩者生成完整的設計提示詞
"""

import sys
import os
from typing import Dict, List, Optional

# 新增上級目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.cross_domain_query import CrossDomainQueryEngine
from core.yaml_sampler import YAMLVariableSampler


class DesignVariableBridge:
    """連線 SQLite元素 和 YAML設計變數的橋接器"""

    def __init__(self, db_path: str = "extracted_results/elements.db",
                 yaml_dir: str = "variables"):
        """
        初始化設計變數橋接器

        Args:
            db_path: SQLite資料庫路徑
            yaml_dir: YAML變數檔案目錄
        """
        self.sqlite_engine = CrossDomainQueryEngine(db_path)
        self.yaml_sampler = YAMLVariableSampler(yaml_dir)

    def generate_design_prompt(self, intent: Dict) -> Dict:
        """
        生成完整設計提示詞（SQLite + YAML）

        Args:
            intent: 使用者意圖字典

        Returns:
            包含完整提示詞和元資料的字典
            {
                'prompt': '完整提示詞',
                'sqlite_elements': {...},
                'yaml_variables': {...},
                'metadata': {...}
            }
        """
        # 1. 從SQLite獲取基礎元素（人物、場景、光影）
        sqlite_elements = self.sqlite_engine.query_by_intent(intent)
        print(f"📊 SQLite元素: {sum(len(elems) for elems in sqlite_elements.values())} 個")

        # 2. 從YAML獲取設計變數（配色、邊框、裝飾）
        design_style = intent.get('design_style', '溫馨可愛')
        yaml_variables = self.yaml_sampler.sample_variables(style=design_style)
        print(f"🎨 YAML變數: 風格={design_style}")

        # 3. 融合兩者
        merged = self.merge_elements_and_variables(
            sqlite_elements,
            yaml_variables,
            intent
        )

        # 4. 應用設計邏輯（可選）
        # design_logic = self.load_design_logic(design_style)

        # 5. 生成最終提示詞
        prompt = self.build_final_prompt(merged)

        return {
            'prompt': prompt,
            'sqlite_elements': sqlite_elements,
            'yaml_variables': yaml_variables,
            'metadata': {
                'design_style': design_style,
                'element_count': sum(len(elems) for elems in sqlite_elements.values()),
                'domains_used': list(sqlite_elements.keys())
            }
        }

    def merge_elements_and_variables(self, sqlite_elements: Dict[str, List[Dict]],
                                    yaml_variables: Dict,
                                    intent: Dict) -> Dict:
        """
        智慧融合SQLite元素和YAML變數

        Args:
            sqlite_elements: SQLite查詢的元素（按domain分組）
            yaml_variables: YAML取樣的變數
            intent: 使用者意圖

        Returns:
            融合後的結構化資料
        """
        merged = {
            'content': [],       # SQLite元素（主體內容）
            'design': [],        # YAML變數（設計規範）
            'technical': []      # 技術引數
        }

        # 處理SQLite元素
        for domain, elements in sqlite_elements.items():
            for elem in elements:
                category = elem.get('category', '')

                # 分類元素
                if domain in ['portrait', 'video', 'art']:
                    # 主體內容
                    merged['content'].append({
                        'domain': domain,
                        'category': category,
                        'template': elem.get('template', ''),
                        'chinese_name': elem.get('chinese_name', '')
                    })
                elif domain == 'common':
                    # 技術引數（光影、攝影技術）
                    if 'lighting' in category or 'photography' in category:
                        merged['technical'].append({
                            'domain': domain,
                            'category': category,
                            'template': elem.get('template', ''),
                            'chinese_name': elem.get('chinese_name', '')
                        })

        # 處理YAML變數（設計規範）
        if 'colors' in yaml_variables:
            colors_data = yaml_variables['colors']
            scheme_name = colors_data.get('scheme_name', '')
            variant = colors_data.get('selected_variant')
            if variant:
                merged['design'].append({
                    'type': 'color',
                    'description': f"Color scheme: {scheme_name}, primary color {variant['name']} ({variant['hex']})"
                })

        if 'borders' in yaml_variables:
            borders_data = yaml_variables['borders']
            border_name = borders_data.get('border_name', '')
            border_config = borders_data.get('border_config', {})
            radius = border_config.get('radius', '')
            if radius:
                merged['design'].append({
                    'type': 'border',
                    'description': f"Border style: {border_name}, border-radius: {radius}"
                })

        if 'decorations' in yaml_variables:
            deco_data = yaml_variables['decorations']
            deco_name = deco_data.get('decoration_name', '')
            merged['design'].append({
                'type': 'decoration',
                'description': f"Decorative elements: {deco_name}"
            })

        return merged

    def build_final_prompt(self, merged: Dict) -> str:
        """
        構建最終提示詞

        Args:
            merged: 融合後的結構化資料

        Returns:
            完整提示詞字串
        """
        parts = []

        # 1. 主體內容（SQLite元素）
        for item in merged['content']:
            template = item['template']
            if template:
                parts.append(template)

        # 2. 設計規範（YAML變數）
        for item in merged['design']:
            description = item['description']
            if description:
                parts.append(description)

        # 3. 技術引數（光影、攝影）
        for item in merged['technical']:
            template = item['template']
            if template:
                parts.append(template)

        return ', '.join(parts)

    def load_design_logic(self, design_style: str) -> Optional[Dict]:
        """
        載入設計邏輯（可選）

        Args:
            design_style: 設計風格名稱

        Returns:
            設計邏輯配置字典
        """
        # 從design-logic目錄載入對應風格的規則
        # 這部分可以後續擴充套件
        return None

    def close(self):
        """關閉資源"""
        self.sqlite_engine.close()


def test_design_bridge():
    """測試設計變數橋接器"""
    print("=" * 80)
    print("測試設計變數橋接器")
    print("=" * 80)

    bridge = DesignVariableBridge()

    # 測試案例：溫馨可愛的兒童教育海報
    print("\n【測試案例】溫馨可愛的兒童教育海報\n")

    intent = {
        'raw_input': '溫馨可愛風格的兒童教育海報',
        'design_style': '溫馨可愛',
        'subject': {
            'age_range': 'child',
            'gender': 'female'
        },
        'atmosphere': {
            'theme': 'educational',
            'mood': 'warm'
        },
        'lighting': 'soft'
    }

    # 生成設計提示詞
    result = bridge.generate_design_prompt(intent)

    # 顯示結果
    print("\n📋 生成結果：")
    print(f"\n風格: {result['metadata']['design_style']}")
    print(f"元素數: {result['metadata']['element_count']}")
    print(f"使用domain: {', '.join(result['metadata']['domains_used'])}")

    print(f"\n✨ 完整提示詞：")
    print("─" * 80)
    print(result['prompt'])
    print("─" * 80)

    # 顯示YAML變數
    if result['yaml_variables']:
        print(f"\n🎨 設計變數：")
        for var_type, var_data in result['yaml_variables'].items():
            if var_type == 'colors':
                print(f"  配色: {var_data.get('scheme_name')}")
            elif var_type == 'borders':
                print(f"  邊框: {var_data.get('border_name')}")
            elif var_type == 'decorations':
                print(f"  裝飾: {var_data.get('decoration_name')}")

    bridge.close()
    print("\n✅ 測試完成")


if __name__ == '__main__':
    test_design_bridge()
