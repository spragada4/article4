"""
The retrieval core. This is the DSA heart of the project — build this in Phase 4.

Planned structure:
- TwoTierIndex: national baseline index (hash map keyed by topic), checked first,
  then a local override index (hash map keyed by (authority, topic)), checked second.
  Local results should be flagged as overriding national defaults when relevant
  (e.g. an Article 4 direction removing a permitted development right).
- Hybrid ranking: merge BM25/keyword score + embedding cosine similarity using a
  min-heap top-k merge instead of sorting the full result set.
- LRUCache: hash map + doubly linked list for repeated (authority, topic, query) lookups.
"""


class TwoTierIndex:
    def __init__(self) -> None:
        self.national: dict = {}
        self.local: dict = {}

    def add_national(self, topic: str, chunk: dict) -> None:
        raise NotImplementedError("Build in Phase 4")

    def add_local(self, authority: str, topic: str, chunk: dict) -> None:
        raise NotImplementedError("Build in Phase 4")

    def query(self, authority: str, topic: str, text: str, k: int = 5) -> list:
        raise NotImplementedError("Build in Phase 4")