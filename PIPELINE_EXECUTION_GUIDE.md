# Weibo Hotspot Automation - Pipeline Execution Guide

Generated: 2025-11-25 16:39:18

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

