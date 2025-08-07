# symbolic_filter_wrapper.py

import os
import pickle
import argparse
import numpy as np
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import uvicorn

from truth_anchors import truth_anchors_scaffold
from symbolic_braid_simulation import SymbolicState, simulate_step


class SymbolicFilter:
    def __init__(self, state_path="braid_state.pkl"):
        self.state_path = state_path
        self.state = self._load_or_initialize_state()

    def _load_or_initialize_state(self):
        if os.path.exists(self.state_path):
            with open(self.state_path, 'rb') as f:
                print("[SymbolicFilter] Loaded existing symbolic state.")
                return pickle.load(f)
        print("[SymbolicFilter] Created new symbolic state.")
        return SymbolicState()

    def _save_state(self):
        with open(self.state_path, 'wb') as f:
            pickle.dump(self.state, f)

    def simulate_symbolic_response(self, prompt: str):
        """
        Simulates the symbolic output of a prompt to evaluate its impact on anchor growth.
        This creates a temporary state for evaluation purposes without modifying the actual state.
        """
        import copy
        simulated_state = copy.deepcopy(self.state)
        simulate_step(simulated_state, truth_anchors_scaffold, {"user_prompt": prompt}, steps=1)
        return simulated_state

    def validate_prompt(self, prompt):
        """Validate if the generated prompt introduces novelty."""
        if not prompt:
            return False

        try:
            original_depth = len(self.state.get("discovered_anchors", {}))
        except Exception as e:
            print(f"⚠️ Error accessing discovered_anchors: {e}")
            return False

        simulated = self.simulate_symbolic_response(prompt)
        new_depth = len(simulated.get("discovered_anchors", {}))

        delta = new_depth - original_depth
        print(f"📈 Prompt validation: symbolic delta = {delta}")
        return delta > 0

    def score_output(self, output: str) -> float:
        """Runs a simulation step, then returns average symbolic resilience as a score."""
        simulate_step(self.state, truth_anchors_scaffold, {}, steps=1)
        self._save_state()
        resilience = list(self.state.symbolic_resilience.values())
        if resilience:
            return float(np.mean(resilience))
        return 0.0

    def reset(self):
        self.state = SymbolicState()
        self._save_state()
        print("[SymbolicFilter] Symbolic state has been reset.")


# ---------- API MODE ----------
app = FastAPI()
symbolic_filter = SymbolicFilter()

class InputPayload(BaseModel):
    prompt: Optional[str] = None
    output: Optional[str] = None

@app.post("/validate")
def validate(input: InputPayload):
    if not input.prompt:
        return {"error": "Missing prompt"}
    result = symbolic_filter.validate_prompt(input.prompt)
    return {"valid": result}

@app.post("/score")
def score(input: InputPayload):
    if not input.output:
        return {"error": "Missing output"}
    score = symbolic_filter.score_output(input.output)
    return {"score": score}

@app.post("/reset")
def reset():
    symbolic_filter.reset()
    return {"status": "reset complete"}


# ---------- ENTRY ----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true", help="Run as REST API service")
    args = parser.parse_args()

    if args.serve:
        print("[SymbolicFilter] Starting REST API server on http://localhost:8000")
        uvicorn.run("symbolic_filter_wrapper:app", host="0.0.0.0", port=8000, reload=False)
