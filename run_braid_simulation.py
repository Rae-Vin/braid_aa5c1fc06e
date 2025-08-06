# run_braid_simulation.py

import argparse
import os
from symbolic_braid_simulation import SymbolicState, simulate_step, save_state, load_state
from truth_anchors import truth_anchors_scaffold, anchor_tiers, symbolic_environment, observe_environment

def run_simulation(steps, state_path):
    if os.path.exists(state_path):
        print(f"[INFO] Loading existing simulation state from: {state_path}")
        state = load_state(state_path)
    else:
        print("[INFO] Initializing new simulation state.")
        state = SymbolicState()

    print(f"[INFO] Running simulation for {steps} steps...")

    interval = 500  # Smaller intervals allow for periodic output and flexibility
    for i in range(0, steps, interval):
        simulate_step(state, truth_anchors_scaffold, anchor_tiers, steps=interval)
        observe_environment(state, symbolic_environment, truth_anchors_scaffold)

        current_depth = state.symbolic_memory_depth[-1] if state.symbolic_memory_depth else 0
        most_resilient = (
            max(state.symbolic_resilience.items(), key=lambda x: x[1])
            if state.symbolic_resilience else (None, 0)
        )

        print(f"[STEP {state.time}] ➤ Symbols: {len(state.discovered_anchors)} | "
              f"Cycles: {len(state.symbolic_cycles)} | Depth: {current_depth} | "
              f"Most Stable: {most_resilient[0]} ({most_resilient[1]})")

        if state.symbolic_cycles:
            last_cycle = state.symbolic_cycles[-1]
            print(f"  [REFLECTION] Detected between {last_cycle['pair']} at step {last_cycle['cycle_detected_at']}")

    save_state(state, state_path)
    print(f"[INFO] Simulation complete. State saved to: {state_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run persistent symbolic braid simulation.")
    parser.add_argument("--steps", type=int, default=1000, help="Number of steps to simulate")
    parser.add_argument("--state", type=str, default="braid_state.pkl", help="Path to save/load state")
    args = parser.parse_args()

    run_simulation(args.steps, args.state)
