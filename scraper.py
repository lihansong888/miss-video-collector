import requests
import re
import json
import base64
from urllib.parse import unquote

target_url = "https://xpdhj.xpdhj9.xyz/index.php/vod/type/id/1.html"
output_file = "vod_list.txt"

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://xpdhj.xpdhj9.xyz/'
    }
    try:
        # 1. 获取分类页
        res = requests.get(target_url, headers=headers, timeout=15)
        # 提取详情页链接和标题（修正后的正则）
        items = re.findall(r'href="(/index.php/vod/detail/id/\d+\.html)" title="([^"]+)"', res.text)
        
        results = []
        for link, title in items[:20]: # 先测试20个
            detail_url = f"https://xpdhj.xpdhj9.xyz{link}"
            det_res = requests.get(detail_url, headers=headers, timeout=10)
            
            # 2. 关键：寻找播放器配置 JSON (MacPlayer 常用的变量)
            player_data = re.search(r'var player_aaaa=(.*?)</script>', det_res.text)
            if player_data:
                try:
                    # 解析 JSON 获取加密的 url
                    config = json.loads(player_data.group(1))
                    video_url = config.get('url', '')
                    
                    # 3. 如果是加密地址则解码 (常见的是 URL 编码)
                    if 'm3u8' not in video_url:
                        video_url = unquote(video_url)
                    
                    # 格式：标题,链接
                    results.append(f"{title},{video_url}")
                except:
                    continue
        
        if results:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(results))
            print(f"成功分析并提取 {len(results)} 条数据")
        else:
            print("未能从播放器配置中提取到地址")

    except Exception as e:
        print(f"分析失败: {e}")

if __name__ == "__main__":
    fetch_data()
