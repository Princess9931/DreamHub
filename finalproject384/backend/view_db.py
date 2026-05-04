#!/usr/bin/env python3
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def view_database():
    if not os.path.exists(DB_PATH):
        print("❌ Database not found!")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("🗄️  DreamHub Database Viewer".center(70))
    print("="*70 + "\n")
    
    # Users Table
    print("👥 REGISTERED USERS")
    print("-" * 70)
    users = cursor.execute('SELECT id, username, password FROM users').fetchall()
    
    if users:
        print(f"{'ID':<5} {'Username':<25} {'Password (SHA-256 Hashed)':<65}")
        print("-" * 95)
        for user in users:
            print(f"{user[0]:<5} {user[1]:<25} {user[2]:<65}")
    else:
        print("No users registered yet")
    
    print("\n")
    
    # Chat History Table
    print("💬 CHAT HISTORY")
    print("-" * 70)
    chats = cursor.execute('SELECT id, username, question, answer, timestamp FROM chat_history ORDER BY timestamp DESC').fetchall()
    
    if chats:
        print(f"{'ID':<5} {'User':<15} {'Timestamp':<20}")
        print("-" * 70)
        for chat in chats:
            print(f"{chat[0]:<5} {chat[1]:<15} {chat[4]:<20}")
            print(f"  Q: {chat[2][:60]}...")
            print(f"  A: {chat[3][:60]}...")
            print("-" * 70)
    else:
        print("No chat history yet")
    
    print("\n" + "="*70)
    print("Database Statistics".center(70))
    print("="*70)
    total_users = len(users)
    total_chats = len(chats)
    print(f"Total Users: {total_users}")
    print(f"Total Chat Messages: {total_chats}")
    print("="*70 + "\n")
    
    conn.close()

if __name__ == '__main__':
    view_database()
