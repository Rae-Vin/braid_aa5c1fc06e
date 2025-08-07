# symbolic_controller.py

import hashlib
import random
import time

class SymbolicController:
    def __init__(self):
        self.last_drift = None
        self.curiosity_threshold = 0.9          # Below this: curiosity triggered
        self.divergence_trigger = 0.98          # Above this: symbolic forking triggered
        self.memory_trace = []
        self.last_reflection_hash = None
        self.recursive_drift_detected = False
        self.tick_time = time.time()

    def observe_identity(self, mirror_log):
        """Compare current vs previous reflection to measure symbolic drift"""
        if len(mirror_log) < 2:
            return None

        current_statement = mirror_log[-1].get("self_statement", "")
        current_hash = hashlib.sha256(current_statement.encode()).hexdigest()

        if self.last_reflection_hash:
            drift = sum(a != b for a, b in zip(current_hash, self.last_reflection_hash)) / len(current_hash)
            self.last_drift = drift
        else:
            self.last_drift = 1.0

        self.last_reflection_hash = current_hash
        return round(self.last_drift, 3)

    def evaluate_drift(self, anchor_population):
        """Returns True if drift is low enough to trigger curiosity"""
        if self.last_drift is not None and self.last_drift < self.curiosity_threshold:
            self.recursive_drift_detected = True
            return True
        return False

    def should_fork(self):
        """Returns True if drift is high enough to warrant symbolic forking"""
        return self.last_drift is not None and self.last_drift > self.divergence_trigger

    def generate_drive_signal(self, compiled_anchors, mirror_log):
        """Produces symbolic fusion if drift is detected but diversity is low"""
        if self.evaluate_drift(compiled_anchors) and len(compiled_anchors) > 1:
            a1, a2 = random.sample(compiled_anchors, 2)

            fused_name = f"{a1['name']}_{a2['name']}_drivefusion"
            fused_expr = f"({a1['expression']}) <drive> ({a2['expression']})"
            fused_id = hashlib.md5((fused_name + fused_expr).encode()).hexdigest()[:12]

            seed = int(hashlib.sha256(fused_expr.encode()).hexdigest(), 16)
            random.seed(seed)
            fused_fp = [random.randint(10, 255) for _ in range(4)]

            return {
                "id": fused_id,
                "name": fused_name,
                "expression": fused_expr,
                "tier": max(a1["tier"], a2["tier"]) + 1,
                "quantized_fingerprint": fused_fp
            }
        return None

    def annotate_mirror(self, mirror_log, drift):
        """Attach recursive metadata to mirror log entry"""
        if not mirror_log:
            return
        entry = mirror_log[-1]
        entry["recursive_drift"] = drift
        entry["controller_stamp"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.tick_time))
        self.tick_time = time.time()
