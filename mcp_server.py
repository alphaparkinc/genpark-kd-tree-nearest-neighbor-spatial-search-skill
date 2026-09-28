import sys
import json
from client import KDTree

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-kd-tree-nearest-neighbor-spatial-search-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "kd_tree_knn_search",
                        "description": "Build KD-Tree and perform k-Nearest Neighbor search",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "dataset": {"type": "array", "items": {"type": "object", "properties": {"point": {"type": "array", "items": {"type": "number"}}, "data": {"type": "string"}}}, "description": "Dataset of points with labels"},
                                "query_point": {"type": "array", "items": {"type": "number"}, "description": "Target coordinate"},
                                "k": {"type": "integer", "default": 3, "description": "Number of nearest neighbors"}
                            },
                            "required": ["dataset", "query_point"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "kd_tree_knn_search":
            dataset = [(item["point"], item.get("data", "")) for item in args.get("dataset", [])]
            query = args.get("query_point", [])
            k = args.get("k", 3)
            tree = KDTree(dataset, k=len(query))
            knn = tree.k_nearest_neighbors(query, k=k)
            res = [{"point": p, "data": d, "distance": dist} for p, d, dist in knn]
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(res)}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
