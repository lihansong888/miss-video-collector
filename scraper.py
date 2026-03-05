import requests
import re
from urllib.parse import unquote

# 加入了 /xpdhj/ 的正确路径
target_url = "https://xpdhj.xpdhj9.xyz/xpdhj/index.php/vod/type/id/1/page/1.html"
output_file = "vod_list.txt"

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://xpdhj.xpdhj9.xyz/'
    }
    all_results = []
    
    try:
        # 第一步：获取列表页
        res = requests.get(target_url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        
        # 按照你的范本逻辑，匹配详情页链接和标题
        items = re.findall(r'href="([^"]+detail/id/[^"]+)" title="([^"]+)"', res.text)
        
        print(f"找到 {len(items)} 个详情页，开始提取播放源...")

        for link, title in items[:15]: # 先处理前15个，确保成功率
            full_detail_url = f"https://xpdhj.xpdhj9.xyz{link}" if link.startswith('/') else link
            
            # 第二步：进入详情页抓取真正的播放源
            try:
                det_res = requests.get(full_detail_url, headers=headers, timeout=10)
                # 寻找 m3u8 地址 (通常藏在 player_aaaa 变量中或加密的 script 中)
                # 我们使用通用匹配，涵盖各种可能出现的 m3u8
                m3u8_match = re.search(r'(https?://[^\s^"]+?\.m3u8)', det_res.text)
                
                if m3u8_match:
                    video_url = unquote(m3u8_match.group(1))
                    # 严格遵守格式：视频文件名,视频链接
                    all_results.append(f"{title},{video_url}")
                    print(f"成功获取: {title}")
                else:
                    # 如果详情页没直接露出来，尝试找播放器里的 ID 再次解析
                    print(f"详情页 {title} 未发现直链，跳过")
            except:
                continue

        # 第三步：保存
        if all_results:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(all_results))
            print(f"✅ 任务完成！共提取 {len(all_results)} 条真实播放源。")
        else:
            print("❌ 未能提取到任何真实 m3u8 链接。")

    except Exception as e:
        print(f"🔥 运行崩溃: {e}")

if __name__ == "__main__":
    fetch_data()
