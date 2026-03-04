import requests
import re

# 目标：xpdhj 的视频列表页
target_url = "https://xpdhj.xpdhj9.xyz/index.php/vod/type/id/1.html"
output_file = "vod_list.txt"

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://xpdhj.xpdhj9.xyz/'
    }
    try:
        # 1. 抓取列表页
        res = requests.get(target_url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        
        # 2. 关键：匹配标题和详情页 ID (根据该站常用的 maccms 系统结构)
        # 这里的正则必须跟网页源码一模一样
        items = re.findall(r'href="(/index.php/vod/detail/id/(\d+)\.html)" title="([^"]+)"', res.text)
        
        results = []
        for link, vod_id, title in items[:30]: # 先测试前30个
            # 3. 构造该站常见的播放解析地址 (很多站不需要进详情页，直接拼接 ID 即可)
            # 或者进入详情页提取
            detail_url = f"https://xpdhj.xpdhj9.xyz{link}"
            det_res = requests.get(detail_url, headers=headers, timeout=10)
            
            # 寻找播放源地址
            m3u8_find = re.search(r'https?://[^\s^"]+?\.m3u8', det_res.text)
            if m3u8_find:
                # 严格遵守你的“标题,链接”格式
                results.append(f"{title},{m3u8_find.group(0)}")
        
        if results:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(results))
            print(f"成功抓取 {len(results)} 条！")
    except Exception as e:
        print(f"出错原因: {e}")

if __name__ == "__main__":
    fetch_data()
