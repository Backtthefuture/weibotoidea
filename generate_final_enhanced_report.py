#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成微博热搜分析增强版HTML报告 - 包含深度分析
"""

import json
import os
from datetime import datetime


def load_data():
    """加载分析数据"""
    with open('hotspot_analysis_results.json', 'r', encoding='utf-8') as f:
        base_results = json.load(f)
    
    with open('deep_dive_analysis.json', 'r', encoding='utf-8') as f:
        deep_results = json.load(f)
    
    return base_results, deep_results


def get_score_badge_class(score):
    """根据分数获取评分徽章样式类"""
    if score >= 80:
        return 'score-excellent'
    elif score >= 60:
        return 'score-good'
    else:
        return 'score-fair'


def calculate_stats(results):
    """计算统计数据"""
    total_topics = len(results)
    high_score_count = sum(1 for r in results if r['total_score'] >= 80)
    deep_dive_count = high_score_count
    qualified_count = sum(1 for r in results if r['has_idea'])
    avg_score = sum(r['total_score'] for r in results) / total_topics if total_topics > 0 else 0

    return {
        'total_topics': total_topics,
        'high_score_count': high_score_count,
        'deep_dive_count': deep_dive_count,
        'qualified_count': qualified_count,
        'avg_score': avg_score
    }


def generate_table_rows(results, deep_results):
    """生成表格行"""
    rows = []
    deep_dive_map = {item['topic']['title']: item for item in deep_results}

    for result in results:
        score_class = get_score_badge_class(result['total_score'])
        title = result['title']
        
        is_deep_dive = title in deep_dive_map
        
        # 产品创意部分
        if result['has_idea'] and result['product']:
            product = result['product']
            
            # 基础创意
            basic_idea_html = f'''
                <div class="product-idea basic-idea">
                    <div class="product-name">{product.get('name', '未命名产品')}</div>
                    <div class="product-info">
                        <div class="product-feature">
                            <span class="label">核心功能</span>
                            <span class="value">{product.get('features', 'N/A')}</span>
                        </div>
                        <div class="product-feature">
                            <span class="label">目标用户</span>
                            <span class="value">{product.get('target_users', 'N/A')}</span>
                        </div>
                    </div>
                    <div class="product-description">{product.get('description', '暂无描述')}</div>
                </div>
            '''
            
            # 深度分析创意
            deep_ideas_html = ''
            if is_deep_dive:
                deep_data = deep_dive_map[title]
                deep_ideas_html = '''
                    <div class="deep-dive-section">
                        <div class="deep-dive-header">
                            <span class="deep-dive-icon">💎</span>
                            <span class="deep-dive-title">深度分析 - 3个维度产品创意</span>
                        </div>
                '''
                
                for dim in deep_data['dimensions']:
                    deep_ideas_html += f'''
                        <div class="deep-idea">
                            <div class="deep-dimension">{dim['dimension']}</div>
                            <div class="deep-function">{dim['core_function']}</div>
                            <div class="deep-users">
                                <span class="label">目标用户</span>
                                <span class="value">{dim['target_users']}</span>
                            </div>
                            <div class="deep-value">
                                <span class="label">独特价值</span>
                                <span class="value">{dim['unique_value']}</span>
                            </div>
                        </div>
                    '''
                
                deep_ideas_html += '</div>'
            
            product_html = basic_idea_html + deep_ideas_html
            
        else:
            reason = result.get('reason', '总分未达60分阈值')
            product_html = f'<div class="no-idea"><span class="no-idea-icon">—</span><span class="no-idea-text">暂无可行产品创意</span><span class="no-idea-reason">{reason}</span></div>'

        # 生成表格行
        deep_badge_html = '<span class="deep-badge">深度分析</span>' if is_deep_dive else ''
        
        row = f'''
            <tr data-score="{result['total_score']}">
                <td class="rank-cell">
                    <span class="rank">#{result['rank']}</span>
                    {deep_badge_html}
                </td>
                <td class="hotspot-cell">
                    <div class="hotspot-title">{result['title']}</div>
                    <div class="heat-info">热度 {result.get('heat', 'N/A'):,}</div>
                </td>
                <td class="summary-cell">
                    <div class="event-summary">{result['summary']}</div>
                </td>
                <td class="product-cell">
                    {product_html}
                </td>
                <td class="score-cell">
                    <div class="score-container">
                        <div class="score-badge {score_class}">
                            <span class="score-number">{result['total_score']}</span>
                            <span class="score-label">分</span>
                        </div>
                        <div class="score-breakdown">
                            <div class="score-item">
                                <span class="score-item-label">有趣</span>
                                <span class="score-item-value">{result['fun_score']}</span>
                            </div>
                            <div class="score-item">
                                <span class="score-item-label">有用</span>
                                <span class="score-item-value">{result['useful_score']}</span>
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
        '''
        rows.append(row)

    return ''.join(rows)


def generate_html_report(results, deep_results, stats):
    """生成增强版HTML报告"""
    
    table_rows = generate_table_rows(results, deep_results)

    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微博热搜产品创意分析 - 增强版 - {datetime.now().strftime('%Y年%m月%d日')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', 'PingFang SC', 'Hiragino Sans GB', sans-serif;
            background: #f5f5f7;
            color: #1d1d1f;
            padding: 60px 20px;
            line-height: 1.47059;
            font-size: 17px;
            font-weight: 400;
            letter-spacing: -0.022em;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        .container {{ max-width: 1600px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 60px; }}
        .title {{ font-size: 56px; font-weight: 700; letter-spacing: -0.005em; color: #1d1d1f; margin-bottom: 8px; line-height: 1.07143; }}
        .subtitle {{ font-size: 21px; font-weight: 400; color: #6e6e73; letter-spacing: 0.011em; line-height: 1.381; }}
        .version-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #ff6b6b, #ff8787);
            color: white;
            padding: 6px 20px;
            border-radius: 980px;
            font-size: 15px;
            font-weight: 600;
            margin-top: 12px;
        }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 48px; }}
        .stat-card {{
            background: #ffffff;
            border-radius: 18px;
            padding: 32px 28px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        .stat-card:hover {{ transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12); }}
        .stat-number {{ font-size: 48px; font-weight: 700; color: #0071e3; line-height: 1.0; margin-bottom: 8px; }}
        .stat-label {{ font-size: 17px; color: #6e6e73; font-weight: 400; }}
        .stat-highlight {{ font-size: 52px; background: linear-gradient(135deg, #ff6b6b, #ff8787); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .methodology {{
            background: #ffffff;
            border-radius: 18px;
            padding: 40px;
            margin-bottom: 32px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        }}
        .methodology h3 {{ font-size: 28px; font-weight: 700; color: #1d1d1f; margin-bottom: 24px; letter-spacing: -0.003em; }}
        .score-weights {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }}
        .weight-item {{ background: #f5f5f7; padding: 24px; border-radius: 12px; }}
        .weight-item strong {{ display: block; font-size: 19px; font-weight: 600; color: #1d1d1f; margin-bottom: 8px; }}
        .weight-description {{ font-size: 15px; color: #6e6e73; line-height: 1.4; }}
        .threshold-note {{ margin-top: 24px; padding: 20px; background: #f5f5f7; border-radius: 12px; font-size: 15px; color: #6e6e73; line-height: 1.4; }}
        .table-wrapper {{ background: #ffffff; border-radius: 18px; overflow: hidden; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08); }}
        .table-header {{ padding: 24px 32px; border-bottom: 1px solid #d2d2d7; display: flex; justify-content: space-between; align-items: center; }}
        .table-title {{ font-size: 24px; font-weight: 600; color: #1d1d1f; }}
        .sort-button {{
            background: #0071e3;
            color: #ffffff;
            border: none;
            border-radius: 980px;
            padding: 8px 20px;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .sort-button:hover {{ background: #0077ed; transform: scale(1.02); }}
        .sort-button:active {{ transform: scale(0.98); }}
        .sort-icon {{ display: inline-block; transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); }}
        .sort-button.desc .sort-icon {{ transform: rotate(180deg); }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{
            background: #f5f5f7;
            padding: 16px 20px;
            text-align: left;
            font-size: 13px;
            font-weight: 600;
            color: #6e6e73;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            border-bottom: 1px solid #d2d2d7;
        }}
        td {{ padding: 24px 20px; border-bottom: 1px solid #d2d2d7; vertical-align: top; }}
        tr:last-child td {{ border-bottom: none; }}
        tr {{ transition: background-color 0.2s ease; }}
        tr:hover {{ background-color: #fbfbfd; }}
        .rank-cell {{ width: 80px; text-align: center; position: relative; }}
        .rank {{ font-size: 20px; font-weight: 700; color: #0071e3; }}
        .deep-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #ff6b6b, #ff8787);
            color: white;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 10px;
            font-weight: 600;
            margin-top: 4px;
        }}
        .hotspot-cell {{ width: 20%; }}
        .hotspot-title {{ font-size: 17px; font-weight: 600; color: #1d1d1f; margin-bottom: 6px; line-height: 1.35; }}
        .heat-info {{ font-size: 13px; color: #ff3b30; font-weight: 500; }}
        .summary-cell {{ width: 24%; }}
        .event-summary {{ font-size: 15px; color: #6e6e73; line-height: 1.5; }}
        .product-cell {{ width: 36%; }}
        .product-idea {{
            background: linear-gradient(135deg, #f5f5f7 0%, #ffffff 100%);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #d2d2d7;
            margin-bottom: 12px;
        }}
        .basic-idea {{ border-left: 4px solid #0071e3; }}
        .product-name {{ font-size: 17px; font-weight: 600; color: #0071e3; margin-bottom: 12px; }}
        .product-info {{ margin-bottom: 12px; }}
        .product-feature {{ display: flex; gap: 12px; margin-bottom: 8px; font-size: 14px; }}
        .product-feature .label {{ color: #6e6e73; font-weight: 500; min-width: 60px; }}
        .product-feature .value {{ color: #1d1d1f; flex: 1; }}
        .product-description {{
            font-size: 14px;
            color: #6e6e73;
            font-style: italic;
            line-height: 1.4;
            padding-top: 12px;
            border-top: 1px solid #d2d2d7;
        }}
        .deep-dive-section {{
            background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
            border-radius: 12px;
            padding: 20px;
            border: 2px solid #ff6b6b;
            margin-top: 12px;
        }}
        .deep-dive-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid #ff8787;
        }}
        .deep-dive-icon {{ font-size: 20px; }}
        .deep-dive-title {{ font-size: 16px; font-weight: 700; color: #ff6b6b; }}
        .deep-idea {{
            background: white;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            border: 1px solid #ffd0d0;
        }}
        .deep-idea:last-child {{ margin-bottom: 0; }}
        .deep-dimension {{
            font-size: 14px;
            font-weight: 700;
            color: #ff6b6b;
            margin-bottom: 8px;
        }}
        .deep-function {{
            font-size: 15px;
            color: #1d1d1f;
            margin-bottom: 12px;
            line-height: 1.4;
        }}
        .deep-users, .deep-value {{
            display: flex;
            gap: 12px;
            margin-bottom: 8px;
            font-size: 13px;
        }}
        .deep-users .label, .deep-value .label {{ color: #6e6e73; font-weight: 500; min-width: 60px; }}
        .deep-users .value, .deep-value .value {{ color: #1d1d1f; flex: 1; }}
        .no-idea {{ text-align: center; padding: 24px; color: #86868b; display: flex; flex-direction: column; align-items: center; gap: 8px; }}
        .no-idea-icon {{ font-size: 32px; opacity: 0.3; }}
        .no-idea-text {{ font-size: 15px; font-weight: 500; }}
        .no-idea-reason {{ font-size: 13px; opacity: 0.7; }}
        .score-cell {{ width: 140px; text-align: center; }}
        .score-container {{ display: flex; flex-direction: column; align-items: center; gap: 12px; }}
        .score-badge {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease;
        }}
        .score-badge:hover {{ transform: scale(1.05); }}
        .score-excellent {{ background: linear-gradient(135deg, #34c759, #30d158); color: #ffffff; }}
        .score-good {{ background: linear-gradient(135deg, #ff9500, #ffb340); color: #ffffff; }}
        .score-fair {{ background: linear-gradient(135deg, #d2d2d7, #e5e5ea); color: #6e6e73; }}
        .score-number {{ font-size: 28px; line-height: 1; }}
        .score-label {{ font-size: 12px; opacity: 0.8; margin-top: 2px; }}
        .score-breakdown {{ display: flex; gap: 12px; font-size: 12px; }}
        .score-item {{ display: flex; flex-direction: column; gap: 2px; }}
        .score-item-label {{ color: #86868b; font-weight: 500; }}
        .score-item-value {{ color: #1d1d1f; font-weight: 600; }}
        .footer {{ text-align: center; margin-top: 60px; padding-top: 40px; border-top: 1px solid #d2d2d7; }}
        .footer-text {{ font-size: 15px; color: #86868b; line-height: 1.6; }}
        @media (max-width: 1024px) {{
            .title {{ font-size: 40px; }}
            .stats {{ grid-template-columns: repeat(2, 1fr); }}
            .score-weights {{ grid-template-columns: 1fr; }}
        }}
        @media (max-width: 768px) {{
            body {{ padding: 40px 16px; }}
            .title {{ font-size: 32px; }}
            .subtitle {{ font-size: 17px; }}
            .stats {{ grid-template-columns: 1fr; }}
            .methodology {{ padding: 24px; }}
            .table-header {{ flex-direction: column; gap: 16px; align-items: flex-start; }}
            th, td {{ padding: 12px; font-size: 14px; }}
            .hotspot-title {{ font-size: 15px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">微博热搜产品创意分析</h1>
            <p class="subtitle">{datetime.now().strftime('%Y年%m月%d日')}</p>
            <div class="version-badge">🔥 增强版 - 深度分析</div>
        </header>
        <div class="stats">
            <div class="stat-card"><div class="stat-number">{stats['total_topics']}</div><div class="stat-label">分析话题数</div></div>
            <div class="stat-card"><div class="stat-number">{stats['qualified_count']}</div><div class="stat-label">生成创意话题</div></div>
            <div class="stat-card"><div class="stat-highlight">{stats['high_score_count']}</div><div class="stat-label">深度分析话题 (≥80分)</div></div>
            <div class="stat-card"><div class="stat-number">{stats['deep_dive_count'] * 3}</div><div class="stat-label">深度分析维度</div></div>
            <div class="stat-card"><div class="stat-number">{stats['avg_score']:.1f}</div><div class="stat-label">平均评分</div></div>
        </div>
        <div class="methodology">
            <h3>评分方法论</h3>
            <div class="score-weights">
                <div class="weight-item"><strong>有趣度 (80分)</strong><div class="weight-description">评估话题的新颖性、传播性和用户体验独特性</div></div>
                <div class="weight-item"><strong>有用度 (20分)</strong><div class="weight-description">评估产品的实用价值和问题解决能力</div></div>
            </div>
            <div class="threshold-note">
                <strong>深度分析机制：</strong>总分≥80分的话题将进行深度分析，从3个不同维度（日常生活、商务办公、教育娱乐）挖掘产品创意潜力，每个维度包含核心功能、目标用户和独特价值说明。
            </div>
        </div>
        <div class="table-wrapper">
            <div class="table-header">
                <div class="table-title">热搜分析详情</div>
                <button class="sort-button" id="sortButton"><span>按评分排序</span><span class="sort-icon">↓</span></button>
            </div>
            <table id="hotspotTable">
                <thead><tr><th>排名</th><th>热点资讯</th><th>关键事件脉络</th><th>产品创意</th><th>综合评分</th></tr></thead>
                <tbody>{table_rows}</tbody>
            </table>
        </div>
        <footer class="footer">
            <p class="footer-text">本报告由微博热搜分析工具自动生成 - 增强版<br>评分标准：有趣度 80% + 有用度 20%<br>深度分析：≥80分话题从3个维度深度挖掘产品创意<br>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
    <script>
        const sortButton = document.getElementById('sortButton');
        const table = document.getElementById('hotspotTable');
        const tbody = table.querySelector('tbody');
        let isDescending = true;
        const originalRows = Array.from(tbody.querySelectorAll('tr'));
        sortButton.addEventListener('click', function() {{
            const rows = Array.from(tbody.querySelectorAll('tr'));
            if (isDescending) {{
                rows.sort((a, b) => parseFloat(b.dataset.score) - parseFloat(a.dataset.score));
                sortButton.classList.add('desc');
                sortButton.querySelector('span:first-child').textContent = '恢复原序';
            }} else {{
                tbody.innerHTML = '';
                originalRows.forEach(row => tbody.appendChild(row));
                sortButton.classList.remove('desc');
                sortButton.querySelector('span:first-child').textContent = '按评分排序';
                isDescending = true;
                return;
            }}
            tbody.innerHTML = '';
            rows.forEach(row => tbody.appendChild(row));
            isDescending = false;
        }});
    </script>
</body>
</html>'''

    return html_content


def main():
    """主函数"""
    print("=" * 60)
    print("微博热搜分析报告生成器 - 增强版")
    print("=" * 60)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 加载数据
    print("【步骤1/3】加载分析数据...")
    results, deep_results = load_data()
    print(f"  📊 基础分析：{len(results)} 个话题")
    print(f"  💎 深度分析：{len(deep_results)} 个高分话题")

    # 计算统计数据
    print("\n【步骤2/3】计算统计数据...")
    stats = calculate_stats(results)
    print(f"  📊 话题总数: {stats['total_topics']}")
    print(f"  ⭐ 生成创意: {stats['qualified_count']}")
    print(f"  🔥 深度分析话题: {stats['deep_dive_count']}")
    print(f"  💎 深度分析维度: {stats['deep_dive_count'] * 3}")
    print(f"  📈 平均分数: {stats['avg_score']:.1f}")

    # 生成HTML报告
    print("\n【步骤3/3】生成增强版HTML报告...")
    html_content = generate_html_report(results, deep_results, stats)

    # 创建output目录（如果不存在）
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 已创建输出目录: {output_dir}")

    # 生成带日期的文件名
    date_str = datetime.now().strftime('%Y%m%d_%H%M')
    output_file = os.path.join(output_dir, f'weibo_hotspot_analysis_enhanced_{date_str}.html')

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ 增强版HTML报告已保存: {output_file}")
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return 1

    print("\n" + "=" * 60)
    print("✅ 增强版报告生成完成！")
    print(f"\n📄 输出文件: {output_file}")
    print(f"📂 输出目录: {output_dir}/")
    print("\n💡 增强版特性:")
    print("   - 🔥 深度分析标识：高分话题（≥80分）显示特殊徽章")
    print("   - 💎 3个维度创意：每个高分话题从不同角度深挖产品创意")
    print("   - ✨ 独特价值展示：每个创意都标注核心价值点")
    print("   - 🎨 差异化样式：深度分析话题有独特的背景色和边框")
    print("   - 📊 增强统计：包含深度分析话题和维度统计")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
