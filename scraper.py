import requests
import re

# 修正后的分类地址（加入了 /xpdhj/）
target_url = "https://xpdhj.xpdhj9.xyz/xpdhj/index.php/vod/type/id/1/page/1.html"
output_file = "vod_list.txt"

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://xpdhj.xpdhj9.xyz/'
    }
    try:
        res = requests.get(target_url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        
        # 模拟你的 XBPQ 逻辑：寻找 data-original 和 title
        # 匹配结果：(图片地址, 详情页链接, 视频标题)
        items = re.findall(r'data-original="([^"]+)".*?href="([^"]+)".*?title="([^"]+)"', res.text, re.S)
        
        results = []
        for img, link, title in items[:50]:
            # 这里的 link 需要补全域名
            full_link = f"https://xpdhj.xpdhj9.xyz{link}" if link.startswith('/') else link
            # 严格按照你要求的：标题,播放页链接 (或进一步提取链接)
            results.append(f"{title},{full_link}")
            
        if results:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(results))
            print(f"✅ 按照影视范本逻辑，成功提取 {len(results)} 条数据！")
    except Exception as e:
        print(f"🔥 失败: {e}")

if __name__ == "__main__":
    fetch_data()
