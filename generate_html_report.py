#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成微博热搜分析HTML报告
"""

import json
import os
import re
import sys
from datetime import datetime


def load_analysis_results():
    """加载所有AI分析结果"""
    print("正在加载AI分析结果...")

    results_dir = 'analysis_results'
    if not os.path.exists(results_dir):
        # 尝试从当前目录查找结果文件
        result_files = [f for f in os.listdir('.') if re.match(r'result_\d+\.json', f)]
    else:
        result_files = [os.path.join(results_dir, f) for f in os.listdir(results_dir)
                       if f.endswith('.json') and f.startswith('result_')]

    if not result_files:
        print("❌ 未找到AI分析结果文件")
        # 尝试加载样例数据用于测试
        return load_sample_data()

    print(f"找到 {len(result_files)} 个结果文件")

    results = []
    for result_file in sorted(result_files, key=lambda x: int(re.search(r'result_(\d+)', x).group(1))):
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 提取排名
            match = re.search(r'result_(\d+)', result_file)
            rank = int(match.group(1)) if match else 0

            # 确保所有必要字段存在
            result = {
                'rank': rank,
                'title': data.get('title', f'热点#{rank}'),
                'fun_score': data.get('fun_score', 0),
                'fun_reason': data.get('fun_reason', ''),
                'useful_score': data.get('useful_score', 0),
                'useful_reason': data.get('useful_reason', ''),
                'total_score': data.get('total_score', 0),
                'has_idea': data.get('has_idea', False),
                'product': data.get('product', None),
                'summary': data.get('summary', '暂无事件脉络'),
                'analysis_notes': data.get('analysis_notes', ''),
                'source_file': result_file
            }

            results.append(result)
            print(f"  ✅ 已加载: {os.path.basename(result_file)} (排名: #{rank})")

        except Exception as e:
            print(f"  ❌ 加载失败 {result_file}: {e}")

    # 按排名排序
    results.sort(key=lambda x: x['rank'])

    print(f"✅ 成功加载 {len(results)} 个分析结果")
    return results


def load_sample_data():
    """加载样例数据（用于测试）"""
    print("⚠️  未找到实际分析结果，加载样例数据用于测试")

    sample_data = [
        {
            "rank": 1,
            "title": "AI技术新突破",
            "fun_score": 70,
            "fun_reason": "AI技术新颖性强，具有极高的传播性和话题性，能引发用户好奇心",
            "useful_score": 18,
            "useful_reason": "可解决实际工作问题，提供智能辅助工具",
            "total_score": 88,
            "has_idea": True,
            "summary": "近期AI技术在自然语言处理和图像生成领域取得重大突破，引发广泛讨论和应用探索。",
            "product": {
                "name": "AI创意助手",
                "features": "智能写作、图像生成、创意建议",
                "target_users": "内容创作者、设计师、营销人员",
                "description": "基于最新AI技术，为创作者提供智能写作和创意生成工具"
            }
        },
        {
            "rank": 2,
            "title": "环保健康生活方式",
            "fun_score": 50,
            "fun_reason": "生活方式话题具有持续关注度，但新颖性一般",
            "useful_score": 20,
            "useful_reason": "直接关系到用户健康，实用价值高",
            "total_score": 70,
            "has_idea": True,
            "summary": "环保和健康生活方式受到越来越多人关注，市场潜力巨大。",
            "product": {
                "name": "绿色生活指南",
                "features": "环保产品推荐、健康生活建议、社区互动",
                "target_users": "注重健康的年轻人群",
                "description": "提供个性化的环保健康生活方式建议和社区交流平台"
            }
        },
        {
            "rank": 3,
            "title": "普通人日常新闻",
            "fun_score": 20,
            "fun_reason": "内容过于普通，缺乏新颖性和传播性",
            "useful_score": 10,
            "useful_reason": "实用价值有限，难以形成独特价值",
            "total_score": 30,
            "has_idea": False,
            "summary": "普通日常新闻，缺乏突出亮点。",
            "product": None
        }
    ]

    return sample_data


def generate_html_content():
    """生成HTML内容"""

    # HTML模板
    html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微博热搜产品创意分析 - {date}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            padding: 20px 0;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            border: 1px solid rgba(94, 234, 212, 0.1);
            padding: 40px 30px;
            margin-bottom: 30px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        }}

        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}

        .title {{
            font-size: 36px;
            background: linear-gradient(135deg, #60a5fa, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            font-weight: 800;
        }}

        .subtitle {{
            font-size: 18px;
            color: #94a3b8;
            margin-bottom: 30px;
        }}

        .legend {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            background: rgba(30, 41, 59, 0.7);
            padding: 8px 16px;
            border-radius: 20px;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }}

        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
        }}

        .table-container {{
            overflow-x: auto;
            border-radius: 12px;
            border: 1px solid rgba(148, 163, 184, 0.1);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}

        thead {{
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        th {{
            background: linear-gradient(135deg, #0ea5e9, #0284c7);
            color: white;
            padding: 16px 12px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
        }}

        th:nth-child(1) {{ width: 6%; }}
        th:nth-child(2) {{ width: 20%; }}
        th:nth-child(3) {{ width: 24%; }}
        th:nth-child(4) {{ width: 28%; }}
        th:nth-child(5) {{ width: 22%; }}

        td {{
            padding: 16px 12px;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            vertical-align: top;
            background: rgba(15, 23, 42, 0.5);
        }}

        tr:nth-child(even) td {{
            background: rgba(30, 41, 59, 0.4);
        }}

        tr:hover td {{
            background: rgba(56, 189, 248, 0.1);
            transition: all 0.3s ease;
        }}

        .rank {{
            font-size: 20px;
            font-weight: 800;
            color: #60a5fa;
            text-align: center;
        }}

        .hotspot-title {{
            font-weight: 600;
            margin-bottom: 8px;
            color: #f1f5f9;
            font-size: 15px;
            line-height: 1.4;
        }}

        .heatmap {{
            font-size: 12px;
            color: #f87171;
            margin-top: 6px;
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .event-summary {{
            color: #cbd5e1;
            line-height: 1.6;
            max-height: 80px;
            overflow: hidden;
            font-size: 14px;
        }}

        .product-idea {{
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(96, 165, 250, 0.1));
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid #38bdf8;
        }}

        .product-name {{
            font-weight: 700;
            color: #38bdf8;
            margin-bottom: 8px;
            font-size: 15px;
        }}

        .product-feature {{
            font-size: 13px;
            color: #cbd5e1;
            line-height: 1.4;
            margin-bottom: 4px;
        }}

        .product-feature strong {{
            color: #60a5fa;
        }}

        .product-desc {{
            font-size: 13px;
            color: #94a3b8;
            line-height: 1.4;
            margin-top: 8px;
            font-style: italic;
        }}

        .no-idea {{
            color: #94a3b8;
            font-style: italic;
            text-align: center;
            padding: 20px;
        }}

        .score-container {{
            text-align: center;
        }}

        .score-badge {{
            display: inline-block;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: 800;
            color: white;
            text-align: center;
            min-width: 80px;
            font-size: 18px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease;
        }}

        .score-badge:hover {{
            transform: translateY(-2px);
        }}

        .score-high {{
            background: linear-gradient(135deg, #10b981, #34d399);
        }}

        .score-medium {{
            background: linear-gradient(135deg, #f59e0b, #fbbf24);
        }}

        .score-low {{
            background: linear-gradient(135deg, #ef4444, #f87171);
        }}

        .score-details {{
            font-size: 12px;
            color: #94a3b8;
            margin-top: 10px;
            line-height: 1.4;
        }}

        .score-bar {{
            display: flex;
            gap: 4px;
            margin-top: 8px;
            justify-content: center;
        }}

        .score-bar-item {{
            height: 4px;
            border-radius: 2px;
            flex: 1;
        }}

        .fun-bar {{
            background: linear-gradient(90deg, #60a5fa, #38bdf8);
        }}

        .useful-bar {{
            background: linear-gradient(90deg, #34d399, #10b981);
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(96, 165, 250, 0.1));
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(148, 163, 184, 0.1);
            text-align: center;
        }}

        .stat-number {{
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(135deg, #60a5fa, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 5px;
        }}

        .stat-label {{
            font-size: 14px;
            color: #94a3b8;
        }}

        .methodology {{
            background: rgba(30, 41, 59, 0.5);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
            border: 1px solid rgba(148, 163, 184, 0.1);
        }}

        .methodology h3 {{
            color: #38bdf8;
            margin-bottom: 15px;
        }}

        .methodology ul {{
            list-style: none;
            padding: 0;
        }}

        .methodology li {{
            padding: 8px 0;
            color: #cbd5e1;
            position: relative;
            padding-left: 20px;
        }}

        .methodology li::before {{
            content: '✓';
            color: #34d399;
            font-weight: bold;
            position: absolute;
            left: 0;
        }}

        .methodology .score-weights {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 15px;
        }}

        .weight-item {{
            background: rgba(15, 23, 42, 0.5);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid rgba(148, 163, 184, 0.1);
        }}

        .weight-item strong {{
            color: #38bdf8;
        }}

        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid rgba(148, 163, 184, 0.1);
            color: #94a3b8;
            font-size: 14px;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 20px 15px;
                margin: 10px;
            }}

            .title {{
                font-size: 28px;
            }}

            .legend {{
                flex-direction: column;
                align-items: center;
            }}

            .methodology .score-weights {{
                grid-template-columns: 1fr;
            }}

            th, td {{
                padding: 12px 8px;
                font-size: 13px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">🔥 微博热搜产品创意分析报告</h1>
            <div class="subtitle">{date}</div>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{total_topics}</div>
                <div class="stat-label">分析话题数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{high_score_count}</div>
                <div class="stat-label">优秀创意 (≥80分)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{medium_score_count}</div>
                <div class="stat-label">良好创意 (60-79分)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{avg_score:.1f}</div>
                <div class="stat-label">平均分</div>
            </div>
        </div>

        <div class="methodology">
            <h3>📊 评分方法论</h3>
            <div class="score-weights">
                <div class="weight-item">
                    <strong>有趣度 (80分)</strong><br>
                    评估话题的新颖性、传播性和用户体验独特性
                </div>
                <div class="weight-item">
                    <strong>有用度 (20分)</strong><br>
                    评估产品的实用价值和问题解决能力
                </div>
            </div>
            <p style="margin-top: 15px; color: #94a3b8; font-size: 13px;">
                总分≥60分才会生成具体产品创意，确保创意的质量与可行性
            </p>
        </div>

        <div class="legend">
            <div class="legend-item">
                <div class="legend-color score-high"></div>
                <span>优秀 (80-100分)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color score-medium"></div>
                <span>良好 (60-79分)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color score-low"></div>
                <span>一般 (&lt;60分)</span>
            </div>
        </div>

        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>热点资讯</th>
                        <th>关键事件脉络</th>
                        <th>产品创意</th>
                        <th>综合评分</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>📈 本报告由微博热搜分析工具自动生成 | 评分标准：有趣度 80% + 有用度 20%</p>
            <p style="margin-top: 10px; font-size: 13px;">
                分析时间: {generation_time} | 数据来源于微博热搜榜
            </p>
        </div>
    </div>
</body>
</html>
'''

    return html_template


def get_score_badge_class(score):
    """根据分数获取评分徽章样式类"""
    if score >= 80:
        return 'score-high'
    elif score >= 60:
        return 'score-medium'
    else:
        return 'score-low'


def calculate_stats(results):
    """计算统计数据"""
    total_topics = len(results)
    high_score_count = sum(1 for r in results if r['total_score'] >= 80)
    medium_score_count = sum(1 for r in results if 60 <= r['total_score'] < 80)
    avg_score = sum(r['total_score'] for r in results) / total_topics if total_topics > 0 else 0

    return {
        'total_topics': total_topics,
        'high_score_count': high_score_count,
        'medium_score_count': medium_score_count,
        'avg_score': avg_score
    }


def generate_table_rows(results):
    """生成表格行"""
    rows = []

    for result in results:
        score_class = get_score_badge_class(result['total_score'])

        # 产品创意部分
        if result['has_idea'] and result['product']:
            product = result['product']
            product_html = f'''
                    <div class="product-idea">
                        <div class="product-name">{product.get('name', '未命名产品')}</div>
                        <div class="product-feature"><strong>功能:</strong> {product.get('features', 'N/A')}</div>
                        <div class="product-feature"><strong>用户:</strong> {product.get('target_users', 'N/A')}</div>
                        <div class="product-desc">{product.get('description', '暂无描述')}</div>
                    </div>
            '''
        else:
            product_html = '<div class="no-idea">暂无可行产品创意</div>'

        # 评分可视化
        fun_percent = (result['fun_score'] / 80) * 100
        useful_percent = (result['useful_score'] / 20) * 100

        row = f'''
                <tr>
                    <td><div class="rank">#{result['rank']}</div></td>
                    <td>
                        <div class="hotspot-title">{result['title']}</div>
                    </td>
                    <td>
                        <div class="event-summary">{result['summary']}</div>
                    </td>
                    <td>
                        {product_html}
                    </td>
                    <td>
                        <div class="score-container">
                            <div class="score-badge {score_class}">{result['total_score']}分</div>
                            <div class="score-details">
                                有趣: {result['fun_score']}分<br>
                                有用: {result['useful_score']}分
                            </div>
                            <div class="score-bar">
                                <div class="score-bar-item fun-bar" style="flex: {fun_percent}%"></div>
                                <div class="score-bar-item useful-bar" style="flex: {useful_percent}%"></div>
                            </div>
                        </div>
                    </td>
                </tr>
        '''
        rows.append(row)

    return ''.join(rows)


def save_html_report(html_content, filename='weibo_hotspot_analysis.html'):
    """保存HTML报告到文件"""
    try:
        # 备份旧文件
        backup_file = None
        if os.path.exists(filename):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f"{filename}.{timestamp}.backup"
            os.rename(filename, backup_file)
            print(f"📁 已备份旧文件: {backup_file}")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        backup_msg = f" (旧文件已备份)" if backup_file else ""
        print(f"✅ HTML报告已保存: {filename}{backup_msg}")
        return True
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False


def generate_json_report(results, filename='weibo_hotspot_analysis.json'):
    """生成JSON格式报告"""
    try:
        report_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_topics': len(results),
                'score_criteria': {
                    'fun_weight': 0.8,
                    'useful_weight': 0.2,
                    'min_score_for_idea': 60
                }
            },
            'results': results
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        print(f"✅ JSON报告已保存: {filename}")
        return True
    except Exception as e:
        print(f"❌ JSON报告保存失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("微博热搜分析报告生成器")
    print("=" * 60)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 加载AI分析结果
    print("【步骤1/3】加载AI分析结果...")
    results = load_analysis_results()
    if not results:
        print("\n❌ 未能加载分析结果")
        return 1

    # 计算统计数据
    print("\n【步骤2/3】计算统计数据...")
    stats = calculate_stats(results)
    print(f"  📊 话题总数: {stats['total_topics']}")
    print(f"  ⭐ 优秀创意: {stats['high_score_count']}")
    print(f"  👍 良好创意: {stats['medium_score_count']}")
    print(f"  📈 平均分数: {stats['avg_score']:.1f}")

    # 生成HTML内容
    print("\n【步骤3/3】生成HTML报告...")
    html_template = generate_html_content()
    table_rows = generate_table_rows(results)

    html_content = html_template.format(
        date=datetime.now().strftime('%Y年%m月%d日'),
        generation_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        table_rows=table_rows,
        **stats
    )

    # 保存HTML报告
    save_html_report(html_content)

    # 保存JSON报告
    generate_json_report(results)

    print("\n" + "=" * 60)
    print("✅ 报告生成完成！")
    print("\n📄 输出文件:")
    print("   - weibo_hotspot_analysis.html (HTML报告)")
    print("   - weibo_hotspot_analysis.json (JSON数据)")
    print("\n💡 下一步:")
    print("   在浏览器中打开 weibo_hotspot_analysis.html 查看完整报告")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
