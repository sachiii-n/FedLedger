import copy

from ledger.events import Event
from ledger.hashing import compute_hash, GENESIS_HASH, utc_now_iso


class Ledger:
    def __init__(self):
        self.events: list[Event] = []

    def append(self, event_type: str, payload: dict, ts: str | None = None) -> Event:
        ts = ts or utc_now_iso()
        seq = len(self.events) + 1
        prev_hash = self.events[-1].event_hash if self.events else GENESIS_HASH
        payload = copy.deepcopy(payload) #stops caller form changing later by editing
        event_hash = compute_hash(seq, prev_hash, event_type, payload, ts)

        event = Event(
            seq=seq,
            ts=ts,
            event_type=event_type,
            payload=payload,
            prev_hash=prev_hash,
            event_hash=event_hash,
        )
        self.events.append(event)
        return event

    def verify_chain(self) -> int | None:
        """Return the seq of the first bad event, or None if the chain is valid."""
        expected_prev = GENESIS_HASH
        for i, e in enumerate(self.events):
            position = i + 1 # not e.seq as it can also be tampered with
            if e.seq != position:
                return position
            if e.prev_hash != expected_prev:
                return position
            recomputed = compute_hash(e.seq, e.prev_hash, e.event_type, e.payload, e.ts)
            if recomputed != e.event_hash:
                return position
            expected_prev = e.event_hash
        return None