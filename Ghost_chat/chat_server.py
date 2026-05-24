import socket
import threading
import sqlite3
from datetime import datetime

# സെർവർ റൺ ചെയ്യേണ്ട ഐപിയും പോർട്ടും
HOST = '127.0.0.1'
PORT = 9999
clients = []

def init_databases():
    """രണ്ട് ഡാറ്റാബേസ് ടേബിളുകൾ നിർമ്മിക്കുന്നു (SQLite സിന്റാക്സ് അനുസരിച്ച്)"""
    conn = sqlite3.connect('ghost_chat.db')
    cursor = conn.cursor()
    
    # 1. യൂസർ ഐപിയും ലോഗിനും സൂക്ഷിക്കാനുള്ള ടേബിൾ
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_logs (
            id INTEGER PRIMARY KEY,
            username TEXT,
            ip_address TEXT,
            login_time TEXT
        )
    ''')
    
    # 2. എജ്യുക്കേഷണൽ ടൂളുകൾ ഷെയർ ചെയ്യാനുള്ള ടേബിൾ
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

def log_user(username, ip_address):
    """യൂസറുടെ ഐപിയും വിവരങ്ങളും ഡാറ്റാബേസിലേക്ക് സുരക്ഷിതമായി സേവ് ചെയ്യുന്നു"""
    conn = sqlite3.connect('ghost_chat.db')
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Parameterized query വഴി സുരക്ഷിതമായി വിവരങ്ങൾ കയറ്റുന്നു
    cursor.execute(
        "INSERT INTO user_logs (username, ip_address, login_time) VALUES (?, ?, ?)",
        (username, str(ip_address), current_time)
    )
    conn.commit()
    conn.close()
    print(f"[💾 ലോഗ് ചെയ്യപ്പെട്ടു] {username} -> {ip_address}")

def broadcast(message, current_client):
    """മെസ്സേജുകൾ മറ്റുള്ളവരിലേക്ക് അയക്കുന്നു"""
    for client in clients:
        if client != current_client:
            try:
                client.send(message)
            except:
                remove(client)

def handle_client(client, client_address):
    """ക്ലയന്റുമായുള്ള ആശയവിനിമയം നിയന്ത്രിക്കുന്നു"""
    username = "Unknown"
    try:
        # ആദ്യത്തെ മെസ്സേജായി യൂസർനെയിം സ്വീകരിക്കുന്നു
        username = client.recv(1024).decode('utf-8')
        # ഐപിയും യൂസർനെയിമും ഒന്നാമത്തെ ഡാറ്റാബേസിലേക്ക് മാറ്റുന്നു
        log_user(username, client_address[0])
    except:
        remove(client)
        return

    while True:
        try:
            message = client.recv(4096)
            if message:
                broadcast(message, client)
            else:
                remove(client)
                break
        except:
            continue

def remove(client):
    if client in clients:
        clients.remove(client)

def start_server():
    init_databases()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    
    print(f"[+] Ghost-Chat അഡ്വാൻസ്ഡ് സെർവർ ആരംഭിച്ചു... [Port: {PORT}]")
    print("[+] സുരക്ഷാ ലോഗുകളും ഡാറ്റാബേസും സജ്ജമാണ്.\n")

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n[-] സെർവർ നിർത്തലാക്കി.")

