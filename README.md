# 🔍 Elasticsearch 向量搜尋實作

使用 Elasticsearch 8.x 建立中文向量資料庫系統，支援 embedding 轉換、index 建立、k-NN 向量查詢與 demo 結果輸出。

📖 原始教學移植自 GitBook，詳見 `/docs` 目錄。

---

## 💡 專案特色

- 使用 [BAAI/bge-large-zh-v1.5](https://huggingface.co/BAAI/bge-large-zh-v1.5) 模型進行中文語意轉向量
- 使用 Elasticsearch `dense_vector` 與 HNSW 建立向量索引
- 使用 Docker 快速部署 Elasticsearch 8.5.0
- 提供 `embed.py` 建立測試資料與批次匯入
- 提供 `search.py` 查詢 CLI 工具（支援語意相似度搜尋）
- 整合 k-NN 搜尋與向量 API 查詢

---

## 🚀 快速開始

```bash
# 建立虛擬環境
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt

# 啟動 Elasticsearch（需先安裝 Docker）
docker-compose up -d

# 建立資料並匯入向量
python embed.py

# 執行查詢
./search.py 飛天汽車

```
## 🧪 查詢輸出範例
```bash
$ ./search.py 飛天汽車
搜尋完成，狀態碼： 200
=== 查詢文字 ===
飛天汽車
=== 搜尋結果 ===
1. 相似度分數: 0.7521
   id: 242
   title: 從無人駕駛到現實：這不再只是幻想
   description: 本影片深入探討 無人駕駛 的應用與未來發展。
   genre: 喜劇
   cast: ['小勞勃道尼', '周星馳']
   release_year: 2004
   views: 1006553
--------------------------------------------------
2. 相似度分數: 0.7463
   id: 115
   title: 從無人駕駛到現實：這不再只是幻想
   description: 本影片深入探討 無人駕駛 的應用與未來發展。
   genre: 教育
   cast: ['王力宏', '小勞勃道尼']
   release_year: 2012
   views: 2154329
