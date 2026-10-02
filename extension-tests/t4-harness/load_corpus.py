#!/usr/bin/env python3
"""T4 corpus loader (harness tooling; indexing is outside the Retriever contract).

Loads t4-corpus.json into both engines, embedding every document with the same
function the stub gateway uses for queries:
  pgvector  through psql inside the container (docker exec), into table `documents`
  Qdrant    through its REST API, into collection `documents`

Usage: load_corpus.py <pgvector-container> <qdrant-url>
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from embedding import DIMENSIONS, embed  # noqa: E402

CORPUS = HERE.parent / "t4-corpus.json"


def sql_text(value):
    return "NULL" if value is None else "'" + str(value).replace("'", "''") + "'"


def load_pgvector(container, documents):
    rows = []
    for d in documents:
        vector = "[" + ",".join(repr(v) for v in embed(d["content"])) + "]"
        rows.append("(" + ",".join([sql_text(d["id"]), sql_text(d["version"]), sql_text(d["tenant"]),
                                    sql_text(d["source"]), sql_text(d["metadata"]["title"]),
                                    sql_text(d["metadata"].get("classification")),
                                    sql_text(d["content"]), sql_text(vector) + "::vector"]) + ")")
    script = ("CREATE EXTENSION IF NOT EXISTS vector;\n"
              "DROP TABLE IF EXISTS documents;\n"
              f"CREATE TABLE documents (id text PRIMARY KEY, version text, tenant text, source text, "
              f"title text, classification text, content text, embedding vector({DIMENSIONS}));\n"
              "INSERT INTO documents VALUES\n" + ",\n".join(rows) + ";\n")
    subprocess.run(["docker", "exec", "-i", container, "psql", "-v", "ON_ERROR_STOP=1", "-q",
                    "-U", "knowledge", "-d", "knowledge"], input=script, text=True, check=True)


def qdrant(method, url, body):
    request = urllib.request.Request(url, data=json.dumps(body).encode(), method=method,
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())


def load_qdrant(base, documents):
    try:
        urllib.request.urlopen(urllib.request.Request(f"{base}/collections/documents", method="DELETE"))
    except Exception:
        pass
    qdrant("PUT", f"{base}/collections/documents", {"vectors": {"size": DIMENSIONS, "distance": "Cosine"}})
    points = []
    for i, d in enumerate(documents, start=1):
        payload = {"doc_id": d["id"], "version": d["version"], "tenant": d["tenant"], "source": d["source"],
                   "title": d["metadata"]["title"], "content": d["content"]}
        if d["metadata"].get("classification"):
            payload["classification"] = d["metadata"]["classification"]
        points.append({"id": i, "vector": embed(d["content"]), "payload": payload})
    qdrant("PUT", f"{base}/collections/documents/points?wait=true", {"points": points})


if __name__ == "__main__":
    documents = json.loads(CORPUS.read_text(encoding="utf-8"))["documents"]
    load_pgvector(sys.argv[1], documents)
    load_qdrant(sys.argv[2], documents)
    print(f"loaded {len(documents)} documents into pgvector and Qdrant")
