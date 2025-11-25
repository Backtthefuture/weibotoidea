#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI分析微博热点并生成产品创意
"""

import json
import os
import re
import sys
from datetime import datetime


def load_search_results():
    """加载所有搜索结果文件"""
    print("正在加载搜索结果...")

    search_results = []
    result_files = [f for f in os.listdir('.') if f.startswith('search_results_') and f.endswith('.json')]

    if not result_files:
        print("❌ 未找到搜索结果文件")
        print("请确保文件名为: search_results_XX.json")
        return []

    print(f"找到 {len(result_files)} 个结果文件")

    for result_file in sorted(result_files):
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 提取文件名中的排名
            match = re.search(r'search_results_(\d+)\.json', result_file)
            rank = int(match.group(1)) if match else 0

            search_results.append({
                'rank': rank,
                'filename': result_file,
                'data': data,
                'title': data.get('title', f'热点#{rank}'),
                'content': data.get('content', '')
            })

            print(f"  ✅ 已加载: {result_file} (排名: #{rank})")

        except Exception as e:
            print(f"  ❌ 加载失败 {result_file}: {e}")

    # 按排名排序
    search_results.sort(key=lambda x: x['rank'])

    print(f"✅ 成功加载 {len(search_results)} 个搜索结果")
    return search_results


def load_hotspot_queries():
    """加载热搜查询列表"""
    try:
        with open('weibo_search_queries.json', 'r', encoding='utf-8') as f:
            queries = json.load(f)
        return queries
    except Exception as e:
        print(f"❌ 加载热搜查询失败: {e}")
        return []


def extract_search_snippet(search_data):
    """从搜索结果中提取摘要"""
    if not search_data:
        return "暂无搜索结果"

    # 根据不同的数据结构提取信息
    if isinstance(search_data, dict):
        # 如果是单个结果
        snippet = search_data.get('snippet', '') or search_data.get('content', '')
        if snippet:
            return snippet[:500]  # 限制长度

        # 尝试其他字段
        for key in ['description', 'summary', 'text', 'body']:
            if key in search_data:
                return str(search_data[key])[:500]

    elif isinstance(search_data, list) and len(search_data) > 0:
        # 如果是列表，取前几个
        snippets = []
        for item in search_data[:3]:
            if isinstance(item, dict):
                snippet = item.get('snippet', '') or item.get('content', '') or item.get('description', '')
                if snippet:
                    snippets.append(snippet)
        return ' | '.join(snippets)[:500]

    return "搜索结果内容较少"


def generate_ai_analysis_prompt(hotspot_data, search_summary):
    """生成AI分析提示"""
    title = hotspot_data.get('title', '未知热点')

    prompt = f"""请分析以下微博热搜话题，并从"有趣"和"有用"两个角度评估生成小产品的可能性。

## 热搜话题
{title}

## 背景信息
{search_summary}

## 评估标准

### 1. 有趣度（满分80分）
- 话题是否新颖、有创意？
- 是否能引发用户好奇心和参与欲？
- 是否有娱乐性、传播性？
- 是否能创造独特的用户体验？

### 2. 有用度（满分20分）
- 是否能解决实际问题？
- 是否有实用价值？
- 是否能提高效率或提供便利？

## 输出要求

请提供以下信息（JSON格式）：

```json
{{
  "fun_score": 0-80,  // 有趣度评分（0-80分）
  "fun_reason": "有趣度评分理由",
  "useful_score": 0-20,  // 有用度评分（0-20分）
  "useful_reason": "有用度评分理由",
  "total_score": 0-100,  // 总分
  "has_idea": true/false,  // 是否生成产品创意
  "product": {{
    "name": "产品名称",
    "features": "核心功能",
    "target_users": "目标用户",
    "description": "产品描述（50字以内）"
  }},
  "summary": "关键事件脉络（100字以内）",
  "analysis_notes": "分析备注"
}}
```

**重要**：如果总分 < 60分，请将 has_idea 设为 false，product 设为 null。

请分析并返回JSON结果："""

    return prompt


def save_analysis_prompts(search_results, hotspot_queries):
    """保存所有AI分析提示"""
    prompts_dir = 'analysis_prompts'
    os.makedirs(prompts_dir, exist_ok=True)

    prompts_data = []

    for i, result in enumerate(search_results):
        rank = result['rank']
        title = result['title']

        # 匹配对应的热搜查询
        hotspot_query = None
        for q in hotspot_queries:
            if q['rank'] == rank:
                hotspot_query = q
                break

        if not hotspot_query:
            hotspot_query = {'title': title, 'rank': rank}

        # 提取搜索摘要
        search_summary = extract_search_snippet(result['data'])

        # 生成AI提示
        prompt = generate_ai_analysis_prompt(hotspot_query, search_summary)

        # 保存提示到文件
        prompt_file = os.path.join(prompts_dir, f'prompt_{rank:02d}.txt')
        try:
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(prompt)

            prompts_data.append({
                'rank': rank,
                'title': title,
                'prompt_file': prompt_file,
                'hotspot_data': hotspot_query,
                'search_summary': search_summary
            })

            print(f"  ✅ 已生成: {prompt_file}")

        except Exception as e:
            print(f"  ❌ 生成失败 prompt_{rank:02d}.txt: {e}")

    print(f"✅ 共生成 {len(prompts_data)} 个AI分析提示")

    # 保存索引文件
    index_file = 'analysis_prompts_index.json'
    try:
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(prompts_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 提示索引已保存: {index_file}")
    except Exception as e:
        print(f"❌ 保存索引失败: {e}")

    return prompts_data


def create_analysis_instructions(prompts_data):
    """创建分析操作说明"""
    instructions = f"""# AI分析操作说明

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 概述

本步骤使用Claude AI分析每个热搜话题，生成产品创意。

## 分析步骤

对于每个热搜话题，需要：

1. 读取提示文件（位于 analysis_prompts/ 目录）
2. 将提示内容发送给Claude AI
3. 收集AI返回的JSON格式分析结果
4. 保存结果到 `analysis_results/result_{{rank}}.json`

## 提示文件列表

总共需要分析: {len(prompts_data)} 个热搜话题

"""

    for prompt_info in prompts_data[:10]:  # 只显示前10个
        instructions += f"""
### #{prompt_info['rank']} - {prompt_info['title']}

- **提示文件**: `{prompt_info['prompt_file']}`
- **输出文件**: `analysis_results/result_{prompt_info['rank']:02d}.json`
- **执行方式**: 将提示文件内容发送给Claude AI
- **期望输出**: JSON格式分析结果

"""

    if len(prompts_data) > 10:
        instructions += f"\n... 还有 {len(prompts_data) - 10} 个话题待分析\n"

    instructions += """
## AI分析指导原则

### 评分标准

1. **有趣度（80分）**
   - 话题新颖性与创意性: 40%
   - 传播性与娱乐性: 30%
   - 用户体验独特性: 30%

2. **有用度（20分）**
   - 实用性: 50%
   - 问题解决能力: 50%

### 产品创意要求

- **总分≥60分**才会生成产品创意
- 产品名称: 简洁有吸引力
- 核心功能: 清晰明确
- 目标用户: 具体精准
- 产品描述: ≤50字

### 事件脉络总结

- 100字以内
- 概括事件核心
- 突出关键信息

## 期望输出格式

```json
{
  "fun_score": 70,
  "fun_reason": "话题新颖，传播性强...",
  "useful_score": 15,
  "useful_reason": "可解决用户实际问题...",
  "total_score": 85,
  "has_idea": true,
  "product": {
    "name": "产品名称",
    "features": "核心功能",
    "target_users": "目标用户",
    "description": "产品描述（50字以内）"
  },
  "summary": "关键事件脉络总结（100字以内）",
  "analysis_notes": "其他分析备注"
}
```

## 手动分析命令

如果手动执行，可以运行：

```bash
python manual_ai_analysis.py
```

## 下一步

所有AI分析完成后，执行：

```bash
python generate_html_report.py
```

生成最终HTML报告。
"""

    # 保存说明文件
    instructions_file = 'AI_ANALYSIS_INSTRUCTIONS.md'
    try:
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        print(f"✅ 分析说明已保存: {instructions_file}")
    except Exception as e:
        print(f"❌ 保存说明失败: {e}")

    return instructions_file


def main():
    """主函数"""
    print("=" * 60)
    print("AI分析 - 微博热点产品创意生成器")
    print("=" * 60)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 加载热搜查询
    print("【步骤1/3】加载热搜查询...")
    hotspot_queries = load_hotspot_queries()
    if not hotspot_queries:
        print("\n❌ 未找到热搜查询数据")
        print("请先运行: python fetch_weibo_hotspot.py")
        return 1

    # 加载搜索结果
    print("\n【步骤2/3】加载搜索结果...")
    search_results = load_search_results()
    if not search_results:
        print("\n❌ 未找到搜索结果数据")
        print("请先完成搜索步骤")
        return 1

    # 生成AI分析提示
    print("\n【步骤3/3】生成AI分析提示...")
    prompts_data = save_analysis_prompts(search_results, hotspot_queries)

    if not prompts_data:
        print("\n❌ 未能生成AI分析提示")
        return 1

    # 创建分析说明
    create_analysis_instructions(prompts_data)

    print("\n✅ AI分析准备工作完成！")
    print("📁 已创建 analysis_prompts/ 目录")
    print("📄 请查看 AI_ANALYSIS_INSTRUCTIONS.md 了解详细步骤")
    print("\n💡 下一步:")
    print("   方法1: 手动将每个提示文件发送给Claude AI")
    print("   方法2: 使用Claude Code批量分析")
    print("\n   收集所有AI分析结果后，运行:")
    print("   python generate_html_report.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
