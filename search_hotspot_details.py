#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索微博热点详细信息
"""

import json
import sys
from datetime import datetime
import subprocess

def load_queries(filename='weibo_search_queries.json'):
    """加载搜索查询"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            queries = json.load(f)
        print(f"✅ 成功加载 {len(queries)} 条搜索查询")
        return queries
    except Exception as e:
        print(f"❌ 加载失败: {e}")
        return []

def generate_search_commands(queries):
    """为每个查询生成搜索命令"""
    commands = []

    for query in queries:
        search_query = query['search_query']
        rank = query['rank']
        title = query['title']

        # 生成claude代码搜索命令
        cmd = f"# 搜索: {title}\n"
        cmd += f"# 排名: #{rank}\n"
        cmd += f"/WebSearch {search_query}\n"

        commands.append({
            'rank': rank,
            'title': title,
            'search_query': search_query,
            'command': cmd
        })

    return commands

def save_search_plan(commands, filename='search_plan.md'):
    """保存搜索计划"""
    content = f"""# 微博热点搜索计划

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 搜索清单

以下是每个热搜话题的搜索查询。请依次使用 Claude Code 的 WebSearch 工具执行搜索。

"""

    for cmd in commands:
        content += f"""
### #{cmd['rank']} - {cmd['title']}

**搜索关键词**: `{cmd['search_query']}`

**执行命令**:
```
/WebSearch {cmd['search_query']}
```

**说明**: 搜索后请保存返回的搜索结果，用于后续AI分析。

---

"""

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 搜索计划已保存到: {filename}")
        return True
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False

def display_plan_summary(commands):
    """显示计划摘要"""
    print(f"\n{'='*60}")
    print("搜索计划摘要")
    print(f"{'='*60}\n")

    for i, cmd in enumerate(commands[:10], 1):  # 只显示前10条
        print(f"#{cmd['rank']:2d} | {cmd['title']}")
        print(f"     🔍 搜索: {cmd['search_query'][:60]}...")

    if len(commands) > 10:
        print(f"\n... 还有 {len(commands) - 10} 条待搜索")

    print(f"\n{'='*60}")
    print(f"总计: {len(commands)} 个搜索任务")
    print(f"{'='*60}\n")

def create_manual_search_instructions(commands, filename='MANUAL_SEARCH.md'):
    """创建手动搜索说明"""
    content = f"""# 手动搜索说明

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 概述

本文件包含微博热搜的搜索任务清单。请按照以下步骤进行搜索：

## 搜索步骤

1. 打开 Claude Code
2. 对于每个热搜话题，执行 WebSearch
3. 将搜索结果保存到文件 `search_results_{{rank}}.json`
4. 所有搜索完成后，运行 AI 分析脚本

## 热搜列表

"""

    for cmd in commands:
        content += f"""
### #{cmd['rank']} - {cmd['title']}

- **搜索关键词**: {cmd['search_query']}
- **输出文件**: `search_results_{cmd['rank']:02d}.json`
- **执行命令**:
  ```
  /WebSearch {cmd['search_query']}
  ```
- **保存结果**: 将返回的JSON数据保存到文件

"""

    content += """
## 下一步

所有搜索结果收集完成后，执行：

```bash
python generate_html_report.py
```

"""

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 手动搜索说明已保存到: {filename}")
        return True
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("微博热点搜索计划生成器")
    print("=" * 60)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 加载查询
    queries = load_queries()
    if not queries:
        print("\n❌ 未能加载搜索查询")
        print("请先运行: python fetch_weibo_hotspot.py")
        return 1

    # 生成搜索命令
    commands = generate_search_commands(queries)

    # 显示摘要
    display_plan_summary(commands)

    # 保存搜索计划
    save_search_plan(commands)

    # 创建手动搜索说明
    create_manual_search_instructions(commands)

    print("\n✅ 搜索计划生成完成！")
    print("📑 请查看以下文件:")
    print("   - search_plan.md (搜索计划)")
    print("   - MANUAL_SEARCH.md (手动操作说明)")
    print("\n💡 下一步:")
    print("   方法1: 使用 Claude Code 依次执行 /WebSearch 命令")
    print("   方法2: 手动搜索并保存结果，然后运行分析脚本")

    return 0

if __name__ == "__main__":
    sys.exit(main())
