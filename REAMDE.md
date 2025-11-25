# 微博热搜产品创意分析工具

自动抓取微博热搜，深度分析热点话题，并生成产品创意与HTML报告。

## 功能特点

✅ **自动获取** - 实时抓取微博热搜榜前15条热点
✅ **深度搜索** - 为每个热点搜索详细背景信息
✅ **AI分析** - 使用Claude AI从有趣度(80%)和有用度(20%)双维度评分
✅ **智能筛选** - 仅对总分≥60分的创意生成具体产品方案
✅ **精美报告** - 生成响应式HTML报告，可视化展示分析结果

## 评分标准

### 有趣度 (80分)
- 话题新颖性与创意性: 40%
- 传播性与娱乐性: 30%
- 用户体验独特性: 30%

### 有用度 (20分)
- 实用性: 50%
- 问题解决能力: 50%

## 安装与使用

### 方式一：使用Claude Code Skill (推荐)

1. 在Claude Code中执行：
```
/weibo_hotspot_analyzer
```

2. 按照提示依次执行搜索和分析步骤。

### 方式二：手动执行脚本

#### 步骤1: 获取微博热搜数据
```bash
python fetch_weibo_hotspot.py
```
输出文件: `weibo_search_queries.json`

#### 步骤2: 搜索热点详细信息
```bash
python search_hotspot_details.py
```
查看生成的 `search_plan.md` 和 `MANUAL_SEARCH.md`，手动执行搜索。

#### 步骤3: AI分析生成产品创意
```bash
python analyze_hotspot_with_ai.py
```
查看生成的 `AI_ANALYSIS_INSTRUCTIONS.md`，将提示发送给Claude AI进行分析。

#### 步骤4: 生成HTML报告
```bash
python generate_html_report.py
```
输出文件: `weibo_hotspot_analysis.html`

## 输出报告

HTML报告包含以下列：

1. **排名** - 微博热搜排名
2. **热点资讯** - 热搜话题标题
3. **关键事件脉络** - 100字内的事件总结
4. **产品创意** - 包括产品名称、核心功能、目标用户和描述
5. **综合评分** - 总分及有趣度、有用度分项得分

### 评分可视化
- 🟢 绿色 (80-100分): 优秀创意，强烈推荐
- 🟡 黄色 (60-79分): 良好创意，值得考虑
- 🔴 红色 (<60分): 一般，暂不推荐

## 文件说明

```
微博热搜分析/
├── .claude/
│   └── commands/
│       └── weibo_hotspot_analyzer.md      # Claude Code Skill文件
├── fetch_weibo_hotspot.py                  # 获取微博热搜
├── search_hotspot_details.py               # 生成搜索计划
├── analyze_hotspot_with_ai.py              # 生成AI分析提示
├── generate_html_report.py                 # 生成HTML报告
├── REAMDE.md                               # 本说明文件
└── weibo_hotspot_analysis.html             # 生成的报告(运行后)
```

## 技术栈

- Python 3
- requests - HTTP请求
- json - 数据处理
- Claude Code - AI分析和搜索

## License

MIT
