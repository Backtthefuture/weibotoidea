#!/usr/bin/env python3
"""
快速测试 - 验证 Claude Agent SDK 是否正常工作
"""

import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def test_agent():
    print("开始测试 Claude Agent SDK...")
    print("-" * 50)

    # 简单的测试提示
    test_prompt = """
    请执行以下简单测试：
    1. 读取当前目录的文件列表
    2. 告诉我你找到了哪些 Python 文件
    3. 完成后回复 "测试成功"
    """

    options = ClaudeAgentOptions(
        env={
            'ANTHROPIC_BASE_URL': 'https://api.pipellm.com',
            'ANTHROPIC_AUTH_TOKEN': 'pipe-8ac85d7a0ee8bfd072e224c416c54878d5c1a5a5e47984868e68a813fab0cf1d'
        },
        allowed_tools=["Read", "Bash", "Glob"],
        permission_mode="acceptEdits",
        cwd="/Users/superhuang/Documents/微博热搜分析",
        max_turns=10,
        model="sonnet"
    )

    try:
        async for message in query(prompt=test_prompt, options=options):
            if hasattr(message, '__class__'):
                message_type = message.__class__.__name__

                if message_type == 'AssistantMessage':
                    for block in message.content:
                        if hasattr(block, 'text') and block.text:
                            print(f"[Claude] {block.text}")

                elif message_type == 'ResultMessage':
                    print("\n" + "=" * 50)
                    print("✅ 测试完成!")
                    print(f"执行轮数: {message.num_turns}")
                    print(f"总耗时: {message.duration_ms / 1000:.2f} 秒")
                    print("=" * 50)
                    return True

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_agent())
    exit(0 if result else 1)
