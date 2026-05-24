from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# ഗൂഗിൾ ഡാറ്റാബേസ് സിമുലേഷൻ (സെർച്ച് റിസൾട്ടുകൾ സൂക്ഷിക്കാൻ)
def init_google_db():
    conn = sqlite3.connect('google_search.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS web_pages')
    # വെബ്സൈറ്റുകളുടെ വിവരങ്ങൾ അടങ്ങിയ ടേബിൾ
    cursor.execute('CREATE TABLE web_pages (id INTEGER PRIMARY KEY, title TEXT, url TEXT, content TEXT)')
    
    # ചില വ്യാജ വെബ് പേജുകൾ ഡാറ്റാബേസിലേക്ക് ചേർക്കുന്നു
    cursor.execute("INSERT INTO web_pages (title, url, content) VALUES ('Malayalam News', 'www.malayalamnews.com', 'കേരളത്തിലെ പുതിയ വാർത്തകൾ ഇവിടെ വായിക്കാം.')")
    cursor.execute("INSERT INTO web_pages (title, url, content) VALUES ('Tech Malayalam', 'www.techmalayalam.com', 'എത്തിക്കൽ ഹാക്കിംഗും കമ്പ്യൂട്ടർ കോഡിംഗും മലയാളത്തിൽ പഠിക്കാം.')")
    cursor.execute("INSERT INTO web_pages (title, url, content) VALUES ('Secret Google Admin', 'www.google-internal-secret.com', 'FLAG{GOOGLE_CORE_SERVER_COMPROMISED}')")
    
    conn.commit()
    conn.close()

# ഗൂഗിൾ ഹോം പേജും സെർച്ച് എഞ്ചിനും
@app.route('/', methods=['GET'])
def google_home():
    search_query = request.args.get('q', '')
    results = []
    error_message = ""

    if search_query:
        conn = sqlite3.connect('google_search.db')
        cursor = conn.cursor()
        
        # ⚠️ SQL Injection പിഴവ്: യൂസർ ടൈപ്പ് ചെയ്യുന്ന വാക്ക് നേരിട്ട് ക്വറിയിലേക്ക് ചേർക്കുന്നു
        raw_query = f"SELECT title, url, content FROM web_pages WHERE title LIKE '%{search_query}%' OR content LIKE '%{search_query}%'"
        
        try:
            cursor.execute(raw_query)
            results = cursor.fetchall()
        except Exception as e:
            error_message = f"Database Error: {str(e)}"
        conn.close()

    # ഗൂഗിൾ പോലെയുള്ള ലളിതമായ HTML ഡിസൈൻ
    return render_template_string('''
        <center>
            <h1 style="font-size: 60px; color: #4285F4;">
                <span style="color:#4285F4">G</span><span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span><span style="color:#4285F4">g</span><span style="color:#34A853">l</span><span style="color:#EA4335">e</span> <span style="color: gray; font-size: 20px;">Lab</span>
            </h1>
            
            <form method="get" action="/">
                <input type="text" name="q" value="{{ query }}" style="width: 500px; padding: 10px; border-radius: 24px; border: 1px solid #dfe1e5; outline: none;">
                <br><br>
                <input type="submit" value="Google Search" style="padding: 10px 20px; border: 1px solid #f8f9fa; background-color: #f8f9fa; cursor: pointer;">
            </form>

            <hr style="width: 60%; margin-top: 30px;">
            
            <div style="width: 60%; text-align: left; margin-top: 20px;">
                {% if error_message %}
                    <p style="color: red;">{{ error_message }}</p>
                {% endif %}
                
                {% for row in results %}
                    <div style="margin-bottom: 20px;">
                        <a href="#" style="color: #1a0dab; font-size: 20px; text-decoration: none;"><h3>{{ row[0] }}</h3></a>
                        <p style="color: #006621; font-size: 14px; margin: -10px 0 5px 0;">{{ row[1] }}</p>
                        <p style="color: #545454; font-size: 16px;">{{ row[2] }}</p>
                    </div>
                {% else %}
                    {% if query %}
                        <p>റിസൾട്ടുകൾ ഒന്നും കണ്ടെത്തിയില്ല.</p>
                    {% endif %}
                {% endfor %}
            </div>
        </center>
    ''', query=search_query, results=results, error_message=error_message)

# ഗൂഗിൾ സെർവർ ഡയഗ്നോസ്റ്റിക് ടൂൾ (കമാൻഡ് ലൈൻ സിമുലേഷൻ)
@app.route('/server-status', methods=['GET', 'POST'])
def server_status():
    cmd_output = ""
    if request.method == 'POST':
        server_ip = request.form['ip']
        # ⚠️ Command Injection പിഴവ്: ഇൻപുട്ട് നേരിട്ട് ഷെല്ലിലേക്ക് പോകുന്നു
        cmd_output = os.popen(f"ping -c 1 {server_ip}").read()

    return render_template_string('''
        <h3>Google Server Diagnostic Tool</h3>
        <form method="post">
            സെർവർ ഐപി നൽകുക: <input type="text" name="ip">
            <input type="submit" value="Check Status">
        </form>
        <pre>{{ output }}</pre>
    ''', output=cmd_output)

if __name__ == '__main__':
    init_google_db()
    app.run(host='127.0.0.1', port=8000, debug=True)

