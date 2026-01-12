
import json
import os
import glob
import re

def main():
    print("Combinining analysis results...")
    results = []
    results_dict = {}  # 用于去重

    # Ensure directory exists
    if not os.path.exists('analysis_results'):
        print("No analysis_results directory found.")
        return

    # Pattern matching the agent's output
    files = glob.glob('analysis_results/result_*.json')
    print(f"Found {len(files)} result files.")

    for f in sorted(files):
        try:
            with open(f, 'r', encoding='utf-8') as fd:
                data = json.load(fd)
                # Try to extract rank from filename if not in data
                if 'rank' not in data:
                    match = re.search(r'result_(\d+).json', f)
                    if match:
                        data['rank'] = int(match.group(1))

                # Merge title info and heat
                rank = data.get('rank')
                if rank:
                    # Try to find title from search_results
                    search_result_file = f"search_results_{rank:02d}.json"
                    if os.path.exists(search_result_file):
                         with open(search_result_file, 'r', encoding='utf-8') as sf:
                             sdata = json.load(sf)
                             if 'title' in sdata and 'title' not in data:
                                 data['title'] = sdata['title']

                    # Try to get heat from weibo_search_queries.json
                    try:
                        with open('weibo_search_queries.json', 'r', encoding='utf-8') as qf:
                            queries = json.load(qf)
                            for q in queries:
                                if q.get('rank') == rank:
                                    data['heat'] = q.get('heat', 0)
                                    if 'title' not in data: # Fallback title
                                         data['title'] = q.get('title')
                                    break
                    except Exception as e:
                        print(f"Error reading queries: {e}")

                # 使用 rank 作为键去重，只保留每个 rank 的最新数据
                if rank:
                    results_dict[rank] = data
                else:
                    results.append(data)
        except Exception as e:
            print(f"Skipping {f}: {e}")

    # 将去重后的结果转换为列表
    results = list(results_dict.values())

    # Sort by rank
    results.sort(key=lambda x: x.get('rank', 999))

    print(f"✅ 去重后保留 {len(results)} 条唯一结果")
    
    output_file = 'hotspot_analysis_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✅ Combined {len(results)} files into {output_file}")

if __name__ == "__main__":
    main()
