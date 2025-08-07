# symbolic_mistral_agent.py

from llama_cpp import Llama
from symbolic_filter_wrapper import SymbolicFilter

class SymbolicLLM:
    def __init__(self, model_path: str, n_ctx: int = 2048):
        print("[🔄] Loading Mistral model...")
        self.llm = Llama(model_path=model_path, n_ctx=n_ctx)
        self.filter = SymbolicFilter()
        print("[✅] Mistral + Braid initialized.")

    def ask(self, prompt: str) -> str:
        # Validate the prompt against symbolic memory
        if not self.filter.validate_prompt(prompt):
            return "⚠️ Prompt rejected: violates symbolic constraints."

        # Generate output from Mistral
        response = self.llm(
            f"### Question:{prompt}### Answer:",
            max_tokens=200,
            stop=["###"],
            echo=False,
            temperature=0.7,
        )
        output = response["choices"][0]["text"].strip()

        # Score symbolic alignment of the response
        score = self.filter.score_output(output)
        return f"{output} 🧠 Symbolic alignment score: {score:.2f}"

    def reset_symbolic_memory(self):
        self.filter.reset()


# Optional CLI interaction
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, help="Path to Mistral GGUF model file")
    args = parser.parse_args()

    agent = SymbolicLLM(model_path=args.model)

    print("🔁 Symbolic LLM loop active. Type 'reset' to clear memory. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        if user_input.lower() == "reset":
            agent.reset_symbolic_memory()
            print("🔄 Symbolic memory reset.")
            continue

        result = agent.ask(user_input)
        print(f"Agent: {result}")
