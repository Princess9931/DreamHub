import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

conn = sqlite3.connect(DB_PATH)
users = conn.execute('SELECT id, username, plain_password, password FROM users').fetchall()

print()
print('=' * 80)
print('  REGISTERED USERS  '.center(80))
print('=' * 80)
print(f'{"ID":<5} {"Username":<30} {"Actual Password":<20}')
print('-' * 80)

if users:
    for u in users:
        plain = u[2] if u[2] else '(purana user - password nahi pata)'
        print(f'{u[0]:<5} {u[1]:<30} {plain:<20}')
    print()
    print(f'Total Users: {len(users)}')
else:
    print('Koi user registered nahi hai abhi.')

print('=' * 80)
conn.close()
