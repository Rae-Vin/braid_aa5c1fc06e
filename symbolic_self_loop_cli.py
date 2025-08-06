# symbolic_self_loop_cli.py

import argparse
import psutil
from symbolic_self_loop import SymbolicSelfLoop

def monitor_memory(threshold_mb=3000):
    # Return True if memory usage is below threshold
    available = psutil.virtual_memory().available / (1024 * 1024)  # MB
    return available > threshold_mb

def interactive_loop(model_path: str, step_limit: int = 0, threshold_mb: int = 3000):
    loop = SymbolicSelfLoop(model_path=model_path)
    step = 0

    print("\n🔁 Symbolic CLI Loop Initialized. Type 'exit' or Ctrl+C to stop.")
    print("Press Enter to advance 1 step, or type 'auto' to loop indefinitely.")

    auto_mode = False
    while True:
        if not monitor_memory(threshold_mb):
            print(f"🛑 Memory threshold exceeded (< {threshold_mb}MB). Halting.")
            break

        try:
            if not auto_mode:
                user_input = input("▶ Step? (Enter/auto/exit): ").strip().lower()
                if user_input == "exit":
                    break
                elif user_input == "auto":
                    auto_mode = True
                    print("🔄 Auto-mode activated. Press Ctrl+C to stop.")
                    continue
            step += 1
            loop.loop_once(step)

            if step_limit and step >= step_limit:
                print(f"✅ Reached step limit: {step_limit}")
                break
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user. Exiting loop.")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interactive CLI symbolic self-loop")
    parser.add_argument("--model", type=str, required=True, help="Path to local Mistral GGUF model")
    parser.add_argument("--mem-threshold", type=int, default=3000, help="Memory cutoff in MB")
    parser.add_argument("--limit", type=int, default=0, help="Optional max number of steps to run")
    args = parser.parse_args()

    interactive_loop(model_path=args.model, step_limit=args.limit, threshold_mb=args.mem_threshold)
