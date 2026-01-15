#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨Domain生成器 - 統一的提示詞生成入口
自動識別需求型別，智慧路由到對應生成器
"""

import sys
import os
import re
from typing import Dict, List, Optional

# 新增上級目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.cross_domain_query import CrossDomainQueryEngine
from core.design_bridge import DesignVariableBridge
from intelligent_generator import IntelligentGenerator


class CrossDomainGenerator:
    """統一的跨Domain生成器"""

    def __init__(self, db_path: str = "extracted_results/elements.db",
                 yaml_dir: str = "variables"):
        """
        初始化跨domain生成器

        Args:
            db_path: SQLite資料庫路徑
            yaml_dir: YAML變數檔案目錄
        """
        self.query_engine = CrossDomainQueryEngine(db_path)
        self.design_bridge = DesignVariableBridge(db_path, yaml_dir)
        self.portrait_generator = IntelligentGenerator(db_path)

    def generate(self, user_input: str, generation_type: str = 'auto') -> Dict:
        """
        統一生成入口

        Args:
            user_input: 使用者輸入（自然語言）
            generation_type: 生成型別
                - 'portrait': 人像（僅SQLite portrait domain）
                - 'design': 設計（SQLite + YAML）
                - 'cross_domain': 跨domain（SQLite多domain）
                - 'auto': 自動識別

        Returns:
            生成結果字典
            {
                'prompt': '完整提示詞',
                'type': '生成型別',
                'metadata': {...}
            }
        """
        # 1. 解析使用者輸入為Intent
        intent = self.parse_user_input(user_input)

        # 2. 自動識別生成型別
        if generation_type == 'auto':
            generation_type = self.classify_generation_type(intent)

        print(f"📌 生成型別: {generation_type}")

        # 3. 路由到對應生成器
        if generation_type == 'portrait':
            # 純人像 → 只用portrait domain（向後相容）
            return self.generate_portrait(intent)

        elif generation_type == 'design':
            # 設計海報/卡片 → SQLite基礎 + YAML設計
            return self.generate_design(intent)

        elif generation_type == 'cross_domain':
            # 複雜場景 → SQLite跨domain
            return self.generate_cross_domain(intent)

        else:
            raise ValueError(f"Unknown generation type: {generation_type}")

    def parse_user_input(self, user_input: str) -> Dict:
        """
        解析使用者輸入為結構化Intent

        Args:
            user_input: 使用者輸入字串

        Returns:
            Intent字典
        """
        intent = {
            'raw_input': user_input,
            'subject': {},
            'action': None,
            'visual_style': {},
            'atmosphere': {},
            'design_style': None,
            'lighting': 'natural'
        }

        user_lower = user_input.lower()

        # 識別人物
        if any(kw in user_lower for kw in ['女', 'woman', 'female', '女性', '少女']):
            intent['subject']['gender'] = 'female'
        elif any(kw in user_lower for kw in ['男', 'man', 'male', '男性', '悟空', 'goku']):
            intent['subject']['gender'] = 'male'

        # 識別人種
        if any(kw in user_input for kw in ['東亞', 'East_Asian', '中國', '日本', '韓國']):
            intent['subject']['ethnicity'] = 'East_Asian'

        # 識別年齡
        if any(kw in user_input for kw in ['年輕', 'young', '少女']):
            intent['subject']['age_range'] = 'young_adult'
        elif any(kw in user_input for kw in ['兒童', 'child', '孩子']):
            intent['subject']['age_range'] = 'child'

        # 識別動作（特殊識別龜派氣功）
        if any(kw in user_input for kw in ['龜派氣功', 'kamehameha', '能量波']):
            intent['action'] = 'kamehameha'
            intent['energy'] = 'blue_energy_blast'

        # 識別藝術風格
        if any(kw in user_input for kw in ['3d', '3D', '蠟像', 'wax']):
            intent['visual_style']['art_style'] = 'wax_figure_3d'
        elif any(kw in user_input for kw in ['動漫', 'anime']):
            intent['visual_style']['art_style'] = 'anime'

        # 識別設計風格
        if any(kw in user_input for kw in ['溫馨可愛', '可愛', 'cute', 'warm']):
            intent['design_style'] = '溫馨可愛'
        elif any(kw in user_input for kw in ['現代簡約', '簡約', 'minimal', 'modern']):
            intent['design_style'] = '現代簡約'

        # 識別設計需求
        if any(kw in user_input for kw in ['海報', 'poster', '卡片', 'card']):
            intent['design_requirement'] = True

        # 識別光影
        if any(kw in user_input for kw in ['電影', 'cinematic', '電影級']):
            intent['lighting'] = 'cinematic'
        elif any(kw in user_input for kw in ['自然', 'natural']):
            intent['lighting'] = 'natural'

        return intent

    def classify_generation_type(self, intent: Dict) -> str:
        """
        自動分類生成型別

        Args:
            intent: 解析的Intent

        Returns:
            生成型別字串
        """
        # 檢查是否是設計需求
        if intent.get('design_style') or intent.get('design_requirement'):
            return 'design'

        # 檢查是否需要多個domain
        need_multiple_domains = False

        # 有動作/能量/特效 → 需要video/art domain
        if intent.get('action') or intent.get('energy'):
            need_multiple_domains = True

        # 有特殊藝術風格（3D、蠟像） → 需要art domain
        visual_style = intent.get('visual_style', {})
        art_style = visual_style.get('art_style', '')
        if any(kw in art_style for kw in ['3d', 'wax', 'holographic']):
            need_multiple_domains = True

        if need_multiple_domains:
            return 'cross_domain'

        # 預設：如果有人物，就是portrait
        if intent.get('subject'):
            return 'portrait'

        # 沒有人物，也不是設計，預設cross_domain
        return 'cross_domain'

    def generate_portrait(self, intent: Dict) -> Dict:
        """
        生成純人像提示詞（向後相容）

        Args:
            intent: 使用者意圖

        Returns:
            生成結果
        """
        print("  → 使用 portrait 生成器（向後相容）")

        # 使用原有的intelligent_generator
        elements = self.portrait_generator.select_elements_by_intent(intent)

        # 檢查一致性
        issues = self.portrait_generator.check_consistency(elements)
        if issues:
            elements, fixes = self.portrait_generator.resolve_conflicts(elements, issues)

        # 生成提示詞
        prompt = self.portrait_generator.compose_prompt(elements, mode='auto')

        return {
            'prompt': prompt,
            'type': 'portrait',
            'metadata': {
                'element_count': len(elements),
                'issues_fixed': len(issues)
            }
        }

    def generate_design(self, intent: Dict) -> Dict:
        """
        生成設計提示詞（SQLite + YAML）

        Args:
            intent: 使用者意圖

        Returns:
            生成結果
        """
        print("  → 使用 design 生成器（SQLite + YAML）")

        result = self.design_bridge.generate_design_prompt(intent)

        return {
            'prompt': result['prompt'],
            'type': 'design',
            'metadata': result['metadata'],
            'yaml_variables': result['yaml_variables']
        }

    def generate_cross_domain(self, intent: Dict) -> Dict:
        """
        生成跨domain提示詞（SQLite多domain + intelligent_generator完整流程）

        修復版：跨域查詢後，複用intelligent_generator的核心能力
        - 一致性檢查
        - 衝突解決
        - 智慧組裝

        Args:
            intent: 使用者意圖

        Returns:
            生成結果
        """
        print("  → 使用 cross_domain 生成器（SQLite多domain + 智慧組裝）")

        # 1. 跨domain查詢獲取候選元素
        elements_by_domain = self.query_engine.query_by_intent(intent)

        # 2. 合併所有domain的元素為統一列表
        all_elements = []
        for domain, elements in elements_by_domain.items():
            for elem in elements:
                # 確保元素有必要的欄位
                if 'template' not in elem:
                    elem['template'] = elem.get('ai_prompt_template', '')
                if 'category' not in elem:
                    elem['category'] = elem.get('category_id', 'unknown')
                # 標記來源domain
                elem['source_domain'] = domain
                all_elements.append(elem)

        print(f"  📊 合併了 {len(all_elements)} 個元素來自 {len(elements_by_domain)} 個domain")

        # 3. 如果元素太少，補充基於intent的智慧選擇
        if len(all_elements) < 5:
            print("  ⚠️  元素較少，使用intelligent_generator補充...")
            extra_elements = self.portrait_generator.select_elements_by_intent(intent)
            # 合併，避免重複
            existing_ids = {e.get('element_id') for e in all_elements}
            for elem in extra_elements:
                if elem.get('element_id') not in existing_ids:
                    elem['source_domain'] = 'portrait_supplement'
                    all_elements.append(elem)
            print(f"  📊 補充後共 {len(all_elements)} 個元素")

        # 4. 使用intelligent_generator檢查一致性
        issues = self.portrait_generator.check_consistency(all_elements)
        if issues:
            print(f"  🔍 發現 {len(issues)} 個一致性問題，正在修復...")
            all_elements, fixes = self.portrait_generator.resolve_conflicts(all_elements, issues)
            for fix in fixes:
                print(f"     {fix}")

        # 5. 基於raw_input增強prompt（提取使用者原始描述中的關鍵資訊）
        enhanced_parts = self._extract_scene_description(intent)
        
        # 6. 使用intelligent_generator的智慧組裝
        base_prompt = self.portrait_generator.compose_prompt(all_elements, mode='auto')
        
        # 7. 組合最終提示詞：增強描述 + 資料庫元素
        if enhanced_parts:
            final_prompt = f"{enhanced_parts}, {base_prompt}"
        else:
            final_prompt = base_prompt

        return {
            'prompt': final_prompt,
            'type': 'cross_domain',
            'metadata': {
                'domains_used': list(elements_by_domain.keys()),
                'element_count': len(all_elements),
                'issues_fixed': len(issues) if issues else 0,
                'enhanced': bool(enhanced_parts)
            }
        }

    def _extract_scene_description(self, intent: Dict) -> str:
        """
        從使用者原始輸入提取場景描述，生成增強的英文描述
        
        這是cross_domain的關鍵增強：將使用者的自然語言描述轉換為結構化的英文prompt
        """
        raw_input = intent.get('raw_input', '')
        if not raw_input:
            return ''
        
        parts = []
        raw_lower = raw_input.lower()
        
        # 場景型別識別
        scene_mappings = {
            # 古代/歷史場景
            ('秦', '宮殿', '大殿'): 'ancient Chinese Qin Dynasty palace hall, grand imperial architecture',
            ('戰國', '秦國'): 'Warring States period, ancient Chinese military setting',
            ('古代', '古裝'): 'ancient Chinese historical setting',
            ('宮廷', '皇宮'): 'Chinese imperial palace, ornate traditional architecture',
            ('戰場', '戰爭'): 'epic battlefield, war scene',
            
            # 動作場景
            ('比武', '對決', '決鬥'): 'intense combat duel, martial arts battle',
            ('劍術', '劍', '刀'): 'sword fighting, blade combat, weapon clash',
            ('武術', '功夫'): 'martial arts, kung fu action',
            ('打鬥', '格鬥'): 'fighting scene, combat action',
            
            # 人物型別
            ('武將', '將軍', '將領'): 'powerful military general, armored warrior',
            ('武士', '劍客'): 'skilled swordsman, warrior',
            ('王', '皇帝', '君主'): 'noble king, imperial ruler',
            
            # 氛圍
            ('史詩', '壯觀'): 'epic cinematic scene, grand scale',
            ('電影級', '大片'): 'blockbuster movie quality, cinematic composition',
            ('激烈', '緊張'): 'intense dramatic action, high tension',
        }
        
        for keywords, english_desc in scene_mappings.items():
            if any(kw in raw_input for kw in keywords):
                parts.append(english_desc)
        
        # 特定人物識別
        character_mappings = {
            '贏稷': 'King Yingji of Qin',
            '秦王': 'King of Qin',
            '白起': 'General Baiqi, legendary military commander',
            '項羽': 'Xiang Yu, mighty warrior king',
            '劉邦': 'Liu Bang, founder of Han Dynasty',
            '韓信': 'Han Xin, brilliant military strategist',
            '悟空': 'Son Goku, powerful martial artist',
        }
        
        for cn_name, en_name in character_mappings.items():
            if cn_name in raw_input:
                parts.append(en_name)
        
        # 視覺風格增強
        if any(kw in raw_lower for kw in ['電影', 'cinematic', '史詩']):
            parts.append('dramatic lighting, dust particles in the air')
        
        if any(kw in raw_lower for kw in ['古代', '戰國', '秦']):
            parts.append('elaborate period costume with intricate bronze patterns')
        
        # 去重並返回
        seen = set()
        unique_parts = []
        for part in parts:
            if part not in seen:
                seen.add(part)
                unique_parts.append(part)
        
        return ', '.join(unique_parts)

    def close(self):
        """關閉資源"""
        self.query_engine.close()
        self.design_bridge.close()
        self.portrait_generator.close()


def test_cross_domain_generator():
    """測試CrossDomainGenerator"""
    print("=" * 80)
    print("測試CrossDomainGenerator統一介面")
    print("=" * 80)

    generator = CrossDomainGenerator()

    # 測試1：純人像（向後相容）
    print("\n【測試1】純人像：生成一個年輕女性肖像\n")
    result1 = generator.generate("生成一個年輕女性肖像")
    print(f"\n型別: {result1['type']}")
    print(f"元素數: {result1['metadata']['element_count']}")
    print(f"提示詞長度: {len(result1['prompt'])} 字元")

    # 測試2：跨domain複雜場景
    print("\n\n【測試2】跨domain：龍珠悟空打龜派氣功的蠟像3D感\n")
    result2 = generator.generate("龍珠動漫的蠟像3D感悟空打出龜派氣功")
    print(f"\n型別: {result2['type']}")
    print(f"使用domain: {', '.join(result2['metadata']['domains_used'])}")
    print(f"元素數: {result2['metadata']['element_count']}")
    print(f"\n提示詞預覽: {result2['prompt'][:200]}...")

    # 測試3：設計海報（SQLite + YAML）
    print("\n\n【測試3】設計：溫馨可愛的兒童教育海報\n")
    result3 = generator.generate("溫馨可愛風格的兒童教育海報")
    print(f"\n型別: {result3['type']}")
    print(f"風格: {result3['metadata']['design_style']}")
    if 'yaml_variables' in result3:
        print(f"配色: {result3['yaml_variables'].get('colors', {}).get('scheme_name')}")
    print(f"\n提示詞: {result3['prompt']}")

    generator.close()
    print("\n\n✅ 所有測試完成")


if __name__ == '__main__':
    test_cross_domain_generator()
