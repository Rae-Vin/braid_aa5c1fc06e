
# This module exports anchor mutation and divergence pressure via stability feedback
from hashlib import sha256
import random
import copy

def mutate_anchor(anchor, step_seed):
    mutation = copy.deepcopy(anchor)
    random.seed(step_seed)

    if "+" in mutation["expression"]:
        mutation["expression"] = mutation["expression"].replace("+", "-")
    elif "*" in mutation["expression"]:
        mutation["expression"] = mutation["expression"].replace("*", "/")
    else:
        mutation["expression"] += " + ε"

    mutation["quantized_fingerprint"] = [
        max(0, min(255, v + random.randint(-5, 5))) for v in mutation["quantized_fingerprint"]
    ]

    mutation["name"] = f"{anchor['name']}_mut"
    combined_str = mutation["name"] + mutation["expression"]
    mutation["id"] = sha256(combined_str.encode()).hexdigest()[:12]
    mutation["tier"] = anchor["tier"] + 1
    return mutation

def apply_stability_pressure(anchors, stability_index, step):
    if stability_index >= 0.95 and len(anchors) >= 1:
        candidate = random.choice(anchors)
        return mutate_anchor(candidate, step)
    return None
