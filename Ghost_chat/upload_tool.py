import sqlite3
from rich.console import Console

console = Console()

def init_tools_db():
    """ടൂളുകൾക്ക് വേണ്ടിയുള്ള പ്രത്യേക ഡാറ്റാബേസ് നിർമ്മിക്കുന്നു"""
    conn = sqlite3.connect('tools_repository.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shared_tools (
            id INTEGER PRIMARY KEY,
            tool_name TEXT,
            description TEXT,
            download_url TEXT,
            uploaded_by TEXT
        )
    ''')
    conn.commit()
    conn.close()

def main():
    init_tools_db()
    console.print("[bold cyan]==================================================[/bold cyan]")
    console.print("[bold white]📤 GHOST-CHAT: EDUCATIONAL TOOLS UPLOADER[/bold white]")
    console.print("[bold cyan]==================================================[/bold cyan]\n")

    username = input("നിങ്ങളുടെ പേര്/യൂസർനെയിം: ").strip()
    tool_name = input("ടൂളിന്റെ പേര് (e.g., Phishing-Simulation): ").strip()
    desc = input("ടൂളിനെക്കുറിച്ചുള്ള വിവരണം (Description): ").strip()
    url = input("GitHub/ഡൗൺലോഡ് ലിങ്ക്: ").strip()

    if tool_name and url:
        conn = sqlite3.connect('tools_repository.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO shared_tools (tool_name, description, download_url, uploaded_by) VALUES (?, ?, ?, ?)",
            (tool_name, desc, url, username if username else "Anonymous")
        )
        conn.commit()
        conn.close()
        console.print("\n[bold green][✔] ടൂൾ വിജയകരമായി ഡാറ്റാബേസിലേക്ക് അപ്‌ലോഡ് ചെയ്യപ്പെട്ടു![/bold green]\n")
    else:
        console.print("\n[bold red][-] എറർ: ടൂളിന്റെ പേരും ലിങ്കും നിർബന്ധമാണ്![/bold red]\n")

if __name__ == "__main__":
    main()

