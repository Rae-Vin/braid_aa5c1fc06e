# capability_mapper.py

def map_cluster_to_capability(cluster):
    anchor_exprs = [a["expression"] for a in cluster]
    if any("^" in e or "ε" in e for e in anchor_exprs):
        return "recursive_reasoning"
    elif all("+" in e or "-" in e for e in anchor_exprs):
        return "arithmetic_simplification"
    elif any("if" in e for e in anchor_exprs):
        return "logic_proof"
    elif any("¬" in e or "∧" in e for e in anchor_exprs):
        return "logical_consistency"
    else:
        return "symbolic_reflection"
