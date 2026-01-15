#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧提示詞生成器 - 配合Claude Skill使用
具備語義理解、常識推理、一致性檢查能力
"""

import sqlite3
import json
from typing import Dict, List, Optional, Tuple


class IntelligentGenerator:
    """智慧提示詞生成器 - 理解意圖，檢查一致性"""

    def __init__(self, db_path: str = "extracted_results/elements.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # 載入常識知識庫
        self.knowledge = self.load_knowledge()

    def load_knowledge(self) -> Dict:
        """載入元素關係和常識約束"""
        return {
            # 人種 → 典型眼睛顏色
            'ethnicity_typical_eyes': {
                'East_Asian': ['black', 'dark brown', 'brown'],
                'Southeast_Asian': ['dark brown', 'brown', 'black'],
                'South_Asian': ['dark brown', 'brown', 'black'],
                'European': ['blue', 'green', 'brown', 'hazel', 'grey'],
                'African': ['dark brown', 'black', 'brown'],
                'Middle_Eastern': ['brown', 'dark brown', 'hazel', 'black'],
                'Latin_American': ['brown', 'dark brown', 'hazel', 'green'],
            },

            # 人種 → 典型髮色
            'ethnicity_typical_hair': {
                'East_Asian': ['black', 'dark brown'],
                'Southeast_Asian': ['black', 'dark brown'],
                'South_Asian': ['black', 'dark brown'],
                'European': ['blonde', 'brown', 'black', 'red', 'auburn'],
                'African': ['black', 'dark brown'],
                'Middle_Eastern': ['black', 'dark brown', 'brown'],
                'Latin_American': ['black', 'dark brown', 'brown'],
            },

            # 風格型別定義
            'style_types': {
                'anime': {'type': 'art_style', 'affects': 'rendering', 'description': '動漫繪畫風格'},
                'manga': {'type': 'art_style', 'affects': 'rendering', 'description': '漫畫繪畫風格'},
                'realistic': {'type': 'art_style', 'affects': 'rendering', 'description': '寫實繪畫風格'},
                'illustration': {'type': 'art_style', 'affects': 'rendering', 'description': '插畫繪畫風格'},

                'cyberpunk': {'type': 'atmosphere', 'affects': 'scene', 'description': '賽博朋克場景氛圍'},
                'fantasy': {'type': 'atmosphere', 'affects': 'scene', 'description': '奇幻場景氛圍'},
                'vintage': {'type': 'atmosphere', 'affects': 'scene', 'description': '復古場景氛圍'},

                'neon': {'type': 'lighting', 'affects': 'lighting', 'description': '霓虹燈光'},
                'dramatic': {'type': 'lighting', 'affects': 'lighting', 'description': '戲劇性燈光'},
            },

            # 導演/風格 → 光影需求對映
            'director_lighting_styles': {
                'zhang_yimou': {
                    'description': '張藝謀電影風格',
                    'lighting_keywords': ['dramatic', 'shadow', 'rim', 'contrast', 'chiaroscuro', 'volumetric'],
                    'required_elements': ['dramatic shadows', 'rim lighting'],
                },
                'cinematic': {
                    'description': '電影級',
                    'lighting_keywords': ['dramatic', 'cinematic', 'rim', 'contrast'],
                    'required_elements': ['dramatic lighting', 'rim lighting'],
                },
                'film_noir': {
                    'description': '黑色電影',
                    'lighting_keywords': ['shadow', 'contrast', 'chiaroscuro', 'low key'],
                    'required_elements': ['dramatic shadows', 'high contrast'],
                },
            },

            # 人物屬性類別（不應該被style關鍵詞覆蓋）
            'subject_attribute_categories': {
                'gender', 'age_range', 'ethnicity', 'skin_tones',
                'eye_types', 'hair_colors', 'hair_styles',
                'face_shapes', 'nose_types', 'lip_types'
            }
        }

    def get_element_by_category(self, domain: str, category: str,
                                value_filter: Optional[str] = None) -> Optional[Dict]:
        """從資料庫獲取元素"""
        query = """
            SELECT element_id, name, chinese_name, ai_prompt_template,
                   keywords, reusability_score, category_id
            FROM elements
            WHERE domain_id = ? AND category_id = ?
        """
        params = [domain, category]

        if value_filter:
            query += " AND (ai_prompt_template LIKE ? OR keywords LIKE ?)"
            params.extend([f"%{value_filter}%", f"%{value_filter}%"])

        query += " ORDER BY reusability_score DESC LIMIT 1"

        self.cursor.execute(query, params)
        row = self.cursor.fetchone()

        if not row:
            return None

        # 驗證name是否匹配value_filter（避免子串誤匹配，如female被male匹配）
        if value_filter and row[1].lower() != value_filter.lower():
            # 如果不匹配，嘗試直接用name精確匹配
            query_exact = """
                SELECT element_id, name, chinese_name, ai_prompt_template,
                       keywords, reusability_score, category_id
                FROM elements
                WHERE domain_id = ? AND category_id = ? AND name = ?
                ORDER BY reusability_score DESC LIMIT 1
            """
            self.cursor.execute(query_exact, [domain, category, value_filter])
            row = self.cursor.fetchone()
            if not row:
                return None

        keywords = None
        if row[4]:
            try:
                keywords = json.loads(row[4])
            except:
                pass

        return {
            'element_id': row[0],
            'name': row[1],
            'chinese_name': row[2],
            'template': row[3],
            'keywords': keywords,
            'reusability': row[5],
            'category': row[6]
        }

    def get_all_elements_by_category(self, domain: str, category: str,
                                     value_filter: Optional[str] = None) -> List[Dict]:
        """從資料庫獲取該類別的所有元素（用於SKILL分析）"""
        query = """
            SELECT element_id, name, chinese_name, ai_prompt_template,
                   keywords, reusability_score, category_id
            FROM elements
            WHERE domain_id = ? AND category_id = ?
        """
        params = [domain, category]

        if value_filter:
            query += " AND (ai_prompt_template LIKE ? OR keywords LIKE ?)"
            params.extend([f"%{value_filter}%", f"%{value_filter}%"])

        query += " ORDER BY reusability_score DESC"

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()

        elements = []
        for row in rows:
            keywords = None
            if row[4]:
                try:
                    keywords = json.loads(row[4])
                except:
                    pass

            elements.append({
                'element_id': row[0],
                'name': row[1],
                'chinese_name': row[2],
                'template': row[3],
                'keywords': keywords,
                'reusability': row[5],
                'category': row[6]
            })

        return elements

    def select_elements_by_intent(self, intent: Dict) -> List[Dict]:
        """
        基於解析的意圖從資料庫選擇元素

        intent格式:
        {
            'subject': {
                'gender': 'female',
                'ethnicity': 'East_Asian',
                'age_range': 'young_adult'
            },
            'visual_style': {
                'art_style': 'anime'
            },
            'atmosphere': {
                'theme': 'cyberpunk'
            }
        }
        """
        elements = []

        # 1. 選擇人物屬性
        subject = intent.get('subject', {})

        if 'gender' in subject:
            elem = self.get_element_by_category('portrait', 'gender', subject['gender'])
            if elem:
                elements.append(elem)

        if 'age_range' in subject:
            elem = self.get_element_by_category('portrait', 'age_range')
            if elem:
                elements.append(elem)

        if 'ethnicity' in subject:
            ethnicity_name = subject['ethnicity']
            elem = self.get_element_by_category('portrait', 'ethnicity', ethnicity_name)
            if elem:
                elements.append(elem)

            # 自動選擇匹配人種的眼睛
            # 對於東亞人，選擇almond/large expressive型別（避免green/blue）
            if ethnicity_name == 'East_Asian':
                eye_elem = self.get_element_by_category('portrait', 'eye_types', 'almond')
            else:
                eye_elem = self.get_element_by_category('portrait', 'eye_types')

            if eye_elem:
                elements.append(eye_elem)

            # 自動選擇匹配人種的髮色
            typical_hair = self.knowledge['ethnicity_typical_hair'].get(ethnicity_name, ['black'])
            hair_color_elem = self.get_element_by_category('portrait', 'hair_colors', typical_hair[0])
            if hair_color_elem:
                elements.append(hair_color_elem)

        # 2. 根據intent選擇服裝和髮型（優先使用intent指定的）
        clothing = intent.get('clothing', 'modern')
        hairstyle = intent.get('hairstyle', 'modern')

        # 服裝關鍵詞對映（靈活搜尋）
        clothing_keywords_map = {
            'traditional_chinese': ['traditional', 'chinese', 'hanfu', 'period'],
            'kimono': ['kimono', 'japanese'],
            'business': ['business', 'suit', 'formal'],
            'casual': ['casual'],
            'formal': ['formal', 'evening']
        }

        # 搜尋服裝元素
        if clothing != 'modern':  # 如果非預設，搜尋特定服裝
            search_keywords = clothing_keywords_map.get(clothing, [clothing])
            clothing_elem = None
            # 嘗試用每個關鍵詞搜尋
            for kw in search_keywords:
                clothing_elem = self.get_element_by_category('portrait', 'clothing_styles', kw)
                if clothing_elem:
                    print(f"✓ 找到服裝元素: '{clothing_elem['chinese_name']}'（搜尋關鍵詞: {kw}）")
                    elements.append(clothing_elem)
                    break

            # 如果沒找到，記錄資訊
            if not clothing_elem:
                print(f"⚠️ 未找到'{clothing}'服裝元素，將透過風格關鍵詞搜尋")
        else:
            # 預設選擇一個現代服裝
            elem = self.get_element_by_category('portrait', 'clothing_styles')
            if elem:
                elements.append(elem)

        # 髮型關鍵詞對映（靈活搜尋）
        hairstyle_keywords_map = {
            'ancient_chinese': ['traditional', 'classical', 'bun', 'updo'],
            'traditional_japanese': ['traditional', 'japanese'],
        }

        # 搜尋髮型元素（如果指定了特殊髮型）
        if hairstyle != 'modern':
            search_keywords = hairstyle_keywords_map.get(hairstyle, [hairstyle])
            hair_style_elem = None
            # 嘗試用每個關鍵詞搜尋
            for kw in search_keywords:
                hair_style_elem = self.get_element_by_category('portrait', 'hair_styles', kw)
                if hair_style_elem:
                    print(f"✓ 找到髮型元素: '{hair_style_elem['chinese_name']}'（搜尋關鍵詞: {kw}）")
                    elements.append(hair_style_elem)
                    break

            # 如果沒找到，記錄資訊
            if not hair_style_elem:
                print(f"⚠️ 未找到'{hairstyle}'髮型元素，將透過風格關鍵詞搜尋")
        else:
            # 預設選擇一個現代髮型
            elem = self.get_element_by_category('portrait', 'hair_styles')
            if elem:
                elements.append(elem)

        # 3. 選擇其他人物屬性
        for attr in ['skin_tones', 'skin_textures', 'face_shapes',
                     'makeup_styles', 'expressions', 'poses']:
            elem = self.get_element_by_category('portrait', attr)
            if elem:
                elements.append(elem)

        # 4. 新增風格元素（lighting, era, director_style等）
        visual_style = intent.get('visual_style', {})
        atmosphere = intent.get('atmosphere', {})
        era = intent.get('era', 'modern')
        lighting = intent.get('lighting', 'natural')

        # 收集所有風格關鍵詞
        style_keywords = []

        # 新增服裝關鍵詞（補充搜尋）
        if clothing != 'modern':
            clothing_search_kws = clothing_keywords_map.get(clothing, [])
            style_keywords.extend(clothing_search_kws)
            print(f"✓ 新增服裝搜尋關鍵詞: {', '.join(clothing_search_kws)}")

        # 添加發型關鍵詞（補充搜尋）
        if hairstyle != 'modern':
            hairstyle_search_kws = hairstyle_keywords_map.get(hairstyle, [])
            style_keywords.extend(hairstyle_search_kws)
            print(f"✓ 添加發型搜尋關鍵詞: {', '.join(hairstyle_search_kws)}")

        # 新增藝術風格
        if 'art_style' in visual_style:
            style_keywords.append(visual_style['art_style'])

        # 新增氛圍主題
        if 'theme' in atmosphere:
            style_keywords.append(atmosphere['theme'])

        # 新增光影關鍵詞
        if lighting:
            style_keywords.append(lighting)

        # 新增時代背景關鍵詞
        if era != 'modern':
            style_keywords.append(era)
            # 古代時期新增相關詞
            if era == 'ancient':
                style_keywords.extend(['traditional', 'period', 'classical'])

        # 檢查導演風格，新增特定關鍵詞
        director_style = atmosphere.get('director_style')
        if director_style:
            # 檢查是否在知識庫中（用於光影擴充套件）
            if director_style in self.knowledge.get('director_lighting_styles', {}):
                lighting_config = self.knowledge['director_lighting_styles'][director_style]
                style_keywords.extend(lighting_config['lighting_keywords'])
                print(f"✓ 識別到'{lighting_config['description']}'，自動新增光影關鍵詞: {', '.join(lighting_config['lighting_keywords'])}")

            # 新增導演風格的特定關鍵詞
            director_keywords = {
                'tsui_hark': ['wuxia', 'martial arts', 'flowing', 'dynamic'],
                'zhang_yimou': ['traditional', 'red', 'gold', 'period drama'],
                'wong_kar_wai': ['nostalgic', 'atmospheric', 'saturated colors']
            }
            if director_style in director_keywords:
                style_keywords.extend(director_keywords[director_style])
                print(f"✓ 識別到導演風格'{director_style}'，新增特徵關鍵詞: {', '.join(director_keywords[director_style])}")

        if style_keywords:
            style_elements = self.search_style_elements(style_keywords)
            elements.extend(style_elements)

        return elements

    def calculate_relevance(self, element: Dict, required_keywords: List[str]) -> float:
        """
        計算元素與需求的相關性得分（0-1）

        引數:
            element: 元素字典
            required_keywords: 使用者需求的關鍵詞列表

        返回:
            相關性得分 (0.0 - 1.0)
        """
        if not required_keywords:
            return 0.5  # 無關鍵詞，預設中等相關性

        template = element.get('template', '').lower()
        keywords = element.get('keywords', [])

        # 構建元素的所有文字
        element_text = template
        if keywords:
            element_text += ' ' + ' '.join(keywords).lower()

        # 計算匹配的關鍵詞數量
        matched = 0
        for kw in required_keywords:
            if kw.lower() in element_text:
                matched += 1

        # 相關性 = 匹配數 / 總關鍵詞數
        relevance = matched / len(required_keywords)

        return relevance

    def search_style_elements(self, keywords: List[str]) -> List[Dict]:
        """搜尋風格元素，排除人物屬性類別，按相關性×質量排序"""
        excluded_categories = self.knowledge['subject_attribute_categories']

        keyword_conditions = " OR ".join(["ai_prompt_template LIKE ?" for _ in keywords])
        query = f"""
            SELECT element_id, name, chinese_name, ai_prompt_template,
                   keywords, reusability_score, category_id
            FROM elements
            WHERE ({keyword_conditions})
              AND ai_prompt_template != ''
            ORDER BY reusability_score DESC
            LIMIT 30
        """

        params = [f"%{kw}%" for kw in keywords]
        self.cursor.execute(query, params)

        elements = []
        for row in self.cursor.fetchall():
            # 過濾掉人物屬性類別
            if row[6] in excluded_categories:
                continue

            keywords_data = None
            if row[4]:
                try:
                    keywords_data = json.loads(row[4])
                except:
                    pass

            elem = {
                'element_id': row[0],
                'name': row[1],
                'chinese_name': row[2],
                'template': row[3],
                'keywords': keywords_data,
                'reusability': row[5],
                'category': row[6]
            }

            # 計算相關性得分
            relevance = self.calculate_relevance(elem, keywords)

            # 綜合得分 = 相關性 × 質量分
            elem['relevance'] = relevance
            elem['final_score'] = relevance * row[5]  # reusability_score

            elements.append(elem)

        # 按綜合得分排序
        elements.sort(key=lambda x: x['final_score'], reverse=True)

        # 返回前10個最相關的
        return elements[:10]

    def check_consistency(self, elements: List[Dict]) -> List[Dict]:
        """
        檢查元素之間的一致性

        返回問題列表，每個問題包含：
        - type: 問題型別
        - severity: 嚴重程度 (low/medium/high)
        - description: 問題描述
        - suggestion: 修正建議
        """
        issues = []

        # 提取關鍵元素
        ethnicity_elem = self.find_element_by_category(elements, 'ethnicity')
        eye_elem = self.find_element_by_category(elements, 'eye_types')
        hair_elem = self.find_element_by_category(elements, 'hair_colors')

        # 檢查1：人種 vs 眼睛顏色（檢測不合理的顏色如green/blue for 東亞人）
        if ethnicity_elem and eye_elem:
            ethnicity_name = self.extract_ethnicity_name(ethnicity_elem['name'])
            eye_template = eye_elem['template'].lower()

            # 檢測不合理的顏色
            incompatible_colors = []
            if ethnicity_name == 'East_Asian':
                # 東亞人不應該有這些眼睛顏色
                if 'green' in eye_template or 'blue' in eye_template or 'violet' in eye_template:
                    incompatible_colors = ['green', 'blue', 'violet']
            elif ethnicity_name == 'African':
                if 'blue' in eye_template or 'green' in eye_template:
                    incompatible_colors = ['blue', 'green']

            if incompatible_colors:
                typical_eyes = self.knowledge['ethnicity_typical_eyes'].get(ethnicity_name, ['brown'])
                issues.append({
                    'type': 'ethnicity_eye_mismatch',
                    'severity': 'medium',
                    'current_ethnicity': ethnicity_elem['chinese_name'],
                    'current_eye': eye_elem['template'],
                    'incompatible_colors': incompatible_colors,
                    'typical_eyes': typical_eyes,
                    'description': f"{ethnicity_elem['chinese_name']}通常不會有包含'{', '.join(incompatible_colors)}'的眼睛",
                    'suggestion': f"建議選擇包含這些顏色的眼型: {', '.join(typical_eyes)}"
                })

        # 檢查2：人種 vs 髮色
        if ethnicity_elem and hair_elem:
            ethnicity_name = self.extract_ethnicity_name(ethnicity_elem['name'])
            typical_hair = self.knowledge['ethnicity_typical_hair'].get(ethnicity_name, [])

            hair_template = hair_elem['template'].lower()
            is_typical = any(color in hair_template for color in typical_hair)

            if not is_typical:
                issues.append({
                    'type': 'ethnicity_hair_mismatch',
                    'severity': 'low',
                    'current_ethnicity': ethnicity_elem['chinese_name'],
                    'current_hair': hair_elem['template'],
                    'typical_hair': typical_hair,
                    'description': f"{ethnicity_elem['chinese_name']}通常不會有'{hair_elem['template']}'",
                    'suggestion': f"建議改為: {', '.join(typical_hair)}"
                })

        # 檢查3：重複類別（但lighting_techniques允許多個）
        category_counts = {}
        for elem in elements:
            cat = elem['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1

        # 允許多個元素的類別
        multi_element_categories = {'lighting_techniques', 'photography_techniques'}

        for cat, count in category_counts.items():
            # lighting_techniques等類別允許多個元素組合
            if count > 1 and cat not in multi_element_categories:
                issues.append({
                    'type': 'duplicate_category',
                    'severity': 'high',
                    'category': cat,
                    'count': count,
                    'description': f"類別'{cat}'出現了{count}次（應該只有1次）",
                    'suggestion': "保留最相關的一個元素"
                })

        return issues

    def check_completeness(self, intent: Dict, prompt: str) -> List[Dict]:
        """
        檢查生成的提示詞是否滿足所有使用者要求

        引數:
            intent: 原始意圖字典
            prompt: 生成的提示詞字串

        返回:
            缺失需求列表，每個包含：
            - requirement: 需求型別
            - expected: 期望的關鍵詞
            - description: 缺失描述
        """
        missing = []
        prompt_lower = prompt.lower()

        # 檢查1：服裝要求
        clothing = intent.get('clothing')
        if clothing and clothing != 'modern':
            clothing_keywords = {
                'traditional_chinese': ['traditional', 'costume', 'hanfu', 'chinese dress', 'period dress'],
                'kimono': ['kimono', 'traditional japanese'],
                'business': ['business', 'suit', 'professional'],
                'casual': ['casual'],
                'formal': ['formal', 'evening gown', 'dress']
            }
            expected_kws = clothing_keywords.get(clothing, [])
            if expected_kws and not any(kw in prompt_lower for kw in expected_kws):
                missing.append({
                    'requirement': 'clothing',
                    'expected': expected_kws,
                    'description': f"使用者要求'{clothing}'服裝，但提示詞中未找到相關描述",
                    'suggestion': f"應包含: {', '.join(expected_kws[:3])}"
                })

        # 檢查2：髮型要求
        hairstyle = intent.get('hairstyle')
        if hairstyle and hairstyle != 'modern':
            hairstyle_keywords = {
                'ancient_chinese': ['traditional hairstyle', 'classical hair', 'hair ornament', 'hairpin', 'bun'],
                'traditional_japanese': ['traditional japanese hair', 'kanzashi']
            }
            expected_kws = hairstyle_keywords.get(hairstyle, [])
            if expected_kws and not any(kw in prompt_lower for kw in expected_kws):
                missing.append({
                    'requirement': 'hairstyle',
                    'expected': expected_kws,
                    'description': f"使用者要求'{hairstyle}'髮型，但提示詞中未找到相關描述",
                    'suggestion': f"應包含: {', '.join(expected_kws[:3])}"
                })

        # 檢查3：時代背景
        era = intent.get('era')
        if era and era != 'modern':
            era_keywords = {
                'ancient': ['traditional', 'period', 'classical', 'ancient'],
                'republic_of_china': ['republic era', '1920s', '1930s', 'vintage']
            }
            expected_kws = era_keywords.get(era, [])
            if expected_kws and not any(kw in prompt_lower for kw in expected_kws):
                missing.append({
                    'requirement': 'era',
                    'expected': expected_kws,
                    'description': f"使用者要求'{era}'時代背景，但提示詞中未找到相關描述",
                    'suggestion': f"應包含: {', '.join(expected_kws[:3])}"
                })

        # 檢查4：導演風格特徵
        atmosphere = intent.get('atmosphere', {})
        director_style = atmosphere.get('director_style')
        if director_style:
            director_keywords = {
                'tsui_hark': ['wuxia', 'martial arts', 'flowing', 'dynamic'],
                'zhang_yimou': ['traditional', 'red', 'gold', 'dramatic'],
                'wong_kar_wai': ['nostalgic', 'atmospheric', 'saturated']
            }
            expected_kws = director_keywords.get(director_style, [])
            if expected_kws and not any(kw in prompt_lower for kw in expected_kws):
                missing.append({
                    'requirement': 'director_style',
                    'expected': expected_kws,
                    'description': f"使用者要求'{director_style}'導演風格，但提示詞中未找到特徵關鍵詞",
                    'suggestion': f"應包含: {', '.join(expected_kws[:3])}"
                })

        # 檢查5：光影要求（必選）
        # 支援兩種格式：字串（舊格式）和dict（框架格式）
        lighting = intent.get('lighting', 'natural')
        if isinstance(lighting, dict):
            lighting = lighting.get('lighting_type', 'natural')

        lighting_keywords = {
            'natural': ['natural', 'window light', 'daylight', 'soft light'],
            'cinematic': ['cinematic', 'dramatic', 'rim light'],
            'zhang_yimou': ['dramatic', 'shadow', 'rim', 'chiaroscuro'],
            'film_noir': ['shadow', 'contrast', 'chiaroscuro', 'low key'],
            'neon': ['neon', 'colorful', 'glow'],
            'soft': ['soft', 'gentle', 'diffused'],
            'dramatic': ['dramatic', 'shadow', 'contrast']
        }
        expected_kws = lighting_keywords.get(lighting, [])
        if expected_kws and not any(kw in prompt_lower for kw in expected_kws):
            missing.append({
                'requirement': 'lighting',
                'expected': expected_kws,
                'description': f"使用者要求'{lighting}'光影，但提示詞中未找到相關描述",
                'suggestion': f"應包含: {', '.join(expected_kws[:3])}"
            })

        return missing

    def resolve_conflicts(self, elements: List[Dict], issues: List[Dict]) -> Tuple[List[Dict], List[str]]:
        """
        解決檢測到的衝突

        返回：(修正後的元素列表, 修正說明列表)
        """
        fixed_elements = elements.copy()
        fixes_applied = []

        for issue in issues:
            if issue['type'] == 'ethnicity_eye_mismatch':
                # 替換為符合人種的眼睛（選擇almond/brown等合適的）
                ethnicity_elem = self.find_element_by_category(fixed_elements, 'ethnicity')
                ethnicity_name = self.extract_ethnicity_name(ethnicity_elem['name']) if ethnicity_elem else 'East_Asian'

                # 為不同人種選擇合適的眼型
                if ethnicity_name == 'East_Asian':
                    new_eye_elem = self.get_element_by_category('portrait', 'eye_types', 'almond brown')
                    if not new_eye_elem:
                        new_eye_elem = self.get_element_by_category('portrait', 'eye_types', 'almond')
                else:
                    new_eye_elem = self.get_element_by_category('portrait', 'eye_types')

                if new_eye_elem:
                    # 移除舊的eye元素
                    fixed_elements = [e for e in fixed_elements if e['category'] != 'eye_types']
                    # 新增新的
                    fixed_elements.append(new_eye_elem)

                    fixes_applied.append(
                        f"✓ 修正眼睛: '{issue['current_eye']}' → '{new_eye_elem['template']}' "
                        f"(符合{issue['current_ethnicity']}特徵)"
                    )

            elif issue['type'] == 'ethnicity_hair_mismatch':
                # 替換髮色
                suggested_color = issue['typical_hair'][0]
                new_hair_elem = self.get_element_by_category('portrait', 'hair_colors', suggested_color)

                if new_hair_elem:
                    fixed_elements = [e for e in fixed_elements if e['category'] != 'hair_colors']
                    fixed_elements.append(new_hair_elem)

                    fixes_applied.append(
                        f"✓ 修正髮色: '{issue['current_hair']}' → '{new_hair_elem['template']}' "
                        f"(符合{issue['current_ethnicity']}特徵)"
                    )

            elif issue['type'] == 'duplicate_category':
                # 保留第一個，刪除其他
                cat = issue['category']
                kept = False
                new_list = []
                for elem in fixed_elements:
                    if elem['category'] == cat:
                        if not kept:
                            new_list.append(elem)
                            kept = True
                    else:
                        new_list.append(elem)

                fixed_elements = new_list
                fixes_applied.append(f"✓ 移除重複的'{cat}'類別元素")

        return fixed_elements, fixes_applied

    def find_element_by_category(self, elements: List[Dict], category: str) -> Optional[Dict]:
        """從元素列表中查詢指定類別的元素"""
        for elem in elements:
            if elem['category'] == category:
                return elem
        return None

    def extract_ethnicity_name(self, name: str) -> str:
        """從元素名稱提取人種標準名稱"""
        mapping = {
            'east_asian': 'East_Asian',
            'southeast_asian': 'Southeast_Asian',
            'south_asian': 'South_Asian',
            'european': 'European',
            'african': 'African',
            'middle_eastern': 'Middle_Eastern',
            'latin_american': 'Latin_American',
        }
        return mapping.get(name.lower(), name)

    def compose_prompt(self, elements: List[Dict], mode: str = 'auto',
                      keywords_limit: int = 3) -> str:
        """
        組合元素生成最終提示詞（帶去重和過濾）

        mode: 'simple', 'auto', 'detailed'
        """
        all_keywords = []
        seen_concepts = set()  # 用於去重

        # 同義詞組（用於去重）
        synonym_groups = {
            'woman': ['woman', 'female', 'lady', 'girl'],
            'man': ['man', 'male', 'gentleman', 'boy'],
            'young': ['young', 'youthful', 'young adult'],
            'fair': ['fair', 'pale', 'light'],
            'East Asian': ['East Asian', 'Chinese', 'Japanese', 'Korean'],
            'eyes': ['eyes', 'eye', 'large expressive eyes', 'almond eyes'],
            'hair': ['hair', 'hairs', 'black hair'],
            'skin': ['skin', 'fair skin', 'pale skin', 'realistic skin texture'],
            'face': ['face', 'oval face'],
            'ponytail': ['ponytail with bangs', 'straight bangs ponytail', 'ponytail and fringe', 'ponytail'],
            'bokeh': ['creamy bokeh', 'cinematic bokeh', 'smooth bokeh', 'bokeh'],
            'dramatic': ['dramatic shadows', 'dramatic lighting', 'dramatic'],
            'rim light': ['rim light', 'edge lighting', 'backlight', 'rim lighting'],
            'gaze': ['innocent gaze', 'gentle smile', 'soft introspective', 'gaze'],
            'pose': ['relaxed', 'casual stance', 'natural pose', 'pose'],
        }

        # 無關/錯誤的關鍵詞黑名單（明顯不屬於人像）
        blacklist = {
            'bottle', 'highlighting', 'condensa', 'elements', 'surroundings',
            'practical', 'string', 'lanterns', 'vintage lamps', 'accent lights'
        }

        # 反向對映：關鍵詞 → 代表詞
        concept_map = {}
        for representative, synonyms in synonym_groups.items():
            for syn in synonyms:
                concept_map[syn.lower()] = representative

        for elem in elements:
            template = elem.get('template', '')
            keywords = elem.get('keywords')

            # 選擇文字
            if mode == 'simple':
                text = template
            elif mode == 'detailed' and keywords and len(keywords) > 0:
                text_list = keywords[:keywords_limit]
            elif mode == 'auto' and keywords and len(keywords) > 2:
                text_list = keywords[:keywords_limit]
            else:
                text = template
                text_list = None

            # 如果有keywords列表，逐個處理
            if text_list:
                for kw in text_list:
                    # 過濾無效關鍵詞
                    if not kw or len(kw.strip()) == 0:
                        continue

                    kw_stripped = kw.strip()
                    kw_lower = kw_stripped.lower()

                    # 黑名單過濾
                    if any(blackword in kw_lower for blackword in blacklist):
                        continue

                    words = kw_stripped.split()

                    # 過濾單個詞碎片（<4字元或明顯無關）
                    if len(words) == 1:
                        # 單詞過濾：短於4字元，或在黑名單
                        if len(kw_stripped) < 4 or kw_lower in blacklist:
                            continue

                    # 去重檢查 - 檢查完整短語
                    concept = concept_map.get(kw_lower, None)

                    # 如果沒有精確匹配，檢查是否完全匹配已知概念
                    # 注意：只對完整短語進行同義詞匹配，不做子串匹配
                    if not concept:
                        # 先嚐試精確匹配整個短語
                        for rep, syns in synonym_groups.items():
                            if kw_lower in [s.lower() for s in syns]:
                                concept = rep
                                break

                    # 如果還是沒找到概念，用完整短語作為唯一標識
                    if not concept:
                        concept = kw_lower

                    if concept not in seen_concepts:
                        all_keywords.append(kw_stripped)
                        seen_concepts.add(concept)
            else:
                # 使用template
                if text and text.strip():
                    text_stripped = text.strip()
                    text_lower = text_stripped.lower()

                    # 黑名單過濾
                    if any(blackword in text_lower for blackword in blacklist):
                        continue

                    # 去重檢查
                    concept = concept_map.get(text_lower, None)

                    # 檢查是否完全匹配已知概念（不做子串匹配）
                    if not concept:
                        for rep, syns in synonym_groups.items():
                            if text_lower in [s.lower() for s in syns]:
                                concept = rep
                                break

                    if not concept:
                        concept = text_lower

                    if concept not in seen_concepts:
                        all_keywords.append(text_stripped)
                        seen_concepts.add(concept)

        return ', '.join(all_keywords)

    def close(self):
        """關閉資料庫連線"""
        self.conn.close()


def test_intelligent_generator():
    """測試智慧生成器"""
    gen = IntelligentGenerator()

    print("="*80)
    print("測試智慧提示詞生成器")
    print("="*80)

    # 測試intent
    intent = {
        'subject': {
            'gender': 'female',
            'ethnicity': 'East_Asian',
            'age_range': 'young_adult'
        },
        'visual_style': {
            'art_style': 'anime'
        },
        'atmosphere': {
            'theme': 'cyberpunk'
        }
    }

    print("\n1. 基於intent選擇元素...")
    elements = gen.select_elements_by_intent(intent)
    print(f"   選擇了 {len(elements)} 個元素")

    print("\n2. 檢查一致性...")
    issues = gen.check_consistency(elements)

    if issues:
        print(f"   發現 {len(issues)} 個問題:")
        for issue in issues:
            print(f"   - [{issue['severity']}] {issue['description']}")
            print(f"     {issue['suggestion']}")

        print("\n3. 修正衝突...")
        fixed_elements, fixes = gen.resolve_conflicts(elements, issues)
        for fix in fixes:
            print(f"   {fix}")
    else:
        print("   ✓ 沒有發現問題")
        fixed_elements = elements

    print("\n4. 生成最終提示詞...")
    prompt = gen.compose_prompt(fixed_elements, mode='auto')
    print(f"\n{prompt}")

    print("\n5. 檢查完整性...")
    missing = gen.check_completeness(intent, prompt)
    if missing:
        print(f"   ⚠️ 發現 {len(missing)} 個缺失的需求:")
        for item in missing:
            print(f"   - {item['description']}")
            print(f"     {item['suggestion']}")
    else:
        print("   ✓ 提示詞滿足所有使用者要求")

    gen.close()


def query_candidates_by_intent(intent: dict, db_path: str = 'extracted_results/elements.db') -> dict:
    """
    【執行層】根據Intent查詢所有候選元素

    輸入：Intent字典（由SKILL構造）
    輸出：候選字典 {field: [elements]}
    """
    from framework_loader import FrameworkDrivenGenerator

    gen = FrameworkDrivenGenerator(db_path)
    candidates = gen.query_all_candidates_by_framework(intent)

    return candidates


def assemble_prompt_from_elements(elements: list, subject_desc: str = '') -> str:
    """
    【執行層】從元素列表拼接提示詞

    輸入：
    - elements: 元素列表（由SKILL選擇）
    - subject_desc: 主體描述（可選，如"A young woman"）

    輸出：完整提示詞字串
    """
    parts = []

    if subject_desc:
        parts.append(subject_desc)

    for element in elements:
        template = element.get('template', '')
        if template:
            parts.append(template)

    return ', '.join(parts)


def save_generated_prompt(prompt_text: str, user_intent: str,
                         elements_used: list, style_tag: str = None,
                         quality_score: float = 9.0,
                         db_path: str = 'extracted_results/elements.db') -> int:
    """
    【執行層】儲存生成的Prompt到資料庫

    這是prompt-analyzer工作的資料來源！

    引數：
    - prompt_text: 完整的提示詞文字
    - user_intent: 使用者的原始需求描述
    - elements_used: 使用的元素列表（每個元素應包含element_id, category, field_name）
    - style_tag: 風格標籤（如ancient_chinese, modern_sci_fi等）
    - quality_score: 質量評分（由SKILL評估，預設9.0）
    - db_path: 資料庫路徑

    返回：
    - prompt_id: 儲存後的Prompt ID
    """
    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 1. 儲存到generated_prompts表
        cursor.execute('''
            INSERT INTO generated_prompts
            (prompt_text, user_intent, quality_score, style_tag, generation_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (prompt_text, user_intent, quality_score, style_tag, datetime.now()))

        prompt_id = cursor.lastrowid

        # 2. 儲存元素關聯到prompt_elements表
        for element in elements_used:
            element_id = element.get('element_id')
            category = element.get('category')
            field_name = element.get('field_name', '')

            if element_id:  # 只儲存有效的element_id
                cursor.execute('''
                    INSERT INTO prompt_elements
                    (prompt_id, element_id, category, field_name)
                    VALUES (?, ?, ?, ?)
                ''', (prompt_id, element_id, category, field_name))

        # 3. 更新元素使用統計
        for element in elements_used:
            element_id = element.get('element_id')
            if element_id:
                # 檢查是否已存在統計記錄
                cursor.execute('''
                    SELECT usage_count, avg_quality
                    FROM element_usage_stats
                    WHERE element_id = ?
                ''', (element_id,))

                existing = cursor.fetchone()

                if existing:
                    # 更新統計
                    old_count = existing[0]
                    old_avg = existing[1]
                    new_count = old_count + 1
                    new_avg = (old_avg * old_count + quality_score) / new_count

                    cursor.execute('''
                        UPDATE element_usage_stats
                        SET usage_count = ?, avg_quality = ?, last_used = ?
                        WHERE element_id = ?
                    ''', (new_count, new_avg, datetime.now(), element_id))
                else:
                    # 建立新統計記錄
                    cursor.execute('''
                        INSERT INTO element_usage_stats
                        (element_id, usage_count, avg_quality, last_used)
                        VALUES (?, 1, ?, ?)
                    ''', (element_id, quality_score, datetime.now()))

        conn.commit()
        print(f"✅ Prompt已儲存到資料庫，ID: #{prompt_id}")
        return prompt_id

    except Exception as e:
        conn.rollback()
        print(f"❌ 儲存Prompt失敗: {e}")
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    # 測試：舊的Intent-based流程
    test_intelligent_generator()
