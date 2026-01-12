#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜数据获取器
使用天行数据API
"""

import warnings
# 禁用urllib3的SSL警告（必须在导入requests之前）
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')

import requests
import json
import sys
import re
import os
from datetime import datetime

# 从环境变量获取天行数据 API Key
TIANXING_API_KEY = os.environ.get('TIANXING_API_KEY')
if not TIANXING_API_KEY:
    print("❌ 错误: 未找到环境变量 TIANXING_API_KEY")
    print("请设置环境变量: export TIANXING_API_KEY='your_api_key'")
    sys.exit(1)

# 天行数据微博热搜API
WEIBO_HOT_URL = f"https://apis.tianapi.com/weibohot/index?key={TIANXING_API_KEY}"


def fetch_weibo_hotspot():
    """获取微博热搜数据"""
    print("正在获取微博热搜数据...")

    try:
        # 获取热搜数据
        response = requests.get(WEIBO_HOT_URL, timeout=15)
        response.raise_for_status()

        data = response.json()

        if data.get('code') == 200 and 'result' in data:
            hotspots = data['result']['list']
            print(f"✅ 成功获取 {len(hotspots)} 条热搜数据")
            return hotspots
        else:
            print(f"❌ 数据结构异常: {data}")
            return []

    except requests.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        return []
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return []


def generate_search_queries(hotspots, max_items=15):
    """为每个热搜生成搜索查询"""
    print(f"\n正在生成搜索查询（前{max_items}条）...")

    queries = []
    for i, item in enumerate(hotspots[:max_items]):
        # 获取热搜标题
        title = item.get('hotword', '')
        if not title:
            continue

        # 获取热度（转换为数字，提取数字部分）
        heat_str = item.get('hotwordnum', '').strip()
        try:
            # 使用正则提取数字
            numbers = re.findall(r'\d+', heat_str)
            heat = int(numbers[0]) if numbers else 0
        except (ValueError, IndexError):
            heat = 0

        # 获取标签
        tag = item.get('hottag', '').strip()

        # 生成搜索查询
        current_month = datetime.now().strftime('%Y年%m月')
        search_query = f"{title} 微博热搜 {current_month}"

        query_info = {
            'rank': i + 1,
            'title': title,
            'heat': heat,
            'category': tag,
            'label_name': tag,
            'search_query': search_query,
            'raw_data': item
        }

        queries.append(query_info)

    print(f"✅ 已生成 {len(queries)} 个搜索查询")
    return queries


def save_queries(queries, filename='weibo_search_queries.json'):
    """保存搜索查询到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(queries, f, ensure_ascii=False, indent=2)

        print(f"✅ 搜索查询已保存到: {filename}")
        return True
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False


def display_top_hotspots(queries, count=10):
    """显示前N条热搜"""
    print(f"\n{'='*60}")
    print(f"微博热搜 TOP {count}")
    print(f"{'='*60}")

    for i, q in enumerate(queries[:count], 1):
        heat = q.get('heat', 'N/A')
        category = q.get('category', '')
        label = q.get('label_name', '')

        print(f"\n#{i:2d} | {q['title']}")
        if heat != 'N/A':
            print(f"     🔥 热度: {heat}")
        if category:
            print(f"     🏷️ 分类: {category}")
        if label:
            print(f"     🏷️ {label}")

    print(f"\n{'='*60}")


def main():
    """主函数"""
    print("=" * 60)
    print("微博热搜数据获取器")
    print("=" * 60)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 获取热搜数据
    hotspots = fetch_weibo_hotspot()

    if not hotspots:
        print("\n❌ 未能获取到热搜数据")
        return 1

    # 生成搜索查询
    queries = generate_search_queries(hotspots, max_items=15)

    if not queries:
        print("\n❌ 未能生成有效的搜索查询")
        return 1

    # 显示热搜
    display_top_hotspots(queries, count=10)

    # 保存到文件
    save_queries(queries)

    print(f"\n✅ 数据获取完成！")
    print(f"📄 输出文件: weibo_search_queries.json")
    print(f"💡 下一步: 使用 search_hotspot_details.py 进行深度搜索")

    return 0


if __name__ == "__main__":
    sys.exit(main())
