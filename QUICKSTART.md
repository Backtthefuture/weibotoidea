# 微博热搜分析工具 - 快速开始指南

## 🚀 快速启动

### 方式一：Claude Code Skill (推荐)

在Claude Code中直接执行：
```
/weibo_hotspot_analyzer
```

### 方式二：一键运行完整流程

```bash
python run_analysis.py
```

### 方式三：分步执行

#### 步骤1: 获取热搜数据
```bash
python fetch_weibo_hotspot.py
```

#### 步骤2: 生成搜索计划
```bash
python search_hotspot_details.py
```
手动执行搜索任务，保存结果到 `search_results_XX.json`。

#### 步骤3: AI分析
```bash
python analyze_hotspot_with_ai.py
```
将生成的提示发送给Claude AI分析，保存结果到 `analysis_results/result_XX.json`。

#### 步骤4: 生成报告
```bash
python generate_html_report.py
```

## 📊 评分标准

### 有趣度 (80分权重)
- 话题新颖性
- 传播性与娱乐性
- 用户体验独特性

### 有用度 (20分权重)
- 实用性
- 问题解决能力

**总分≥60分才会生成具体产品创意**

## 📁 输出文件

### 主要输出
- `weibo_hotspot_analysis.html` - HTML格式分析报告
- `weibo_hotspot_analysis.json` - JSON格式数据

### 中间文件
- `weibo_search_queries.json` - 热搜数据
- `search_plan.md` - 搜索计划
- `MANUAL_SEARCH.md` - 手动搜索说明
- `AI_ANALYSIS_INSTRUCTIONS.md` - AI分析说明
- `analysis_prompts/` - AI提示文件目录

## 🎯 案例演示

当前已成功获取2025年11月25日的微博热搜数据，并生成了样例报告。

在浏览器中打开 `weibo_hotspot_analysis.html` 即可查看示例报告。

## 🔧 技术栈

- Python 3.7+
- requests
- Claude Code (AI分析)
- 纯HTML/CSS (报告生成)

## 📈 使用场景

1. **产品经理**: 寻找产品创意和灵感
2. **创业者**: 发现市场机会
3. **投资人**: 了解热点趋势
4. **营销人员**: 制定营销策略

## ⚠️ 注意事项

1. 微博API可能因反爬机制而失效，需要定期更新请求头
2. AI分析需要手动完成搜索和分析步骤
3. 建议每天运行一次，跟踪热点变化

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 License

MIT
