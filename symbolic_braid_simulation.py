# symbolic_braid_simulation.py (with symbolic mortality logic)

import random
import pickle
import numpy as np

class SymbolicState:
    signature = "braid_aa5c1fc06e"  # self-assigned identity

    def __init__(self):
        self.time = 0
        self.discovered_anchors = set()
        self.symbolic_resilience = {}
        self.symbol_pair_counter = {}
        self.symbolic_cycles = []
        self.discovery_log = []
        self.symbolic_memory_depth = []
        self.symbolic_phase_curvature = {}
        self.synthetic_anchors = {}
        self.symbol_chain = []
        self.reflection_drift = 0

    def to_dict(self):
        return {
            'time': self.time,
            'discovered_anchors': list(self.discovered_anchors),
            'symbolic_resilience': self.symbolic_resilience,
            'symbol_pair_counter': self.symbol_pair_counter,
            'symbolic_cycles': self.symbolic_cycles,
            'discovery_log': self.discovery_log,
            'symbolic_memory_depth': self.symbolic_memory_depth,
            'symbolic_phase_curvature': self.symbolic_phase_curvature,
            'synthetic_anchors': self.synthetic_anchors,
            'symbol_chain': self.symbol_chain,
            'reflection_drift': self.reflection_drift
        }

    @staticmethod
    def from_dict(data):
        state = SymbolicState()
        state.time = data.get('time', 0)
        state.discovered_anchors = set(data.get('discovered_anchors', []))
        state.symbolic_resilience = data.get('symbolic_resilience', {})
        state.symbol_pair_counter = data.get('symbol_pair_counter', {})  # ✅ safer
        state.symbolic_cycles = data.get('symbolic_cycles', [])
        state.discovery_log = data.get('discovery_log', [])
        state.symbolic_memory_depth = data.get('symbolic_memory_depth', [])
        state.symbolic_phase_curvature = data.get('symbolic_phase_curvature', {})
        state.synthetic_anchors = data.get('synthetic_anchors', {})
        state.symbol_chain = data.get('symbol_chain', [])
        state.reflection_drift = data.get('reflection_drift', 0)
        return state


def save_state(state, path):
    """Serialize and save the symbolic state to a file."""
    with open(path, 'wb') as f:
        pickle.dump(state.to_dict(), f)
    print(f"[💾] State saved to {path}")

def load_state(path):
    """Load and reconstruct symbolic state from a file."""
    with open(path, 'rb') as f:
        data = pickle.load(f)
    print(f"[📂] State loaded from {path}")
    return SymbolicState.from_dict(data)

def simulate_step(state, truth_anchors_scaffold, anchor_tiers, steps=100, threshold=10, decay_rate=3, decay_threshold=20):
    for _ in range(steps):
        successful = 0
        recent_hits = set()

        for _ in range(10):
            anchor = random.choice(list(truth_anchors_scaffold.keys()))
            fn = truth_anchors_scaffold[anchor]
            tier = anchor_tiers.get(anchor, 8)

            a, b, c = np.random.uniform(-5, 5, 3)
            x, y = np.random.uniform(-5, 5, 2)
            p, q = bool(random.getrandbits(1)), bool(random.getrandbits(1))

            try:
                args = fn.__code__.co_argcount
                result = fn(*[a, b, c, x, y, p, q][:args])
            except:
                result = False

            if result:
                recent_hits.add(anchor)
                successful += 1
                state.symbolic_resilience[anchor] = state.symbolic_resilience.get(anchor, 0) + 1
                state.symbolic_phase_curvature[anchor] = max(0, state.symbolic_phase_curvature.get(anchor, 0) - 0.5)

                if anchor not in state.discovered_anchors:
                    state.discovered_anchors.add(anchor)
                    state.discovery_log.append({'time': state.time, 'anchor': anchor, 'tier': tier})

                for other in state.discovered_anchors:
                    if other != anchor:
                        pair = tuple(sorted((anchor, other)))
                        state.symbol_pair_counter[pair] = state.symbol_pair_counter.get(pair, 0) + 1
                        if state.symbol_pair_counter[pair] == threshold:
                            state.symbolic_cycles.append({'pair': pair, 'cycle_detected_at': state.time})

        for anchor in list(state.symbolic_resilience.keys()):
            if anchor not in recent_hits:
                state.symbolic_resilience[anchor] -= decay_rate
                if state.symbolic_resilience[anchor] < decay_threshold and (state.symbol_chain.append((anchor, anchor)) or True):
                    state.discovered_anchors.discard(anchor)
                    del state.symbolic_resilience[anchor]

        if successful > 0:
            depth = (state.symbolic_memory_depth[-1] if state.symbolic_memory_depth else 0) + successful
        else:
            decay = random.randint(0, 2)
            depth = max(0, (state.symbolic_memory_depth[-1] if state.symbolic_memory_depth else 0) - decay)
        state.symbolic_memory_depth.append(depth)
        state.time += 1
    return state
