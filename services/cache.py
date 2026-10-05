"""Tiny in-memory TTL cache that avoids repeated API calls during a search session."""
import time
from config import Config

_store = {}
def get(key):
    item = _store.get(key)
    if item and time.time() - item[0] < Config.CACHE_TTL: return item[1]
    _store.pop(key, None); return None
def set(key, value): _store[key] = (time.time(), value)
