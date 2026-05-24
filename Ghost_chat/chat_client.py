import socket
import threading
import sqlite3
from cryptography.fernet import Fernet
from rich.console import Console
from rich.table import Table

console = Console()

HOST = '127.0.0.1'
PORT = 9999

# 🔑 Fernet ലൈബ്രറിക്ക് ആവശ്യമായ ശരിയായ 32-byte Base64 കീ ഇവിടെ നൽകിയിരിക്കുന്നു
SHARED_KEY = b'vK2xN_5q8Zg9W_pX6mJ8yL3nK1rT4vB6sN8mQ0pW2eE='
cipher_suite = Fernet(SHARED_KEY)

def upload_tool_to_db(username):
    """ഡാറ്റാബേസിലേക്ക് പുതിയ എജ്യുക്കേഷണൽ ടൂൾ വിവരങ്ങൾ കയറ്റുന്നു"""
    console.print("\n[bold yellow]📤 പുതിയ എജ്യുക്കേഷണൽ ടൂൾ അപ്‌ലോഡ് ഫോം:[/bold yellow]")
    tool_name = input("ടൂളിന്റെ പേര് (e.g., Phishing-Lab): ").strip()
    desc = input("ഇത് എന്താണെന്ന് വിവരിക്കുക (Description): ").strip()
    url = input("ഡൗൺലോഡ് ലിങ്ക്/GitHub ലിങ്ക്: ").strip()
    
    if tool_name and url:
        conn = sqlite3.connect('ghost_chat.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO shared_tools (tool_name, description, download_url, uploaded_by) VALUES (?, ?, ?, ?)",
            (tool_name, desc, url, username)
        )
        conn.commit()
        conn.close()
        console.print("[bold green][✔] ടൂൾ വിജയകരമായി ഡാറ്റാബേസിൽ സേവ് ചെയ്യപ്പെട്ടു![/bold green]\n")
    else:
        console.print("[bold red][-] പേരും ലിങ്കും നിർബന്ധമാണ്![/bold red]\n")

def show_shared_tools():
    """ഡാറ്റാബേസിലുള്ള എല്ലാ ടൂളുകളും മനോഹരമായ ഒരു ടേബിളായി കാണിക്കുന്നു"""
    conn = sqlite3.connect('ghost_chat.db')
    cursor = conn.cursor()
    cursor.execute("SELECT tool_name, description, download_url, uploaded_by FROM shared_tools")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        console.print("\n[bold red][!] ഡാറ്റാബേസിൽ നിലവിൽ ടൂളുകൾ ഒന്നും ലഭ്യമല്ല.[/bold red]\n")
        return
        
    table = Table(title="📥 ലഭ്യമായ സുരക്ഷാ പഠന ടൂളുകൾ")
    table.add_column("പേര്", style="cyan", no_wrap=True)
    table.add_column("വിവരണം", style="magenta")
    table.add_column("ഡൗൺലോഡ് യുആർഎൽ (Link)", style="green")
    table.add_column("അപ്‌ലോഡ് ചെയ്തത്", style="yellow")
    
    for row in rows:
        table.add_row(row[0], row[1], row[2], row[3])
        
    console.print("\n")
    console.print(table)
    console.print("\n")

def receive_messages(client_socket):
    while True:
        try:
            encrypted_message = client_socket.recv(4096)
            if encrypted_message:
                decrypted_message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
                console.print(f"\n[bold green]💬 {decrypted_message}[/bold green]")
            else:
                break
        except:
            continue

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except:
        console.print("[bold red]Error: സെർവറുമായി ബന്ധപ്പെടാൻ സാധിക്കുന്നില്ല![/bold red]")
        return

    console.print("[bold cyan]==================================================[/bold cyan]")
    console.print("[bold white]🔐 GHOST-CHAT v1.0: END-TO-END ENCRYPTED SYSTEM[/bold white]")
    console.print("[bold cyan]==================================================[/bold cyan]\n")

    username = input("നിങ്ങളുടെ യൂസർനെയിം ടൈപ്പ് ചെയ്യുക: ").strip()
    if not username:
        username = "Anonymous"

    client.send(username.encode('utf-8'))
    console.print(f"\n[bold yellow][✔] സ്വാഗതം {username}! നിങ്ങൾ സുരക്ഷിതമായി ചാറ്റിൽ ജോയിൻ ചെയ്തു.[/bold yellow]")
    console.print("[bold cyan]💡 അഡ്വാൻസ്ഡ് കമാൻഡുകൾ: [/bold cyan][white]'/upload' (ടൂൾ കയറ്റാൻ), '/download' (ലിസ്റ്റ് കാണാൻ), 'exit' (പുറത്തുപോകാൻ)[/white]\n")

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        try:
            message_text = input()
            
            if message_text.lower() == 'exit':
                console.print("[bold red][-] നിങ്ങൾ ചാറ്റിൽ നിന്നും പുറത്തുകടന്നു.[/bold red]")
                client.close()
                break
                
            if message_text.lower() == '/upload':
                upload_tool_to_db(username)
                continue
                
            if message_text.lower() == '/download':
                show_shared_tools()
                continue
                
            if message_text.strip() == "":
                continue

            full_message = f"{username}: {message_text}"
            encrypted_message = cipher_suite.encrypt(full_message.encode('utf-8'))
            client.send(encrypted_message)
            
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold red][-] കണക്ഷൻ അവസാനിപ്പിച്ചു.[/bold red]")
            client.close()
            break

if __name__ == "__main__":
    start_client()

