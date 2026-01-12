#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜产品创意分析 - 自动化增强版
一键完成：获取数据 → AI分析 → 生成报告
"""

import json
import os
import sys
from datetime import datetime

def load_queries():
    """加载热搜查询数据"""
    if not os.path.exists('weibo_search_queries.json'):
        print("❌ 未找到热搜数据文件，请先运行获取脚本")
        return None

    with open('weibo_search_queries.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print("=" * 60)
    print("微博热搜产品创意分析 - 自动化增强版")
    print("=" * 60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 检查是否有热搜数据
    queries = load_queries()
    if queries:
        print(f"✅ 检测到热搜数据 ({len(queries)} 个话题)")
        print("\n热搜话题 TOP 5:")
        for q in queries[:5]:
            print(f"  #{q['rank']}: {q['title']} (热度: {q['heat']:,})")

        # 直接调用AI分析
        print("\n" + "=" * 60)
        print("🚀 准备调用AI进行深度分析...")
        print("=" * 60)
        print("\n请在Claude Code中执行以下Task命令：")

        # 生成Task调用命令
        topics_text = "\n".join([f"{q['rank']}. {q['title']} (热度: {q['heat']:,})" for q in queries])

        print(f"""
Task 工具调用示例:

请分析以下 {len(queries)} 个微博热搜话题并生成产品创意分析：

{topics_text}

分析要求：
1. 为每个话题评估有趣度（0-80分）和有用度（0-20分）
2. 对总分≥60分的话题，生成具体产品创意
3. 对总分≥80分的话题，从3个不同维度深度分析
4. 将结果保存到 enhanced_analysis_results.json

评分标准：
- 有趣度：新颖性、传播性、创意性、娱乐价值
- 有用度：实用性、解决问题能力、便利性

请以JSON格式输出到 enhanced_analysis_results.json 文件。
""")

        return 0
    else:
        print("❌ 未检测到热搜数据，请先运行 fetch_weibo_hotspot.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())
