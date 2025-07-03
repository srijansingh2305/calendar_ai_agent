# nodes/slots.py
REQUIRED_SLOTS = ["person", "date", "time", "duration", "location", "purpose"]

def is_slot_filled(slots: dict, slot: str) -> bool:
    return slot in slots and slots[slot] not in [None, ""]

def all_slots_filled(slots: dict) -> bool:
    return all(slot in slots and slots[slot] for slot in REQUIRED_SLOTS)

