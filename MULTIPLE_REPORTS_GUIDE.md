# 多报告生成指南 - 支持同一天多次生成

## 📋 更新内容

### ✅ 核心改进

1. **时间戳命名规则**
   - 旧版：`weibo_hotspot_analysis_enhanced_20251203.html`
   - 新版：`weibo_hotspot_analysis_enhanced_20251203_1845.html`
   - 格式：`YYYYMMDD_HHMM` (年月日_时分)

2. **每次都重新获取数据**
   - 重新调用微博热搜API获取最新数据
   - 重新进行AI分析
   - 重新生成报告

3. **支持同一天多次生成**
   - 不再覆盖之前的报告
   - 每个文件都有唯一的时间戳
   - 可以保留历史版本的完整记录

## 🚀 使用方法

### 完整流程（一键运行）

```bash
# 第一步：重新获取热搜数据
python3 fetch_weibo_hotspot.py

# 第二步：AI分析（使用Task工具）
# 需要在Claude Code中执行Task命令分析热搜话题

# 第三步：生成带时间戳的HTML报告
python3 generate_enhanced_report.py
```

### 自动化脚本

```bash
# 使用自动化增强版脚本
python3 auto_run_enhanced.py
```

## 📁 文件命名示例

```
output/
├── weibo_hotspot_analysis_enhanced_20251203_1837.html  # 第一次生成 (18:37)
├── weibo_hotspot_analysis_enhanced_20251203_1845.html  # 第二次生成 (18:45)
├── weibo_hotspot_analysis_enhanced_20251203_1852.html  # 第三次生成 (18:52)
└── weibo_hotspot_analysis_enhanced_20251204_0900.html  # 第二天生成 (09:00)
```

## 📊 报告特性

### 增强版报告 (enhanced)
- ✅ 高分话题（≥80分）展示3个深度产品创意
- ✅ 每个创意包含不同维度和独特价值
- ✅ 深度分析话题有特殊标识和样式
- ✅ 统计数据包含"深度分析话题"卡片

### 基础版报告 (apple)
- ✅ 每个话题1个产品创意
- ✅ 简洁的苹果设计风格
- ✅ 基础统计信息

## 🔧 修改的文件

1. **generate_enhanced_report.py**
   - 修改文件名生成规则：添加时间戳
   - 优化数据加载逻辑：支持Task工具生成的JSON格式

2. **generate_apple_style_report.py**
   - 修改文件名生成规则：添加时间戳

3. **新增脚本**
   - `auto_run_enhanced.py`: 自动化分析流程
   - `run_full_analysis.py`: 完整流程脚本

## 💡 最佳实践

1. **建议工作流**
   ```
   每日开始 → fetch_weibo_hotspot.py → Task工具分析 → generate_enhanced_report.py
   ```

2. **查看历史报告**
   - 所有报告都在 `output/` 目录
   - 按文件名中的时间戳排序
   - 可以方便地比较不同时间的分析结果

3. **数据文件**
   - `weibo_search_queries.json`: 热搜原始数据
   - `enhanced_analysis_results.json`: AI分析结果
   - HTML报告: 可视化展示结果

## 📝 注意事项

- ⚠️ 每次运行前确保网络连接正常（需要获取最新热搜数据）
- ⚠️ AI分析需要使用Task工具手动触发
- ⚠️ 文件名时间戳为生成时间，不代表数据获取时间
- ⚠️ 同一天内的多次生成会在output目录保留所有版本

## 🎯 适用场景

- 每日定期生成报告
- 需要对比不同时段的热搜趋势
- 保留历史分析记录的完整版本
- 团队协作时可以基于不同版本进行讨论

---

更新日期：2025年12月3日
版本：v2.0 - 支持多报告生成
