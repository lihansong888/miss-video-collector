import requests
import re

# 目标：njavtv 列表页
target_url = "https://njavtv.com/cn" 
output_file = "vod_list.txt"

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://njavtv.com/'
    }
    try:
        # 获取列表页
        response = requests.get(target_url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            # 提取视频标题和详情页链接
            items = re.findall(r'href="(/v/[^"]+)" title="([^"]+)"', response.text)
            
            results = []
            # 遍历提取前 10 个视频详情
            for link, title in items[:10]:
                detail_url = f"https://njavtv.com{link}"
                detail_res = requests.get(detail_url, headers=headers, timeout=10)
                
                # 寻找真实的 m3u8 播放地址
                m3u8_match = re.search(r'https?://media-hls\.saawsedge\.com/[^\s^"]+?\.m3u8', detail_res.text)
                
                if m3u8_match:
                    video_url = m3u8_match.group(0)
                    # 严格执行你的格式：标题,链接
                    results.append(f"{title},{video_url}")
            
            # 保存为 txt 文件
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(results))
            print(f"提取成功：已更新 {len(results)} 条数据")
    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == "__main__":
    fetch_data()
