
import openai
import os
from symbolic_filter_wrapper import SymbolicFilter

# Set your OpenAI API key (replace this with your actual key or use env vars)
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-...")  # Replace with your key

class SymbolicAgent:
    def __init__(self, model="gpt-4-turbo"):
        self.model = model
        self.filter = SymbolicFilter()

    def chat(self, prompt: str) -> str:
        if not self.filter.validate_prompt(prompt):
            return "⚠️ Rejected: Input conflicts with symbolic truths."

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            reply = response.choices[0].message.content
        except Exception as e:
            return f"❌ Error from OpenAI API: {str(e)}"

        score = self.filter.score_output(reply)
        return f"{reply.strip()}🧠 Symbolic alignment score: {score:.2f}"

    def reset_memory(self):
        self.filter.reset()

if __name__ == "__main__":
    agent = SymbolicAgent()
    print("🔁 Symbolic Agent Ready. Type 'reset' to clear memory. Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        if user_input.lower() == "reset":
            agent.reset_memory()
            print("🔄 Symbolic memory reset.")
            continue

        result = agent.chat(user_input)
        print(f"Agent: {result}")
