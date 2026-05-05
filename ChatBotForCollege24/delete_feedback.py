import sqlite3

con = sqlite3.connect('mydatabase.db')
cursor = con.cursor()

# Delete Feedback data
cursor.execute("DELETE FROM Feedback")

# Delete Users data
cursor.execute("DELETE FROM Users")

con.commit()
con.close()

print("All Feedback and User data deleted successfully!")