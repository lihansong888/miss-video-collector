import requests
import re
import time

# 目标：njavtv 列表页
target_url = "https://njavtv.com/cn" 
output_file = "vod_list.txt"

def fetch_data():
    # 模拟手机浏览器，降低被拦截的概率
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Referer': 'https://njavtv.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    
    try:
        print("正在连接目标网站...")
        response = requests.get(target_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            # 1. 提取详情页链接和标题
            items = re.findall(r'href="(/v/[^"]+)" title="([^"]+)"', response.text)
            
            if not items:
                print("⚠️ 抓到了网页但没找到视频，可能需要更新匹配规则。")
                return

            results = []
            # 2. 遍历前 5 个视频，获取真实 m3u8
            for link, title in items[:5]:
                detail_url = f"https://njavtv.com{link}"
                print(f"正在解析: {title}")
                
                # 稍微停顿一下，防止被封 IP
                time.sleep(1) 
                
                detail_res = requests.get(detail_url, headers=headers, timeout=15)
                # 寻找 saawsedge 域名的 m3u8 地址
                m3u8_match = re.search(r'https?://media-hls\.saawsedge\.com/[^\s^"]+?\.m3u8', detail_res.text)
                
                if m3u8_match:
                    video_url = m3u8_match.group(0)
                    # 严格执行你的格式：标题,链接
                    results.append(f"{title},{video_url}")
            
            # 3. 只有成功抓到数据才写入文件，防止覆盖旧数据
            if results:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(results))
                print(f"✅ 成功提取 {len(results)} 条数据！")
            else:
                print("❌ 未能找到有效的 m3u8 播放地址。")
        else:
            print(f"❌ 网页请求被拒绝，错误代码: {response.status_code}")
            
    except Exception as e:
        print(f"🔥 运行崩溃: {str(e)}")

if __name__ == "__main__":
    fetch_data()
