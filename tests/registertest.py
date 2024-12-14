import unittest
import sqlite3
DATABASE_PATH = ':memory:'
def register(username, email, password):
    print(DATABASE_PATH)
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        # Membuat tabel accounts jika belum ada
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT,
                password TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO accounts (username, email, password) VALUES(?,?,?)
        """, (username, email, password))
        connection.commit()

        cursor.execute("""SELECT * FROM accounts""")
        connection.commit()

        print(cursor.fetchall())
        connection.close()
        return True
    except Exception as error:
        print(f"Error: {error}")
        return False

class TestRegisterFunction(unittest.TestCase):
    
    def test_register_success(self):
        result = register('john', 'johny@example.com', 'securepassword123')
        self.assertTrue(result)
if __name__ == '__main__':
    unittest.main()
