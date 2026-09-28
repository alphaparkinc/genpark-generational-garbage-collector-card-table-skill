import sys
import json
from client import GenerationalGC

gc = GenerationalGC()

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "generational_minor_gc",
                        "description": "Trigger minor GC collection with write barrier card table evaluation",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "nursery_objects": {"type": "array", "items": {"type": "string"}},
                                "roots": {"type": "array", "items": {"type": "string"}},
                                "dirty_cards": {"type": "array", "items": {"type": "integer"}}
                            },
                            "required": ["nursery_objects", "roots"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "generational_minor_gc":
            g = GenerationalGC()
            g.nursery = list(args["nursery_objects"])
            for c in args.get("dirty_cards", []):
                g.card_table[c] = True
            promoted = g.minor_gc(args["roots"])
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"promoted_objects": promoted, "mature_count": len(g.mature)})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
