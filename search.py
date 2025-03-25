#!/Users/qawsed123144/Documents/CS/ELK/vector/myvenv/bin/python
import sys
import json
import requests
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('BAAI/bge-large-zh-v1.5')

if __name__ == "__main__":
    # 從命令列取得文字
    query_text = " ".join(sys.argv[1:])
    if not query_text:
        print("請輸入查詢文字，例如：")
        print(f"  ./search.py AI的未來")
        sys.exit(1)

    query_embedding = model.encode([query_text])[0].tolist()

    # k-NN 查詢
    es_query = {
        "size": 5,  # 回傳幾筆
        "knn": {
            "field": "embedding",
            "query_vector": query_embedding,
            "k": 5,
            "num_candidates": 10
        }
    }

    es_url = "http://localhost:9200/vector_index/_search"
    headers = {"Content-Type": "application/json"}
    response = requests.post(es_url, headers=headers,
                             data=json.dumps(es_query))
    result = response.json()

    if response.status_code != 200:
        print("Elasticsearch returned an error.")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)

    # 4) 顯示結果
    print("搜尋完成，狀態碼：", response.status_code)
    hits = result.get("hits", {}).get("hits", [])
    print("=== 查詢文字 ===")
    print(query_text)
    print("=== 搜尋結果 ===")
    for idx, hit in enumerate(hits):
        source = hit.get("_source", {})
        score = hit.get("_score", "N/A")
        print(f"{idx+1}. 相似度分數: {score:.4f}")
        for key, value in source.items():
            if key != "embedding":  # 避免顯示 embedding
                print(f"   {key}: {value}")
        print("-" * 50)
