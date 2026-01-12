#!/bin/bash
# 微博热搜分析 - 定时任务启动脚本
# 用于 cron 定时调用

set -e

# ========== 配置区域 ==========
PROJECT_DIR="/Users/superhuang/Documents/微博热搜分析"
LOG_DIR="$PROJECT_DIR/logs"
PYTHON_BIN="/opt/anaconda3/bin/python3"  # 使用 Anaconda Python（已安装 Agent SDK）

# ========== 主程序 ==========

# 创建日志目录
mkdir -p "$LOG_DIR"

# 生成日志文件名（带时间戳）
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
LOG_FILE="$LOG_DIR/weibo_analysis_$TIMESTAMP.log"

# 记录开始
echo "========================================" >> "$LOG_FILE"
echo "微博热搜分析 - 定时执行" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "工作目录: $PROJECT_DIR" >> "$LOG_FILE"
echo "Python: $PYTHON_BIN" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 切换到项目目录
cd "$PROJECT_DIR"

# 运行 Agent 脚本，输出重定向到日志文件
$PYTHON_BIN run_weibo_agent.py >> "$LOG_FILE" 2>&1

# 记录退出状态
EXIT_CODE=$?

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
if [ $EXIT_CODE -eq 0 ]; then
    echo "执行结果: ✅ 成功" >> "$LOG_FILE"

    # 可选：发送 macOS 通知
    osascript -e 'display notification "微博热搜分析已完成" with title "任务成功" sound name "Glass"' 2>/dev/null || true
else
    echo "执行结果: ❌ 失败 (退出码: $EXIT_CODE)" >> "$LOG_FILE"

    # 可选：发送错误通知
    osascript -e 'display notification "微博热搜分析执行失败，请查看日志" with title "任务失败" sound name "Basso"' 2>/dev/null || true
fi
echo "结束时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# 清理旧日志（保留最近 30 天）
find "$LOG_DIR" -name "weibo_analysis_*.log" -type f -mtime +30 -delete 2>/dev/null || true

# 输出到标准输出（cron 会发送邮件）
echo "微博热搜分析完成 - $(date '+%Y-%m-%d %H:%M:%S')"
echo "日志: $LOG_FILE"

exit $EXIT_CODE
