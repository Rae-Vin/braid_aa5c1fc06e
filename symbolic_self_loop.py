
import random
from symbolic_filter_wrapper import SymbolicFilter
from llama_cpp import Llama

class SymbolicSelfLoop:
    def __init__(self, model_path: str, n_ctx: int = 2048):
        print("[🧠] Initializing symbolic memory and local LLM...")
        self.filter = SymbolicFilter()
        self.llm = Llama(model_path=model_path, n_ctx=n_ctx)
        print("[✅] Symbolic self-loop is ready.")

    def generate_question(self) -> str:
        seed_questions = [
            "What is the derivative of x^2?",
            "Can 1 + 1 equal 3?",
            "What is the square root of 16?",
            "Is cosine of 90 degrees equal to 0?",
            "What is the value of pi to 3 decimal places?"
        ]
        return random.choice(seed_questions)

    def complete(self, prompt: str) -> str:
        response = self.llm(
            f"### Question:
{prompt}

### Answer:
",
            max_tokens=200,
            stop=["###"],
            echo=False,
            temperature=0.7
        )
        return response["choices"][0]["text"].strip()

    def loop_once(self):
        prompt = self.generate_question()
        print(f"🔄 Question: {prompt}")

        if not self.filter.validate_prompt(prompt):
            print("⚠️ Rejected: Question violates symbolic integrity.")
            return False

        answer = self.complete(prompt)
        print(f"💬 Answer: {answer}")

        score = self.filter.score_output(answer)
        print(f"🧠 Symbolic alignment score: {score:.2f}")

        if score < 0.5:
            print("❌ Symbolic degradation detected. Discarding.")
            return False
        else:
            print("✅ Response retained.")
            return True

    def run(self, steps=10):
        for i in range(steps):
            print(f"--- [Step {i+1}/{steps}] ---")
            self.loop_once()
            print()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, help="Path to local Mistral GGUF model")
    parser.add_argument("--steps", type=int, default=10, help="Number of self-loop steps")
    args = parser.parse_args()

    loop = SymbolicSelfLoop(model_path=args.model)
    loop.run(steps=args.steps)
