# braid_pipeline_runner.py

from symbolic_self_loop import SymbolicSelfLoop
from anchor_tracker import track_emergence
from semantic_cluster import cluster_anchors
from capability_mapper import map_cluster_to_capability
from language_fusion import fuse_with_llm

import os
import json

MODEL_PATH = "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
RUN_DIR = "braid_pipeline_logs"
STEPS = 1000
CLUSTER_K = 5

os.makedirs(RUN_DIR, exist_ok=True)

loop = SymbolicSelfLoop(model_path=MODEL_PATH)
llm = loop.llm

print(f"[🚀] Starting symbolic simulation batch for {STEPS} steps...")
for step in range(1, STEPS + 1):
    loop.loop_once(step)

    if step % 250 == 0:
        print(f"\n[🔍] Analyzing symbolic state at step {step}...")

        anchors = list(loop.filter.state.discovered_anchors)
        fingerprints = loop.filter.state.symbolic_resilience
        compiled = [
            {
                "anchor": a,
                "expression": a,
                "tier": fingerprints.get(a, 0),
                "quantized_fingerprint": [fingerprints.get(a, 0)] * 4
            } for a in anchors
        ]

        clusters = cluster_anchors(compiled, k=CLUSTER_K)

        for idx, cluster in enumerate(clusters):
            cap = map_cluster_to_capability(cluster)
            output = fuse_with_llm(cap, cluster, llm)

            print(f"\n[🧠] Cluster {idx+1} Capability: {cap}")
            print(f"[🗣️] Generated Output:\n{output}")

            with open(os.path.join(RUN_DIR, f"step_{step}_cluster_{idx+1}.json"), "w") as f:
                json.dump({
                    "step": step,
                    "capability": cap,
                    "anchor_expressions": [a["expression"] for a in cluster],
                    "generated": output
                }, f, indent=2)

print("\n✅ Simulation batch complete.")
