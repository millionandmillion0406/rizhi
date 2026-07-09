#!/usr/bin/env python3
"""AI Knowledge Butler - Personal knowledge manager"""
import os, sys, json, sqlite3, hashlib, uuid, threading, time, re
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
from flask import Flask, request, jsonify, Response

app = Flask(__name__)
BASE = "/home/ubuntu/knowledge_butler"
os.makedirs(BASE, exist_ok=True)

DB = os.path.join(BASE, "kb.db")
DEEPSEEK_KEY = "your-deepseek-key-here"

# === SQLite Setup ===
conn = sqlite3.connect(DB, check_same_thread=False)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("""
CREATE TABLE IF NOT EXISTS entries (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    summary TEXT,
    tags TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP,
    access_count INTEGER DEFAULT 0
)""")
conn.execute("""
CREATE TABLE IF NOT EXISTS connections (
    id TEXT PRIMARY KEY,
    entry_a TEXT, entry_b TEXT,
    reason TEXT,
    strength REAL DEFAULT 0.5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(entry_a) REFERENCES entries(id),
    FOREIGN KEY(entry_b) REFERENCES entries(id)
)""")
conn.execute("""
CREATE TABLE IF NOT EXISTS embeddings (
    entry_id TEXT PRIMARY KEY,
    vector BLOB,
    FOREIGN KEY(entry_id) REFERENCES entries(id)
)""")
conn.commit()

# === Embedding (lazy loaded) ===
embed_model = None
def get_embedding(text):
    global embed_model
    if embed_model is None:
        from sentence_transformers import SentenceTransformer
        embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    return embed_model.encode([text])[0].tolist()

def cosine_sim(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

# === DeepSeek API ===
def call_deepseek(prompt, max_tokens=2000):
    import requests
    r = requests.post("https://api.deepseek.com/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"},
        json={"model": "deepseek-chat", "messages": [
            {"role": "user", "content": prompt}
        ], "max_tokens": max_tokens, "temperature": 0.3}, timeout=60)
    return r.json()["choices"][0]["message"]["content"]

# === Core: Ingest ===
def ingest(content, source="wechat"):
    eid = hashlib.md5(content.encode()).hexdigest()[:12]
    
    # Check duplicate
    cur = conn.execute("SELECT id FROM entries WHERE id=?", (eid,))
    if cur.fetchone():
        return eid, "duplicate"
    
    # DeepSeek extract summary + tags
    prompt = f"""分析以下内容，返回JSON（不要其他文字）�?{{"summary": "一句话摘要�?0字内�?, "tags": ["标签1", "标签2", "标签3"]}}

内容：{content[:2000]}"""
    
    try:
        result = call_deepseek(prompt, 200)
        meta = json.loads(result) if result.strip().startswith('{') else {"summary": content[:50], "tags": ["未分�?]}
    except:
        meta = {"summary": content[:50], "tags": ["未分�?]}
    
    summary = meta.get("summary", content[:50])
    tags = ",".join(meta.get("tags", ["未分�?]))
    
    # Store
    conn.execute("INSERT INTO entries(id,content,summary,tags,source) VALUES(?,?,?,?,?)",
                 (eid, content, summary, tags, source))
    
    # Embed
    try:
        vec = get_embedding(content[:1000])
        conn.execute("INSERT OR REPLACE INTO embeddings(entry_id,vector) VALUES(?,?)",
                     (eid, json.dumps(vec)))
    except: pass
    
    conn.commit()
    return eid, summary

# === Core: Search ===
def search(query, top_k=5):
    results = []
    
    # 1. Keyword search (SQLite FTS)
    try:
        cur = conn.execute(
            "SELECT id, content, summary, tags FROM entries WHERE content LIKE ? OR summary LIKE ? OR tags LIKE ? LIMIT ?",
            (f"%{query}%", f"%{query}%", f"%{query}%", top_k))
        for row in cur.fetchall():
            results.append({"id": row[0], "content": row[1][:200], "summary": row[2], "tags": row[3], "score": 0.5})
    except: pass
    
    # 2. Vector search
    try:
        qvec = get_embedding(query)
        cur = conn.execute("SELECT entry_id, vector FROM embeddings")
        vec_results = []
        for row in cur.fetchall():
            v = json.loads(row[1])
            sim = float(cosine_sim(qvec, v))
            vec_results.append((row[0], sim))
        vec_results.sort(key=lambda x: x[1], reverse=True)
        
        for eid, sim in vec_results[:top_k]:
            cur2 = conn.execute("SELECT id, content, summary, tags FROM entries WHERE id=?", (eid,))
            row = cur2.fetchone()
            if row:
                results.append({"id": row[0], "content": row[1][:200], "summary": row[2], "tags": row[3], "score": float(sim)})
    except: pass
    
    # Deduplicate and sort by score
    seen = set()
    unique = []
    for r in results:
        if r["id"] not in seen:
            seen.add(r["id"])
            unique.append(r)
    unique.sort(key=lambda x: x["score"], reverse=True)
    return unique[:top_k]

# === Core: Find Connections ===
def find_connections():
    """Scan for new connections between entries"""
    cur = conn.execute("SELECT id, summary, content FROM entries ORDER BY created_at DESC LIMIT 20")
    recent = cur.fetchall()
    if len(recent) < 2: return []
    
    # Build prompt for DeepSeek
    entries_text = "\n".join([f"[{r[0]}] {r[1]}" for r in recent])
    prompt = f"""以下是我的知识库条目，找出其�?-3对有意义的关联。返回JSON数组：[{{"a":"id1","b":"id2","reason":"关联原因(20字内)","strength":0.8}}]

{entries_text}"""
    
    try:
        result = call_deepseek(prompt, 500)
        connections = json.loads(result) if result.strip().startswith('[') else []
    except:
        return []
    
    saved = []
    for c in connections:
        cid = hashlib.md5(f"{c['a']}{c['b']}{c['reason']}".encode()).hexdigest()[:12]
        try:
            conn.execute("INSERT OR IGNORE INTO connections(id,entry_a,entry_b,reason,strength) VALUES(?,?,?,?,?)",
                        (cid, c['a'], c['b'], c['reason'], c.get('strength', 0.5)))
            saved.append(c)
        except: pass
    
    conn.commit()
    return saved

# === API Routes ===
@app.route("/")
def index():
    cur = conn.execute("SELECT COUNT(*) FROM entries")
    count = cur.fetchone()[0]
    return jsonify({"status": "ok", "entries": count, "name": "AI Knowledge Butler"})

@app.route("/api/ingest", methods=["POST"])
def api_ingest():
    data = request.json
    content = data.get("content", "").strip()
    if not content: return jsonify({"error": "empty"}), 400
    
    eid, summary = ingest(content, data.get("source", "api"))
    return jsonify({"id": eid, "summary": summary})

@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").strip()
    if not q: return jsonify({"results": []})
    results = search(q)
    return jsonify({"results": results})

@app.route("/api/connections")
def api_connections():
    cur = conn.execute("""
        SELECT c.reason, c.strength, 
               e1.summary as a_summary, e2.summary as b_summary,
               c.created_at
        FROM connections c
        JOIN entries e1 ON c.entry_a = e1.id
        JOIN entries e2 ON c.entry_b = e2.id
        ORDER BY c.created_at DESC LIMIT 10""")
    results = [{"reason": r[0], "strength": r[1], "a": r[2], "b": r[3], "time": r[4]} for r in cur.fetchall()]
    return jsonify({"connections": results})

@app.route("/api/stats")
def api_stats():
    cur = conn.execute("SELECT COUNT(*) FROM entries")
    entries = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM connections")
    connections = cur.fetchone()[0]
    cur = conn.execute("SELECT tags FROM entries")
    all_tags = []
    for (tags,) in cur.fetchall():
        all_tags.extend(tags.split(","))
    from collections import Counter
    top_tags = Counter(all_tags).most_common(10)
    return jsonify({"entries": entries, "connections": connections, "top_tags": top_tags})

# === Daily Connection Scan ===
def daily_scan():
    while True:
        time.sleep(3600 * 6)  # Every 6 hours
        try:
            conns = find_connections()
            if conns: print(f"Found {len(conns)} connections")
        except Exception as e:
            print(f"Scan error: {e}")

threading.Thread(target=daily_scan, daemon=True).start()
print("Knowledge Butler ready")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)



