from flask import Flask, request, render_template_string
import sqlite3
import html

app = Flask(__name__)

# സുരക്ഷിതമായ ഡാറ്റാബേസ് സെറ്റ് ചെയ്യുന്നു
def init_secure_db():
    conn = sqlite3.connect('secure_search.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS web_pages')
    cursor.execute('CREATE TABLE web_pages (id INTEGER PRIMARY KEY, title TEXT, url TEXT, content TEXT)')
    
    # ഡാറ്റകൾ ചേർക്കുന്നു
    cursor.execute("INSERT INTO web_pages (title, url, content) VALUES ('Malayalam Tech News', 'https://www.malayalamtechnews.com', 'എത്തിക്കൽ ഹാക്കിംഗും സൈബർ സെക്യൂരിറ്റിയും സുരക്ഷിതമായി പഠിക്കാനുള്ള വഴികൾ.')")
    cursor.execute("INSERT INTO web_pages (title, url, content) VALUES ('Python Programming', 'https://www.python.org', 'പൈത്തൺ ഉപയോഗിച്ച് സുരക്ഷിതമായ വെബ് ആപ്ലിക്കേഷനുകൾ നിർമ്മിക്കുന്നത് എങ്ങനെ?')")
    cursor.execute("INSERT INTO web_pages (title, url, content) VALUES ('Google Security Tips', 'https://safety.google', 'നിങ്ങളുടെ ഗൂഗിൾ അക്കൗണ്ടുകൾ എങ്ങനെ സുരക്ഷിതമായി സൂക്ഷിക്കാം എന്ന് മനസ്സിലാക്കുക.')")
    
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def secure_search():
    search_query = request.args.get('q', '').strip()
    results = []
    error_message = ""

    if search_query:
        # 1. ഇൻപുട്ട് ഫിൽട്ടറിംഗ് (XSS അറ്റാക്ക് തടയാൻ): 
        # ഉപയോക്താവ് നൽകുന്ന കോഡുകളെ വെറും ടെക്സ്റ്റ് മാത്രമായി മാറ്റുന്നു
        safe_query = html.escape(search_query)

        conn = sqlite3.connect('secure_search.db')
        cursor = conn.cursor()
        
        # 2. Parameterized Query (SQL Injection പൂർണ്ണമായും തടയാൻ):
        # ഇവിടെ ക്വറിയിലേക്ക് നേരിട്ട് ഇൻപുട്ട് ചേർക്കാതെ '?' ചിഹ്നമാണ് ഉപയോഗിച്ചിരിക്കുന്നത്
        secure_sql = "SELECT title, url, content FROM web_pages WHERE title LIKE ? OR content LIKE ?"
        match_pattern = f"%{safe_query}%"
        
        try:
            cursor.execute(secure_sql, (match_pattern, match_pattern))
            results = cursor.fetchall()
        except Exception as e:
            error_message = "ഒരു സാങ്കേതിക പിഴവ് സംഭവിച്ചു."
        finally:
            conn.close()

    # അഡ്വാൻസ്ഡ് ബ്ലാക്ക് ബാക്ക്ഗ്രൗണ്ട് (Dark Mode) ഡിസൈൻ
    dark_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Google Secure Lab</title>
        <style>
            body {
                background-color: #121212;
                color: #e0e0e0;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }
            .container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin-top: 100px;
            }
            .logo {
                font-size: 50px;
                font-weight: bold;
                margin-bottom: 30px;
                letter-spacing: -1px;
            }
            .search-box {
                width: 550px;
                padding: 12px 20px;
                font-size: 16px;
                background-color: #202124;
                border: 1px solid #5f6368;
                border-radius: 24px;
                color: white;
                outline: none;
            }
            .search-box:focus {
                background-color: #303134;
                border-color: #8ab4f8;
            }
            .btn {
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #303134;
                color: #e8eaed;
                border: 1px solid #303134;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
            }
            .btn:hover {
                border-color: #5f6368;
            }
            .results-container {
                width: 600px;
                margin-top: 40px;
                text-align: left;
            }
            .result-item {
                margin-bottom: 25px;
            }
            .result-item a {
                color: #8ab4f8;
                font-size: 18px;
                text-decoration: none;
            }
            .result-item a:hover {
                text-decoration: underline;
            }
            .result-url {
                color: #bdc1c6;
                font-size: 14px;
                margin: 2px 0;
            }
            .result-snippet {
                color: #9aa0a6;
                font-size: 15px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">
                <span style="color:#4285F4">G</span><span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span><span style="color:#4285F4">g</span><span style="color:#34A853">l</span><span style="color:#EA4335">e</span>
                <span style="font-size: 18px; color: #9aa0a6; font-weight: normal; margin-left: 5px;">Secure Lab</span>
            </div>
            
            <form method="get" action="/">
                <input type="text" name="q" class="search-box" autocomplete="off" value="{{ query }}">
                <br>
                <center><input type="submit" value="Google Search" class="btn"></center>
            </form>

            <div class="results-container">
                {% if results %}
                    {% for row in results %}
                        <div class="result-item">
                            <a href="{{ row[1] }}" target="_blank"><h3>{{ row[0] }}</h3></a>
                            <p class="result-url">{{ row[1] }}</p>
                            <p class="result-snippet">{{ row[2] }}</p>
                        </div>
                    {% endfor %}
                {% else %}
                    {% if query %}
                        <p style="color: #9aa0a6;">ഫലങ്ങൾ ഒന്നും കണ്ടെത്തിയില്ല.</p>
                    {% endif %}
                {% endif %}
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(dark_html, query=search_query, results=results)

if __name__ == '__main__':
    init_secure_db()
    # ലോക്കലായി സെറ്റ് ചെയ്യുന്നു
    app.run(host='127.0.0.1', port=8080, debug=True)

