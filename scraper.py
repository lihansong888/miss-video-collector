import requests
import re

# 目标：njavtv 列表页
target_url = "https://njavtv.com/cn" 
output_file = "vod_list.txt"

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Referer': 'https://njavtv.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    try:
        # 获取网页源代码
        response = requests.get(target_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        
        # 核心逻辑：先看能不能抓到网页
        if response.status_code == 200:
            # 改进的匹配模式
            items = re.findall(r'href="(/v/[^"]+)" title="([^"]+)"', response.text)
            
            if not items:
                print("⚠️ 警告：抓到了网页但没找到视频列表，可能是网页改版了。")
                return

            results = []
            # 演示前 5 个，确保成功率
            for link, title in items[:5]:
                detail_url = f"https://njavtv.com{link}"
                detail_res = requests.get(detail_url, headers=headers, timeout=15)
                
                # 寻找具体的 m3u8 地址
                m3u8_match = re.search(r'https?://media-hls\.saawsedge\.com/[^\s^"]+?\.m3u8', detail_res.text)
                
                if m3u8_match:
                    video_url = m3u8_match.group(0)
                    # 严格执行格式：标题,链接
                    results.append(f"{title},{video_url}")
            
            # 只有抓到内容才写入，防止把旧文件覆盖成空的
            if results:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(results))
                print(f"✅ 成功提取 {len(results)} 条数据！")
            else:
                print("❌ 未能提取到有效的 m3u8 链接。")
        else:
            print(f"❌ 网页请求失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"🔥 运行崩溃: {e}")

if __name__ == "__main__":
    fetch_data()
