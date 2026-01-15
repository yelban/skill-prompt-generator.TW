#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
框架載入器和框架驅動的提示詞生成器
Framework Loader and Framework-Driven Prompt Generator
"""

import yaml
import os
from typing import Dict, List, Optional, Any


class FrameworkLoader:
    """框架載入器"""

    @staticmethod
    def load(framework_path: str = "prompt_framework.yaml") -> Dict:
        """
        載入框架配置檔案

        引數:
            framework_path: 框架配置檔案路徑

        返回:
            框架配置字典
        """
        if not os.path.exists(framework_path):
            raise FileNotFoundError(f"框架配置檔案不存在: {framework_path}")

        with open(framework_path, 'r', encoding='utf-8') as f:
            framework = yaml.safe_load(f)

        print(f"✓ 載入框架: {framework['description']}")
        print(f"  版本: {framework['framework_version']}")
        print(f"  類別數: {len(framework['categories'])}")

        return framework

    @staticmethod
    def get_all_fields(framework: Dict) -> Dict[str, Dict]:
        """
        獲取框架中所有的欄位定義

        返回:
            {
                'subject.gender': {...},
                'styling.makeup': {...},
                ...
            }
        """
        all_fields = {}

        for category_name, category_config in framework['categories'].items():
            for field_name, field_config in category_config['fields'].items():
                full_field_name = f"{category_name}.{field_name}"
                all_fields[full_field_name] = {
                    'category': category_name,
                    'field': field_name,
                    **field_config
                }

        return all_fields

    @staticmethod
    def get_required_fields(framework: Dict) -> List[str]:
        """獲取所有必選欄位"""
        required = []

        for category_name, category_config in framework['categories'].items():
            if category_config.get('required'):
                for field_name, field_config in category_config['fields'].items():
                    if field_config.get('required'):
                        required.append(f"{category_name}.{field_name}")

        return required

    @staticmethod
    def apply_dependencies(intent: Dict, framework: Dict) -> Dict:
        """
        應用框架的依賴規則

        引數:
            intent: 原始intent
            framework: 框架配置

        返回:
            應用規則後的intent
        """
        updated_intent = intent.copy()

        dependencies = framework.get('dependencies', [])

        for rule in dependencies:
            # 檢查條件是否滿足
            if 'when' in rule:
                conditions_met = True

                for condition_field, condition_value in rule['when'].items():
                    category, field = condition_field.split('.')
                    actual_value = updated_intent.get(category, {}).get(field)

                    if actual_value != condition_value:
                        conditions_met = False
                        break

                # 如果條件滿足，應用then規則
                if conditions_met and 'then' in rule:
                    print(f"✓ 應用依賴規則: {rule.get('name', '未命名')}")

                    for then_field, then_value in rule['then'].items():
                        category, field = then_field.split('.')

                        if category not in updated_intent:
                            updated_intent[category] = {}

                        updated_intent[category][field] = then_value
                        print(f"  → 設定 {then_field} = {then_value}")

        return updated_intent

    @staticmethod
    def validate_intent(intent: Dict, framework: Dict) -> List[Dict]:
        """
        驗證intent的完整性和一致性

        返回:
            問題列表
        """
        issues = []

        validation = framework.get('validation', {})

        # 檢查必選欄位
        required_fields = validation.get('required_fields', [])
        for req in required_fields:
            field_path = req['field']
            category, field = field_path.split('.')

            if category not in intent or field not in intent[category]:
                issues.append({
                    'type': 'missing_required',
                    'field': field_path,
                    'severity': 'error',
                    'message': req['error_message']
                })

        # 檢查一致性
        consistency_checks = validation.get('consistency_checks', [])
        for check in consistency_checks:
            if 'when' in check:
                # 檢查條件
                for condition_field, condition_values in check['when'].items():
                    category, field = condition_field.split('.')
                    actual_value = intent.get(category, {}).get(field)

                    # 如果值在條件列表中，說明有問題
                    if isinstance(condition_values, list):
                        if actual_value in condition_values:
                            issues.append({
                                'type': 'consistency_check',
                                'name': check['name'],
                                'severity': check['severity'],
                                'message': check['message'],
                                'suggestion': check.get('suggestion', '')
                            })
                    else:
                        if actual_value == condition_values:
                            # 檢查其他條件欄位
                            pass

        return issues


class FrameworkDrivenGenerator:
    """框架驅動的生成器"""

    def __init__(self, db_path: str = "extracted_results/elements.db",
                 framework_path: str = "prompt_framework.yaml"):
        """
        初始化

        引數:
            db_path: 資料庫路徑
            framework_path: 框架配置檔案路徑
        """
        # 載入框架
        self.framework = FrameworkLoader.load(framework_path)

        # 載入IntelligentGenerator（用於資料庫查詢）
        from intelligent_generator import IntelligentGenerator
        self.generator = IntelligentGenerator(db_path)

    def generate_by_framework(self, intent: Dict) -> Dict:
        """
        根據框架和intent生成提示詞

        引數:
            intent: 使用者意圖（可能不完整）

        返回:
            {
                'intent': 完整的intent,
                'elements': 查詢到的元素列表,
                'prompt': 最終提示詞,
                'issues': 問題列表,
                'fixes': 修正說明
            }
        """
        print("\n" + "="*80)
        print("框架驅動生成")
        print("="*80)

        # 步驟1：應用依賴規則，補全intent
        print("\n📋 步驟1：應用框架依賴規則")
        print("-"*80)

        complete_intent = FrameworkLoader.apply_dependencies(intent, self.framework)

        # 步驟2：驗證intent
        print("\n✓ 步驟2：驗證Intent")
        print("-"*80)

        validation_issues = FrameworkLoader.validate_intent(complete_intent, self.framework)

        if validation_issues:
            print(f"⚠️ 發現 {len(validation_issues)} 個驗證問題:")
            for issue in validation_issues:
                print(f"  - [{issue['severity']}] {issue['message']}")
        else:
            print("✓ Intent驗證透過")

        # 步驟3：根據框架查詢資料庫
        print("\n🔍 步驟3：根據框架查詢資料庫")
        print("-"*80)

        elements = self.query_by_framework(complete_intent)

        print(f"✓ 查詢到 {len(elements)} 個元素")

        # 步驟4：一致性檢查
        print("\n✓ 步驟4：一致性檢查")
        print("-"*80)

        consistency_issues = self.generator.check_consistency(elements)

        fixes_applied = []
        if consistency_issues:
            print(f"⚠️ 發現 {len(consistency_issues)} 個一致性問題")
            elements, fixes_applied = self.generator.resolve_conflicts(elements, consistency_issues)
            for fix in fixes_applied:
                print(f"  {fix}")
        else:
            print("✓ 沒有發現一致性問題")

        # 步驟5：生成提示詞
        print("\n✨ 步驟5：生成最終提示詞")
        print("-"*80)

        prompt = self.generator.compose_prompt(elements, mode='auto', keywords_limit=3)

        # 步驟6：完整性檢查
        print("\n🎯 步驟6：完整性檢查")
        print("-"*80)

        completeness_issues = self.generator.check_completeness(complete_intent, prompt)

        if completeness_issues:
            print(f"⚠️ 發現 {len(completeness_issues)} 個缺失的需求:")
            for item in completeness_issues:
                print(f"  - {item['description']}")
        else:
            print("✓ 提示詞滿足所有使用者要求")

        return {
            'intent': complete_intent,
            'elements': elements,
            'prompt': prompt,
            'validation_issues': validation_issues,
            'consistency_issues': consistency_issues,
            'completeness_issues': completeness_issues,
            'fixes': fixes_applied
        }

    def query_all_candidates_by_framework(self, intent: Dict) -> Dict[str, List[Dict]]:
        """
        查詢所有候選元素（供SKILL分析選擇）

        返回:
            {
                'makeup': [所有makeup元素列表],
                'lighting': [所有lighting元素列表],
                ...
            }
        """
        candidates = {}

        # 遍歷框架的所有category
        for category_name, category_config in self.framework['categories'].items():

            # 跳過不需要查詢資料庫的category
            if category_name in ['subject', 'expression', 'scene', 'technical']:
                continue

            # 獲取該category的intent值
            category_intent = intent.get(category_name, {})

            # 遍歷該category的所有欄位
            for field_name, field_config in category_config['fields'].items():

                # 獲取欄位值
                field_value = category_intent.get(field_name, field_config.get('default'))

                # 如果該欄位有db_category（需要查詢資料庫）
                if 'db_category' in field_config:

                    db_category = field_config['db_category']
                    field_key = f"{category_name}.{field_name}"

                    # 查詢該類別的所有元素
                    all_elements = self.generator.get_all_elements_by_category('portrait', db_category)

                    if all_elements:
                        candidates[field_key] = all_elements
                        print(f"✓ {field_key}: 查詢到 {len(all_elements)} 個候選元素")

        # 查詢subject相關的候選
        subject = intent.get('subject', {})

        if 'ethnicity' in subject:
            # 眼睛候選
            eye_candidates = self.generator.get_all_elements_by_category('portrait', 'eye_types')
            if eye_candidates:
                candidates['facial.eyes'] = eye_candidates
                print(f"✓ facial.eyes: 查詢到 {len(eye_candidates)} 個候選元素")

            # 髮色候選
            hair_candidates = self.generator.get_all_elements_by_category('portrait', 'hair_colors')
            if hair_candidates:
                candidates['styling.hair_color'] = hair_candidates
                print(f"✓ styling.hair_color: 查詢到 {len(hair_candidates)} 個候選元素")

        return candidates

    def query_by_framework(self, intent: Dict) -> List[Dict]:
        """
        根據框架遍歷查詢所有欄位

        這是核心方法：程式碼不需要知道有哪些欄位，只遍歷框架
        """
        elements = []

        # 1. 處理主體屬性（特殊處理）
        subject = intent.get('subject', {})

        if 'gender' in subject:
            elem = self.generator.get_element_by_category('portrait', 'gender', subject['gender'])
            if elem:
                elements.append(elem)

        if 'ethnicity' in subject:
            elem = self.generator.get_element_by_category('portrait', 'ethnicity', subject['ethnicity'])
            if elem:
                elements.append(elem)

                # 自動選擇匹配人種的眼睛和頭髮
                ethnicity_name = subject['ethnicity']

                if ethnicity_name == 'East_Asian':
                    eye_elem = self.generator.get_element_by_category('portrait', 'eye_types', 'almond')
                else:
                    eye_elem = self.generator.get_element_by_category('portrait', 'eye_types')

                if eye_elem:
                    elements.append(eye_elem)

                typical_hair = self.generator.knowledge['ethnicity_typical_hair'].get(ethnicity_name, ['black'])
                hair_color_elem = self.generator.get_element_by_category('portrait', 'hair_colors', typical_hair[0])
                if hair_color_elem:
                    elements.append(hair_color_elem)

        if 'age_range' in subject:
            elem = self.generator.get_element_by_category('portrait', 'age_range')
            if elem:
                elements.append(elem)

        # 2. 遍歷框架的所有category（除了subject和expression）
        for category_name, category_config in self.framework['categories'].items():

            # 跳過已處理的
            if category_name in ['subject', 'expression', 'scene', 'technical']:
                continue

            # 獲取該category的intent值
            category_intent = intent.get(category_name, {})

            # 遍歷該category的所有欄位
            for field_name, field_config in category_config['fields'].items():

                # 獲取欄位值
                field_value = category_intent.get(field_name, field_config.get('default'))

                # 如果該欄位有db_category（需要查詢資料庫）
                if 'db_category' in field_config and field_value:

                    # 跳過預設值或auto
                    if field_value in ['modern', 'natural', 'auto', 'none']:
                        continue

                    db_category = field_config['db_category']

                    # 獲取搜尋關鍵詞
                    keywords_map = field_config.get('search_keywords', {})
                    keywords = keywords_map.get(field_value, [field_value])

                    # 查詢資料庫
                    elem = None
                    for kw in keywords:
                        elem = self.generator.get_element_by_category('portrait', db_category, kw)
                        if elem:
                            print(f"✓ {category_name}.{field_name} = '{field_value}' → 找到: '{elem['chinese_name']}'（關鍵詞: {kw}）")
                            elements.append(elem)
                            break

                    if not elem:
                        print(f"⚠️ {category_name}.{field_name} = '{field_value}' → 未找到元素")

        # 3. 處理其他固定類別
        for attr in ['skin_tones', 'skin_textures', 'face_shapes', 'expressions', 'poses']:
            elem = self.generator.get_element_by_category('portrait', attr)
            if elem:
                elements.append(elem)

        # 4. 處理風格關鍵詞
        style_keywords = []

        # 從scene收集關鍵詞
        scene = intent.get('scene', {})
        if 'atmosphere' in scene and scene['atmosphere']:
            style_keywords.append(scene['atmosphere'])

        if 'director_style' in scene and scene['director_style']:
            style_keywords.append(scene['director_style'])

            # 應用導演風格的關鍵詞擴充套件
            director_keywords = {
                'tsui_hark': ['wuxia', 'martial arts', 'flowing', 'dynamic'],
                'zhang_yimou': ['traditional', 'red', 'gold', 'period drama'],
                'wong_kar_wai': ['nostalgic', 'atmospheric', 'saturated colors']
            }
            if scene['director_style'] in director_keywords:
                style_keywords.extend(director_keywords[scene['director_style']])

        # 從era收集關鍵詞
        if 'era' in scene and scene['era'] != 'modern':
            style_keywords.append(scene['era'])
            if scene['era'] == 'ancient':
                style_keywords.extend(['traditional', 'period', 'classical'])

        if style_keywords:
            style_elements = self.generator.search_style_elements(style_keywords)
            elements.extend(style_elements)

        return elements

    def close(self):
        """關閉資料庫連線"""
        self.generator.close()


class ElementSelector:
    """
    元素選擇器 - 實現全域性最優選擇策略

    功能：
    - 從候選元素列表中選擇最匹配使用者需求的元素
    - 使用多維度評分機制（關鍵詞匹配 + 質量評分 + 語義一致性）
    - 替代簡單的貪心策略（第一個匹配就選）
    """

    @staticmethod
    def calculate_match_score(
        element: Dict,
        user_keywords: List[str],
        user_intent: Dict,
        field_name: str = ""
    ) -> float:
        """
        計算元素與使用者需求的匹配度

        引數:
            element: 候選元素
            user_keywords: 使用者需求關鍵詞列表（如 ['round', 'plump', 'full']）
            user_intent: 使用者完整意圖（用於語義一致性檢查）
            field_name: 欄位名（如 'facial.face_shape'）

        返回:
            匹配度評分（0-100）

        評分維度：
            1. 關鍵詞匹配度（60%）- 使用者關鍵詞在元素中出現的比例
            2. 元素質量評分（30%）- 元素的reusability_score
            3. 語義一致性（10%）- 檢測是否有語義衝突
        """
        score = 0.0

        # 獲取元素的關鍵詞和模板
        elem_keywords_raw = element.get('keywords', '')
        elem_template = element.get('ai_prompt_template', '')
        elem_name = element.get('name', '')

        # 處理keywords欄位（可能是字串或列表）
        if isinstance(elem_keywords_raw, list):
            elem_keywords_str = ' '.join(elem_keywords_raw)
        elif isinstance(elem_keywords_raw, str):
            try:
                import json
                keywords_list = json.loads(elem_keywords_raw)
                elem_keywords_str = ' '.join(keywords_list)
            except:
                elem_keywords_str = elem_keywords_raw
        else:
            elem_keywords_str = str(elem_keywords_raw)

        # 轉為小寫便於匹配
        elem_keywords_lower = elem_keywords_str.lower()
        elem_template_lower = elem_template.lower() if elem_template else ''
        elem_name_lower = elem_name.lower() if elem_name else ''

        # 維度1：關鍵詞匹配度（60分）
        if user_keywords:
            matched_count = 0
            total_keywords = len(user_keywords)

            for user_kw in user_keywords:
                user_kw_lower = user_kw.lower()

                # 檢查是否在關鍵詞、模板或名稱中出現
                if (user_kw_lower in elem_keywords_lower or
                    user_kw_lower in elem_template_lower or
                    user_kw_lower in elem_name_lower):
                    matched_count += 1

            keyword_match_rate = matched_count / total_keywords
            score += keyword_match_rate * 60

        # 維度2：元素質量評分（30分）
        reusability = element.get('reusability_score', 0.0)
        if reusability > 0:
            score += (reusability / 10.0) * 30

        # 維度3：語義一致性檢查（±10分）
        # 檢測語義衝突並扣分
        consistency_penalty = ElementSelector._check_semantic_consistency(
            element, user_keywords, user_intent, field_name
        )
        score += consistency_penalty

        return max(0.0, min(100.0, score))  # 限制在0-100範圍

    @staticmethod
    def _check_semantic_consistency(
        element: Dict,
        user_keywords: List[str],
        user_intent: Dict,
        field_name: str
    ) -> float:
        """
        檢查語義一致性，返回加分或扣分

        返回:
            分數調整值（-20 到 +10）
        """
        penalty = 0.0

        # 處理keywords欄位
        elem_keywords_raw = element.get('keywords', '')
        if isinstance(elem_keywords_raw, list):
            elem_keywords_str = ' '.join(elem_keywords_raw)
        elif isinstance(elem_keywords_raw, str):
            try:
                import json
                keywords_list = json.loads(elem_keywords_raw)
                elem_keywords_str = ' '.join(keywords_list)
            except:
                elem_keywords_str = elem_keywords_raw
        else:
            elem_keywords_str = str(elem_keywords_raw)

        elem_keywords_lower = elem_keywords_str.lower()
        elem_template = element.get('ai_prompt_template', '')
        elem_template_lower = elem_template.lower() if elem_template else ''

        # 規則1：嬰兒肥 vs 精緻
        # 如果使用者要求嬰兒肥（plump/chubby/full），但元素是精緻的（refined/delicate）→ 扣分
        baby_fat_keywords = ['plump', 'chubby', 'full', 'baby fat', 'rounded']
        refined_keywords = ['refined', 'delicate', 'classical', 'sculpted', 'elegant']

        user_wants_baby_fat = any(kw in ' '.join(user_keywords).lower() for kw in baby_fat_keywords)
        elem_is_refined = any(kw in elem_keywords_lower or kw in elem_template_lower for kw in refined_keywords)

        if user_wants_baby_fat and elem_is_refined:
            penalty -= 20  # 嚴重衝突，大幅扣分

        # 規則2：獎勵完美匹配
        # 如果使用者關鍵詞都在元素中出現 → 加分
        if user_keywords:
            all_matched = all(
                kw.lower() in elem_keywords_lower or kw.lower() in elem_template_lower
                for kw in user_keywords
            )
            if all_matched:
                penalty += 10  # 完美匹配，加分

        return penalty

    @staticmethod
    def select_best_element(
        candidates: List[Dict],
        user_keywords: List[str],
        user_intent: Dict = None,
        field_name: str = "",
        debug: bool = False
    ) -> tuple:
        """
        從候選列表中選擇最佳元素（全域性最優策略）

        引數:
            candidates: 候選元素列表
            user_keywords: 使用者需求關鍵詞
            user_intent: 使用者完整意圖（可選）
            field_name: 欄位名（可選，用於除錯）
            debug: 是否輸出除錯資訊

        返回:
            (最佳元素, 最佳得分)
        """
        if not candidates:
            return None, 0.0

        if user_intent is None:
            user_intent = {}

        best_element = None
        best_score = 0.0

        if debug:
            print(f"\n{'='*80}")
            print(f"🎯 全域性最優選擇：{field_name}")
            print(f"{'='*80}")
            print(f"候選數量：{len(candidates)}")
            print(f"使用者關鍵詞：{user_keywords}")
            print()

        # 遍歷所有候選，計算每個的匹配度
        scores = []
        for i, elem in enumerate(candidates):
            score = ElementSelector.calculate_match_score(
                elem, user_keywords, user_intent, field_name
            )
            scores.append((elem, score))

            if debug:
                print(f"{i+1}. {elem.get('chinese_name', elem.get('name'))}")
                print(f"   得分：{score:.1f}")
                print(f"   關鍵詞：{elem.get('keywords', 'N/A')[:60]}...")
                print()

            # 更新最佳
            if score > best_score:
                best_score = score
                best_element = elem

        if debug and best_element:
            print(f"✅ 最佳選擇：{best_element.get('chinese_name', best_element.get('name'))}")
            print(f"   得分：{best_score:.1f}")
            print(f"{'='*80}\n")

        return best_element, best_score

    @staticmethod
    def select_from_candidates_dict(
        candidates_dict: Dict[str, List[Dict]],
        intent: Dict,
        keywords_map: Dict[str, List[str]],
        debug: bool = False
    ) -> Dict[str, Dict]:
        """
        從多個欄位的候選中批次選擇最佳元素

        引數:
            candidates_dict: {field_name: [候選列表]}
            intent: 使用者完整意圖
            keywords_map: {field_name: [關鍵詞列表]}
            debug: 是否輸出除錯資訊

        返回:
            {field_name: 最佳元素}
        """
        selected = {}

        for field_name, candidates in candidates_dict.items():
            keywords = keywords_map.get(field_name, [])

            best_elem, score = ElementSelector.select_best_element(
                candidates, keywords, intent, field_name, debug
            )

            if best_elem:
                selected[field_name] = best_elem

        return selected
