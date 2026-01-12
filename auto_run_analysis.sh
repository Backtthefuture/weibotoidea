#!/bin/bash
#
# 微博热搜自动分析脚本
# 用于配合 launchd 或 cron 实现定时自动运行
#

# 设置工作目录
cd "$(dirname "$0")" || exit 1
WORK_DIR=$(pwd)

# 创建日志目录
LOG_DIR="${WORK_DIR}/logs"
mkdir -p "$LOG_DIR"

# 日志文件
DATE_STR=$(date +%Y%m%d)
TIME_STR=$(date +%H%M%S)
LOG_FILE="${LOG_DIR}/analysis_${DATE_STR}_${TIME_STR}.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "开始执行微博热搜分析"
log "工作目录: $WORK_DIR"
log "=========================================="

# 检查 claude 命令是否存在
if ! command -v claude &> /dev/null; then
    # 尝试常见安装路径
    if [ -f "/usr/local/bin/claude" ]; then
        CLAUDE_CMD="/usr/local/bin/claude"
    elif [ -f "$HOME/.local/bin/claude" ]; then
        CLAUDE_CMD="$HOME/.local/bin/claude"
    elif [ -f "$HOME/.npm-global/bin/claude" ]; then
        CLAUDE_CMD="$HOME/.npm-global/bin/claude"
    else
        log "错误: 找不到 claude 命令"
        exit 1
    fi
else
    CLAUDE_CMD="claude"
fi

log "使用 Claude: $CLAUDE_CMD"

# 执行分析任务
# 注意：-p 参数表示 headless 模式，非交互式运行
$CLAUDE_CMD -p "请执行微博热搜分析任务：

1. 首先获取最新的微博热搜数据（使用天行数据API）
2. 对前15条热搜进行详细搜索和分析
3. 为每个热搜评分并生成产品创意
4. 对高分话题（>=80分）进行深度分析
5. 生成增强版HTML报告

请确保完成所有步骤并保存结果文件。" \
    --allowedTools "Read,Write,Bash,WebFetch,WebSearch,Grep,Glob" \
    --max-turns 50 \
    2>&1 | tee -a "$LOG_FILE"

EXIT_CODE=${PIPESTATUS[0]}

log "=========================================="
if [ $EXIT_CODE -eq 0 ]; then
    log "分析任务完成"
else
    log "分析任务失败，退出码: $EXIT_CODE"
fi
log "日志保存于: $LOG_FILE"
log "=========================================="

# 清理7天前的日志
find "$LOG_DIR" -name "analysis_*.log" -mtime +7 -delete 2>/dev/null

exit $EXIT_CODE
