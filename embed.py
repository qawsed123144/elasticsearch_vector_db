import json
import random
import requests
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('BAAI/bge-large-zh-v1.5')

# 隨機產生影片數據
genres = ["動作", "科幻", "驚悚", "紀錄片", "教育", "喜劇", "劇情"]
actors = ["王力宏", "張學友", "湯姆漢克斯", "劉德華", "周星馳", "艾瑪華森", "小勞勃道尼"]
title_templates = [
    "{}大解析：你從未見過的深度剖析",
    "揭開{}的祕密：這些你一定要知道",
    "{}革命：如何改變未來世界",
    "從{}到現實：這不再只是幻想",
    "科技與{}：突破性的應用與影響",
    "真相曝光：{} 的黑暗面",
    "大導演推薦！{} 讓你顛覆想像",
    "TOP 10 必看 {} 作品，錯過可惜！",
    "全球熱議！{} 如何影響你的生活？",
    "這部 {} 影片，讓全世界都震驚！"
]
keywords = [
    "人工智慧", "區塊鏈", "量子計算", "虛擬實境", "無人駕駛", "元宇宙", "網路安全", "外星生命",
    "深度學習", "黑客帝國", "未來科技", "高智能機器人", "AI 人工智慧助理", "恐怖電影解析",
    "真實犯罪紀錄", "豪華遊艇生活", "NBA 傳奇球星", "好萊塢影史", "影視大爆料", "全球財經趨勢",
    "航太工程", "未來城市設計", "頂級餐廳美食", "明星私生活揭秘", "超自然現象", "全球旅行探險",
    "二戰歷史", "日韓娛樂圈", "爆款動畫推薦", "影評解析", "奇幻小說改編影集", "獨立電影推薦"
]

videos = []
for i in range(1, 1001):
    keyword = random.choice(keywords)
    title = random.choice(title_templates).format(keyword)
    description = f"本影片深入探討 {keyword} 的應用與未來發展。"

    videos.append({
        "id": i,
        "title": title,
        "description": description,
        "genre": random.choice(genres),
        "cast": random.sample(actors, 2),
        "release_year": random.randint(2000, 2024),
        "views": random.randint(50000, 5000000)
    })

print(f"已產生 {len(videos)} 部影片數據，開始產生 embedding...")

# 轉換為 JSONL 格式
jsonl_filename = "bulk_videos.jsonl"
with open(jsonl_filename, "w", encoding="utf-8") as f:
    for vid in videos:
        # 標題 + 描述 + 類別 + 演員 作為 embedding 的來源
        text_for_embedding = vid["title"] + " " + vid["description"] + " " + vid["genre"] + " " + " ".join(vid["cast"])
        embedding = model.encode([text_for_embedding])[0].tolist()

        index_meta = {"index": {"_index": "vector_index", "_id": vid["id"]}}
        f.write(json.dumps(index_meta, ensure_ascii=False) + "\n")

        vid["embedding"] = embedding
        f.write(json.dumps(vid, ensure_ascii=False) + "\n")

print(f"已產生 {jsonl_filename}，準備匯入 Elasticsearch...")

# 匯入 ES (_bulk API)
es_url = "http://localhost:9200/_bulk"
headers = {"Content-Type": "application/json"}

with open(jsonl_filename, "rb") as f:
    response = requests.post(es_url, headers=headers, data=f)

print("Bulk Import Status:", response.status_code)
print(response.text)