import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def get_conn():
    return sqlite3.connect(DB_PATH)

def show_all_users():
    conn = get_conn()
    users = conn.execute('SELECT id, username, plain_password FROM users').fetchall()
    conn.close()
    print()
    print(f'{"ID":<5} {"Username":<30} {"Password":<20}')
    print('-' * 60)
    for u in users:
        pwd = u[2] if u[2] else '(nahi pata)'
        print(f'{u[0]:<5} {u[1]:<30} {pwd:<20}')
    print(f'\nTotal Users: {len(users)}')

def delete_user():
    show_all_users()
    print()
    username = input("Kaun sa user delete karna hai? Username daalo: ").strip()
    confirm = input(f'Pakka delete karna hai "{username}" ko? (haan/nahi): ').strip().lower()
    if confirm == 'haan':
        conn = get_conn()
        # User delete karo
        c = conn.execute('DELETE FROM users WHERE username = ?', (username,))
        # Uska chat history bhi delete karo
        conn.execute('DELETE FROM chat_history WHERE username = ?', (username,))
        conn.commit()
        conn.close()
        if c.rowcount > 0:
            print(f'✅ "{username}" aur uska chat history dono delete ho gaye!')
        else:
            print(f'❌ "{username}" nahi mila database mein.')
    else:
        print('❌ Delete cancel kar diya.')

def delete_user_chat():
    conn = get_conn()
    users_with_chat = conn.execute(
        'SELECT DISTINCT username, COUNT(*) as total FROM chat_history GROUP BY username'
    ).fetchall()
    conn.close()

    if not users_with_chat:
        print('Kisi ka chat history nahi hai abhi.')
        return

    print()
    print('In users ka chat history hai:')
    print(f'{"Username":<30} {"Messages":<10}')
    print('-' * 40)
    for u in users_with_chat:
        print(f'{u[0]:<30} {u[1]:<10}')

    print()
    username = input("Kis user ka chat delete karna hai? Username daalo: ").strip()
    confirm = input(f'Pakka delete karna hai "{username}" ka sara chat? (haan/nahi): ').strip().lower()
    if confirm == 'haan':
        conn = get_conn()
        c = conn.execute('DELETE FROM chat_history WHERE username = ?', (username,))
        conn.commit()
        conn.close()
        if c.rowcount > 0:
            print(f'✅ "{username}" ka poora chat history delete ho gaya! ({c.rowcount} messages)')
        else:
            print(f'❌ "{username}" ka koi chat nahi mila.')
    else:
        print('❌ Delete cancel kar diya.')

def delete_all_chats():
    confirm = input('Pakka SABKA chat history delete karna hai? (haan/nahi): ').strip().lower()
    if confirm == 'haan':
        conn = get_conn()
        c = conn.execute('DELETE FROM chat_history')
        conn.commit()
        conn.close()
        print(f'✅ Sabka chat history delete ho gaya! ({c.rowcount} messages)')
    else:
        print('❌ Delete cancel kar diya.')

# ── MAIN MENU ──
while True:
    print()
    print('=' * 50)
    print('   DATABASE MANAGER'.center(50))
    print('=' * 50)
    print('1. Sabke Users dekhna')
    print('2. Kisi User ko delete karna (chat bhi)')
    print('3. Kisi User ka Chat History delete karna')
    print('4. Sabka Chat History delete karna')
    print('5. Bahar jaana (Exit)')
    print('=' * 50)

    choice = input('Option chuno (1-5): ').strip()

    if choice == '1':
        show_all_users()
    elif choice == '2':
        delete_user()
    elif choice == '3':
        delete_user_chat()
    elif choice == '4':
        delete_all_chats()
    elif choice == '5':
        print('Bye!')
        break
    else:
        print('❌ Galat option, 1-5 mein se chuno.')
