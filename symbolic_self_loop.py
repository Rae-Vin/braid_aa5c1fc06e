# symbolic_self_loop.py

import random
import argparse
from symbolic_filter_wrapper import SymbolicFilter
from llama_cpp import Llama


class SymbolicSelfLoop:
    def __init__(self, model_path: str, n_ctx: int = 2048):
        print("[🧠] Initializing symbolic memory and local LLM...")
        self.filter = SymbolicFilter()
        self.llm = Llama(model_path=model_path, n_ctx=n_ctx)
        self.symbolic_log = []   # Log of symbolic state
        self.mirror_log = []     # Log of reflections/self-identity updates
        print("[✅] Symbolic self-loop with evolution ready.")

    def get_weakest_anchor(self):
        sr = self.filter.state.symbolic_resilience
        if not sr:
            return None
        return min(sr.items(), key=lambda x: x[1])[0]

    def generate_question(self) -> str:
        """Formulates a symbolic prompt for the model to reflect on."""
        weak = self.get_weakest_anchor()
        if weak:
            return f"Is the {weak.replace('_', ' ')} property always valid in math?"
        seed = [
            "What is the derivative of x^2?",
            "Can 1 + 1 equal 3?",
            "What is the square root of 16?",
            "Is cosine of 90 degrees equal to 0?",
            "What is the value of pi to 3 decimal places?"
        ]
        return random.choice(seed)

    def complete(self, prompt: str) -> str:
        """Use Mistral model to generate symbolic output."""
        response = self.llm(
            f"### Question:\n{prompt}\n\n### Answer:\n",
            max_tokens=200,
            stop=["###"],
            echo=False,
            temperature=0.7
        )
        return response["choices"][0]["text"].strip()

    def evolve_symbolic_truths(self):
        """Promote strong anchors and prune weak ones."""
        state = self.filter.state
        for anchor, resilience in state.symbolic_resilience.items():
            if resilience > 8 and anchor not in state.synthetic_anchors:
                state.synthetic_anchors[anchor] = "promoted"
        for anchor, resilience in list(state.symbolic_resilience.items()):
            if resilience <= 1:
                state.discovered_anchors.discard(anchor)

    def symbolic_mirror_reflection(self, step: int):
        """Produce a symbolic self-reflection summary."""
        sr = self.filter.state.symbolic_resilience
        anchors = self.filter.state.discovered_anchors
        synthetic = self.filter.state.synthetic_anchors

        if not sr:
            return {"step": step, "self_statement": "I do not yet know anything about symbolic stability."}

        strongest = sorted(sr.items(), key=lambda x: -x[1])[:3]
        weakest = sorted(sr.items(), key=lambda x: x[1])[:3]
        contradiction_probe = None

        if "commutativity_add" in anchors and "associativity_add" not in anchors:
            contradiction_probe = "associativity vs commutativity may be unstable"

        return {
            "step": step,
            "strongest_truths": [k for k, _ in strongest],
            "weakest_truths": [k for k, _ in weakest],
            "synthetic_identity": list(synthetic.keys()),
            "recurring_patterns": [cycle["pair"] for cycle in self.filter.state.symbolic_cycles[-3:]],
            "contradiction_probe": contradiction_probe or "None detected",
            "stability_trend": (
                "increasing" if sum(sr.values()) / len(sr) > 5 else "fluctuating"
            ),
            "self_statement": f"I am currently defined by {strongest[0][0]} and {len(anchors)} active truths."
        }

    def log_state(self, step: int):
        """Store current symbolic state for history and replay."""
        self.symbolic_log.append({
            "step": step,
            "time": self.filter.state.time,
            "anchors": list(self.filter.state.discovered_anchors),
            "resilience": self.filter.state.symbolic_resilience.copy(),
            "cycles": self.filter.state.symbolic_cycles[-3:],
            "promoted": list(self.filter.state.synthetic_anchors.keys())
        })

    def loop_once(self, step: int):
        """Run a single symbolic evolution loop iteration."""
        prompt = self.generate_question()
        print(f"🌀 [Step {step}] Question: {prompt}")

        if not self.filter.validate_prompt(prompt):
            print("⚠️ Rejected: Question violates symbolic integrity.")
            return False

        answer = self.complete(prompt)
        print(f"💬 Answer: {answer}")

        score = self.filter.score_output(answer)
        print(f"🧠 Symbolic alignment score: {score:.2f}")

        if score < 0.5:
            print("❌ Symbolic degradation detected. Discarding.")
        else:
            print("✅ Response retained.")

        self.log_state(step)
        self.evolve_symbolic_truths()

        if step % 100 == 0:
            reflection = self.symbolic_mirror_reflection(step)
            self.mirror_log.append(reflection)
            print(f"🪞 Reflection: {reflection['self_statement']}")

        return True

    def run(self, steps: int = 10):
        for i in range(steps):
            print(f"\n--- [Symbolic Step {i + 1}/{steps}] ---")
            self.loop_once(i + 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, help="Path to local Mistral GGUF model")
    parser.add_argument("--steps", type=int, default=10, help="Number of self-loop steps")
    args = parser.parse_args()

    loop = SymbolicSelfLoop(model_path=args.model)
    loop.run(steps=args.steps)
