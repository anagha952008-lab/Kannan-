import sqlite3
from rich.console import Console
from rich.table import Table

console = Console()

def main():
    console.print("[bold cyan]==================================================[/bold cyan]")
    console.print("[bold white]📥 GHOST-CHAT: EDUCATIONAL TOOLS REPOSITORY[/bold white]")
    console.print("[bold cyan]==================================================[/bold cyan]\n")

    try:
        conn = sqlite3.connect('tools_repository.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, tool_name, description, download_url, uploaded_by FROM shared_tools")
        rows = cursor.fetchall()
        conn.close()
    except sqlite3.OperationalError:
        console.print("[bold red][!] ഡാറ്റാബേസ് നിലവിലില്ല അല്ലെങ്കിൽ ടൂളുകൾ ഒന്നും അപ്‌ലോഡ് ചെയ്യപ്പെട്ടിട്ടില്ല.[/bold red]\n")
        return

    if not rows:
        console.print("[bold red][!] നിലവിൽ ഡാറ്റാബേസിൽ ടൂളുകൾ ഒന്നും ലഭ്യമല്ല.[/bold red]\n")
        return

    # മനോഹരമായ ഒരു ടേബിൾ നിർമ്മിക്കുന്നു
    table = Table(title="ലഭ്യമായ സുരക്ഷാ പഠന ടൂളുകൾ")
    table.add_column("ID", style="dim", width=6)
    table.add_column("ടൂളിന്റെ പേര്", style="cyan", no_wrap=True)
    table.add_column("വിവരണം", style="magenta")
    table.add_column("ഡൗൺലോഡ് ലിങ്ക് (URL)", style="green")
    table.add_column("അപ്‌ലോഡ് ചെയ്തത്", style="yellow")

    for row in rows:
        table.add_row(str(row[0]), row[1], row[2], row[3], row[4])

    console.print(table)
    console.print("\n[bold yellow]💡 നിർദ്ദേശം:[/bold yellow] മുകളിൽ കാണുന്ന ലിങ്കുകൾ കോപ്പി ചെയ്ത് ബ്രൗസറിലോ ടെർമിനലിലോ ഉപയോഗിച്ച് ടൂളുകൾ ഡൗൺലോഡ് ചെയ്യാം.\n")

if __name__ == "__main__":
    main()

