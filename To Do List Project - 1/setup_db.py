import mysql.connector

# Connect to database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="D$ai1919",
    database="todo_app"
)
cursor = db.cursor()

try:
    # Add description column if it doesn't exist
    cursor.execute("""
        ALTER TABLE tasks 
        ADD COLUMN description LONGTEXT DEFAULT NULL
    """)
    db.commit()
    print("✓ Description column added successfully!")
except mysql.connector.Error as err:
    if "Duplicate column name" in str(err):
        print("✓ Description column already exists")
    else:
        print(f"Error: {err}")

try:
    # Add is_important column if it doesn't exist
    cursor.execute("""
        ALTER TABLE tasks 
        ADD COLUMN is_important INT DEFAULT 0
    """)
    db.commit()
    print("✓ Important flag column added successfully!")
except mysql.connector.Error as err:
    if "Duplicate column name" in str(err):
        print("✓ Important flag column already exists")
    else:
        print(f"Error: {err}")
finally:
    db.close()
