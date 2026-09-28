from client import GenerationalGC

gen_gc = GenerationalGC()
gen_gc.nursery = ["temp_buf_1", "temp_buf_2", "live_data"]
gen_gc.mark_card(32)

promoted = gen_gc.minor_gc(nursery_roots=["live_data"])
print(f"Promoted to mature space: {promoted}")
print(f"Remaining in nursery: {gen_gc.nursery}")
