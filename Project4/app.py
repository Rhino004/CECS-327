import os
import json
import hashlib
import threading
from pathlib import Path
from typing import List, Tuple, Dict

from flask import Flask, request, jsonify, send_from_directory, abort
import requests

app = Flask(__name__)

# ---------- Config ----------
STORAGE_DIR = Path("./storage")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# A node identifies itself by MY_URL (required) and knows peers via PEERS (comma-separated URLs).
# Example:
#   MY_URL=http://node1:5000
#   PEERS=http://node1:5000,http://node2:5000,http://node3:5000
MY_URL = os.environ.get("MY_URL", "").rstrip("/")
PEERS_ENV = os.environ.get("PEERS", "")
PEERS: List[str] = [p.strip().rstrip("/") for p in PEERS_ENV.split(",") if p.strip()]

if not MY_URL:
    raise RuntimeError("Environment variable MY_URL must be set (e.g., http://node1:5000).")
if MY_URL not in PEERS:
    # Be forgiving: if user forgot to include self, add it.
    PEERS.append(MY_URL)

# ---------- In-memory KV store ----------
kv_store: Dict[str, str] = {}
kv_lock = threading.Lock()

# ---------- Hashing utilities (SHA-1) ----------
def sha1_int(s: str) -> int:
    return int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16)

def build_ring(peers: List[str]) -> List[Tuple[int, str]]:
    ring = sorted((sha1_int(p), p) for p in set(peers))
    return ring

def find_responsible_node(key: str, ring: List[Tuple[int, str]]) -> str:
    """Consistent-hash style: key belongs to the first node with hash >= key_hash (or wrap)."""
    key_hash = sha1_int(key)
    for node_hash, node_url in ring:
        if key_hash <= node_hash:
            return node_url
    # wrap-around
    return ring[0][1]

def get_ring() -> List[Tuple[int, str]]:
    # In a more advanced system, this could be dynamic. Here we use the env-provided list.
    return build_ring(PEERS)

def is_me(url: str) -> bool:
    return url.rstrip("/") == MY_URL.rstrip("/")

# ---------- Helpers ----------
REQUEST_TIMEOUT = 3  # seconds

def forward_json(method: str, url: str, json_payload=None):
    try:
        if method == "POST":
            r = requests.post(url, json=json_payload, timeout=REQUEST_TIMEOUT)
        elif method == "GET":
            r = requests.get(url, timeout=REQUEST_TIMEOUT)
        else:
            return None, 405
        return (r.json() if r.headers.get("content-type","").startswith("application/json") else r.text), r.status_code
    except requests.RequestException as e:
        return {"error": f"forwarding failed: {str(e)}"}, 502

# ---------- Routes: health & peers ----------
@app.get("/health")
def health():
    return jsonify({"status": "ok", "url": MY_URL})

@app.get("/peers")
def peers():
    ring = get_ring()
    return jsonify({
        "me": MY_URL,
        "peers": PEERS,
        "ring": [{"hash": h, "url": u} for h, u in ring]
    })

# ---------- Phase 1: File Upload & Download ----------
@app.post("/upload")
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "no file part"}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "empty filename"}), 400
    dest = STORAGE_DIR / f.filename
    f.save(dest)
    return jsonify({"status": "uploaded", "filename": f.filename})

@app.get("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(STORAGE_DIR, filename, as_attachment=False)

# ---------- Phase 2 & 3: KV Store with DHT routing ----------
@app.post("/kv")
def kv_put():
    data = request.get_json(silent=True) or {}
    key = data.get("key")
    value = data.get("value")
    if key is None or value is None:
        return jsonify({"error": "expected JSON with 'key' and 'value'"}), 400

    ring = get_ring()
    responsible = find_responsible_node(key, ring)

    if not is_me(responsible):
        # Forward to responsible node
        payload = {"key": key, "value": value}
        body, code = forward_json("POST", f"{responsible}/kv", json_payload=payload)
        return (body, code)

    # Store locally
    with kv_lock:
        kv_store[key] = value
    return jsonify({"status": "stored", "key": key, "value": value, "node": MY_URL})

@app.get("/kv/<path:key>")
def kv_get(key):
    ring = get_ring()
    responsible = find_responsible_node(key, ring)

    if not is_me(responsible):
        body, code = forward_json("GET", f"{responsible}/kv/{key}")
        return (body, code)

    with kv_lock:
        if key not in kv_store:
            return jsonify({"error": "key not found", "key": key}), 404
        value = kv_store[key]
    return jsonify({"key": key, "value": value, "node": MY_URL})

# Convenience: list local keys (debug)
@app.get("/kv")
def kv_list_local():
    with kv_lock:
        return jsonify({"local_node": MY_URL, "keys": kv_store})

# ---------- Main ----------
if __name__ == "__main__":
    # For local debugging only; in Docker we run via waitress.
    app.run(host="0.0.0.0", port=5000, debug=False)
