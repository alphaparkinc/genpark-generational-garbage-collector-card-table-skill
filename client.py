"""Generational Garbage Collector with Card Table.
100% Python Standard Library.
"""

import collections

class GenerationalGC:
    """Two-generation GC (nursery + mature) with card table write barrier."""
    def __init__(self, card_size=16):
        self.nursery = []
        self.mature = []
        self.card_table = collections.defaultdict(bool)

    def mark_card(self, mature_obj_offset):
        card = mature_obj_offset // 16
        self.card_table[card] = True

    def minor_gc(self, nursery_roots):
        survivors = []
        for obj in self.nursery:
            if obj in nursery_roots or any(self.card_table.values()):
                self.mature.append(obj)
                survivors.append(obj)
        self.nursery.clear()
        self.card_table.clear()
        return survivors
