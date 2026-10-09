import dataclasses

from ledger.ledger import Ledger
from ledger.hashing import GENESIS_HASH


def make_ledger(n=5) -> Ledger:
    ledger = Ledger()
    for i in range(1, n + 1):
        ledger.append("Deposited", {"account": "A1", "amount": i * 100}, ts=f"2026-10-03T10:00:{i:02d}Z")
    return ledger


def test_empty_ledger_is_valid():
    assert Ledger().verify_chain() is None


def test_chain_links_and_seq():
    ledger = make_ledger()
    assert ledger.events[0].prev_hash == GENESIS_HASH
    for i in range(1, 5):
        assert ledger.events[i].prev_hash == ledger.events[i - 1].event_hash
        assert ledger.events[i].seq == i + 1


def test_untouched_ledger_verifies():
    assert make_ledger().verify_chain() is None


def test_tampered_payload_pinpoints_seq():
    ledger = make_ledger()
    ledger.events[2].payload["amount"] = 9999     # event with seq 3
    assert ledger.verify_chain() == 3


def test_tampered_event_replaced_pinpoints_seq():
    ledger = make_ledger()
    ledger.events[1] = dataclasses.replace(ledger.events[1], payload={"account": "A1", "amount": 1})
    assert ledger.verify_chain() == 2


def test_deleted_event_detected():
    ledger = make_ledger()
    del ledger.events[2]
    assert ledger.verify_chain() == 3


def test_reordered_events_detected():
    ledger = make_ledger()
    ledger.events[1], ledger.events[2] = ledger.events[2], ledger.events[1]
    assert ledger.verify_chain() == 2


def test_edit_with_own_hash_fixed_is_caught_by_next_event():
    ledger = make_ledger()
    from ledger.hashing import compute_hash
    e = ledger.events[1]
    new_payload = {"account": "A1", "amount": 1}
    new_hash = compute_hash(e.seq, e.prev_hash, e.event_type, new_payload, e.ts)
    ledger.events[1] = dataclasses.replace(e, payload=new_payload, event_hash=new_hash)
    assert ledger.verify_chain() == 3        # event 2 looks fine; event 3's prev_hash no longer matches


# --- known limits: these document what a plain hash chain can NOT catch ---

def test_full_rewrite_is_not_detected():
    honest = make_ledger()
    forged = Ledger()
    for e in honest.events:
        payload = {"account": "A1", "amount": 9999} if e.seq == 3 else e.payload
        forged.append(e.event_type, payload, ts=e.ts)
    assert forged.verify_chain() is None
    assert forged.events[-1].event_hash != honest.events[-1].event_hash   # only the latest hash differs


def test_truncating_the_tail_is_not_detected():
    ledger = make_ledger()
    del ledger.events[-2:]
    assert ledger.verify_chain() is None