import json
import os

def get_offline_protocol(query: str) -> str:
    path = os.path.join(os.path.dirname(__file__), "fallback_protocols.json")
    if not os.path.exists(path):
        return "Offline protocols file missing."
    
    with open(path, "r") as f:
        protocols = json.load(f)
    
    query_lower = query.lower()
    for key, text in protocols.items():
        if key in query_lower:
            return text
            
    return "Standard Protocol: Keep patient calm, monitor breathing, apply direct pressure to wounds, and call campus security immediately."