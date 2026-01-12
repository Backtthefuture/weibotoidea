#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成智能首页和历史归档索引
"""

import os
import glob
import json
from datetime import datetime


def parse_report_filename(filename):
    """
    解析报告文件名获取日期时间
    格式: 2026-01-12-09-00.html
    """
    try:
        basename = os.path.basename(filename)
        name_without_ext = basename.replace('.html', '')
        parts = name_without_ext.split('-')

        if len(parts) >= 5:
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
            hour = int(parts[3])
            minute = int(parts[4])

            dt = datetime(year, month, day, hour, minute)
            return {
                'filename': basename,
                'datetime': dt,
                'date_str': dt.strftime('%Y年%m月%d日'),
                'time_str': dt.strftime('%H:%M'),
                'time_label': get_time_label(hour),
                'timestamp': dt.strftime('%Y-%m-%d %H:%M')
            }
    except:
        pass

    return None


def get_time_label(hour):
    """根据小时获取时段标签"""
    if 6 <= hour < 12:
        return '早报'
    elif 12 <= hour < 18:
        return '午报'
    else:
        return '晚报'


def generate_archive_index():
    """生成归档页面索引"""
    print("生成历史归档索引...")

    archive_dir = 'analysis_results/archive'
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    # 获取所有报告文件
    report_files = glob.glob(os.path.join(archive_dir, '*.html'))
    report_files = [f for f in report_files if not f.endswith('index.html')]

    reports = []
    for f in report_files:
        info = parse_report_filename(f)
        if info:
            reports.append(info)

    # 按时间倒序排序
    reports.sort(key=lambda x: x['datetime'], reverse=True)

    # 按日期分组
    reports_by_date = {}
    for report in reports:
        date_str = report['date_str']
        if date_str not in reports_by_date:
            reports_by_date[date_str] = []
        reports_by_date[date_str].append(report)

    # 生成HTML
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微博热搜分析 - 历史报告</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 2px solid #f0f0f0;
        }

        .header h1 {
            font-size: 32px;
            color: #333;
            margin-bottom: 10px;
        }

        .header p {
            color: #666;
            font-size: 16px;
        }

        .back-link {
            display: inline-block;
            margin-bottom: 20px;
            color: #667eea;
            text-decoration: none;
            font-size: 16px;
        }

        .back-link:hover {
            text-decoration: underline;
        }

        .date-group {
            margin-bottom: 30px;
        }

        .date-title {
            font-size: 20px;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e0e0e0;
        }

        .report-list {
            display: grid;
            gap: 10px;
        }

        .report-item {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            background: #f8f9fa;
            border-radius: 10px;
            text-decoration: none;
            color: inherit;
            transition: all 0.3s ease;
        }

        .report-item:hover {
            background: #667eea;
            color: white;
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }

        .report-time {
            font-size: 18px;
            font-weight: 600;
            margin-right: 15px;
            min-width: 60px;
        }

        .report-label {
            display: inline-block;
            padding: 4px 12px;
            background: #667eea;
            color: white;
            border-radius: 20px;
            font-size: 14px;
            margin-right: 15px;
        }

        .report-item:hover .report-label {
            background: white;
            color: #667eea;
        }

        .report-date {
            color: #999;
            font-size: 14px;
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }

        .empty-state svg {
            width: 100px;
            height: 100px;
            margin-bottom: 20px;
            opacity: 0.5;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="../" class="back-link">← 返回首页</a>

        <div class="header">
            <h1>📚 历史报告归档</h1>
            <p>浏览所有微博热搜分析报告</p>
        </div>
'''

    if reports_by_date:
        for date_str in sorted(reports_by_date.keys(), reverse=True):
            date_reports = reports_by_date[date_str]
            html += f'''
        <div class="date-group">
            <div class="date-title">📅 {date_str}</div>
            <div class="report-list">
'''
            for report in date_reports:
                html += f'''
                <a href="{report['filename']}" class="report-item">
                    <div class="report-time">{report['time_str']}</div>
                    <span class="report-label">{report['time_label']}</span>
                    <div class="report-date">{report['timestamp']}</div>
                </a>
'''
            html += '''
            </div>
        </div>
'''
    else:
        html += '''
        <div class="empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h3>暂无历史报告</h3>
            <p>报告将在首次运行后显示在这里</p>
        </div>
'''

    html += '''
    </div>
</body>
</html>
'''

    # 写入文件
    index_path = os.path.join(archive_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ 归档索引已生成: {index_path}")
    return reports


def generate_smart_homepage(reports):
    """生成智能首页（带时间选择器）"""
    print("生成智能首页...")

    # 生成报告列表 JSON
    reports_json = json.dumps([{
        'filename': r['filename'],
        'timestamp': r['timestamp'],
        'date_str': r['date_str'],
        'time_str': r['time_str'],
        'time_label': r['time_label']
    } for r in reports], ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微博热搜分析 - 产品创意报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}

        .top-bar {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 15px 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 15px;
        }}

        .logo {{
            font-size: 20px;
            font-weight: 600;
            color: #667eea;
        }}

        .controls {{
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }}

        .time-selector {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .time-selector label {{
            font-size: 14px;
            color: #666;
        }}

        .time-selector select {{
            padding: 8px 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .time-selector select:hover {{
            border-color: #667eea;
        }}

        .time-selector select:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        .btn {{
            padding: 8px 16px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
        }}

        .btn:hover {{
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}

        .btn-secondary {{
            background: #6c757d;
        }}

        .btn-secondary:hover {{
            background: #5a6268;
        }}

        .report-frame {{
            width: 100%;
            height: calc(100vh - 70px);
            border: none;
            display: block;
        }}

        .loading {{
            text-align: center;
            padding: 100px 20px;
            color: white;
            font-size: 18px;
        }}

        .empty-state {{
            text-align: center;
            padding: 100px 20px;
            color: white;
        }}

        .empty-state h2 {{
            font-size: 32px;
            margin-bottom: 20px;
        }}

        .empty-state p {{
            font-size: 18px;
            opacity: 0.8;
            margin-bottom: 30px;
        }}

        @media (max-width: 768px) {{
            .top-bar {{
                padding: 10px 15px;
            }}

            .logo {{
                font-size: 16px;
            }}

            .controls {{
                width: 100%;
                justify-content: space-between;
            }}

            .time-selector {{
                flex: 1;
            }}

            .time-selector select {{
                flex: 1;
                min-width: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="top-bar">
        <div class="logo">📊 微博热搜产品创意分析</div>
        <div class="controls">
            <div class="time-selector">
                <label for="report-select">🕒 选择报告：</label>
                <select id="report-select">
                    <option value="">加载中...</option>
                </select>
            </div>
            <a href="archive/" class="btn btn-secondary">📚 历史归档</a>
        </div>
    </div>

    <div id="content">
        <div class="loading">正在加载最新报告...</div>
    </div>

    <script>
        // 报告列表数据
        const reports = {reports_json};

        // 初始化
        function init() {{
            if (reports.length === 0) {{
                showEmptyState();
                return;
            }}

            // 填充下拉菜单
            const select = document.getElementById('report-select');
            select.innerHTML = '';

            reports.forEach((report, index) => {{
                const option = document.createElement('option');
                option.value = report.filename;
                option.textContent = `${{report.timestamp}} - ${{report.time_label}}`;
                if (index === 0) option.selected = true;
                select.appendChild(option);
            }});

            // 加载最新报告
            loadReport(reports[0].filename);

            // 绑定选择事件
            select.addEventListener('change', (e) => {{
                loadReport(e.target.value);
            }});
        }}

        // 加载报告
        function loadReport(filename) {{
            const content = document.getElementById('content');
            content.innerHTML = `<iframe class="report-frame" src="archive/${{filename}}"></iframe>`;
        }}

        // 显示空状态
        function showEmptyState() {{
            const select = document.getElementById('report-select');
            select.innerHTML = '<option>暂无报告</option>';
            select.disabled = true;

            document.getElementById('content').innerHTML = `
                <div class="empty-state">
                    <h2>🎉 欢迎使用微博热搜分析系统</h2>
                    <p>系统将每天自动分析微博热搜并生成产品创意报告</p>
                    <p>首次报告生成后将显示在这里</p>
                </div>
            `;
        }}

        // 启动
        init();
    </script>
</body>
</html>
'''

    # 写入文件
    index_path = 'analysis_results/index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ 智能首页已生成: {index_path}")


def main():
    print("=" * 60)
    print("生成索引页面")
    print("=" * 60)

    # 生成归档索引并获取报告列表
    reports = generate_archive_index()

    # 生成智能首页
    generate_smart_homepage(reports)

    print("\n✅ 所有索引页面生成完成！")
    print(f"   - 智能首页: analysis_results/index.html")
    print(f"   - 归档索引: analysis_results/archive/index.html")
    print(f"   - 报告总数: {len(reports)}")


if __name__ == "__main__":
    main()
