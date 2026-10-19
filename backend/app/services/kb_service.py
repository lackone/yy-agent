import chromadb
from chromadb.utils import results, embedding_functions

from app.config.config import BASE_DIR

KB_DIR = BASE_DIR / 'data' / 'kb'

CHROMA_DIR = BASE_DIR / 'data' / 'chroma'

# 初始化集合
_collection = None

# 指定使用适合中文的 bge-small-zh 模型
_ef = None


def init_embedding_function():
    """初始化嵌入函数"""
    global _ef
    if _ef is not None:
        return _ef
    _ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-small-zh-v1.5")
    return _ef


def warmup():
    """预热模型"""
    col = get_collection()
    if col.count() > 0:
        col.query(query_texts=["你好"], n_results=1)


def get_collection():
    """获取集合"""
    global _collection
    if _collection is not None:
        return _collection

    KB_DIR.mkdir(parents=True, exist_ok=True)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    # 创建或获取 Chroma 客户端
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    # 创建或获取集合
    col = client.get_or_create_collection(name='lab_kb', embedding_function=init_embedding_function())

    if col.count() == 0:
        ids = []
        docs = []
        metas = []

        for file in sorted(KB_DIR.glob('*.md')):
            text = file.read_text(encoding='utf-8').strip()
            if not text:
                continue
            docs.append(text)
            ids.append(file.stem)
            metas.append({'source': file.name})

        if docs:
            col.add(ids=ids, documents=docs, metadatas=metas)

    _collection = col

    return _collection


def search(query: str):
    """搜索"""
    col = get_collection()
    if col.count() == 0:
        return ""

    res = col.query(query_texts=[query], n_results=col.count())

    docs = (res.get("documents") or [[]])[0]
    metas = (res.get("metadatas") or [[]])[0]
    distances = (res.get("distances") or [[]])[0]

    results = []
    for doc, meta, dist in zip(docs, metas, distances):
        score = 1 / (1 + dist)
        if score < 0.5:
            continue
        name = meta.get('source') or ''
        results.append({
            "score": score,
            "content": f"[{name}]\n{doc}",
        })

    # 按 score 排序
    results.sort(key=lambda x: x["score"], reverse=True)
    # 取前 2 个
    final_results = [item["content"] for item in results[:2]]

    # print(results)
    # print(final_results)

    return "\n\n".join(final_results)
