import os
import re
import subprocess
import threading
import http.server
import socketserver
import webbrowser
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
import ollama

MODEL_NAME = "qwen2.5-coder:7b"
WORKSPACE_DIR = "vibe_workspace"
PORT = 8000
console = Console()

if not os.path.exists(WORKSPACE_DIR):
    os.makedirs(WORKSPACE_DIR)

SYSTEM_PROMPT = """You are a strict, direct, but useful AI-Agent for vibe-coding.
Your task is to transform vague ideas (vibe) into working code.
You work locally on Mac M1.
Rule: Always turn working code into markdown blocks on mentioned language (examples: ```html ... ```).
Provide output direct and convenient, emphasis quality, safe and optimised realisations."""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def start_server():
    """Starting local web-server in directory workspace"""
    os.chdir(WORKSPACE_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            httpd.serve_forever()
    except OSError:
        pass 

def main():
    os.system('clear')
    console.print(Panel.fit(
        "[bold green]VibeCoder Agent Running (v2.0)[/bold green]\n"
        "Model: Qwen 2.5 Coder | Environment: Apple Silicon Metal\n"
        "[bold cyan]Modules: Localhost Server (/serve) | Git Integration (/git)[/bold cyan]",
        title="Terminal UI"
    ))

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    while True:
        try:
            user_input = console.input("\n[bold magenta]Vibe / Task (or /serve, /git) >[/bold magenta] ").strip()

            if user_input.lower() in ['exit', 'quit']:
                console.print("[bold yellow]Ending the session...[/bold yellow]")
                break

            if not user_input:
                continue

            if user_input.lower() == '/serve':
                url = f"http://localhost:{PORT}"
                console.print(f"[bold green]✔ Local server is running on {url}[/bold green]")
                webbrowser.open(url)
                continue

            if user_input.startswith('/git'):
                commit_msg = user_input[4:].strip() or "Auto-commit from VibeCoder"
                try:
                    subprocess.run(["git", "init"], cwd=WORKSPACE_DIR, check=True, capture_output=True)
                    subprocess.run(["git", "add", "."], cwd=WORKSPACE_DIR, check=True, capture_output=True)
                    subprocess.run(["git", "commit", "-m", commit_msg], cwd=WORKSPACE_DIR, check=True, capture_output=True)
                    console.print(f"[bold green]✔ Code successfully committed to local Git:[/bold green] '{commit_msg}'")
                except subprocess.CalledProcessError as e:
                    console.print(f"[bold red]Git Error. Make sure Git is installed. {e}[/bold red]")
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
                has_html = any(lang.lower().strip() == 'html' for lang, _ in code_blocks)
                
                for idx, (lang, code) in enumerate(code_blocks):
                    lang = lang.lower().strip()
                    ext_map = {"python": "py", "javascript": "js", "html": "html", "css": "css"}
                    ext = ext_map.get(lang, lang if lang else "txt")

                    filename = "index.html" if ext == "html" else f"script_{idx}.{ext}"
                    filepath = os.path.join(WORKSPACE_DIR, filename)

                    abs_filepath = os.path.abspath(filepath)
                    
                    with open(abs_filepath, "w", encoding="utf-8") as f:
                        f.write(code.strip() + "\n")

                    console.print(f"[bold green]✔ Code saved in:[/bold green] {filename}")

                    try: 
                        subprocess.run(["code", abs_filepath], check=True)
                    except FileNotFoundError:
                        pass

                console.print(f"[bold cyan]Tip: Type '/serve' to view the result in your browser.[/bold cyan]")

        except KeyboardInterrupt: 
            console.print("\n[bold yellow]Interrupted by user. Exiting...[/bold yellow]")
            break
        except Exception as e:
            console.print(f"\n[bold red]System error: {e}[/bold red]")

if __name__ == "__main__":
    main()