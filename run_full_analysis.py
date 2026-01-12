#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜产品创意分析 - 完整流程
每次执行都会重新获取数据、分析并生成报告
"""

import os
import sys
import json
import subprocess
from datetime import datetime

def run_command(command, description):
    """运行命令并显示进度"""
    print(f"\n{'=' * 60}")
    print(f"🔄 {description}")
    print('=' * 60)
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ 执行失败: {description}")
        return False
    return True

def main():
    print("=" * 60)
    print("微博热搜产品创意分析 - 完整流程")
    print("=" * 60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 确保在项目目录中
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📂 工作目录: {script_dir}")

    # 步骤1: 获取微博热搜数据
    if not run_command("python3 fetch_weibo_hotspot.py", "步骤1: 获取微博热搜数据"):
        return 1

    # 检查是否成功获取数据
    if not os.path.exists('weibo_search_queries.json'):
        print("❌ 未找到热搜数据文件，分析终止")
        return 1

    print("\n✅ 步骤1完成：热搜数据获取成功")

    # 步骤2: 使用AI分析热搜话题
    print("\n" + "=" * 60)
    print("🔄 步骤2: AI分析热搜话题并生成产品创意")
    print("=" * 60)
    print("\n正在使用AI分析15个热搜话题...")

    # 这里将通过Task工具进行分析
    print("\n⚠️  请使用 Claude Code 的 Task 工具执行热搜分析")
    print("   或者使用以下命令：")
    print("   python3 -c \"from analyze_hotspot_with_ai import main; main()\"")

    return 0

if __name__ == "__main__":
    sys.exit(main())
