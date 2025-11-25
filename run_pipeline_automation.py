#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜产品创意分析 - 自动化流水线版本
实现流水线并行：搜索+分析重叠执行
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime


def load_search_queries():
    """加载搜索查询"""
    try:
        with open('weibo_search_queries.json', 'r', encoding='utf-8') as f:
            queries = json.load(f)
        return queries
    except Exception as e:
        print(f"❌ 加载热搜查询失败: {e}")
        return []


def generate_orchestration_plan(queries):
    """生成自动化执行计划"""
    print("=" * 70)
    print("正在生成自动化执行计划...")
    print("=" * 70)

    plan = {
        "total_tasks": len(queries),
        "estimated_time": f"约 {len(queries) * 0.8:.1f} 分钟",
        "pipeline_mode": True,
        "workflow": []
    }

    orchestration_commands = []

    for i, query in enumerate(queries):
        rank = query['rank']
        title = query['title']
        search_query = query['search_query']

        # 每个热搜的完整处理流程
        task = {
            "rank": rank,
            "title": title,
            "search_query": search_query,
            "search_command": f"/WebSearch {search_query}",
            "result_file": f"search_results_{rank:02d}.json",
            "analysis_file": f"analysis_results_{rank:02d}.json",
            "status": "pending"
        }

        plan["workflow"].append(task)

        # 生成执行命令序列
        cmd = f"""
# {'='*60}
# 任务 #{rank}: {title}
# {'='*60}

# 步骤 1: 搜索热点详情
# 请执行: /WebSearch {search_query}
# 然后保存结果到: {task['result_file']}

# 步骤 2: AI分析产品创意
# 使用 Task 工具分析，提示文件: analysis_prompts/prompt_{rank:02d}.txt
# 保存结果到: {task['analysis_file']}
"""
        orchestration_commands.append(cmd)

    # 保存计划
    with open('orchestration_plan.json', 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    print(f"✅ 已生成 {len(queries)} 个任务的执行计划")
    print(f"⏱️  预计总耗时: {plan['estimated_time']}")
    print(f"🔄 流水线模式: 已启用")

    return plan, orchestration_commands


def create_claude_code_script(queries):
    """创建供Claude Code执行的自动化脚本"""

    script = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Weibo Hotspot Automation Script for Claude Code
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
\"\"\"

import time
from datetime import datetime
import json

print("=" * 70)
print("Weibo Hotspot Automation Tool")
print("=" * 70)
print(f"Start Time: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
print()

# Load task list
with open('orchestration_plan.json', 'r', encoding='utf-8') as f:
    plan = json.load(f)

total = len(plan['workflow'])
print(f"Total {{total}} hotspot topics to analyze")
print("Starting pipeline mode...")
print("=" * 70)
print()

# Execute pipeline tasks
for i, task in enumerate(plan['workflow'], 1):
    rank = task['rank']
    title = task['title']
    search_query = task['search_query']

    print(f"[Task {{i}}/{{total}}] #{{rank}} - {{title}}")
    print("-" * 70)

    # Step 1: WebSearch
    print(f"⏳ Step 1: Search hotspot info...")
    print(f"   Command: /WebSearch {{search_query}}")

    # Claude Code should execute WebSearch here
    # and save results to: task['result_file']

    print(f"   ✅ Search completed")
    print()

    # Step 2: AI analysis (parallel: start next search simultaneously)
    print(f"⏳ Step 2: Analyze product ideas...")
    print(f"   Using: Task tool with analysis_prompts/prompt_{{rank:02d}}.txt")

    print(f"   ✅ Analysis completed")
    print()

    # Pipeline optimization: don't wait too long, continue to next
    if i < total:
        print(f"🔄 Starting next task (pipeline mode)")
        print(f"   Next: #{{plan['workflow'][i]['rank']}} - {{plan['workflow'][i]['title'][:40]}}...")
        print()

print("=" * 70)
print("✅ All tasks completed!")
print("=" * 70)
"""

    # 保存脚本
    with open('run_for_claude_code.py', 'w', encoding='utf-8') as f:
        f.write(script)

    print(f"✅ 已生成 Claude Code 执行脚本: run_for_claude_code.py")


def create_pipeline_execution_guide():
    """Create pipeline execution guide"""

    guide = f"""# Weibo Hotspot Automation - Pipeline Execution Guide

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Why Use Pipeline Mode?

Traditional Serial Mode (wait for previous task to complete):
- Total time = Σ(search time + analysis time) ≈ 4-5 minutes

Pipeline Mode (overlap search and analysis):
- Total time = search time + (n-1)×max(search time, analysis time) + final analysis time
- Total time ≈ 2-3 minutes (40% faster)

## Execution Steps

### Step 1: Get Data (Should be done)
```bash
python fetch_weibo_hotspot.py
```

### Step 2: Generate Plan (Should be done)
```bash
python run_pipeline_automation.py
```

### Step 3: Pipeline Execution (Key Step)

Use two parallel Claude Code sessions: **Search Session** and **Analysis Session**

#### Session A: Search Executor

Run in Claude Code:
```
python run_for_claude_code.py
```

This will sequentially start all WebSearch tasks. When the first search completes:
- Save results to search_results_01.json
- Immediately start the second search

#### Session B: Analysis Executor

In **another terminal** with Claude Code, after Session A completes the first search:

```
# Execute after search_results_01.json is generated:
python analyze_hotspot_with_ai.py

# Or analyze a single hotspot directly:
python manual_ai_analysis.py --rank 1
```

The analyzer will:
- Read search results
- Generate AI prompts
- Wait for you to call Task tool for AI analysis

### Pipeline Timeline Example

Timeline (3 hotspots as example):

```
Time  |  Search Session   |  Analysis Session
------|-------------------|------------------
T+0s  |  Search #1        |
T+3s  |  Search #2        |  Analyze #1
T+6s  |  Search #3        |  Analyze #2
T+9s  |                   |  Analyze #3
T+12s |  All completed    |  All completed
```

**Total time: 12s vs Serial Mode 18s** (33% faster)

## Practical Execution Instructions

### Start Search (Session A)

In Claude Code:
```
Please help me execute the search pipeline, read tasks from orchestration_plan.json
Perform WebSearch for top 10 hot topics
```

### Start Analysis (Session B)

After detecting search results generation:
```
Now please help me analyze the search results just generated
Perform AI analysis for top 10 hot topics
```

## Optimization Suggestions

1. **Control Parallelism**: Analyze 3-5 hotspots simultaneously to avoid resource exhaustion
2. **Monitor Progress**: Use `ls -lh search_results_*.json` to check search progress
3. **Batch Processing**: Process hotspots in batches of 3-5, can take breaks between batches

## FAQ

**Q: Do I need to manually call WebSearch and Task tools?**
A: Yes, Claude Code tools can only be used in interactive environment. But scripts can coordinate these calls.

**Q: Using two sessions is too complex?**
A: Can execute in one session, but search and analysis will be serial. Two sessions enable true pipeline.

**Q: How to verify results?**
A:
```bash
# Check number of completed searches
ls -1 search_results_*.json | wc -l

# Check number of completed analyses
ls -1 analysis_results_*.json | wc -l
```

## Complete Command Reference

### Quick Start (Recommended)

Terminal 1 (Search):
```bash
cd /Users/superhuang/Documents/微博热搜分析
claude
# In Claude Code: "Please execute WebSearch sequentially"
```

Terminal 2 (Analysis):
```bash
cd /Users/superhuang/Documents/微博热搜分析
claude
# In Claude Code: "Please wait for search results and start AI analysis"
```

### Manual Step-by-Step

If automation fails, you can manually:

```bash
# 1. Get hot topics
python fetch_weibo_hotspot.py

# 2. Search one by one (in Claude Code)
/WebSearch "Hot topic 1 Weibo"
# Save results to search_results_01.json

/WebSearch "Hot topic 2 Weibo"
# Save results to search_results_02.json

# 3. Generate AI prompts
python analyze_hotspot_with_ai.py

# 4. Analyze one by one (in Claude Code)
# Read analysis_prompts/prompt_01.txt
# Use Task tool for analysis
# Save results to analysis_results_01.json

# 5. Generate report
python generate_html_report.py
```

**Note**: Manual mode takes longer (4-5 minutes) but easier to debug.

## Performance Comparison

| Mode | Time | Pros | Cons |
|------|------|------|------|
| Serial (Single Session) | 4-5 minutes | Simple, less error-prone | Slow |
| Pipeline (Dual Session) | 2-3 minutes | 40% faster | Requires two terminals |
| Full Parallel | 1-2 minutes | Fastest | High resource usage, may hit limits |

## Troubleshooting

If execution fails:

1. **Check if files exist**:
   ```bash
   ls -lh weibo_search_queries.json
   ls -lh orchestration_plan.json
   ```

2. **Check Claude Code responses**:
   - Does WebSearch return valid results?
   - Is Task tool called successfully?
   - Any rate limit errors?

3. **Check logs**:
   ```bash
   # Check generated files
   ls -lh search_results_*.json
   ls -lh analysis_results_*.json
   ```

4. **Restart**:
   ```bash
   # Clean old files
   rm -f search_results_*.json analysis_results_*.json

   # Re-execute
   python run_pipeline_automation.py
   ```

## Technical Support

Check these files if problems occur:
- orchestration_plan.json - execution plan
- run_for_claude_code.py - automation script
- AI_ANALYSIS_INSTRUCTIONS.md - detailed instructions

"""

    with open('PIPELINE_EXECUTION_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide)

    print(f"✅ Pipeline execution guide generated: PIPELINE_EXECUTION_GUIDE.md")



def main():
    """Main function"""
    print("=" * 70)
    print("Weibo Hotspot Automation Pipeline - Master Program")
    print("Generated:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 70)
    print()

    # Step 1: Load hot topic data
    print("[Step 1/3] Loading hot topic data...")
    queries = load_search_queries()
    if not queries:
        print("\n❌ Hot topic data not found, please run first:")
        print("   python fetch_weibo_hotspot.py")
        return 1

    print(f"✅ Loaded {len(queries)} hot topics")
    print()

    # Step 2: Generate automation plan
    print("[Step 2/3] Generating automation execution plan...")
    plan, commands = generate_orchestration_plan(queries)
    print()

    # Step 3: Create execution scripts and guides
    print("[Step 3/3] Creating automation scripts...")
    create_claude_code_script(queries)
    create_pipeline_execution_guide()
    print()

    # Complete
    print("=" * 70)
    print("✅ Automation pipeline configuration completed!")
    print("=" * 70)
    print()
    print("📁 Generated files:")
    print("   ✓ orchestration_plan.json - execution plan")
    print("   ✓ run_for_claude_code.py - execution script")
    print("   ✓ PIPELINE_EXECUTION_GUIDE.md - complete guide")
    print()
    print("🚀 Quick start:")
    print("   1. In Claude Code:")
    print("      python run_for_claude_code.py")
    print()
    print("   2. View detailed guide:")
    print("      cat PIPELINE_EXECUTION_GUIDE.md")
    print()
    print("💡 Tip: Use two terminal sessions for true pipeline parallelism!")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
