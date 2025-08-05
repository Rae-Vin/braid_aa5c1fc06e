
import random
from symbolic_filter_wrapper import SymbolicFilter
from llama_cpp import Llama

class SymbolicSelfLoop:
    def __init__(self, model_path: str, n_ctx: int = 2048):
        print("[🧠] Initializing symbolic memory and local LLM...")
        self.filter = SymbolicFilter()
        self.llm = Llama(model_path=model_path, n_ctx=n_ctx)
        self.symbolic_log = []  # In-memory log of symbolic state
        print("[✅] Symbolic self-loop with evolution ready.")

    def get_weakest_anchor(self):
        # Return the anchor with the lowest resilience
        sr = self.filter.state.symbolic_resilience
        if not sr:
            return None
        return min(sr.items(), key=lambda x: x[1])[0]

    def generate_question(self) -> str:
        # Adaptively generate a question based on symbolic gaps or weak areas
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
        response = self.llm(
            f"### Question:\n{prompt}\n\n### Answer:\n",
            max_tokens=200,
            stop=["###"],
            echo=False,
            temperature=0.7
        )
        return response["choices"][0]["text"].strip()

    def evolve_symbolic_truths(self):
        # Conservatively promote or demote symbolic truths
        state = self.filter.state
        for anchor, resilience in state.symbolic_resilience.items():
            if resilience > 8 and anchor not in state.synthetic_anchors:
                state.synthetic_anchors[anchor] = "promoted"
        for anchor, resilience in list(state.symbolic_resilience.items()):
            if resilience <= 1:
                state.discovered_anchors.discard(anchor)

    def log_state(self, step):
        self.symbolic_log.append({
            "step": step,
            "time": self.filter.state.time,
            "anchors": list(self.filter.state.discovered_anchors),
            "resilience": self.filter.state.symbolic_resilience.copy(),
            "cycles": self.filter.state.symbolic_cycles[-3:],
            "promoted": list(self.filter.state.synthetic_anchors.keys())
        })

    def loop_once(self, step):
        prompt = self.generate_question()
        print(f"🔄 [Step {step}] Question: {prompt}")

        if not self.filter.validate_prompt(prompt):
            print("⚠️ Rejected: Question violates symbolic integrity.")
            return

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

    def run(self, steps=10):
        for i in range(steps):
            print(f"--- [Symbolic Step {i+1}/{steps}] ---")
            self.loop_once(i + 1)
            print()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, help="Path to local Mistral GGUF model")
    parser.add_argument("--steps", type=int, default=10, help="Number of self-loop steps")
    args = parser.parse_args()

    loop = SymbolicSelfLoop(model_path=args.model)
    loop.run(steps=args.steps)
