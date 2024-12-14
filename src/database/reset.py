"""
Jika karena suatu alasan tertentu terpaksa mereset ID warehouse,
Anda dapat menggunakan script berikut:
"""
import sqlite3

# Connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Reset the auto-increment value
cursor.execute("""UPDATE sqlite_sequence
               SET seq = (SELECT MAX(id) FROM Warehouse)
               WHERE name = 'Warehouse';""")
# cursor.execute("SELECT * FROM Warehouse;")

# Commit changes
conn.commit()

# Close connection
conn.close()
