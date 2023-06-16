import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
)

# cursor object
cursor_obj = db.cursor()

# create db
cursor_obj.execute("CREATE DATABASE crm_db")
print('db created successfully!!')