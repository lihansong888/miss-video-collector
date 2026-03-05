import requests
import re
from urllib.parse import unquote

# 1. 目标地址：你刚才提供的详情页（可以改成列表页循环）
target_url = "https://njavtv.com/ja/sone-524-uncensored-leak"
output_file = "vod_list.txt"

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://njavtv.com/'
    }
    try:
        # 2. 获取页面源码
        res = requests.get(target_url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        
        # 3. 提取标题：从 <title> 标签或 h1 提取
        title_match = re.search(r'<title>(.*?)</title>', res.text)
        title = title_match.group(1).split('|')[0].strip() if title_match else "未知视频"

        # 4. 提取播放源：该站点的 m3u8 通常在 media-hls.saawsedge.com 域名下
        # 我们直接匹配该特征地址
        m3u8_match = re.search(r'(https?://media-hls\.saawsedge\.com/[^\s^"]+?\.m3u8)', res.text)
        
        if m3u8_match:
            video_url = m3u8_match.group(1)
            # 5. 严格遵守你的格式：视频文件名,视频链接
            result = f"{title},{video_url}"
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"✅ 成功抓取播放源：{title}")
        else:
            print("❌ 网页内未找到 .m3u8 播放地址，可能被加密或隐藏。")

    except Exception as e:
        print(f"🔥 运行出错: {e}")

if __name__ == "__main__":
    fetch_data()
