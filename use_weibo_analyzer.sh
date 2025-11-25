#!/bin/bash
# 微博热搜分析工具快捷脚本

echo "🚀 启动微博热搜产品创意分析工具..."
echo ""
echo "请选择运行模式："
echo "1) Claude Code Skill (自动模式)"
echo "2) 一键运行完整流程"
echo "3) 仅获取微博热搜数据"
echo "4) 生成搜索计划"
echo "5) 生成AI分析提示"
echo "6) 生成HTML报告"
echo "q) 退出"
echo ""
read -p "请输入选项 [1-6,q]: " choice

case $choice in
    1)
        echo ""
        echo "📦 请复制以下命令到 Claude Code："
        echo "   /weibo_hotspot_analyzer"
        echo ""
        ;;
    2)
        echo ""
        python run_analysis.py
        ;;
    3)
        echo ""
        python fetch_weibo_hotspot.py
        ;;
    4)
        echo ""
        python search_hotspot_details.py
        ;;
    5)
        echo ""
        python analyze_hotspot_with_ai.py
        ;;
    6)
        echo ""
        python generate_html_report.py
        ;;
    q|Q)
        echo "👋 再见！"
        exit 0
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac
