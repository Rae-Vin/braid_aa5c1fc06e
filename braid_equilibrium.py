# braid_equilibrium.py
import statistics

class BraidEquilibrium:
    def __init__(self):
        self.history = {
            "anchor_count": [],
            "fused_count": [],
            "mirror_coherence": [],
            "identity_shift": []
        }

    def update_metrics(self, anchors, fusions, mirror_log):
        self.history["anchor_count"].append(len(anchors))
        self.history["fused_count"].append(fusions)

        if len(mirror_log) >= 2:
            last = mirror_log[-1].get("self_statement", "")
            prev = mirror_log[-2].get("self_statement", "")
            coherence = 1.0 if last == prev else 0.0
            self.history["mirror_coherence"].append(coherence)

            last_set = set(mirror_log[-1].get("strongest", []))
            prev_set = set(mirror_log[-2].get("strongest", []))
            union = last_set.union(prev_set)
            shift = 1 - len(last_set.intersection(prev_set)) / max(len(union), 1)
            self.history["identity_shift"].append(shift)

    def calculate_stability_index(self):
        if len(self.history["anchor_count"]) < 3:
            return 0.5  # Default neutral stability when insufficient history

        recent_shift = statistics.mean(self.history["identity_shift"][-3:])
        recent_coherence = statistics.mean(self.history["mirror_coherence"][-3:])
        anchor_growth = (
            self.history["anchor_count"][-1] - self.history["anchor_count"][-3]
        ) / 3.0

        # Combine metrics into stability score
        score = (
            0.6 * recent_coherence
            + 0.3 * (1 - recent_shift)
            + 0.1 * (1 - abs(anchor_growth) / 10)
        )
        return round(max(0.0, min(1.0, score)), 3)

    def recommend_adjustments(self):
        stability = self.calculate_stability_index()
        fusion_rate = max(1, int(5 * (1 - stability)))
        reflection_interval = max(1, int(10 * (1 - stability)))
        return {
            "stability_index": stability,
            "recommended_fusion_rate": fusion_rate,
            "mirror_reflection_interval": reflection_interval
        }
