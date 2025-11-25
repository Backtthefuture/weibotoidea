# 微博热搜分析 - 快速启动指南

生成时间: 2025-11-25 16:39:18

## 最简单的方式（单终端，串行执行）

如果你不想使用复杂的双终端模式，可以用这个最简单的方式：

```bash
# 1. 获取微博热搜数据（已完成）
python fetch_weibo_hotspot.py

# 2. 开始分析（在Claude Code中运行）
# 直接告诉我："请帮我分析微博热搜，生成产品创意"
```

我（Claude Code）会自动完成：
- 读取微博热搜数据
- 逐个搜索热点详情
- 逐个AI分析并生成产品创意
- 生成HTML报告

**总耗时**: 约 4-5 分钟

---

## 最快的方式（双终端，流水线并行）

使用两个终端实现40%提速：

### 终端 1：搜索执行器

```bash
cd /Users/superhuang/Documents/微博热搜分析
claude

# 在Claude Code中告诉我：
# "请按顺序对微博热搜进行WebSearch搜索"
```

### 终端 2：分析执行器

```bash
cd /Users/superhuang/Documents/微博热搜分析
claude

# 等待第一个搜索结果出现后告诉我：
# "请对搜索结果进行AI分析，生成产品创意"
```

**总耗时**: 约 2-3 分钟（比串行快40%）

---

## 使用 /weibo_hotspot_analyzer 命令

在Claude Code中直接运行命令：

```
/weibo_hotspot_analyzer
```

我会自动执行完整流程，使用推荐的最佳方式。

---

## 当前热搜 TOP 5

```
#1: Mate80价格 (🔥 118.6万)
#2: 麒麟9030 (🔥 45.5万)
#3: 流感高发季防护指南来了 (🔥 45.3万)
#4: 枭起青壤直播 (🔥 44.7万)
#5: iG Uzi (🔥 44.4万)
```

**提示**: 15个热搜话题将分析，只显示评分≥60的产品创意。

---

## 输出文件

分析完成后会生成：

- 📄 `weibo_hotspot_analysis.html` - 可视化报告（建议用浏览器打开）
- 📊 `weibo_hotspot_analysis.json` - 原始数据
- 📋 `weibo_search_queries.json` - 热搜数据

---

## 需要帮助？

1. 查看详细指南：`cat PIPELINE_EXECUTION_GUIDE.md`
2. 查看Skill文档：`cat .claude/commands/weibo_hotspot_analyzer.md`
3. 直接问我任何问题！

🚀 现在想开始吗？告诉我你想用哪种方式！
