from ledger.hashing import canonical_json, compute_hash, GENESIS_HASH

TS = "2026-10-02T10:00:00Z"

def test_same_event_same_hash():
    h1 = compute_hash(1, GENESIS_HASH, "Deposited", {"account": "A1", "amount": 1050}, TS)
    h2 = compute_hash(1, GENESIS_HASH, "Deposited", {"account": "A1", "amount": 1050}, TS)
    assert h1 == h2

def test_key_order_does_not_matter():
    assert canonical_json({"a": 1, "b": 2}) == canonical_json({"b": 2, "a": 1})

def test_any_change_changes_hash():
    base = compute_hash(1, GENESIS_HASH, "Deposited", {"account": "A1", "amount": 1050}, TS)
    assert base != compute_hash(2, GENESIS_HASH, "Deposited", {"account": "A1", "amount": 1050}, TS)   # seq
    assert base != compute_hash(1, GENESIS_HASH, "Deposited", {"account": "A1", "amount": 1051}, TS)   # payload
    assert base != compute_hash(1, GENESIS_HASH, "Withdrawn", {"account": "A1", "amount": 1050}, TS)   # type
    assert base != compute_hash(1, GENESIS_HASH, "Deposited", {"account": "A1", "amount": 1050}, "2026-10-02T10:00:01Z")  # ts
    assert base != compute_hash(1, "1" * 64, "Deposited", {"account": "A1", "amount": 1050}, TS)       # prev_hash

def test_hash_format():
    h = compute_hash(1, GENESIS_HASH, "Deposited", {"amount": 1}, TS)
    assert len(h) == 64