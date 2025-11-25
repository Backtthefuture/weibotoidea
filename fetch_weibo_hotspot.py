#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜数据获取器
"""

import requests
import json
import sys
from datetime import datetime

# 微博热搜API
WEIBO_HOT_URL = "https://weibo.com/ajax/side/hotSearch"


def fetch_weibo_hotspot():
    """获取微博热搜数据"""
    print("正在获取微博热搜数据...")

    try:
        # 设置请求头模拟浏览器
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://weibo.com/",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "X-Requested-With": "XMLHttpRequest"
        }

        # 创建会话
        session = requests.Session()
        session.headers.update(headers)

        # 先访问主页获取cookies
        session.get("https://weibo.com", timeout=15)

        # 再获取热搜数据
        response = session.get(WEIBO_HOT_URL, timeout=15)
        response.raise_for_status()

        data = response.json()

        if 'data' in data and 'realtime' in data['data']:
            hotspots = data['data']['realtime']
            print(f"✅ 成功获取 {len(hotspots)} 条热搜数据")
            return hotspots
        else:
            print(f"❌ 数据结构异常: {data.keys() if isinstance(data, dict) else '非JSON响应'}")
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
        title = item.get('note', '') or item.get('word', '')
        if not title:
            continue

        # 生成搜索查询
        current_month = datetime.now().strftime('%Y年%m月')
        search_query = f"{title} 微博热搜 {current_month}"

        query_info = {
            'rank': i + 1,
            'title': title,
            'heat': item.get('num', 'N/A'),
            'category': item.get('category', ''),
            'label_name': item.get('label_name', ''),
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
