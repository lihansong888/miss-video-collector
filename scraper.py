import requests

# 目标地址
target_url = "https://surrit.com/5866cb77-a476-46b5-a0ad-2e58e55c3958/720p/video.m3u8"
output_file = "vod_list.txt"

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://missav123.com/'
    }
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        if response.status_code == 200:
            lines = response.text.split('\n')
            results = []
            count = 1
            base_url = target_url.rsplit('/', 1)[0]
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    full_path = line if line.startswith('http') else f"{base_url}/{line}"
                    # 严格遵守你的“分类$地址”范本逻辑
                    results.append(f"视频切片{count:03d}${full_path}")
                    count += 1
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(results))
            print("抓取成功！")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    fetch_data()

