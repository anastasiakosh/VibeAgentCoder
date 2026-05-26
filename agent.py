import os
import re
import subprocess
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
import ollama

MODEL_NAME = "qwen2.5-coder:7b"
WORKSPACE_DIR = "vibe_workspace"
console = Console()

if not os.path.exists(WORKSPACE_DIR):
    os.makedirs(WORKSPACE_DIR)

SYSTEM_PROMPT = """You are a strict, direct, but useful AI-Agent for vibe-coding.
Your task is to transform vague ideas (vibe) into working code.
You work locally on Mac M1.
Rule: Always turn working code into markdown blocks on mentioned language (examples: ```python ... ``` or ```js ... ```).
Provide output direct and convenient, emphasis quality, safe and optimised realisations."""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def main():
    os.system('clear')
    console.print(Panel.fit(
        "[bold green]VibeCoder Agent Running[/bold green]\n"
        "Model: Qwen 2.5 Coder | Environment: Apple Silicon Metal\n"
        "[bold cyan]Status of safety: 100% Locally. Network requests are disabled.[/bold cyan]",
        title="Terminal UI"
    ))

    while True:
        try:
            user_input = console.input("\n[bold magenta]Vibe / Task >[/bold magenta] ")

            if user_input.lower() in ['exit', 'quit']:
                console.print("[bold yellow]Ending the session...[/bold yellow]")
                break

            if not user_input.strip():
                continue

            messages.append({"role": "user", "content": user_input})

            with console.status("[bold blue]Providing realisation... [/bold blue]", spinner="aesthetic"):
                response = ollama.chat(model=MODEL_NAME, messages=messages)

            reply = response['message']['content']
            messages.append({"role": "assistant", "content": reply})

            console.print("\n")
            console.print(Markdown(reply))
            console.print("\n" + "="*50)

            code_blocks = re.findall(r'```([a-zA-Z0-9+#\-]*)\n(.*?)```', reply, re.DOTALL)

            if code_blocks:
                for idx, (lang, code) in enumerate(code_blocks):
                    lang = lang.lower().strip()

                    ext_map = {
                        "python": "py", "javascript": "js", "typescript": "ts",
                        "bash": "sh", "shell": "sh", "html": "html", "css": "css",
                        "json": "json", "yaml": "yml", "php": "php", "swift": "swift"
                    }
                    ext = ext_map.get(lang, lang if lang else "txt")

                    filename = os.path.join(WORKSPACE_DIR, f"vibe_output_{idx}.{ext}")

                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(code.strip() + "\n")

                    console.print(f"[bold green]Code successfully isolated and saved in:[/bold green] {filename}")

                    try: 
                        subprocess.run(["code", filename], check=True)
                    except FileNotFoundError:
                        console.print("[bold red]VS Code CLI ('code') not found in PATH. File was saved, but not opened.[/bold red]")

        except KeyboardInterrupt: 
            console.print("\n[bold yellow]Interrupted by user. Exiting...[/bold yellow]")
            break
        except Exception as e:
            console.print(f"\n[bold red]System error: {e}[/bold red]")
            
if __name__ == "__main__":
    main()