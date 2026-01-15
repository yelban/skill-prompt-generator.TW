#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨Domain查詢引擎 - 智慧查詢多個domain並組合元素
核心功能：根據使用者意圖自動識別需要的domains，智慧查詢和組合
"""

import sqlite3
import json
import sys
import os
from typing import Dict, List, Optional, Set, Any

# 新增上級目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.variable_sampler import SQLiteVariableSampler
from intelligent_generator import IntelligentGenerator


class CrossDomainQueryEngine:
    """跨Domain智慧查詢引擎"""

    def __init__(self, db_path: str = "extracted_results/elements.db"):
        """
        初始化跨domain查詢引擎

        Args:
            db_path: 資料庫路徑
        """
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.sampler = SQLiteVariableSampler(db_path)
        self.generator = IntelligentGenerator(db_path)

    def query_by_intent(self, intent: Dict) -> Dict[str, List[Dict]]:
        """
        根據使用者意圖跨domain查詢元素

        Args:
            intent: 使用者意圖字典

        Returns:
            按domain分組的元素字典
            {
                'portrait': [element1, element2, ...],
                'video': [element3, ...],
                'art': [element4, ...],
                'common': [element5, ...]
            }
        """
        # 1. 分析需要哪些domains
        required_domains = self.analyze_required_domains(intent)
        print(f"📊 分析結果：需要 {len(required_domains)} 個domain: {', '.join(required_domains)}")

        # 2. 構建跨domain SQL查詢計劃
        query_plan = self.build_query_plan(intent, required_domains)

        # 3. 執行查詢，從多個domains獲取元素
        elements = {}
        for domain, categories in query_plan.items():
            print(f"  🔍 查詢 {domain} domain: {', '.join(categories)}")
            elements[domain] = self.query_domain(domain, categories, intent)

        # 4. 應用變數取樣（如果元素有變數）
        sampled_elements = {}
        for domain, domain_elements in elements.items():
            sampled_elements[domain] = []
            for elem in domain_elements:
                # 檢查是否有變數
                try:
                    result = self.sampler.sample_element_with_variables(
                        elem['element_id'],
                        style_context=intent.get('visual_style')
                    )
                    # 如果有變數，使用取樣後的結果
                    if result['variables']:
                        elem_copy = elem.copy()
                        elem_copy['template'] = result['result']
                        elem_copy['sampled_variables'] = result['variables']
                        sampled_elements[domain].append(elem_copy)
                    else:
                        sampled_elements[domain].append(elem)
                except:
                    # 沒有變數或採樣失敗，使用原始元素
                    sampled_elements[domain].append(elem)

        return sampled_elements

    def analyze_required_domains(self, intent: Dict) -> List[str]:
        """
        分析意圖需要哪些domains

        Args:
            intent: 使用者意圖字典

        Returns:
            需要的domain列表
        """
        domains = set()

        # 有人物 → portrait
        if 'subject' in intent:
            domains.add('portrait')

        # 有動作/能量/運動 → video
        video_keywords = ['action', 'pose', 'energy', 'movement', 'motion', 'dynamic']
        if any(k in intent for k in video_keywords):
            domains.add('video')

        # 檢查特殊動作關鍵詞
        raw_input = intent.get('raw_input', '').lower()
        if any(kw in raw_input for kw in ['kamehameha', '龜派氣功', '能量', 'energy', '氣息']):
            domains.add('video')

        # 有藝術風格 → art
        if 'art_style' in intent or 'visual_style' in intent:
            visual_style = intent.get('visual_style', {})
            if isinstance(visual_style, dict):
                art_style = visual_style.get('art_style', '')
            else:
                art_style = str(visual_style)

            # 特殊藝術風格需要art domain
            art_keywords = ['3d', 'wax', '蠟像', 'holographic', 'sculpture', 'rendering']
            if any(kw in art_style.lower() for kw in art_keywords):
                domains.add('art')

        # 有設計需求 → design
        design_keywords = ['layout', 'composition', 'typography', 'poster', 'card']
        if any(k in intent for k in design_keywords):
            domains.add('design')

        # 有產品 → product
        if 'product' in intent:
            domains.add('product')

        # 始終包含common（光影、技術引數）
        domains.add('common')

        return list(domains)

    def build_query_plan(self, intent: Dict, domains: List[str]) -> Dict[str, List[str]]:
        """
        構建查詢計劃

        Args:
            intent: 使用者意圖
            domains: 需要查詢的domain列表

        Returns:
            查詢計劃字典 {domain: [categories]}
        """
        query_plan = {}

        for domain in domains:
            if domain == 'portrait':
                query_plan['portrait'] = [
                    'gender', 'age_range', 'ethnicity',
                    'eye_types', 'face_shapes', 'skin_tones',
                    'makeup_styles', 'hair_styles', 'hair_colors',
                    'expressions', 'poses'
                ]

            elif domain == 'video':
                query_plan['video'] = [
                    'scene_types',      # 能量氣息、動態場景
                    'motion_effects',   # 動態效果
                    'camera_movements'  # 鏡頭運動
                ]

            elif domain == 'art':
                query_plan['art'] = [
                    'art_styles',        # 3D渲染、蠟像質感
                    'special_effects'    # 全息、粒子效果
                ]

            elif domain == 'design':
                query_plan['design'] = [
                    'layout_types',
                    'visual_styles',
                    'composition_techniques'
                ]

            elif domain == 'product':
                query_plan['product'] = [
                    'photography_styles',
                    'lighting_setups'
                ]

            elif domain == 'common':
                query_plan['common'] = [
                    'lighting_techniques',
                    'photography_techniques',
                    'poses',
                    'technical_quality'
                ]

        return query_plan

    def query_domain(self, domain: str, categories: List[str], intent: Dict) -> List[Dict]:
        """
        查詢單個domain的元素

        Args:
            domain: domain ID
            categories: 要查詢的category列表
            intent: 使用者意圖（用於關鍵詞提取）

        Returns:
            元素列表
        """
        elements = []

        for category in categories:
            # 從intent提取該category的關鍵詞
            keywords = self.extract_keywords_from_intent(intent, category)

            # 獲取候選元素
            candidates = self.get_all_elements_by_category(domain, category)

            if not candidates:
                continue

            # 使用ElementSelector選擇最佳元素
            from framework_loader import ElementSelector

            best_elem, score = ElementSelector.select_best_element(
                candidates=candidates,
                user_keywords=keywords,
                user_intent=intent,
                field_name=f"{domain}.{category}",
                debug=False
            )

            if best_elem and score > 20:  # 分數閾值
                elements.append(best_elem)

        return elements

    def extract_keywords_from_intent(self, intent: Dict, category: str) -> List[str]:
        """
        從intent中提取特定category的關鍵詞

        Args:
            intent: 使用者意圖
            category: category ID

        Returns:
            關鍵詞列表
        """
        keywords = []
        raw_input = intent.get('raw_input', '')

        # 根據category提取不同的關鍵詞
        if category == 'scene_types':
            # 場景型別：能量、氣息、氛圍
            scene_keywords = ['energy', 'aura', 'atmosphere', 'power', '能量', '氣息', '氛圍']
            keywords.extend([kw for kw in scene_keywords if kw in raw_input.lower()])

        elif category == 'motion_effects':
            # 動態效果：動作、運動
            motion_keywords = ['motion', 'movement', 'action', 'dynamic', '動作', '運動', '動態']
            keywords.extend([kw for kw in motion_keywords if kw in raw_input.lower()])

        elif category == 'art_styles':
            # 藝術風格
            visual_style = intent.get('visual_style', {})
            if isinstance(visual_style, dict):
                art_style = visual_style.get('art_style', '')
                if art_style:
                    keywords.append(art_style)
            # 從raw_input提取
            art_keywords = ['3d', 'wax', '蠟像', 'holographic', 'realistic', 'rendering']
            keywords.extend([kw for kw in art_keywords if kw in raw_input.lower()])

        elif category == 'special_effects':
            # 特效
            effect_keywords = ['glow', 'particle', 'holographic', 'energy', '發光', '粒子', '全息']
            keywords.extend([kw for kw in effect_keywords if kw in raw_input.lower()])

        elif category == 'lighting_techniques':
            # 光影技術
            lighting = intent.get('lighting', 'natural')
            if lighting:
                keywords.append(lighting)

        # 如果沒有關鍵詞，使用空列表（會選擇評分最高的）
        return keywords if keywords else []

    def get_all_elements_by_category(self, domain: str, category: str) -> List[Dict]:
        """
        從資料庫獲取該category的所有元素

        Args:
            domain: domain ID
            category: category ID

        Returns:
            元素列表
        """
        return self.generator.get_all_elements_by_category(domain, category)

    def close(self):
        """關閉資料庫連線"""
        self.sampler.close()
        self.generator.close()
        self.db.close()


def test_cross_domain_query():
    """測試跨domain查詢"""
    print("=" * 80)
    print("測試跨Domain查詢引擎")
    print("=" * 80)

    engine = CrossDomainQueryEngine()

    # 測試案例：龍珠悟空打龜派氣功
    print("\n【測試案例】龍珠悟空打龜派氣功的蠟像3D感\n")

    intent = {
        'raw_input': '龍珠動漫的蠟像3D感悟空打出龜派氣功',
        'subject': {
            'gender': 'male',
            'ethnicity': 'East_Asian',
            'character': 'Son Goku'
        },
        'action': 'kamehameha',
        'energy': 'blue_energy_blast',
        'visual_style': {
            'art_style': 'wax_figure_3d'
        },
        'render': '3d_realistic'
    }

    # 執行跨domain查詢
    results = engine.query_by_intent(intent)

    # 顯示結果
    print("\n📋 查詢結果：")
    total_elements = 0
    for domain, elements in results.items():
        if elements:
            print(f"\n  【{domain} domain】({len(elements)}個元素)")
            for elem in elements[:3]:  # 只顯示前3個
                print(f"    - {elem['chinese_name']} ({elem['category']})")
            total_elements += len(elements)

    print(f"\n✅ 共獲取 {total_elements} 個元素，來自 {len(results)} 個domain")

    engine.close()


if __name__ == '__main__':
    test_cross_domain_query()
