# anchor_tracker.py

def track_emergence(state):
    emergence_data = []
    for anchor in state.discovery_log[-50:]:
        expression = anchor.get("expression", "")
        tier = anchor.get("tier", 0)
        score = len(set(expression)) + tier * 0.5
        emergence_data.append((anchor["anchor"], score))
    return sorted(emergence_data, key=lambda x: -x[1])
