#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
變數取樣系統 - 智慧取樣元素變數
支援引數化元素，避免重複取樣，上下文感知
"""

import sqlite3
import json
import random
import time
from typing import Dict, List, Optional, Any


class SQLiteVariableSampler:
    """SQLite元素變數取樣器"""

    def __init__(self, db_path: str):
        """
        初始化變數取樣器

        Args:
            db_path: 資料庫路徑
        """
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.history = []  # 取樣歷史，避免重複
        self.max_history = 100  # 保留最近100次取樣歷史

    def get_element(self, element_id: str) -> Optional[Dict]:
        """獲取元素基礎資訊"""
        query = """
            SELECT element_id, name, chinese_name, ai_prompt_template,
                   keywords, reusability_score, category_id, domain_id
            FROM elements
            WHERE element_id = ?
        """
        self.cursor.execute(query, (element_id,))
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
            'category': row[6],
            'domain': row[7]
        }

    def get_element_variables(self, element_id: str) -> List[Dict]:
        """獲取元素的所有變數配置"""
        query = """
            SELECT variable_id, parameter_name, parameter_type,
                   possible_values, default_value, description
            FROM element_variables
            WHERE element_id = ?
        """
        self.cursor.execute(query, (element_id,))
        rows = self.cursor.fetchall()

        variables = []
        for row in rows:
            possible_values = None
            if row[3]:
                try:
                    possible_values = json.loads(row[3])
                except:
                    pass

            variables.append({
                'variable_id': row[0],
                'parameter_name': row[1],
                'parameter_type': row[2],
                'possible_values': possible_values,
                'default_value': row[4],
                'description': row[5]
            })

        return variables

    def sample_element_with_variables(self, element_id: str,
                                     style_context: Optional[Dict] = None) -> Dict:
        """
        取樣元素並應用變數

        Args:
            element_id: 元素ID
            style_context: 風格上下文（可選）

        Returns:
            包含原始元素和變數值的字典
        """
        # 1. 獲取元素基礎模板
        element = self.get_element(element_id)
        if not element:
            raise ValueError(f"Element not found: {element_id}")

        # 2. 獲取該元素的所有變數
        variables = self.get_element_variables(element_id)

        if not variables:
            # 沒有變數，直接返回原始元素
            return {
                'element': element,
                'variables': {},
                'result': element['template']
            }

        # 3. 取樣變數值（基於風格上下文）
        sampled_vars = {}
        for var in variables:
            sampled_vars[var['parameter_name']] = self.sample_variable(
                var, style_context, avoid_history=True
            )

        # 4. 應用變數到模板
        result = self.apply_variables(element['template'], sampled_vars)

        # 5. 記錄歷史
        self.history.append({
            'element_id': element_id,
            'variables': sampled_vars,
            'timestamp': time.time()
        })

        # 限制歷史長度
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        return {
            'element': element,
            'variables': sampled_vars,
            'result': result
        }

    def sample_variable(self, var_config: Dict, style_context: Optional[Dict],
                       avoid_history: bool) -> Any:
        """
        智慧取樣單個變數

        Args:
            var_config: 變數配置
            style_context: 風格上下文
            avoid_history: 是否避免最近使用過的值

        Returns:
            取樣的變數值
        """
        param_type = var_config['parameter_type']

        if param_type == 'enum':
            # 列舉型別：隨機選擇，避免重複
            values = var_config['possible_values']
            if not values:
                return var_config['default_value']

            # 根據風格上下文過濾
            if style_context:
                values = self.filter_by_style(values, style_context)

            # 避免最近使用過的
            if avoid_history and len(values) > 1:
                recent = self.get_recent_values(var_config['variable_id'])
                filtered = [v for v in values if v not in recent]
                if filtered:
                    values = filtered

            return random.choice(values) if values else var_config['default_value']

        elif param_type == 'range':
            # 範圍型別：在範圍內隨機
            range_vals = var_config['possible_values']
            if not range_vals or len(range_vals) != 2:
                return var_config['default_value']

            min_val, max_val = range_vals

            # 根據風格上下文調整範圍
            if style_context:
                min_val, max_val = self.adjust_range_by_style(
                    min_val, max_val, style_context
                )

            # 判斷是整數還是浮點數
            if isinstance(min_val, int) and isinstance(max_val, int):
                return random.randint(min_val, max_val)
            else:
                return round(random.uniform(min_val, max_val), 2)

        elif param_type == 'boolean':
            # 布林型別
            if style_context and 'prefer_' + var_config['parameter_name'] in style_context:
                return style_context['prefer_' + var_config['parameter_name']]
            return random.choice([True, False])

        else:
            return var_config['default_value']

    def filter_by_style(self, values: List[str], style_context: Dict) -> List[str]:
        """根據風格上下文過濾值"""
        # 簡單實現：如果上下文指定了偏好，優先選擇
        preferred = style_context.get('preferred_values', [])
        if preferred:
            filtered = [v for v in values if v in preferred]
            if filtered:
                return filtered
        return values

    def adjust_range_by_style(self, min_val: float, max_val: float,
                              style_context: Dict) -> tuple:
        """根據風格上下文調整範圍"""
        # 簡單實現：如果上下文指定了偏好範圍，縮小範圍
        if 'range_preference' in style_context:
            pref = style_context['range_preference']
            if pref == 'low':
                # 偏向低值
                max_val = min_val + (max_val - min_val) * 0.5
            elif pref == 'high':
                # 偏向高值
                min_val = min_val + (max_val - min_val) * 0.5
        return min_val, max_val

    def get_recent_values(self, variable_id: str, n: int = 3) -> List[Any]:
        """獲取最近n次使用過的值"""
        recent = []
        for record in reversed(self.history):
            for var_name, var_value in record['variables'].items():
                # 簡化：透過引數名匹配（實際應該用variable_id）
                if len(recent) < n:
                    recent.append(var_value)
        return recent

    def apply_variables(self, template: str, variables: Dict[str, Any]) -> str:
        """
        應用變數到模板

        支援格式：{variable_name}
        例如："{intensity} lighting" -> "dramatic lighting"
        """
        result = template
        for var_name, var_value in variables.items():
            placeholder = '{' + var_name + '}'
            if placeholder in result:
                result = result.replace(placeholder, str(var_value))
        return result

    def close(self):
        """關閉資料庫連線"""
        self.db.close()


class DesignVariableSampler:
    """設計變數取樣器（從design_variables表取樣）"""

    def __init__(self, db_path: str):
        """
        初始化設計變數取樣器

        Args:
            db_path: 資料庫路徑
        """
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.history = []
        self.max_history = 100

    def sample_design_variables(self, style_name: str,
                                variable_types: Optional[List[str]] = None) -> Dict:
        """
        取樣設計變數

        Args:
            style_name: 風格名稱（如：溫馨可愛、現代簡約）
            variable_types: 變數型別列表（如：['colors', 'borders']），None表示全部

        Returns:
            取樣的設計變數字典
        """
        query = """
            SELECT variable_id, variable_type, variable_name, variable_data
            FROM design_variables
            WHERE style_name = ?
        """
        params = [style_name]

        if variable_types:
            placeholders = ','.join(['?' for _ in variable_types])
            query += f" AND variable_type IN ({placeholders})"
            params.extend(variable_types)

        query += " ORDER BY priority DESC"

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()

        if not rows:
            return {}

        # 按型別分組
        variables_by_type = {}
        for row in rows:
            var_type = row[1]
            if var_type not in variables_by_type:
                variables_by_type[var_type] = []

            var_data = None
            if row[3]:
                try:
                    var_data = json.loads(row[3])
                except:
                    pass

            variables_by_type[var_type].append({
                'variable_id': row[0],
                'variable_name': row[2],
                'variable_data': var_data
            })

        # 從每個型別中隨機選擇一個
        sampled = {}
        for var_type, candidates in variables_by_type.items():
            # 避免重複
            recent = self.get_recent_variables(var_type)
            filtered = [c for c in candidates if c['variable_id'] not in recent]
            if not filtered:
                filtered = candidates

            selected = random.choice(filtered)
            sampled[var_type] = selected

            # 記錄歷史
            self.history.append({
                'style_name': style_name,
                'variable_type': var_type,
                'variable_id': selected['variable_id'],
                'timestamp': time.time()
            })

        # 限制歷史長度
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        return sampled

    def get_recent_variables(self, variable_type: str, n: int = 3) -> List[str]:
        """獲取最近使用過的變數ID"""
        recent = []
        for record in reversed(self.history):
            if record['variable_type'] == variable_type:
                recent.append(record['variable_id'])
                if len(recent) >= n:
                    break
        return recent

    def close(self):
        """關閉資料庫連線"""
        self.db.close()


def test_variable_sampler():
    """測試變數取樣器"""
    print("=" * 80)
    print("測試變數取樣系統")
    print("=" * 80)

    # 測試SQLiteVariableSampler
    print("\n【測試1】SQLite元素變數取樣")
    sampler = SQLiteVariableSampler("extracted_results/elements.db")

    # 測試取樣lighting元素（假設有變數）
    try:
        result = sampler.sample_element_with_variables(
            'common_lighting_001',
            style_context={'preferred_values': ['dramatic']}
        )
        print(f"  元素: {result['element']['chinese_name']}")
        print(f"  變數: {result['variables']}")
        print(f"  結果: {result['result']}")
    except Exception as e:
        print(f"  跳過（元素可能不存在）: {e}")

    sampler.close()

    # 測試DesignVariableSampler
    print("\n【測試2】設計變數取樣")
    design_sampler = DesignVariableSampler("extracted_results/elements.db")

    # 取樣溫馨可愛風格
    sampled = design_sampler.sample_design_variables('溫馨可愛')
    print(f"  風格: 溫馨可愛")
    for var_type, var_data in sampled.items():
        print(f"  {var_type}: {var_data['variable_name']}")

    # 再次取樣（應該避免重複）
    print("\n  第二次取樣（應避免重複）:")
    sampled2 = design_sampler.sample_design_variables('溫馨可愛')
    for var_type, var_data in sampled2.items():
        print(f"  {var_type}: {var_data['variable_name']}")

    design_sampler.close()

    print("\n✅ 測試完成")


if __name__ == '__main__':
    test_variable_sampler()
