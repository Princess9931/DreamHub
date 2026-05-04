import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

# ✏️ Yahan username daalo jiska chat dekhna hai
username = input("Kis user ka chat dekhna hai? Username daalo: ").strip()

conn = sqlite3.connect(DB_PATH)
chats = conn.execute(
    'SELECT id, question, answer, timestamp FROM chat_history WHERE username = ? ORDER BY timestamp DESC',
    (username,)
).fetchall()
conn.close()

print()
print('=' * 80)
print(f'  CHAT HISTORY: {username}  '.center(80))
print('=' * 80)

if chats:
    for i, chat in enumerate(chats, 1):
        print(f'\n[{i}] Time: {chat[3]}')
        print(f'  Q: {chat[1]}')
        print(f'  A: {chat[2][:200]}...' if len(chat[2]) > 200 else f'  A: {chat[2]}')
        print('-' * 80)
    print(f'\nTotal Messages: {len(chats)}')
else:
    print(f'\n"{username}" ka koi chat history nahi mila.')
    print()
    # Sab users dikhao jinka chat hai
    conn = sqlite3.connect(DB_PATH)
    users_with_chat = conn.execute(
        'SELECT DISTINCT username, COUNT(*) as total FROM chat_history GROUP BY username'
    ).fetchall()
    conn.close()
    if users_with_chat:
        print('In users ka chat history available hai:')
        for u in users_with_chat:
            print(f'  - {u[0]}  ({u[1]} messages)')

print('=' * 80)
