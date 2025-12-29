import sqlite3

DB_NAME = "healthcare.db"

# --- IMPORTANT ---
# In the quotes below, type the EXACT username you used to sign up.
USERNAME_TO_PROMOTE = "Tea" 

def promote_user_to_admin(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_admin = 1 WHERE username = ?", (username,))
    if cursor.rowcount > 0:
        print(f"✅ Success! User '{username}' is now an admin.")
    else:
        print(f"❌ Error: User '{username}' not found. Check the spelling.")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    promote_user_to_admin(USERNAME_TO_PROMOTE)