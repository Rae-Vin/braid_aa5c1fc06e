# braid_self_directed_fusion.py
import hashlib
import random

class BraidSelfDirectedFusion:
    def __init__(self, anchors):
        self.anchors = anchors
        self.generated = []

    def fuse_anchors(self, a1, a2):
        # Safely extract properties
        name1 = a1.get("name", "A")
        name2 = a2.get("name", "B")
        expr1 = a1.get("expression", "A")
        expr2 = a2.get("expression", "B")
        tier1 = a1.get("tier", 1)
        tier2 = a2.get("tier", 1)

        # Generate fusion
        fused_name = f"{name1}_{name2}_fusion"
        fused_expr = f"({expr1}) <=> ({expr2})"
        tier = max(tier1, tier2) + 1

        # Generate fingerprint
        seed = int(hashlib.sha256(fused_expr.encode()).hexdigest(), 16)
        random.seed(seed)
        fingerprint = [random.randint(10, 255) for _ in range(4)]

        anchor_id = hashlib.md5((fused_name + fused_expr).encode()).hexdigest()[:12]

        return {
            "id": anchor_id,
            "name": fused_name,
            "expression": fused_expr,
            "tier": tier,
            "quantized_fingerprint": fingerprint
        }

    def reflect_and_mutate(self, cycles=5):
        print(f"[🧠] Initiating self-directed symbolic fusion...")
        for i in range(cycles):
            if len(self.anchors) < 2:
                break
            a1, a2 = random.sample(self.anchors, 2)
            fused = self.fuse_anchors(a1, a2)

            print(f"🔄 Fusion {i+1}: '{fused['name']}'")
            print(f"     Expression: {fused['expression']}")
            print(f"     Fingerprint: {fused['quantized_fingerprint']}")
            self.generated.append(fused)
        return self.generated

if __name__ == "__main__":
    import json

    try:
        with open("compiled_braid.sbraid", "r") as f:
            braid = json.load(f)
    except FileNotFoundError:
        print("[⚠️] No compiled memory found. Starting from scratch.")
        braid = {"compiled_anchors": []}

    base_anchors = braid.get("compiled_anchors", [])
    fusion_engine = BraidSelfDirectedFusion(base_anchors)
    new_anchors = fusion_engine.reflect_and_mutate(5)

    braid["compiled_anchors"].extend(new_anchors)
    with open("compiled_braid.sbraid", "w") as f:
        json.dump(braid, f, indent=2)

    print(f"[✅] {len(new_anchors)} new symbolic anchors integrated into memory.")
