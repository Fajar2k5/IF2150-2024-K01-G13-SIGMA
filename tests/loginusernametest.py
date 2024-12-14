import unittest
import sqlite3

DATABASE_PATH = ':memory:'

def verifyLoginbyEmail(email, password, connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT email, password FROM accounts WHERE email = ? AND password = ?
    """, (email, password))
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
        response = verifyLoginbyEmail('test@example.com', 'testpassword', self.connection)
        self.assertEqual(len(response), 1)  
        self.assertEqual(response[0][0], 'test@example.com')  
        self.assertEqual(response[0][1], 'testpassword')  

    def test_verify_login_failure(self):
        
        response = verifyLoginbyEmail('wrongemail', 'testpassword', self.connection)
        self.assertEqual(len(response), 0)  

    
        response = verifyLoginbyEmail('test@example.com', 'wrongpassword', self.connection)
        self.assertEqual(len(response), 0)  

    def tearDown(self):
        self.cursor.execute("DROP TABLE IF EXISTS accounts")
        self.connection.commit()
        self.connection.close()

if __name__ == '__main__':
    unittest.main()
