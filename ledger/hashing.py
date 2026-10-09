import hashlib
import json
from datetime import datetime, timezone

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

GENESIS_HASH="0"*64 #prev_hash for 1st event

def canonical_json(obj)->str:
    return json.dumps(obj, sort_keys=True, separators=(",",":"),ensure_ascii=False)

def compute_hash(seq: int, prev_hash: str, event_type: str, payload: dict, ts: str )->str:
    body = canonical_json({"seq":seq, "event_type": event_type, "payload": payload, "ts": ts})
    return hashlib.sha256((prev_hash+body).encode("utf-8")).hexdigest()