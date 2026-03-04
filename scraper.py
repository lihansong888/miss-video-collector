import requests
import re

# 你可以改为分类页或者具体的视频页
target_url = "https://njavtv.com/cn" 
output_file = "vod_list.txt"

def fetch_njav_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://njavtv.com/'
    }
    
    try:
        # 1. 先抓取列表页获取所有视频的详情页链接
        response = requests.get(target_url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        # 匹配标题和详情页路径
        items = re.findall(r'href="(/v/[^"]+)" title="([^"]+)"', response.text)
        
        results = []
        
        # 2. 遍历每个视频页（这里为了演示仅演示前3个，避免GitHub Action运行超时）
        for link, title in items[:5]:
            detail_url = f"https://njavtv.com{link}"
            detail_res = requests.get(detail_url, headers=headers, timeout=10)
            
            # 3. 在详情页中寻找隐藏的 m3u8 地址
            # 这里的正则根据你提供的 edge-hls.saawsedge.com 结构进行了匹配优化
            m3u8_match = re.search(r'https?://[^\s^"]+?\.m3u8', detail_res.text)
            
            if m3u8_match:
                m3u8_url = m3u8_match.group(0)
                # 严格遵守你的范本逻辑：视频文件名$视频链接
                results.append(f"{title}${m3u8_url}")
        
        # 4. 自动保存为 txt
        if results:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(results))
            print(f"成功更新 {len(results)} 条数据")
        else:
            print("未提取到有效地址，请检查目标站是否开启了防火墙")
            
    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == "__main__":
    fetch_njav_data()
