import sqlite3
import time
import random

# ഗൂഗിളിൽ നിന്നും ഓട്ടോമാറ്റിക്കായി വരാൻ സാധ്യതയുള്ള വലിയ ഡാറ്റാ ലിസ്റ്റ് (Simulation)
google_live_data = [
    ("Wikipedia", "https://www.wikipedia.org", "ലോകത്തിലെ എല്ലാ വിവരങ്ങളും അടങ്ങിയ സ്വതന്ത്ര വിജ്ഞാനകോശം."),
    ("GitHub", "https://github.com", "ഡെവലപ്പർമാർക്ക് കോഡുകൾ സൂക്ഷിക്കാനും പങ്കുവെക്കാനുമുള്ള പ്ലാറ്റ്‌ഫോം."),
    ("Stack Overflow", "https://stackoverflow.com", "പ്രോഗ്രാമിംഗ് സംശയങ്ങൾക്കും പരിഹാരങ്ങൾക്കുമായുള്ള ഏറ്റവും വലിയ കമ്മ്യൂണിറ്റി."),
    ("NASA", "https://www.nasa.gov", "ബഹിരാകാശ ഗവേഷണ വാർത്തകളും പുതിയ കണ്ടെത്തലുകളും."),
    ("BBC News", "https://www.bbc.com", "ആഗോള വാർത്തകളും തത്സമയ വിവരങ്ങളും ഇവിടെ വായിക്കാം."),
    ("Reddit", "https://www.reddit.com", "വിവിധ വിഷയങ്ങളെക്കുറിച്ചുള്ള ചർച്ചകളും ട്രെൻഡിംഗ് വാർത്തകളും.")
]

def auto_update_database():
    print("[+] ഗൂഗിൾ ഡാറ്റാബേസ് സിൻക്രണൈസേഷൻ ആരംഭിക്കുന്നു...")
    
    conn = sqlite3.connect('secure_search.db')
    cursor = conn.cursor()
    
    # ടേബിൾ നിലവിലുണ്ടെന്ന് ഉറപ്പാക്കുന്നു
    cursor.execute('CREATE TABLE IF NOT EXISTS web_pages (id INTEGER PRIMARY KEY, title TEXT, url TEXT, content TEXT)')
    
    # ലിസ്റ്റിലുള്ള ഓരോ ഡാറ്റയും ഓട്ടോമാറ്റിക്കായി ഡാറ്റാബേസിലേക്ക് ചേർക്കുന്നു
    for title, url, content in google_live_data:
        # ഡാറ്റ നേരത്തെ തന്നെ ഉണ്ടോ എന്ന് പരിശോധിക്കുന്നു (ഡ്യൂപ്ലിക്കേറ്റ് തടയാൻ)
        cursor.execute("SELECT * FROM web_pages WHERE url = ?", (url,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO web_pages (title, url, content) VALUES (?, ?, ?)", (title, url, content))
            print(f"[✔] പുതിയ പേജ് ചേർത്തു: {title}")
            time.sleep(1) # ഓരോ സെക്കൻഡിലും ഓട്ടോമാറ്റിക്കായി അപ്ഡേറ്റ് ആകുന്നു
            
    conn.commit()
    conn.close()
    print("[+] ഡാറ്റാബേസ് പൂർണ്ണമായും അപ്ഡേറ്റ് ചെയ്യപ്പെട്ടു!")

if __name__ == "__main__":
    auto_update_database()

