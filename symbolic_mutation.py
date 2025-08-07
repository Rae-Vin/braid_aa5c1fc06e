# symbolic_mutation.py

from hashlib import sha256
import random
import copy

def mutate_anchor(anchor, step_seed):
    """Apply symbolic mutation to a given anchor based on a deterministic seed."""
    mutation = copy.deepcopy(anchor)
    random.seed(step_seed)

    ops = ["+", "-", "*", "/", "^", "ε"]
    expression = mutation["expression"]

    # Recursive epsilon stacking or operator mutation
    if random.random() < 0.5:
        # ε stack scaling
        mutation["expression"] = f"({expression}) + ε^{mutation['tier'] + 1}"
    else:
        # Swap one operator
        op_to_replace = random.choice(ops[:4])  # Avoid ε and ^ for base replacements
        op_new = random.choice([op for op in ops if op != op_to_replace])
        mutation["expression"] = expression.replace(op_to_replace, op_new, 1)

    # Update fingerprint with bounded entropy
    mutation["quantized_fingerprint"] = [
        max(0, min(255, v + random.randint(-15, 15))) for v in mutation["quantized_fingerprint"]
    ]

    # Rename and re-ID the mutation
    mutation["name"] = f"{anchor['name']}_mut_{step_seed}"
    combined_str = mutation["name"] + mutation["expression"]
    mutation["id"] = sha256(combined_str.encode()).hexdigest()[:12]
    mutation["tier"] = anchor["tier"] + 1

    return mutation

def apply_stability_pressure(anchors, stability_index, step):
    """Return a mutated anchor if symbolic stasis exceeds the threshold."""
    if stability_index >= 0.95 and len(anchors) >= 1:
        candidate = random.choice(anchors)
        return mutate_anchor(candidate, step)
    return None
