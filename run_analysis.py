#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜产品创意分析 - 完整自动化脚本
"""

import sys
import subprocess
import time
from datetime import datetime


def print_banner():
    """打印程序横幅"""
    print("\n" + "=" * 70)
    print(" " * 15 + "🔥 微博热搜产品创意分析工具 🔥")
    print(" " * 10 + "AI-Powered Weibo Hotspot Analysis Tool")
    print("=" * 70)
    print(f"\n执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 70)


def print_step(step_num, total, title):
    """打印步骤信息"""
    print(f"\n【步骤 {step_num}/{total}】{title}")
    print("-" * 70)


def run_script(script_name, description):
    """运行Python脚本"""
    print(f"\n📦 正在运行: {description}")
    print(f"   脚本: {script_name}\n")

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        # 打印输出
        if result.stdout:
            print(result.stdout)

        # 如果有错误
        if result.stderr:
            print(f"⚠️  警告/错误信息:")
            print(result.stderr)

        # 检查返回码
        if result.returncode == 0:
            print(f"✅ {description} - 成功")
            return True
        else:
            print(f"❌ {description} - 失败 (返回码: {result.returncode})")
            return False

    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False


def main():
    """主函数 - 执行完整分析流程"""
    print_banner()

    total_steps = 4

    # 步骤1: 获取微博热搜
    print_step(1, total_steps, "获取微博热搜数据")
    success = run_script('fetch_weibo_hotspot.py', '获取微博热搜')
    if not success:
        print("\n❌ 第一步失败，请检查网络连接或API可用性")
        return 1

    # 暂停一下，让用户查看结果
    time.sleep(2)

    # 步骤2: 生成搜索计划
    print_step(2, total_steps, "生成搜索计划")
    success = run_script('search_hotspot_details.py', '生成搜索计划')
    if not success:
        print("\n❌ 第二步失败")
        return 1

    # 步骤3: AI分析
    print_step(3, total_steps, "AI分析准备")
    success = run_script('analyze_hotspot_with_ai.py', '生成AI分析提示')
    if not success:
        print("\n❌ 第三步失败")
        return 1

    # 步骤4: 生成报告
    print_step(4, total_steps, "生成HTML报告")
    success = run_script('generate_html_report.py', '生成HTML报告')
    if not success:
        print("\n❌ 第四步失败")
        return 1

    # 完成
    print("\n" + "=" * 70)
    print(" 🎉 全部步骤执行完成！")
    print("=" * 70)
    print("\n📄 输出文件:")
    print("   ✓ weibo_hotspot_analysis.html (主报告)")
    print("   ✓ weibo_hotspot_analysis.json (数据文件)")
    print("   ✓ weibo_search_queries.json (热搜数据)")
    print("\n📁 辅助文件:")
    print("   ✓ search_plan.md (搜索计划)")
    print("   ✓ MANUAL_SEARCH.md (手动搜索说明)")
    print("   ✓ AI_ANALYSIS_INSTRUCTIONS.md (AI分析说明)")
    print("   ✓ analysis_prompts/ (AI提示文件目录)")
    print("\n💡 下一步操作:")
    print("   1. 在浏览器中打开 weibo_hotspot_analysis.html")
    print("   2. 查看分析结果和产品创意")
    print("   3. 分数≥80的建议重点关注")
    print("\n" + "=" * 70 + "\n")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断执行")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ 程序异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
