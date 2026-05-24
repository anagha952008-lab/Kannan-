import os
import sys
import time
import threading
import requests  # ലളിതമായ കണക്ഷന് വേണ്ടി ഗൂഗിൾ ലൈബ്രറി ഒഴിവാക്കി
from dotenv import load_dotenv

from cryptography.fernet import Fernet
from rich.console import Console
from rich.table import Table

# .env ഫയൽ ലോഡ് ചെയ്യുന്നു
load_dotenv()
FB_URL = os.getenv("FIREBASE_URL")

console = Console()

if not FB_URL:
    console.print("[bold red]\n[-] എറർ: .env ഫയലിൽ FIREBASE_URL കണ്ടെത്തിയില്ല![/bold red]")
    sys.exit()

# URL-ന്റെ അവസാനം '/' ഉണ്ടെന്ന് ഉറപ്പാക്കുന്നു
if not FB_URL.endswith('/'):
    FB_URL += '/'

# 🔑 മെസ്സേജുകൾ ലോക്ക് ചെയ്യാനുള്ള രഹസ്യ കീ (Fernet Encryption)
SHARED_KEY = b'vK2xN_5q8Zg9W_pX6mJ8yL3nK1rT4vB6sN8mQ0pW2eE='
cipher_suite = Fernet(SHARED_KEY)

def upload_tool_to_db(username):
    """പുതിയ ടൂളുകൾ അപ്‌ലോഡ് ചെയ്യാനുള്ള ഫങ്ക്ഷൻ"""
    console.print("\n[bold yellow]📤 പുതിയ എജ്യുക്കേഷണൽ ടൂൾ അപ്‌ലോഡ് ഫോം:[/bold yellow]")
    tool_name = input("ടൂളിന്റെ പേര്: ").strip()
    desc = input("വിവരണം (Description): ").strip()
    url = input("GitHub/ഡൗൺലോഡ് ലിങ്ക്: ").strip()
    
    if tool_name and url:
        try:
            # REST API വഴി പാസ്‌വേഡ് ഇല്ലാതെ അപ്‌ലോഡ് ചെയ്യുന്നു
            tool_data = {
                'tool_name': tool_name,
                'description': desc,
                'download_url': url,
                'uploaded_by': username
            }
            response = requests.post(f"{FB_URL}shared_tools.json", json=tool_data)
            if response.status_code == 200:
                console.print("[bold green][✔] ടൂൾ വിജയകരമായി ക്ലൗഡിൽ സേവ് ചെയ്യപ്പെട്ടു![/bold green]\n")
            else:
                console.print(f"[bold red][-] അപ്‌ലോഡ് പരാജയപ്പെട്ടു. Status: {response.status_code}[/bold red]\n")
        except Exception as e:
            console.print(f"[bold red][-] അപ്‌ലോഡ് പരാജയപ്പെട്ടു: {e}[/bold red]\n")
    else:
        console.print("[bold red][-] പേരും ലിങ്കും നിർബന്ധമാണ്![/bold red]\n")

def show_shared_tools():
    """ടൂളുകളുടെ ലിസ്റ്റ് കാണിക്കുന്ന ഫങ്ക്ഷൻ"""
    try:
        response = requests.get(f"{FB_URL}shared_tools.json")
        data = response.json()
    except:
        console.print("[bold red][!] ഡാറ്റ ലോഡ് ചെയ്യാൻ കഴിഞ്ഞില്ല.[/bold red]\n")
        return
    
    if not data:
        console.print("\n[bold red][!] Nilavil tools onnum labhyamalla.[/bold red]\n")
        return
        
    table = Table(title="📥 ലഭ്യമായ സുരക്ഷാ പഠന ടൂളുകൾ (Firebase Cloud)")
    table.add_column("പേര്", style="cyan", no_wrap=True)
    table.add_column("വിവരണം", style="magenta")
    table.add_column("ലിങ്ക്", style="green")
    table.add_column("അപ്‌ലോഡ് ചെയ്തത്", style="yellow")
    
    for key, val in data.items():
        table.add_row(val.get('tool_name', ''), val.get('description', ''), val.get('download_url', ''), val.get('uploaded_by', ''))
        
    console.print("\n")
    console.print(table)
    console.print("\n")

def fetch_live_messages():
    """ബാക്ക്ഗ്രൗണ്ടിൽ പുതിയ മെസ്സേജുകൾ സുരക്ഷിതമായി നിരീക്ഷിക്കുന്നു (No Credentials Needed)"""
    known_messages = set()
    
    # ആദ്യ തവണ റൺ ചെയ്യുമ്പോൾ പഴയ മെസ്സേജുകൾ ലോഡ് ചെയ്യുന്നു
    try:
        res = requests.get(f"{FB_URL}secure_messages.json")
        initial_data = res.json() or {}
        for k in initial_data.keys():
            known_messages.add(k)
    except:
        pass

    while True:
        try:
            time.sleep(2)  # ഓരോ 2 സെക്കൻഡിലും പുതിയ മെസ്സേജുകൾ ഉണ്ടോ എന്ന് നോക്കുന്നു
            response = requests.get(f"{FB_URL}secure_messages.json")
            data = response.json()
            
            if data:
                for msg_id, hex_msg in data.items():
                    if msg_id not in known_messages:
                        known_messages.add(msg_id)
                        # എൻക്രിപ്റ്റ് ചെയ്ത മെസ്സേജ് ഡീക്രിപ്റ്റ് ചെയ്യുന്നു
                        encrypted_bytes = bytes.fromhex(hex_msg)
                        decrypted_message = cipher_suite.decrypt(encrypted_bytes).decode('utf-8')
                        console.print(f"\n[bold green]💬 {decrypted_message}[/bold green]")
        except:
            continue

def start_client():
    console.print("[bold cyan]==================================================[/bold cyan]")
    console.print("[bold white]🔥 GHOST-CHAT v4.1: FIREBASE REALTIME SYSTEM[/bold white]")
    console.print("[bold cyan]==================================================[/bold cyan]\n")

    username = input("നിങ്ങളുടെ യൂസർനെയിം ടൈപ്പ് ചെയ്യുക: ").strip()
    if not username:
        username = "Anonymous"

    console.print(f"\n[bold yellow][✔] സ്വാഗതം {username}! നിങ്ങൾ സുരക്ഷിതമായി ജോയിൻ ചെയ്തു.[/bold yellow]")
    console.print("[bold cyan]💡 കമാൻഡുകൾ: [/bold cyan][white]'/upload', '/download', 'exit'[/white]\n")

    # ബാക്ക്ഗ്രൗണ്ടിൽ പുതിയ മെസ്സേജുകൾ കേൾക്കാൻ ത്രെഡ് സ്റ്റാർട്ട് ചെയ്യുന്നു
    threading.Thread(target=fetch_live_messages, daemon=True).start()

    while True:
        try:
            message_text = input()
            
            if message_text.lower() == 'exit':
                console.print("[bold red][-] നിങ്ങൾ ചാറ്റിൽ നിന്നും പുറത്തുകടന്നു.[/bold red]")
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
            # മെസ്സേജ് സുരക്ഷിതമായി ലോക്ക് ചെയ്യുന്നു (Encrypt)
            encrypted_message = cipher_suite.encrypt(full_message.encode('utf-8'))
            
            # ഫയർബേസിലേക്ക് മെസ്സേജ് പുഷ് ചെയ്യുന്നു
            requests.post(f"{FB_URL}secure_messages.json", json=encrypted_message.hex())
            
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold red][-] കണക്ഷൻ അവസാനിപ്പിച്ചു.[/bold red]")
            break

if __name__ == "__main__":
    start_client()

