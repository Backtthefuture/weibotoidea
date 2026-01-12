# AI分析操作说明

**生成时间**: 2026-01-12 08:03:37

## 概述

本步骤使用Claude AI分析每个热搜话题，生成产品创意。

## 分析步骤

对于每个热搜话题，需要：

1. 读取提示文件（位于 analysis_prompts/ 目录）
2. 将提示内容发送给Claude AI
3. 收集AI返回的JSON格式分析结果
4. 保存结果到 `analysis_results/result_{rank}.json`

## 提示文件列表

总共需要分析: 15 个热搜话题


### #1 - 特朗普表态让万千台湾民众看清现实

- **提示文件**: `analysis_prompts/prompt_01.txt`
- **输出文件**: `analysis_results/result_01.json`
- **执行方式**: 将提示文件内容发送给Claude AI
- **期望输出**: JSON格式分析结果


### #2 - 烟台暴雪下冒烟了

- **提示文件**: `analysis_prompts/prompt_02.txt`
- **输出文件**: `analysis_results/result_02.json`
- **执行方式**: 将提示文件内容发送给Claude AI
- **期望输出**: JSON格式分析结果


### #3 - 中国农民种地科技感拉满

- **提示文件**: `analysis_prompts/prompt_03.txt`
- **输出文件**: `analysis_results/result_03.json`
- **执行方式**: 将提示文件内容发送给Claude AI
- **期望输出**: JSON格式分析结果


### #4 - 蔡依林演唱会被举报

- **提示文件**: `analysis_prompts/prompt_04.txt`
- **输出文件**: `analysis_results/result_04.json`
- **执行方式**: 将提示文件内容发送给Claude AI
- **期望输出**: JSON格式分析结果


### #5 - 林昀儒男单冠军

- **提示文件**: `analysis_prompts/prompt_05.txt`
- **输出文件**: `analysis_results/result_05.json`
- **执行方式**: 将提示文件内容发送给Claude AI
- **期望输出**: JSON格式分析结果


### #6 - 手欠小狗每个人路过都要摸一下

- **提示文件**: `analysis_prompts/prompt_06.txt`
- **输出文件**: `analysis_results/result_06.json`
- **执行方式**: 将提示文件内容发送给Claude AI
- **期望输出**: JSON格式分析结果


### #7 - 伊朗哀悼3天

- **提示文件**: `analysis_prompts/prompt_07.txt`
- **输出文件**: `analysis_results/result_07.json`
- **执行方式**: 将提示文件内容发送给Claude AI
- **期望输出**: JSON格式分析结果


### #8 - 山东威海下了倾盆大瓢雪

- **提示文件**: `analysis_prompts/prompt_08.txt`
- **输出文件**: `analysis_results/result_08.json`
- **执行方式**: 将提示文件内容发送给Claude AI
- **期望输出**: JSON格式分析结果


### #9 - 国乒WTT多哈冠军赛无缘冠军

- **提示文件**: `analysis_prompts/prompt_09.txt`
- **输出文件**: `analysis_results/result_09.json`
- **执行方式**: 将提示文件内容发送给Claude AI
- **期望输出**: JSON格式分析结果


### #10 - 社保工作人员用漏洞挪用养老金超百万

- **提示文件**: `analysis_prompts/prompt_10.txt`
- **输出文件**: `analysis_results/result_10.json`
- **执行方式**: 将提示文件内容发送给Claude AI
- **期望输出**: JSON格式分析结果


... 还有 5 个话题待分析

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
