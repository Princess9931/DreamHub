#!/usr/bin/env python3
import json
import sqlite3
import hashlib
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import mimetypes

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FINALPROFILE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'finalprofile'))


def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                plain_password TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE qa_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL UNIQUE,
                answer TEXT NOT NULL,
                category TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        # Add default Q&A
        add_default_qa()
    else:
        # Add tables if they don't exist
        conn = sqlite3.connect(DB_PATH)
        try:
            conn.execute('''
                CREATE TABLE chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        except sqlite3.OperationalError:
            pass
        
        try:
            conn.execute('''
                CREATE TABLE qa_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL UNIQUE,
                    answer TEXT NOT NULL,
                    category TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            add_default_qa()
        except sqlite3.OperationalError:
            pass

        # Add plain_password column if it doesn't exist (migration)
        try:
            conn.execute('ALTER TABLE users ADD COLUMN plain_password TEXT')
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists
        finally:
            conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(password, hashed):
    return hash_password(password) == hashed


def add_default_qa():
    """Add default education Q&A to database"""
    default_qa = [
        ("10th के बाद क्या करें", "10th के बाद आपके पास तीन विकल्प हैं: 1) 11th Science लो अगर Engineering/Medical चाहिए 2) Commerce लो अगर CA/Business चाहिए 3) Arts लो अगर humanities में रुचि हो। हर stream के बाद अलग career paths हैं।", "Education Path"),
        ("Engineering कैसे करें", "Engineering में जाने के लिए: 1) 10th pass करो 2) 11th-12th में Physics, Chemistry, Math पढ़ो 3) JEE Main/Advanced की परीक्षा दो 4) Top colleges में admission लो। हार्ड work और dedication जरूरी है।", "Education Path"),
        ("Medical कैसे करें", "Medical में जाने के लिए: 1) 10th pass करो 2) 11th-12th में Biology, Chemistry, Physics पढ़ो 3) NEET exam दो 4) Government या private medical college में admission लो। यह बहुत competitive है।", "Education Path"),
        ("Government Job के लिए क्या करें", "Government job के लिए: 1) Graduation complete करो 2) SSC, RRB, UPSC जैसी परीक्षाओं की तैयारी करो 3) सही coaching लो 4) Mock tests दो 5) Hard work करो। हर exam के लिए अलग preparation strategy है।", "Government Job"),
        ("UPSC क्या है", "UPSC (Union Public Service Commission) भारत की सबसे बड़ी परीक्षा है IAS, IPS जैसी prestigious posts के लिए। यह बहुत hard है और 2-3 साल की dedicated preparation चाहिए।", "Government Job"),
        ("SSC क्या है", "SSC (Staff Selection Commission) ने कई exams कराती है जैसे SSC CGL, CHSL जो government clerks और assistants के लिए होते हैं। यह UPSC से आसान है।", "Government Job"),
        ("Commerce stream क्या है", "Commerce stream में आप Accounting, Economics, Business Studies पढ़ते हो। इसके बाद CA, CS, या MBA कर सकते हो। Business और finance में career अच्छे होते हैं।", "Education Path"),
        ("Arts stream किसे चुनना चाहिए", "Arts stream उन लिए है जो humanities, languages, social sciences में interested हैं। बाद में journalist, lawyer, teacher, civil servant बन सकते हो।", "Education Path"),
        ("Diploma क्या है", "Diploma एक 2 साल का technical course है जो 10th के बाद किया जा सकता है। इसमें practical skills सिखाई जाती हैं और government/private jobs मिल सकती हैं।", "Alternate Path"),
        ("ITI क्या है", "ITI (Industrial Training Institute) से आप electrical, plumbing, welding जैसे technical trades सीख सकते हो। यह practical और job-focused है। 8th pass के बाद कर सकते हो।", "Alternate Path"),
    ]
    
    conn = sqlite3.connect(DB_PATH)
    for question, answer, category in default_qa:
        try:
            conn.execute(
                'INSERT INTO qa_answers (question, answer, category) VALUES (?, ?, ?)',
                (question, answer, category)
            )
        except sqlite3.IntegrityError:
            pass  # Question already exists
    conn.commit()
    conn.close()


class CareerGuidanceHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
        except:
            data = {}

        parsed = urlparse(self.path)
        path = parsed.path
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if path == '/register':
            if not username or not password:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Username and password required'}).encode())
                return

            try:
                conn = sqlite3.connect(DB_PATH)
                conn.execute('INSERT INTO users (username, password, plain_password) VALUES (?, ?, ?)',
                             (username, hash_password(password), password))
                conn.commit()
                conn.close()
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Registered Successfully ✅'}).encode())
            except sqlite3.IntegrityError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'User already exists ❌'}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Error ❌', 'error': str(e)}).encode())

        elif path == '/login':
            if not username or not password:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Username and password required'}).encode())
                return

            try:
                conn = sqlite3.connect(DB_PATH)
                user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
                conn.close()

                if not user:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'msg': 'User not found ❌'}).encode())
                elif check_password(password, user[2]):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'msg': 'Login Success ✅'}).encode())
                else:
                    self.send_response(401)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'msg': 'Invalid Credentials ❌'}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Error ❌', 'error': str(e)}).encode())

        elif path == '/save-chat':
            username = data.get('username', 'anonymous').strip()
            question = data.get('question', '').strip()
            answer = data.get('answer', '').strip()

            if not question or not answer:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Question and answer required'}).encode())
                return

            try:
                conn = sqlite3.connect(DB_PATH)
                conn.execute('''
                    INSERT INTO chat_history (username, question, answer)
                    VALUES (?, ?, ?)
                ''', (username, question, answer))
                conn.commit()
                conn.close()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Chat saved ✅'}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Error saving chat', 'error': str(e)}).encode())
        
        elif path == '/add-qa':
            question = data.get('question', '').strip()
            answer = data.get('answer', '').strip()
            category = data.get('category', 'General').strip()

            if not question or not answer:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Question and answer required'}).encode())
                return

            try:
                conn = sqlite3.connect(DB_PATH)
                conn.execute(
                    'INSERT INTO qa_answers (question, answer, category) VALUES (?, ?, ?)',
                    (question, answer, category)
                )
                conn.commit()
                conn.close()
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Q&A added ✅'}).encode())
            except sqlite3.IntegrityError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Question already exists'}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Error', 'error': str(e)}).encode())

        elif path == '/search-qa':
            query = data.get('query', '').strip().lower()

            if not query:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Query required'}).encode())
                return

            try:
                conn = sqlite3.connect(DB_PATH)
                # Search in questions
                results = conn.execute(
                    'SELECT * FROM qa_answers WHERE LOWER(question) LIKE ? OR LOWER(answer) LIKE ?',
                    (f'%{query}%', f'%{query}%')
                ).fetchall()
                conn.close()
                
                if results:
                    qa_list = [{'question': r[1], 'answer': r[2], 'category': r[3]} for r in results]
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'found': True, 'results': qa_list}).encode())
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'found': False, 'msg': 'No matching Q&A found'}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

        elif path == '/delete-qa':
            qa_id = data.get('id')

            if not qa_id:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'ID required'}).encode())
                return

            try:
                conn = sqlite3.connect(DB_PATH)
                conn.execute('DELETE FROM qa_answers WHERE id = ?', (qa_id,))
                conn.commit()
                conn.close()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Q&A deleted ✅'}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'msg': 'Error', 'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'msg': 'Not found'}).encode())

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/get-all-qa':
            try:
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = sqlite3.Row
                qas = conn.execute('SELECT * FROM qa_answers ORDER BY id DESC').fetchall()
                conn.close()
                
                qa_list = [dict(qa) for qa in qas]
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'qas': qa_list, 'total': len(qa_list)}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
            return

        if path == '/get-chat-history':
            username = parsed_path.query.split('=')[1] if '=' in parsed_path.query else 'anonymous'
            try:
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = sqlite3.Row
                chats = conn.execute('''
                    SELECT * FROM chat_history WHERE username = ? ORDER BY timestamp DESC
                ''', (username,)).fetchall()
                conn.close()
                
                chat_list = [dict(chat) for chat in chats]
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'chats': chat_list}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
            return

        if path == '/':
            path = '/index.html'

        # Special route: /finalprofile/ served from project/finalprofile/
        if path.startswith('/finalprofile/'):
            relative = path[len('/finalprofile/'):]
            file_path = os.path.join(FINALPROFILE_ROOT, relative.lstrip('/'))
        else:
            file_path = os.path.join(PROJECT_ROOT, path.lstrip('/'))
        
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                content_type, _ = mimetypes.guess_type(file_path)
                if not content_type:
                    content_type = 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(f'Error: {str(e)}'.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'<h1>404 Not Found</h1>')

    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {format % args}")


if __name__ == '__main__':
    init_db()
    server = HTTPServer(('0.0.0.0', 5000), CareerGuidanceHandler)
    print('Server running on http://localhost:5000')
    print('Open http://localhost:5000/frontend/login.html in your browser')
    server.serve_forever()
