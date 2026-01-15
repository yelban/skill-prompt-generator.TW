#!/usr/bin/env python3
"""
提示詞預處理和聚類指令碼
支援 txt, csv, json 格式的自動解析和清洗
"""

import json
import csv
import re
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter


class PromptPreprocessor:
    """提示詞預處理器"""

    def __init__(self, min_length: int = 10):
        self.min_length = min_length
        self.prompts = []
        self.metadata = {}

    def load_file(self, file_path: str) -> List[str]:
        """自動識別格式並載入檔案"""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"檔案不存在: {file_path}")

        suffix = path.suffix.lower()

        if suffix == '.txt':
            return self._load_txt(path)
        elif suffix == '.csv':
            return self._load_csv(path)
        elif suffix == '.json':
            return self._load_json(path)
        else:
            raise ValueError(f"不支援的檔案格式: {suffix}. 支援 .txt, .csv, .json")

    def _load_txt(self, path: Path) -> List[str]:
        """載入txt檔案（每行一個提示詞）"""
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        prompts = [line.strip() for line in lines if line.strip()]
        self.metadata['format'] = 'txt'
        self.metadata['original_count'] = len(prompts)
        return prompts

    def _load_csv(self, path: Path) -> List[str]:
        """載入csv檔案（自動識別提示詞列）"""
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            return []

        # 智慧識別提示詞列（包含 prompt, text, description 等關鍵詞）
        headers = list(rows[0].keys())
        prompt_col = None

        for keyword in ['prompt', 'text', 'description', 'content']:
            for header in headers:
                if keyword in header.lower():
                    prompt_col = header
                    break
            if prompt_col:
                break

        # 如果沒找到，使用第一列
        if not prompt_col:
            prompt_col = headers[0]

        prompts = [row[prompt_col].strip() for row in rows if row.get(prompt_col, '').strip()]

        self.metadata['format'] = 'csv'
        self.metadata['prompt_column'] = prompt_col
        self.metadata['original_count'] = len(prompts)

        return prompts

    def _load_json(self, path: Path) -> List[str]:
        """載入json檔案（支援陣列或物件陣列）"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, list):
            # 如果是字串陣列
            if all(isinstance(item, str) for item in data):
                prompts = data
            # 如果是物件陣列，嘗試找到提示詞欄位
            else:
                prompt_key = None
                for key in ['prompt', 'text', 'description', 'content']:
                    if data and key in data[0]:
                        prompt_key = key
                        break

                if not prompt_key:
                    prompt_key = list(data[0].keys())[0] if data else None

                prompts = [item[prompt_key] for item in data if prompt_key in item]
                self.metadata['prompt_key'] = prompt_key
        else:
            raise ValueError("JSON格式錯誤：需要陣列或物件陣列")

        self.metadata['format'] = 'json'
        self.metadata['original_count'] = len(prompts)

        return prompts

    def clean_prompts(self, prompts: List[str]) -> List[str]:
        """清洗提示詞"""
        cleaned = []

        for prompt in prompts:
            # 去除多餘空格
            prompt = re.sub(r'\s+', ' ', prompt.strip())

            # 統一標點（全形轉半形）
            prompt = prompt.replace('，', ', ').replace('。', '. ')

            # 過濾短提示
            if len(prompt) >= self.min_length:
                cleaned.append(prompt)

        # 去重（保持順序）
        seen = set()
        unique = []
        for p in cleaned:
            if p not in seen:
                seen.add(p)
                unique.append(p)

        self.metadata['after_cleaning'] = len(unique)
        self.metadata['duplicates_removed'] = len(cleaned) - len(unique)

        return unique

    def extract_keywords(self, prompts: List[str], top_n: int = 50) -> List[tuple]:
        """提取高頻關鍵詞（用於聚類）"""
        # 簡單的關鍵詞提取（基於詞頻）
        all_words = []

        # 停用詞（需要擴充套件）
        stopwords = {'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}

        for prompt in prompts:
            # 分詞（簡化版，按逗號和空格）
            words = re.split(r'[,\s]+', prompt.lower())
            words = [w.strip('.,!?;:()[]{}') for w in words]
            words = [w for w in words if w and w not in stopwords and len(w) > 2]
            all_words.extend(words)

        # 統計詞頻
        word_counts = Counter(all_words)

        return word_counts.most_common(top_n)

    def simple_cluster(self, prompts: List[str], n_clusters: int = 5) -> Dict[str, List[str]]:
        """簡單聚類（基於關鍵詞共現）"""
        # 提取關鍵詞
        keywords = self.extract_keywords(prompts, top_n=30)
        top_keywords = [kw[0] for kw in keywords[:n_clusters * 2]]

        # 為每個關鍵詞建立簇
        clusters = {f"cluster_{i}": [] for i in range(n_clusters)}
        cluster_keywords = {}

        # 選擇最具代表性的關鍵詞
        for i in range(min(n_clusters, len(top_keywords))):
            cluster_keywords[f"cluster_{i}"] = top_keywords[i]

        # 分配提示詞到簇
        unassigned = []

        for prompt in prompts:
            assigned = False
            prompt_lower = prompt.lower()

            # 檢查是否包含簇關鍵詞
            for cluster_id, keyword in cluster_keywords.items():
                if keyword in prompt_lower:
                    clusters[cluster_id].append(prompt)
                    assigned = True
                    break

            if not assigned:
                unassigned.append(prompt)

        # 未分配的放入最後一個簇或新簇
        if unassigned:
            clusters["cluster_other"] = unassigned

        # 移除空簇
        clusters = {k: v for k, v in clusters.items() if v}

        return clusters

    def generate_stats(self, prompts: List[str]) -> Dict[str, Any]:
        """生成統計資訊"""
        lengths = [len(p) for p in prompts]

        return {
            "total_prompts": len(prompts),
            "avg_length": sum(lengths) / len(lengths) if lengths else 0,
            "min_length": min(lengths) if lengths else 0,
            "max_length": max(lengths) if lengths else 0,
            "top_keywords": self.extract_keywords(prompts, top_n=20)
        }


def main():
    """命令列介面"""
    import sys

    if len(sys.argv) < 2:
        print("用法: python preprocessor.py <檔案路徑> [輸出檔案]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "preprocessed_prompts.json"

    preprocessor = PromptPreprocessor()

    # 載入和清洗
    print(f"正在載入: {input_file}")
    prompts = preprocessor.load_file(input_file)
    print(f"原始數量: {len(prompts)}")

    prompts = preprocessor.clean_prompts(prompts)
    print(f"清洗後: {len(prompts)}")

    # 聚類
    clusters = preprocessor.simple_cluster(prompts, n_clusters=5)
    print(f"\n聚類結果:")
    for cluster_id, cluster_prompts in clusters.items():
        print(f"  {cluster_id}: {len(cluster_prompts)} 條")

    # 生成統計
    stats = preprocessor.generate_stats(prompts)

    # 儲存結果
    result = {
        "metadata": preprocessor.metadata,
        "statistics": stats,
        "clusters": {k: v[:10] for k, v in clusters.items()},  # 每簇只儲存前10個示例
        "all_prompts": prompts
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n結果已儲存到: {output_file}")


if __name__ == "__main__":
    main()
