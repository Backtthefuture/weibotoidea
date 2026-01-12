#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为每个热搜话题生成AI分析提示
"""

import json

def generate_analysis_prompts():
    """为每个热搜话题生成分析提示"""

    # 读取热搜查询
    with open('weibo_search_queries.json', 'r', encoding='utf-8') as f:
        queries = json.load(f)

    prompts = []

    for query in queries:
        title = query['title']
        heat = query['heat']
        rank = query['rank']

        prompt = f"""
请分析以下微博热搜话题，并从"有趣"和"有用"两个角度评估生成产品创意的可能性。

热搜话题：{title}
热搜排名：#{rank}
热度：{heat:,}

请按照以下标准评估：

1. **有趣度（满分80分）**：
   - 话题是否新颖、有创意？
   - 是否能引发用户好奇心和参与欲？
   - 是否有娱乐性、传播性？
   - 是否能创造独特的用户体验？

2. **有用度（满分20分）**：
   - 是否能解决实际问题？
   - 是否有实用价值？
   - 是否能提高效率或提供便利？

请提供：
- 有趣度评分（0-80）和理由
- 有用度评分（0-20）和理由
- 总分（有趣度+有用度）
- 关键事件脉络总结（100字以内）
- 如果总分≥60分，请提供一个具体的产品Idea，包括：
  * 产品名称
  * 核心功能
  * 目标用户
  * 简要描述（50字以内）

如果总分<60分，请说明原因。

请以JSON格式返回结果，包含以下字段：
- rank: 话题排名
- title: 话题标题
- heat: 热度
- fun_score: 有趣度评分（0-80）
- fun_reason: 有趣度理由
- useful_score: 有用度评分（0-20）
- useful_reason: 有用度理由
- total_score: 总分
- summary: 事件脉络总结（100字以内）
- has_idea: 是否有产品创意（true/false）
- product: 如果有创意，包含product对象（name, features, target_users, description），否则为null
- reason: 如果没有创意，说明原因
"""

        prompts.append({
            'rank': rank,
            'title': title,
            'heat': heat,
            'prompt': prompt.strip()
        })

    return prompts

if __name__ == "__main__":
    print("=" * 60)
    print("生成AI分析提示...")
    print("=" * 60)

    prompts = generate_analysis_prompts()

    print(f"\n✅ 已生成 {len(prompts)} 个分析提示")

    # 保存提示
    with open('analysis_prompts.json', 'w', encoding='utf-8') as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)

    print(f"📄 提示已保存到: analysis_prompts.json")
    print("\n接下来将使用Task工具进行AI分析...")
    print("=" * 60)
