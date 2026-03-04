import requests
import re
import time

# 目标基础 URL
base_url = "https://xpdhj.xpdhj9.xyz"
# 爬取前 10 页（你可以根据需要把 11 改成 51 或更多，实现万级抓取）
max_pages = 11 
output_file = "vod_list.txt"

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': base_url
    }
    
    all_results = []
    
    for page in range(1, max_pages):
        # 构造分页 URL，例如 /index.php/vod/type/id/1/page/1.html
        # 注意：这里的路径需要根据该站实际分类页调整
        list_url = f"{base_url}/index.php/vod/type/id/1/page/{page}.html"
        print(f"正在爬取第 {page} 页...")
        
        try:
            res = requests.get(list_url, headers=headers, timeout=15)
            res.encoding = 'utf-8'
            
            # 1. 匹配视频标题和详情页链接
            # 常见格式：<a href="/index.php/vod/detail/id/123.html" title="视频名称">
            items = re.findall(r'href="(/index.php/vod/detail/id/\d+\.html)" title="([^"]+)"', res.text)
            
            for link, title in items:
                detail_url = f"{base_url}{link}"
                # 2. 进入详情页拿 m3u8
                # 为了速度，这里演示逻辑；如果网站直接在源码里有 m3u8，直接匹配即可
                # 很多站点的 m3u8 藏在详情页的 script 标签里
                detail_res = requests.get(detail_url, headers=headers, timeout=10)
                m3u8_match = re.search(r'https?://[^\s^"]+?\.m3u8', detail_res.text)
                
                if m3u8_match:
                    video_url = m3u8_match.group(0)
                    all_results.append(f"{title},{video_url}")
            
            time.sleep(1) # 稍微停顿，防止被封
        except Exception as e:
            print(f"第 {page} 页抓取失败: {e}")

    # 3. 统一保存
    if all_results:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(all_results))
        print(f"✅ 全自动抓取完成！共获得 {len(all_results)} 条数据。")

if __name__ == "__main__":
    fetch_data()
