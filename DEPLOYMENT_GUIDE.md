# 🚀 微博热搜分析 - 云端部署配置指南

本指南将帮助你将微博热搜分析项目部署到 GitHub Actions，实现定时自动运行并在 GitHub Pages 上查看报告。

---

## 📋 目录

1. [前置准备](#前置准备)
2. [配置 GitHub Secrets](#配置-github-secrets)
3. [启用 GitHub Pages](#启用-github-pages)
4. [配置定时任务](#配置定时任务)
5. [手动触发测试](#手动触发测试)
6. [查看分析报告](#查看分析报告)
7. [常见问题](#常见问题)

---

## 🎯 前置准备

### 1. 获取必要的 API Keys

你需要准备以下 API Key：

#### a) 天行数据 API Key（必需）
- 访问：[https://www.tianapi.com/](https://www.tianapi.com/)
- 注册账号并申请「微博热搜」API
- 复制你的 API Key（格式类似：`c96a7333c975965e491ff49466a1844b`）

#### b) Anthropic Claude API Token（必需）
- 如果使用 PipeLLM 代理：访问 [https://pipellm.com](https://pipellm.com)
- 如果使用官方 API：访问 [https://console.anthropic.com/](https://console.anthropic.com/)
- 获取你的 API Token

#### c) Anthropic Base URL（可选）
- 如果使用 PipeLLM：`https://api.pipellm.com`
- 如果使用官方 API：`https://api.anthropic.com`（或留空使用默认值）

### 2. 推送代码到 GitHub

确保你的项目已经推送到 GitHub 仓库：

```bash
# 如果还没有 Git 仓库，先初始化
git init
git add .
git commit -m "feat: 配置云端自动化部署"

# 关联远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/your-username/weibo-hotspot-analyzer.git

# 推送到 GitHub
git push -u origin main
```

---

## 🔐 配置 GitHub Secrets

GitHub Secrets 用于安全地存储敏感信息（API Keys），只有 GitHub Actions 运行时可以访问。

### 步骤：

1. **进入仓库设置**
   - 打开你的 GitHub 仓库
   - 点击 **Settings**（设置）

2. **进入 Secrets 配置**
   - 左侧菜单找到 **Secrets and variables** → **Actions**

3. **添加以下 Secrets**

   点击 **New repository secret** 按钮，依次添加：

   | Secret 名称 | 说明 | 示例值 |
   |------------|------|--------|
   | `TIANXING_API_KEY` | 天行数据 API Key | `c96a7333c975965e491ff49466a1844b` |
   | `ANTHROPIC_AUTH_TOKEN` | Claude API Token | `pipe-8ac85d7a0ee8bfd072e224...` |
   | `ANTHROPIC_BASE_URL` | Claude API Base URL（可选） | `https://api.pipellm.com` |

   > **注意**：
   > - Secret 名称必须完全匹配（区分大小写）
   > - 添加后无法查看内容，但可以更新
   > - `ANTHROPIC_BASE_URL` 如果不使用代理可以不添加

4. **验证配置**

   添加完成后，你应该看到 3 个 Secrets：

   ```
   ✅ TIANXING_API_KEY
   ✅ ANTHROPIC_AUTH_TOKEN
   ✅ ANTHROPIC_BASE_URL
   ```

---

## 🌐 启用 GitHub Pages

GitHub Pages 用于托管生成的 HTML 报告，让你可以在线查看分析结果。

### 步骤：

1. **进入 Pages 设置**
   - 仓库页面 → **Settings** → **Pages**

2. **配置 Source**
   - **Source**: 选择 `Deploy from a branch`
   - **Branch**: 选择 `gh-pages` 分支
   - **Folder**: 选择 `/ (root)`

3. **保存设置**
   - 点击 **Save**

4. **等待部署**
   - 首次配置后，GitHub 会自动创建 `gh-pages` 分支
   - 等待几分钟后，你的网站将在以下地址可用：
     ```
     https://your-username.github.io/your-repo-name/
     ```

5. **（可选）配置自定义域名**
   - 如果有自己的域名，可以在 **Custom domain** 中配置
   - 参考 [GitHub 官方文档](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

---

## ⏰ 配置定时任务

项目已经配置好定时任务，默认每天运行 2 次：

- **北京时间 09:00**（UTC 01:00）
- **北京时间 21:00**（UTC 13:00）

### 修改定时时间

如果需要修改运行时间，编辑 `.github/workflows/daily-analysis.yml` 文件：

```yaml
schedule:
  - cron: '0 1 * * *'   # 北京时间 09:00
  - cron: '0 13 * * *'  # 北京时间 21:00
```

**Cron 格式说明**：
```
* * * * *
│ │ │ │ │
│ │ │ │ └─ 星期几 (0-6, 0=Sunday)
│ │ │ └─── 月份 (1-12)
│ │ └───── 日期 (1-31)
│ └─────── 小时 (0-23, UTC 时区)
└───────── 分钟 (0-59)
```

**时区转换**：
- UTC 时间 = 北京时间 - 8 小时
- 例如：北京时间 10:00 = UTC 02:00

**常用示例**：
```yaml
# 每天北京时间 8:00
- cron: '0 0 * * *'

# 每天北京时间 12:00 和 18:00
- cron: '0 4 * * *'
- cron: '0 10 * * *'

# 每 6 小时运行一次
- cron: '0 */6 * * *'
```

> ⚠️ **重要提醒**：
> - GitHub Actions 定时任务**不保证准时执行**，可能延迟几分钟到十几分钟
> - 建议最小间隔 5 分钟以上
> - 如果任务运行时间较长，避免设置过于频繁的定时任务

---

## 🧪 手动触发测试

在首次配置后，建议手动触发一次测试，确保配置正确。

### 步骤：

1. **进入 Actions 页面**
   - 仓库主页 → 点击顶部 **Actions** 标签

2. **选择 Workflow**
   - 左侧找到 **微博热搜每日分析** workflow

3. **手动运行**
   - 点击右侧 **Run workflow** 按钮
   - 选择分支（通常是 `main`）
   - 点击绿色的 **Run workflow** 按钮

4. **查看运行状态**
   - 页面会显示正在运行的任务
   - 点击任务可以查看详细日志
   - 等待任务完成（通常需要 3-5 分钟）

5. **检查结果**
   - ✅ 如果显示绿色勾号，说明运行成功
   - ❌ 如果显示红色 X，点击查看错误日志

### 常见运行错误：

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `未找到环境变量 TIANXING_API_KEY` | 未配置 Secret | 检查 Secrets 配置 |
| `401 Unauthorized` | API Key 无效 | 更新 Secret 中的 API Key |
| `404 Not Found` | API 地址错误 | 检查 `ANTHROPIC_BASE_URL` |
| `未找到 HTML 报告文件` | 脚本未生成报告 | 查看完整日志，检查脚本错误 |

---

## 📊 查看分析报告

任务成功运行后，可以通过以下方式查看报告：

### 1. 在线查看（推荐）

访问你的 GitHub Pages 网站：

```
https://your-username.github.io/your-repo-name/
```

**示例**：
- 用户名：`superhuang`
- 仓库名：`weibo-hotspot-analyzer`
- 网址：`https://superhuang.github.io/weibo-hotspot-analyzer/`

### 2. 查看历史报告

所有历史报告都保存在 `gh-pages` 分支的 `archive/` 目录：

```
https://your-username.github.io/your-repo-name/archive/
```

点击日期文件名查看历史报告：
- `2026-01-12.html` - 2026年1月12日的报告
- `2026-01-11.html` - 2026年1月11日的报告

### 3. 下载报告

1. 进入 Actions 页面
2. 点击最近的运行记录
3. 在 **Artifacts** 部分可以下载生成的文件

---

## ❓ 常见问题

### Q1: 定时任务没有按时运行？

**A**: GitHub Actions 的 cron 任务不保证准时执行，可能延迟几分钟到十几分钟。这是正常现象，GitHub 会在资源允许时尽快执行。

**解决方案**：
- 如果需要精确时间，考虑使用其他云服务（Google Cloud Scheduler, AWS EventBridge）
- 对于热搜分析，延迟几分钟通常不影响使用

---

### Q2: 如何查看运行日志？

**A**:
1. 进入仓库的 **Actions** 页面
2. 点击任意运行记录
3. 展开各个步骤查看详细日志
4. 红色表示失败，绿色表示成功

---

### Q3: 如何停止定时任务？

**A**: 有两种方式：

**方式 1：禁用 Workflow**
1. Actions 页面 → 选择 workflow
2. 点击右上角的 **...** → **Disable workflow**

**方式 2：删除或注释定时配置**
编辑 `.github/workflows/daily-analysis.yml`，删除或注释 `schedule` 部分：

```yaml
# schedule:
#   - cron: '0 1 * * *'
#   - cron: '0 13 * * *'
```

---

### Q4: 如何更新 API Key？

**A**:
1. 进入 **Settings** → **Secrets and variables** → **Actions**
2. 找到需要更新的 Secret（如 `TIANXING_API_KEY`）
3. 点击 Secret 名称 → **Update secret**
4. 输入新的值并保存

---

### Q5: GitHub Actions 免费额度够用吗？

**A**: 对于个人项目完全够用！

**免费额度**：
- 公开仓库：✅ **完全免费，无限使用**
- 私有仓库：每月 2,000 分钟

**实际使用**：
- 每次运行约 3-5 分钟
- 每天运行 2 次 = 10 分钟/天
- 每月约 300 分钟

> 💡 **建议**：将仓库设为公开，享受无限免费额度

---

### Q6: 报告页面显示 404？

**A**: 可能的原因：

1. **GitHub Pages 未启用**
   - 检查 Settings → Pages 是否正确配置

2. **gh-pages 分支不存在**
   - 至少运行一次 workflow 后才会创建
   - 手动触发一次测试

3. **URL 地址错误**
   - 检查用户名和仓库名是否正确
   - 格式：`https://username.github.io/repo-name/`

4. **等待部署完成**
   - GitHub Pages 部署可能需要几分钟
   - 查看 Actions 页面确认部署状态

---

### Q7: 如何在本地测试？

**A**:

```bash
# 1. 设置环境变量（替换为你的实际 API Key）
export TIANXING_API_KEY='your_tianxing_api_key'
export ANTHROPIC_AUTH_TOKEN='your_anthropic_token'
export ANTHROPIC_BASE_URL='https://api.pipellm.com'

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行脚本
python3 run_weibo_agent.py

# 4. 查看生成的 HTML 文件
open 微博热搜产品创意分析报告.html
```

---

### Q8: 如何监控任务失败？

**A**:

**方式 1：GitHub 通知**
- Settings → Notifications → Actions
- 启用「发送失败通知」

**方式 2：邮件通知**
- GitHub 会自动发送 workflow 失败邮件到你的注册邮箱

**方式 3：查看 Actions 页面**
- 定期检查 Actions 页面的运行状态
- 红色 X 表示失败

---

## 🎉 完成！

恭喜！你已经成功配置了微博热搜分析的云端自动化部署。

### 接下来：

- ⏰ **自动运行**：系统会每天自动分析微博热搜
- 📊 **查看报告**：访问你的 GitHub Pages 网址查看最新报告
- 📈 **历史记录**：所有历史报告都保存在 `archive/` 目录
- 🔄 **持续更新**：无需任何操作，报告会自动更新

### 需要帮助？

- 📖 查看 [GitHub Actions 官方文档](https://docs.github.com/actions)
- 📖 查看 [GitHub Pages 官方文档](https://docs.github.com/pages)
- 💬 在仓库 Issues 中提问
- 📧 联系项目维护者

---

**祝使用愉快！** 🚀
