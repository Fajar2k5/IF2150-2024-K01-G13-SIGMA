import unittest
import sqlite3

DATABASE_PATH = ':memory:'

def verifyLoginbyUsername(username, password, connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT username, password FROM accounts WHERE username = ? AND password = ?
    """, (username, password))
    response = cursor.fetchall()
    return response

class TestVerifyLogin(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT,
                password TEXT
            )
        """)
        self.connection.commit()
        self.cursor.execute("""
            INSERT INTO accounts (username, email, password) VALUES (?, ?, ?)
        """, ('testuser', 'test@example.com', 'testpassword'))
        self.connection.commit()

    def test_verify_login_success(self):
        response = verifyLoginbyUsername('testuser', 'testpassword', self.connection)
        self.assertEqual(len(response), 1)  
        self.assertEqual(response[0][0], 'testuser')  
        self.assertEqual(response[0][1], 'testpassword')  

    def test_verify_login_failure(self):
        
        response = verifyLoginbyUsername('wronguser', 'testpassword', self.connection)
        self.assertEqual(len(response), 0)  

    
        response = verifyLoginbyUsername('testuser', 'wrongpassword', self.connection)
        self.assertEqual(len(response), 0)  

    def tearDown(self):
        self.cursor.execute("DROP TABLE IF EXISTS accounts")
        self.connection.commit()
        self.connection.close()

if __name__ == '__main__':
    unittest.main()
