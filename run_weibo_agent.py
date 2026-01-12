#!/usr/bin/env python3
"""
微博热搜分析 - 自动化 Agent 脚本
使用 Claude Agent SDK 自动执行完整的分析流程
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from claude_agent_sdk import query, ClaudeAgentOptions
except ImportError:
    print("错误：未安装 Claude Agent SDK")
    print("请运行：pip install claude-agent-sdk")
    sys.exit(1)


async def run_weibo_analysis():
    """
    执行完整的微博热搜分析 workflow
    """

    # 设置工作目录
    project_root = Path(__file__).parent
    os.chdir(project_root)

    print("=" * 60)
    print("微博热搜分析 - 自动化执行")
    print("=" * 60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"工作目录: {project_root}")
    print("=" * 60)
    print()

    # 定义完整的 workflow 步骤
    workflow_prompt = """
请按照以下步骤完成微博热搜分析：

1. **安装依赖**
   - 运行: pip install requests

2. **获取微博热点数据**
   - 运行: python3 fetch_weibo_hotspot.py
   - 这会生成 weibo_search_queries.json 文件

3. **搜索热点详情**
   - 读取 weibo_search_queries.json 文件
   - 对前 15 个条目（rank 1-15）进行网络搜索
   - 对每个条目：
     * 使用 WebSearch 工具搜索 search_query 或 title
     * 创建文件 search_results_{rank}.json（两位数字格式，如 01, 02）
     * JSON 格式: {"title": "标题", "content": "搜索结果摘要"}

4. **生成 AI 分析提示**
   - 运行: python3 analyze_hotspot_with_ai.py
   - 这会在 analysis_prompts/ 目录生成提示文件

5. **执行 AI 分析**
   - 创建 analysis_results 目录（如果不存在）
   - 列出 analysis_prompts/ 中的所有提示文件
   - 对每个 prompt_XX.txt 文件：
     * 读取提示内容
     * 你自己处理这个提示（生成分析结果）
     * 保存 JSON 响应到 analysis_results/result_{rank}.json

6. **合并结果**
   - 运行: python3 combine_results.py

7. **生成报告**
   - 运行: python3 generate_apple_style_report.py

完成后请报告：
- 成功生成的文件列表
- 任何错误或警告
- 最终报告的位置
"""

    # 从环境变量获取 API Token
    anthropic_token = os.environ.get('ANTHROPIC_AUTH_TOKEN')
    if not anthropic_token:
        print("❌ 错误: 未找到环境变量 ANTHROPIC_AUTH_TOKEN")
        print("请设置环境变量: export ANTHROPIC_AUTH_TOKEN='your_token'")
        return False

    # 配置 Agent 选项
    options = ClaudeAgentOptions(
        # 使用 PipeLLM 代理配置
        env={
            'ANTHROPIC_BASE_URL': os.environ.get('ANTHROPIC_BASE_URL', 'https://api.pipellm.com'),
            'ANTHROPIC_AUTH_TOKEN': anthropic_token
        },
        # 允许的工具
        allowed_tools=[
            "Read",       # 读取文件
            "Write",      # 写入文件
            "Bash",       # 运行终端命令
            "Glob",       # 文件模式匹配
            "Grep",       # 文本搜索
            "WebSearch",  # 网络搜索
            "WebFetch",   # 获取网页内容
            "Edit"        # 编辑文件
        ],
        # 自动接受文件编辑
        permission_mode="acceptEdits",
        # 设置工作目录
        cwd=str(project_root),
        # 最大执行轮次（防止无限循环）
        max_turns=100,
        # 使用默认模型
        model="sonnet"
    )

    # 运行 agent
    message_count = 0
    error_occurred = False

    try:
        print("正在执行 workflow...")
        print("-" * 60)
        print()

        async for message in query(
            prompt=workflow_prompt,
            options=options
        ):
            message_count += 1

            # 打印消息用于调试
            if hasattr(message, '__class__'):
                message_type = message.__class__.__name__

                # 只打印关键消息
                if message_type == 'AssistantMessage':
                    for block in message.content:
                        if hasattr(block, 'text') and block.text:
                            # 打印 Claude 的文本消息（限制长度）
                            text = block.text.strip()
                            if text:
                                print(f"[Claude] {text[:300]}")
                                if len(text) > 300:
                                    print("         ...")
                        elif hasattr(block, 'name'):
                            # 打印工具调用
                            print(f"[工具] 正在使用: {block.name}")

                elif message_type == 'ToolResultMessage':
                    # 打印工具结果（简化）
                    for block in message.content:
                        if hasattr(block, 'tool_name'):
                            print(f"[完成] {block.tool_name}")

                elif message_type == 'ResultMessage':
                    print()
                    print("=" * 60)
                    print("执行完成！")
                    print("=" * 60)
                    print(f"执行轮数: {message.num_turns}")
                    print(f"总耗时: {message.duration_ms / 1000:.2f} 秒")
                    if hasattr(message, 'total_cost_usd') and message.total_cost_usd:
                        print(f"API 成本: ${message.total_cost_usd:.4f}")

                    if message.is_error:
                        error_occurred = True
                        print(f"状态: 错误")
                        print(f"错误信息: {message.result}")
                    else:
                        print(f"状态: 成功")
                    print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n[中止] 用户中断执行")
        return False
    except Exception as e:
        print(f"\n\n[错误] Agent 执行失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        error_occurred = True
        return False

    print()
    print(f"处理消息数: {message_count}")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return not error_occurred


async def main():
    """主程序入口"""
    try:
        success = await run_weibo_analysis()
        if success:
            print("\n✅ 微博热搜分析完成！")
            sys.exit(0)
        else:
            print("\n❌ 分析过程中出现错误")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 致命错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
