from dataclasses import dataclass

@dataclass(frozen=True) #makes event immutable
class Event:
    seq: int 
    ts: str
    event_type: str #deposited/transferPosted
    prev_hash: str
    event_hash: str
